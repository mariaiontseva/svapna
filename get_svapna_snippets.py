#!/usr/bin/env python3

import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime

def get_svapna_snippets_with_context():
    """Get actual svapna snippets with 6+ lines of context"""
    
    # Connect to database
    conn = sqlite3.connect('/Users/mariaiontseva/muktabodha_texts.db')
    cursor = conn.cursor()
    
    # Get ALL svapna occurrences
    cursor.execute("""
        SELECT t.display_name, t.tradition, t.author, si.content, si.filename
        FROM search_index si 
        JOIN texts t ON si.filename = t.filename
        WHERE LOWER(si.content) LIKE '%svapn%'
        ORDER BY t.display_name
    """)
    
    all_results = cursor.fetchall()
    print(f"Found {len(all_results)} texts with svapna")
    
    # Categories with patterns
    categories = {
        'diksha_initiation': {
            'patterns': [r'dīkṣ', r'upadeś', r'abhiṣek', r'saṃskār'],
            'snippets': [],
            'count': 0
        },
        'visualization': {
            'patterns': [r'darśan', r'dṛṣṭ', r'paśy', r'bhāvan', r'dhyān'],
            'snippets': [],
            'count': 0
        },
        'yoga': {
            'patterns': [r'yog', r'samādh', r'prāṇāyām', r'āsan', r'kuṇḍalin'],
            'snippets': [],
            'count': 0
        },
        'mantra': {
            'patterns': [r'mantr', r'vidyā', r'bīj', r'jap'],
            'snippets': [],
            'count': 0
        },
        'consciousness': {
            'patterns': [r'jāgr', r'suṣupt', r'turīy', r'cetan', r'nidr'],
            'snippets': [],
            'count': 0
        },
        'deity': {
            'patterns': [r'dev', r'śiv', r'śakt', r'viṣṇ', r'kṛṣṇ', r'kāl', r'durg'],
            'snippets': [],
            'count': 0
        }
    }
    
    # Process each text
    total_svapna_count = 0
    all_snippets = []
    
    for text_name, tradition, author, full_content, filename in all_results:
        # Split content into lines
        lines = full_content.split('\n')
        
        # Find all svapna occurrences in this text
        for i, line in enumerate(lines):
            if 'svapn' in line.lower():
                total_svapna_count += len(re.findall(r'svapn\w*', line, re.IGNORECASE))
                
                # Get 6 lines of context (3 before, current, 2 after)
                start = max(0, i - 3)
                end = min(len(lines), i + 3)
                context_lines = lines[start:end]
                
                # Clean the lines
                cleaned_lines = []
                for ctx_line in context_lines:
                    # Remove verse numbers and special markers
                    clean = re.sub(r'\|\|.*?\|\|', '', ctx_line)
                    clean = re.sub(r'^\d+\s*', '', clean)
                    clean = clean.strip()
                    if clean:
                        cleaned_lines.append(clean)
                
                if cleaned_lines:
                    snippet = {
                        'text': text_name,
                        'tradition': tradition or 'Unknown',
                        'author': author or 'Unknown',
                        'line_number': i + 1,
                        'context': '\n'.join(cleaned_lines),
                        'highlight_line': len(cleaned_lines) // 2 if cleaned_lines else 0
                    }
                    
                    # Categorize the snippet
                    full_context = ' '.join(cleaned_lines).lower()
                    for cat_name, cat_data in categories.items():
                        for pattern in cat_data['patterns']:
                            if re.search(pattern, full_context, re.IGNORECASE):
                                cat_data['count'] += 1
                                if len(cat_data['snippets']) < 10:  # Keep 10 examples per category
                                    cat_data['snippets'].append(snippet)
                                break
                    
                    # Add to all snippets (keep first 100)
                    if len(all_snippets) < 100:
                        all_snippets.append(snippet)
    
    # Get statistics
    print(f"\nTotal svapna occurrences found: {total_svapna_count}")
    print("\nCategory distribution:")
    for cat_name, cat_data in categories.items():
        print(f"  {cat_name}: {cat_data['count']} occurrences, {len(cat_data['snippets'])} snippets saved")
    
    # Create output
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_texts': len(all_results),
        'total_occurrences': total_svapna_count,
        'categories': {},
        'sample_snippets': all_snippets[:50]  # First 50 general snippets
    }
    
    # Add categorized snippets
    for cat_name, cat_data in categories.items():
        output['categories'][cat_name] = {
            'count': cat_data['count'],
            'percentage': round((cat_data['count'] / total_svapna_count * 100), 2) if total_svapna_count > 0 else 0,
            'snippets': cat_data['snippets']
        }
    
    # Save to JSON
    with open('/Users/mariaiontseva/svapna-deploy/svapna_snippets_context.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved snippets to svapna_snippets_context.json")
    
    conn.close()
    return output

if __name__ == "__main__":
    get_svapna_snippets_with_context()