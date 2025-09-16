#!/usr/bin/env python3

import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime

def extract_all_svapna_snippets():
    """Extract ALL svapna occurrences with full 6-line context"""
    
    # Connect to database
    conn = sqlite3.connect('/Users/mariaiontseva/muktabodha_texts.db')
    cursor = conn.cursor()
    
    # Get ALL texts with svapna
    cursor.execute("""
        SELECT t.display_name, t.tradition, t.author, si.content, si.filename
        FROM search_index si 
        JOIN texts t ON si.filename = t.filename
        WHERE LOWER(si.content) LIKE '%svapn%'
        ORDER BY t.display_name
    """)
    
    all_results = cursor.fetchall()
    print(f"Processing {len(all_results)} texts with svapna...")
    
    # Categories for classification
    categories = {
        'diksha_initiation': {
            'patterns': [r'dīkṣ', r'upadeś', r'abhiṣek', r'saṃskār', r'śaktipāt'],
            'snippets': [],
            'count': 0
        },
        'visualization': {
            'patterns': [r'darśan', r'dṛṣṭ', r'paśy', r'bhāvan', r'dhyān', r'ālok', r'prakāś'],
            'snippets': [],
            'count': 0
        },
        'yoga': {
            'patterns': [r'yog', r'samādh', r'prāṇāyām', r'āsan', r'kuṇḍalin', r'bandh', r'mudr'],
            'snippets': [],
            'count': 0
        },
        'mantra': {
            'patterns': [r'mantr', r'vidyā', r'bīj', r'jap', r'stotr', r'kavac'],
            'snippets': [],
            'count': 0
        },
        'consciousness': {
            'patterns': [r'jāgr', r'suṣupt', r'turīy', r'cetan', r'nidr', r'bodh', r'prabodh'],
            'snippets': [],
            'count': 0
        },
        'deity': {
            'patterns': [r'dev[aīi]', r'śiv', r'śakt', r'viṣṇ', r'kṛṣṇ', r'kāl[īi]', r'durg', r'gaṇeś', r'bhairav'],
            'snippets': [],
            'count': 0
        },
        'tantra': {
            'patterns': [r'tantr', r'yantr', r'cakr', r'maṇḍal', r'pūj', r'hom'],
            'snippets': [],
            'count': 0
        },
        'philosophical': {
            'patterns': [r'māy', r'brahm', r'ātm', r'tattv', r'saṃsār', r'mokṣ', r'mukt'],
            'snippets': [],
            'count': 0
        }
    }
    
    # Store ALL snippets
    all_snippets = []
    total_svapna_count = 0
    texts_processed = 0
    
    for text_name, tradition, author, full_content, filename in all_results:
        texts_processed += 1
        if texts_processed % 50 == 0:
            print(f"Processed {texts_processed}/{len(all_results)} texts...")
        
        # Split content into lines
        lines = full_content.split('\n')
        
        # Find ALL svapna occurrences in this text
        for line_idx, line in enumerate(lines):
            if 'svapn' in line.lower():
                # Count occurrences in this line
                svapna_in_line = re.findall(r'svapn\w*', line, re.IGNORECASE)
                total_svapna_count += len(svapna_in_line)
                
                # Get 6-8 lines of context (3-4 before, current, 2-3 after)
                start = max(0, line_idx - 3)
                end = min(len(lines), line_idx + 4)
                context_lines = []
                
                for i in range(start, end):
                    # Clean each line
                    clean_line = lines[i].strip()
                    # Remove verse markers but keep verse numbers
                    clean_line = re.sub(r'\|\|([^|]+)\|\|', r'[\1]', clean_line)
                    if clean_line:
                        context_lines.append(clean_line)
                
                if context_lines:
                    context_text = '\n'.join(context_lines)
                    
                    # Create snippet object
                    snippet = {
                        'id': f"{filename}_{line_idx}",
                        'text': text_name,
                        'tradition': tradition or 'Unknown',
                        'author': author or 'Unknown',
                        'line_number': line_idx + 1,
                        'context': context_text,
                        'svapna_count': len(svapna_in_line),
                        'categories': []
                    }
                    
                    # Categorize the snippet
                    context_lower = context_text.lower()
                    for cat_name, cat_data in categories.items():
                        for pattern in cat_data['patterns']:
                            if re.search(pattern, context_lower, re.IGNORECASE):
                                cat_data['count'] += 1
                                cat_data['snippets'].append(snippet['id'])
                                snippet['categories'].append(cat_name)
                                break
                    
                    # Add to all snippets
                    all_snippets.append(snippet)
    
    print(f"\nExtraction complete!")
    print(f"Total svapna occurrences: {total_svapna_count}")
    print(f"Total snippets extracted: {len(all_snippets)}")
    print(f"\nCategory distribution:")
    for cat_name, cat_data in categories.items():
        print(f"  {cat_name}: {cat_data['count']} occurrences")
    
    # Create output structure
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_texts': len(all_results),
        'total_occurrences': total_svapna_count,
        'total_snippets': len(all_snippets),
        'categories': {},
        'all_snippets': all_snippets
    }
    
    # Add category summaries
    for cat_name, cat_data in categories.items():
        output['categories'][cat_name] = {
            'count': cat_data['count'],
            'percentage': round((cat_data['count'] / total_svapna_count * 100), 2) if total_svapna_count > 0 else 0,
            'snippet_ids': cat_data['snippets'][:100]  # First 100 IDs per category
        }
    
    # Save to JSON
    print(f"\nSaving to svapna_all_snippets.json...")
    with open('/Users/mariaiontseva/svapna-deploy/svapna_all_snippets.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(all_snippets)} snippets!")
    
    # Also create a lighter version for web display (first 500 snippets per category)
    output_light = {
        'timestamp': output['timestamp'],
        'total_texts': output['total_texts'],
        'total_occurrences': output['total_occurrences'],
        'total_snippets': output['total_snippets'],
        'categories': output['categories'],
        'snippets_by_category': {}
    }
    
    # Group snippets by category for easier access
    for cat_name in categories.keys():
        cat_snippets = [s for s in all_snippets if cat_name in s['categories']]
        output_light['snippets_by_category'][cat_name] = cat_snippets[:500]
    
    # Add uncategorized snippets
    uncategorized = [s for s in all_snippets if not s['categories']]
    output_light['snippets_by_category']['uncategorized'] = uncategorized[:500]
    
    # Save light version
    with open('/Users/mariaiontseva/svapna-deploy/svapna_snippets_display.json', 'w', encoding='utf-8') as f:
        json.dump(output_light, f, ensure_ascii=False, indent=2)
    
    print(f"Also saved display version with categorized snippets")
    
    conn.close()
    return output

if __name__ == "__main__":
    extract_all_svapna_snippets()