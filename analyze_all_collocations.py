#!/usr/bin/env python3

import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime

def analyze_all_svapna_collocations():
    """Comprehensive analysis of all svapna collocations across all texts"""
    
    # Connect to database
    conn = sqlite3.connect('/Users/mariaiontseva/muktabodha_texts.db')
    cursor = conn.cursor()
    
    # Get ALL texts with svapna
    cursor.execute("""
        SELECT t.display_name, t.tradition, t.author, t.period, si.content
        FROM search_index si 
        JOIN texts t ON si.filename = t.filename
        WHERE LOWER(si.content) LIKE '%svapn%'
        ORDER BY t.display_name
    """)
    
    results = cursor.fetchall()
    print(f"Found {len(results)} texts with svapna occurrences")
    
    # Detailed categorization
    categories = {
        'initiation': {
            'patterns': [r'dīkṣ[aāiīuūeo]', r'upadeś[aāiīuūeo]', r'abhiṣek[aāiīuūeo]', 
                        r'saṃskār[aāiīuūeo]', r'śaktipāt[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'visualization': {
            'patterns': [r'darśan[aāiīuūeo]', r'dṛṣṭ[aāiīuūeo]', r'paśy[aāiīuūeo]', 
                        r'bhāvan[aāiīuūeo]', r'dhyān[aāiīuūeo]', r'cakṣu', r'netr[aāiīuūeo]',
                        r'ālok[aāiīuūeo]', r'prakāś[aāiīuūeo]', r'dṛś[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'yoga_practice': {
            'patterns': [r'yog[aāiīuūeo]', r'samādh[aāiīuūeo]', r'prāṇāyām[aāiīuūeo]', 
                        r'āsan[aāiīuūeo]', r'mudr[aāiīuūeo]', r'bandh[aāiīuūeo]', r'kuṇḍalin[īi]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'mantra_vidya': {
            'patterns': [r'mantr[aāiīuūeo]', r'vidyā', r'bīj[aāiīuūeo]', r'jap[aāiīuūeo]', 
                        r'stotr[aāiīuūeo]', r'kavac[aāiīuūeo]', r'nyās[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'guru_transmission': {
            'patterns': [r'guru', r'ācāry[aāiīuūeo]', r'deśik[aāiīuūeo]', r'śiṣy[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'deity_communion': {
            'patterns': [r'dev[aāiīuūeo]', r'śiv[aāiīuūeo]', r'śakt[iī]', r'viṣṇ[uū]', 
                        r'kṛṣṇ[aāiīuūeo]', r'gaṇeś[aāiīuūeo]', r'bhairav[aāiīuūeo]', 
                        r'kāl[īi]', r'tār[aāiīuūeo]', r'durg[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'consciousness_states': {
            'patterns': [r'jāgr[aṛ]t', r'suṣupt[aāiīuūeo]', r'turīy[aāiīuūeo]', r'cetan[aāiīuūeo]',
                        r'bodh[aāiīuūeo]', r'prabodh[aāiīuūeo]', r'nidr[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'tantric_practice': {
            'patterns': [r'tantr[aāiīuūeo]', r'yantr[aāiīuūeo]', r'cakr[aāiīuūeo]', 
                        r'maṇḍal[aāiīuūeo]', r'pūj[aāiīuūeo]', r'hom[aāiīuūeo]', r'yāg[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'siddhi_powers': {
            'patterns': [r'siddh[aāiīuūeo]', r'vibhūt[iī]', r'aiśvary[aāiīuūeo]', 
                        r'śakt[iī]', r'bal[aāiīuūeo]', r'phal[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'philosophical': {
            'patterns': [r'māy[aāiīuūeo]', r'brahm[aāiīuūeo]', r'ātm[aāiīuūeo]', 
                        r'tattv[aāiīuūeo]', r'saṃsār[aāiīuūeo]', r'mokṣ[aāiīuūeo]', r'mukti'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'time_context': {
            'patterns': [r'kāl[aāiīuūeo]', r'rātr[aāiīuūeoau]', r'niś[aāiīuūeo]', 
                        r'divā', r'ahorātr[aāiīuūeo]', r'muhūrt[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        },
        'body_subtle': {
            'patterns': [r'nāḍ[īi]', r'prāṇ[aāiīuūeo]', r'vāyu', r'bindu', r'śarīr[aāiīuūeo]',
                        r'deha', r'kāy[aāiīuūeo]', r'sūkṣm[aāiīuūeo]'],
            'count': 0,
            'texts': set(),
            'examples': []
        }
    }
    
    # Analyze each text
    text_analysis = {}
    total_svapna_count = 0
    
    for text_name, tradition, author, period, content in results:
        if text_name not in text_analysis:
            text_analysis[text_name] = {
                'tradition': tradition,
                'author': author,
                'period': period,
                'svapna_count': 0,
                'categories': []
            }
        
        # Clean content
        content_clean = re.sub(r'\|\|.*?\|\|', '', content)
        content_clean = re.sub(r'[0-9]+', '', content_clean)
        
        # Count svapna occurrences in this text
        svapna_matches = re.findall(r'svapn[aāiīuūeo\w]*', content_clean, re.IGNORECASE)
        text_analysis[text_name]['svapna_count'] += len(svapna_matches)
        total_svapna_count += len(svapna_matches)
        
        # Find collocations for each category
        words = content_clean.split()
        for i, word in enumerate(words):
            if 'svapn' in word.lower():
                # Get context window
                start = max(0, i-7)
                end = min(len(words), i+8)
                context_window = ' '.join(words[start:end])
                
                # Check each category
                for cat_name, cat_data in categories.items():
                    for pattern in cat_data['patterns']:
                        if re.search(pattern, context_window, re.IGNORECASE):
                            cat_data['count'] += 1
                            cat_data['texts'].add(text_name)
                            if len(cat_data['examples']) < 5:  # Keep top 5 examples
                                cat_data['examples'].append({
                                    'text': text_name,
                                    'tradition': tradition,
                                    'context': context_window[:200]  # First 200 chars
                                })
                            if cat_name not in text_analysis[text_name]['categories']:
                                text_analysis[text_name]['categories'].append(cat_name)
                            break
    
    # Calculate percentages and prepare data
    category_stats = {}
    for cat_name, cat_data in categories.items():
        category_stats[cat_name] = {
            'count': cat_data['count'],
            'percentage': round((cat_data['count'] / total_svapna_count * 100), 2) if total_svapna_count > 0 else 0,
            'unique_texts': len(cat_data['texts']),
            'examples': cat_data['examples']
        }
    
    # Sort by count
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # Tradition-wise analysis
    tradition_stats = defaultdict(lambda: {'texts': 0, 'svapna_count': 0})
    for text_name, data in text_analysis.items():
        if data['tradition']:
            tradition_stats[data['tradition']]['texts'] += 1
            tradition_stats[data['tradition']]['svapna_count'] += data['svapna_count']
    
    # Create comprehensive analysis
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_texts': len(text_analysis),
        'total_svapna_occurrences': total_svapna_count,
        'categories': dict(sorted_categories),
        'tradition_distribution': dict(tradition_stats),
        'top_texts_by_svapna': sorted(
            [(name, data['svapna_count']) for name, data in text_analysis.items()],
            key=lambda x: x[1], reverse=True
        )[:20],
        'text_details': text_analysis
    }
    
    # Save analysis
    with open('/Users/mariaiontseva/svapna-deploy/svapna_comprehensive_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    # Print summary
    print(f"\n=== COMPREHENSIVE SVAPNA ANALYSIS ===")
    print(f"Total texts analyzed: {len(text_analysis)}")
    print(f"Total svapna occurrences: {total_svapna_count}")
    print(f"\n=== CATEGORY DISTRIBUTION ===")
    for cat_name, stats in sorted_categories:
        print(f"{cat_name:25} {stats['count']:6} ({stats['percentage']:5.1f}%) in {stats['unique_texts']} texts")
    
    print(f"\n=== TRADITION DISTRIBUTION ===")
    for tradition, stats in tradition_stats.items():
        print(f"{tradition:20} {stats['texts']} texts, {stats['svapna_count']} occurrences")
    
    conn.close()
    return analysis

if __name__ == "__main__":
    analyze_all_svapna_collocations()