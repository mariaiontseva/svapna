#!/usr/bin/env python3

import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime

def find_svapna_diksha_collocations():
    """Find all svapna + dīkṣā collocations and other interesting patterns"""
    
    # Connect to database
    conn = sqlite3.connect('/Users/mariaiontseva/muktabodha_texts.db')
    cursor = conn.cursor()
    
    # Get all svapna occurrences with context
    cursor.execute("""
        SELECT t.display_name, t.tradition, si.content
        FROM search_index si 
        JOIN texts t ON si.filename = t.filename
        WHERE LOWER(si.content) LIKE '%svapn%'
        ORDER BY t.display_name
    """)
    
    results = cursor.fetchall()
    print(f"Found {len(results)} svapna occurrences")
    
    # Collections for analysis
    diksha_contexts = []
    visualization_contexts = []
    yoga_contexts = []
    mantra_contexts = []
    guru_contexts = []
    deity_contexts = []
    siddhi_contexts = []
    japa_contexts = []
    
    # Bigrams and trigrams
    bigrams = Counter()
    trigrams = Counter()
    compounds = Counter()
    
    # Patterns to search for
    diksha_patterns = [
        r'dīkṣ[aāiīuūeo]',
        r'dīkṣit[aāiīuūeo]',
        r'upadeś[aāiīuūeo]',
        r'abhiṣek[aāiīuūeo]',
        r'saṃskār[aāiīuūeo]'
    ]
    
    visualization_patterns = [
        r'darśan[aāiīuūeo]',
        r'dṛṣṭ[aāiīuūeo]',
        r'paśy[aāiīuūeo]',
        r'bhāvan[aāiīuūeo]',
        r'dhyān[aāiīuūeo]',
        r'cakṣu',
        r'netr[aāiīuūeo]',
        r'ālok[aāiīuūeo]',
        r'prakāś[aāiīuūeo]'
    ]
    
    yoga_patterns = [
        r'yog[aāiīuūeo]',
        r'samādh[aāiīuūeo]',
        r'prāṇāyām[aāiīuūeo]',
        r'āsan[aāiīuūeo]',
        r'mudr[aāiīuūeo]',
        r'bandh[aāiīuūeo]'
    ]
    
    mantra_patterns = [
        r'mantr[aāiīuūeo]',
        r'vidyā',
        r'bīj[aāiīuūeo]',
        r'jap[aāiīuūeo]',
        r'stotr[aāiīuūeo]'
    ]
    
    for text_name, tradition, content in results:
        # Clean content
        content_clean = re.sub(r'\|\|.*?\|\|', '', content)
        content_clean = re.sub(r'[0-9]+', '', content_clean)
        words = content_clean.split()
        
        for i, word in enumerate(words):
            if 'svapn' in word.lower():
                # Get context window (5 words before and after)
                start = max(0, i-5)
                end = min(len(words), i+6)
                context_window = ' '.join(words[start:end])
                
                # Record bigrams
                if i > 0:
                    bigrams[f"{words[i-1]} svapna"] += 1
                if i < len(words)-1:
                    bigrams[f"svapna {words[i+1]}"] += 1
                
                # Record trigrams
                if i > 1:
                    trigrams[f"{words[i-2]} {words[i-1]} svapna"] += 1
                if i < len(words)-2:
                    trigrams[f"svapna {words[i+1]} {words[i+2]}"] += 1
                
                # Check for compounds
                if len(word) > 7:
                    compounds[word] += 1
                
                # Check for dīkṣā collocations
                for pattern in diksha_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        diksha_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'context': context_window,
                            'full_line': content_clean
                        })
                        break
                
                # Check for visualization
                for pattern in visualization_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        visualization_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'context': context_window
                        })
                        break
                
                # Check for yoga
                for pattern in yoga_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        yoga_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'context': context_window
                        })
                        break
                
                # Check for mantra
                for pattern in mantra_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        mantra_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'context': context_window
                        })
                        break
    
    # Deduplicate contexts
    diksha_contexts = list({(d['text'], d['context']): d for d in diksha_contexts}.values())
    visualization_contexts = list({(d['text'], d['context']): d for d in visualization_contexts}.values())
    yoga_contexts = list({(d['text'], d['context']): d for d in yoga_contexts}.values())
    mantra_contexts = list({(d['text'], d['context']): d for d in mantra_contexts}.values())
    
    # Sort by frequency
    top_bigrams = bigrams.most_common(100)
    top_trigrams = trigrams.most_common(50)
    top_compounds = compounds.most_common(50)
    
    # Create analysis
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_occurrences': len(results),
        'unique_texts': len(set(r[0] for r in results)),
        'collocations': {
            'diksha_svapna': {
                'count': len(diksha_contexts),
                'texts': len(set(d['text'] for d in diksha_contexts)),
                'examples': diksha_contexts[:30]
            },
            'visualization_svapna': {
                'count': len(visualization_contexts),
                'texts': len(set(d['text'] for d in visualization_contexts)),
                'examples': visualization_contexts[:30]
            },
            'yoga_svapna': {
                'count': len(yoga_contexts),
                'texts': len(set(d['text'] for d in yoga_contexts)),
                'examples': yoga_contexts[:30]
            },
            'mantra_svapna': {
                'count': len(mantra_contexts),
                'texts': len(set(d['text'] for d in mantra_contexts)),
                'examples': mantra_contexts[:30]
            }
        },
        'top_bigrams': [{'phrase': b[0], 'count': b[1]} for b in top_bigrams],
        'top_trigrams': [{'phrase': t[0], 'count': t[1]} for t in top_trigrams],
        'top_compounds': [{'compound': c[0], 'count': c[1]} for c in top_compounds],
        'special_bigrams': {
            'with_diksha': [b for b in top_bigrams if any(p in b[0].lower() for p in ['dīkṣ', 'dikṣ'])],
            'with_vision': [b for b in top_bigrams if any(p in b[0].lower() for p in ['darś', 'dṛṣṭ', 'paśy'])],
            'with_yoga': [b for b in top_bigrams if 'yog' in b[0].lower()],
            'with_mantra': [b for b in top_bigrams if 'mantr' in b[0].lower()],
            'with_guru': [b for b in top_bigrams if any(p in b[0].lower() for p in ['guru', 'ācāry'])],
            'with_deity': [b for b in top_bigrams if any(p in b[0].lower() for p in ['dev', 'śiv', 'śakt', 'viṣṇ', 'kṛṣṇ'])]
        }
    }
    
    # Save analysis
    with open('/Users/mariaiontseva/svapna-deploy/svapna_diksha_collocations.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== SVAPNA COLLOCATION ANALYSIS ===")
    print(f"Total occurrences: {len(results)}")
    print(f"Unique texts: {len(set(r[0] for r in results))}")
    print(f"\n=== SPECIAL COLLOCATIONS ===")
    print(f"Dīkṣā-svapna: {len(diksha_contexts)} occurrences in {len(set(d['text'] for d in diksha_contexts))} texts")
    print(f"Visualization-svapna: {len(visualization_contexts)} occurrences")
    print(f"Yoga-svapna: {len(yoga_contexts)} occurrences")
    print(f"Mantra-svapna: {len(mantra_contexts)} occurrences")
    print(f"\n=== TOP BIGRAMS ===")
    for phrase, count in top_bigrams[:10]:
        print(f"  {phrase}: {count}")
    print(f"\n=== TOP COMPOUNDS ===")
    for compound, count in top_compounds[:10]:
        print(f"  {compound}: {count}")
    
    conn.close()
    return analysis

if __name__ == "__main__":
    find_svapna_diksha_collocations()