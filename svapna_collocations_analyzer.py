#!/usr/bin/env python3

import json
import re
from collections import defaultdict, Counter
from datetime import datetime

def analyze_svapna_collocations():
    """Find all interesting collocations where svapna occurs"""
    
    # Load existing svapna analysis data
    with open('/Users/mariaiontseva/svapna-deploy/svapna_analysis.json', 'r', encoding='utf-8') as f:
        svapna_data = json.load(f)
    
    results = svapna_data['results']
    print(f"Found {len(results)} svapna occurrences")
    
    # Analyze collocations
    collocations = defaultdict(list)
    diksha_contexts = []
    visualization_contexts = []
    compound_patterns = Counter()
    bigrams = Counter()
    trigrams = Counter()
    
    # Patterns to look for
    diksha_patterns = [
        r'dīkṣā.*svapn',
        r'svapn.*dīkṣā',
        r'dīkṣita.*svapn',
        r'svapn.*dīkṣita',
        r'svapne.*dīkṣā',
        r'svapnopadesa',
        r'svapnādīkṣā'
    ]
    
    visualization_patterns = [
        r'svapn.*darśan',
        r'darśan.*svapn',
        r'svapn.*dṛṣṭ',
        r'dṛṣṭ.*svapn',
        r'svapn.*paśy',
        r'paśy.*svapn',
        r'svapn.*bhāvan',
        r'bhāvan.*svapn',
        r'svapn.*dhyān',
        r'dhyān.*svapn',
        r'svapn.*cakṣu',
        r'svapn.*netra'
    ]
    
    for occ in results:
        text_name = occ.get('text', '')
        tradition = occ.get('tradition', '')
        content = occ.get('content', '')
        line_num = occ.get('line_number', 0)
        
        # Clean content
        content_clean = re.sub(r'\|\|.*?\|\|', '', content)
        content_clean = re.sub(r'[0-9]+', '', content_clean)
        
        # Find svapna position
        words = content_clean.split()
        
        for i, word in enumerate(words):
            if 'svapn' in word.lower():
                # Get context words
                prev_word = words[i-1] if i > 0 else ''
                next_word = words[i+1] if i < len(words)-1 else ''
                prev2_word = words[i-2] if i > 1 else ''
                next2_word = words[i+2] if i < len(words)-2 else ''
                
                # Record bigrams
                if prev_word:
                    bigrams[f"{prev_word} + svapna"] += 1
                if next_word:
                    bigrams[f"svapna + {next_word}"] += 1
                
                # Record trigrams
                if prev_word and prev2_word:
                    trigrams[f"{prev2_word} {prev_word} svapna"] += 1
                if next_word and next2_word:
                    trigrams[f"svapna {next_word} {next2_word}"] += 1
                
                # Check for compounds
                if '-' in word or len(word) > 10:
                    compound_patterns[word] += 1
                
                # Check for dīkṣā collocations
                context_window = ' '.join(words[max(0, i-5):min(len(words), i+6)])
                for pattern in diksha_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        diksha_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'line': line_num,
                            'context': context_window,
                            'pattern': pattern
                        })
                        break
                
                # Check for visualization collocations
                for pattern in visualization_patterns:
                    if re.search(pattern, context_window, re.IGNORECASE):
                        visualization_contexts.append({
                            'text': text_name,
                            'tradition': tradition,
                            'line': line_num,
                            'context': context_window,
                            'pattern': pattern
                        })
                        break
    
    # Get top collocations
    top_bigrams = bigrams.most_common(50)
    top_trigrams = trigrams.most_common(30)
    top_compounds = compound_patterns.most_common(50)
    
    # Special interest collocations
    special_collocations = {
        'dream_initiation': [],
        'dream_vision': [],
        'dream_yoga': [],
        'dream_mantra': [],
        'dream_guru': [],
        'dream_deity': [],
        'dream_practice': [],
        'dream_signs': []
    }
    
    # Categorize special collocations
    for bigram, count in bigrams.items():
        lower_bigram = bigram.lower()
        
        if any(term in lower_bigram for term in ['dīkṣ', 'dikṣ', 'upadeś']):
            special_collocations['dream_initiation'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['darś', 'dṛṣṭ', 'paśy', 'cakṣu']):
            special_collocations['dream_vision'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['yoga', 'yog', 'dhyān', 'samādhi']):
            special_collocations['dream_yoga'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['mantra', 'vidyā', 'bīja']):
            special_collocations['dream_mantra'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['guru', 'ācārya', 'deśika']):
            special_collocations['dream_guru'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['deva', 'devī', 'īśvara', 'śiva', 'śakti']):
            special_collocations['dream_deity'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['sādhanā', 'abhyāsa', 'prayoga']):
            special_collocations['dream_practice'].append({'phrase': bigram, 'count': count})
        elif any(term in lower_bigram for term in ['lakṣaṇa', 'cihna', 'saṅketa', 'phala']):
            special_collocations['dream_signs'].append({'phrase': bigram, 'count': count})
    
    # Sort special collocations
    for category in special_collocations:
        special_collocations[category].sort(key=lambda x: x['count'], reverse=True)
    
    # Create analysis result
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_occurrences': len(results),
        'diksha_collocations': {
            'count': len(diksha_contexts),
            'contexts': diksha_contexts[:20]  # Top 20
        },
        'visualization_collocations': {
            'count': len(visualization_contexts),
            'contexts': visualization_contexts[:20]  # Top 20
        },
        'top_bigrams': [{'phrase': bg[0], 'count': bg[1]} for bg in top_bigrams],
        'top_trigrams': [{'phrase': tg[0], 'count': tg[1]} for tg in top_trigrams],
        'top_compounds': [{'compound': cp[0], 'count': cp[1]} for cp in top_compounds],
        'special_collocations': special_collocations,
        'statistical_summary': {
            'unique_bigrams': len(bigrams),
            'unique_trigrams': len(trigrams),
            'unique_compounds': len(compound_patterns),
            'texts_with_diksha_svapna': len(set(ctx['text'] for ctx in diksha_contexts)),
            'texts_with_visualization_svapna': len(set(ctx['text'] for ctx in visualization_contexts))
        }
    }
    
    # Save analysis
    with open('/Users/mariaiontseva/svapna-deploy/svapna_collocations_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\nAnalysis complete!")
    print(f"Found {len(diksha_contexts)} dīkṣā-svapna collocations")
    print(f"Found {len(visualization_contexts)} visualization-svapna collocations")
    print(f"Top bigrams: {top_bigrams[:5]}")
    print(f"Saved to svapna_collocations_analysis.json")
    
    return analysis

if __name__ == "__main__":
    analyze_svapna_collocations()