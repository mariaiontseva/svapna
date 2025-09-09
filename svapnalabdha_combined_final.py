#!/usr/bin/env python3

import sqlite3
import json
import re
from datetime import datetime

def connect_db():
    """Connect to SQLite database"""
    db_path = '/Users/mariaiontseva/sanskrit_texts.db'
    return sqlite3.connect(db_path)

def search_svapnalabdha():
    """Search for all svapnalabdha occurrences with context"""
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Search for svapnalabdha (various forms)
    patterns = [
        '%svapnalabdh%',
        '%svapna-labdh%',
        '%svapna labdh%'
    ]
    
    all_results = []
    
    for pattern in patterns:
        cursor.execute("""
            SELECT t.display_name, t.tradition, t.author, t.period, si.content, si.filename
            FROM search_index si 
            JOIN texts t ON si.filename = t.filename
            WHERE LOWER(si.content) LIKE LOWER(?)
            ORDER BY t.display_name
        """, (pattern,))
        
        for row in cursor.fetchall():
            text_name = row[0]
            tradition = row[1] or 'Unknown Tradition'
            author = row[2] or 'Unknown'
            period = row[3] or 'Unknown Period'
            content = row[4]
            filename = row[5]
            
            # Find all occurrences in this text
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'svapna[\s-]?labdh', line, re.IGNORECASE):
                    # Get context (3 lines before and after)
                    start = max(0, i - 3)
                    end = min(len(lines), i + 4)
                    context_lines = lines[start:end]
                    
                    # Clean the lines
                    context_lines = [re.sub(r'\|', '', line).strip() for line in context_lines]
                    context_lines = [line for line in context_lines if line]
                    
                    # Extract the specific compound
                    compound_match = re.search(r'(svapna[\s-]?labdh\w*)', line, re.IGNORECASE)
                    compound = compound_match.group(1) if compound_match else 'svapnalabdha'
                    
                    result = {
                        'text': text_name,
                        'author': author,
                        'tradition': tradition,
                        'filename': filename,
                        'compound': compound,
                        'line_number': i + 1,
                        'sanskrit_lines': context_lines
                    }
                    
                    all_results.append(result)
    
    conn.close()
    return all_results

# Complete English translations mapped by text and line
english_translations = {
    "AcaraBhedaTantra": {
        "default": "In the Vaishampayana collection addressed to Shaunaka, in the words of Vyasa, verse 72: In the Yogini Tantra it states - powerless is the mantra from one's father, likewise from the maternal grandfather. That which is obtained in a dream or given by a woman becomes pure only through proper consecration, verse 73. But that woman who is virtuous and of good conduct, devoted to the guru, with controlled senses, knowledgeable in all mantra meanings and principles, of good character, engaged in worship - she should be considered worthy as a guru."
    },
    "Agnipuranam": {
        3602: "Seeing a blazing fire, worshipping Shiva, or Vishnu - one who obtains a mantra in a dream sees the accomplishment of that mantra.",
        7773: "One who sees or obtains a mantra in a dream while sleeping, that mantra quickly bears fruit for them."
    },
    "Anandbhairav Kalpa": {
        813: "Through the mouth of the guru I obtained the knowledge called dream-obtained. He who seeks accomplishment in illusion magic without mantra and meditation - the sages say he is confused by delusion, fallen from the authority of scriptures.",
        2165: "Dream-obtained means gained through a dream - that knowledge which he obtained. The fool who seeks accomplishment in the supreme tantra filled with meditation on Brahman without mantra and meditation is confused by delusion. Fallen from scriptural authority means one who lacks the eligibility described in scripture. Accomplishment in illusion magic can also be accomplished through this dream-obtained supreme knowledge alone."
    },
    "Bhutadamaratantra": {
        "default": "One should offer meat, liquor and other substances to one's mantra. That which is obtained in a dream, heard, or seen - all that should be concealed."
    },
    "Brahmayamalam": {
        8975: "Even thousands and millions of mantras obtained in dreams do not succeed. Because I have compassion for you, I speak what brings welfare to all people.",
        21562: "In sleep, what is obtained in a dream from the guru's mouth becomes fruitful. And that mantra given by a woman is successful, so say the best of the twice-born. I speak of the mantra that bestows all accomplishments, there is no doubt in this."
    },
    "Durgarcanasrti": {
        "default": "That mantra obtained in a dream or given by a woman becomes accomplished through consecration alone. After knowing one's own mantra, one should perform consecration and purification."
    },
    "Gautama Tantram": {
        "default": "A valiant hero free from sorrow, with five faces. That which is dream-obtained or woman-given becomes pure through consecration alone."
    },
    "JayaSamhita": {
        "default": "That which is obtained in a dream is purified through consecration alone. And that given by a woman also becomes pure through consecration."
    },
    "Kaksaputtantra": {
        "default": "That which is obtained in a dream or given by a woman is purified through consecration alone. But a woman who is virtuous, of good conduct, devoted to the guru, with controlled senses, knowing all mantra meanings and principles, of good character, engaged in worship - she should be worthy as a guru."
    },
    "Kalivilasatantra": {
        "default": "What is obtained in a dream or given by a woman is accomplished through proper ritual consecration. But that woman should be initiated, a great practitioner, intent on repeating her received mantra, of good qualities, knowing the meaning of mantras, devoted to the guru, and with conquered senses."
    },
    "Kamadhenutantra": {
        "default": "That given by a woman or obtained in a dream - the practitioner accomplishes it quickly through consecration alone."
    },
    "Kaulajnananirnaya": {
        "default": "The highest secret mantra, whether obtained in a dream or given by a woman, for one who desires accomplishment - that certainly becomes fruitful through consecration. I have obtained the vidya mantra in a dream, received from the guru's lotus mouth."
    },
    "Kularatnoddyota": {
        "default": "What is obtained in a dream or given by a woman - that great mantra is accomplished through consecration alone."
    },
    "Mahakalasamhita Guhyakalikhanda": {
        "default": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    "Mahakalasaṃhita Kamakalakhanda": {
        "default": "What is obtained in a dream or given by a woman should be consecrated by the practitioner."
    },
    "MahanirvaNatantram": {
        "default": "What is obtained in a dream or given by a woman - that mantra becomes fruitful through consecration."
    },
    "Matasara": {
        "default": "Through these five consecrations, what is obtained in a dream and what is woman-given becomes pure - thus it is remembered in the tradition."
    },
    "Merutantram": {
        "default": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    "Niruttaratantram": {
        "default": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    "Prapancasaratantram": {
        "default": "Through effort alone, Parvati, the mantras that are self-arisen, obtained in dreams, or given by women become accomplished."
    },
    "Rudrayamalam": {
        17839: "What is obtained in a dream or given by a woman is purified through consecration alone.",
        25309: "What is obtained in a dream or given by a woman becomes fruitful through consecration. What is self-arisen also becomes accomplished through consecration."
    },
    "Samvarodayatantram": {
        "default": "By the accomplished yogini, a garland equal to pearls was made. Having purified the supreme essence through various tantras and obtained in a dream from the lineage - thus having been accomplished, this is now being composed by me."
    },
    "Saradatilaka": {
        "default": "Even the supreme mantra, when obtained in a dream or given by a woman, if one desiring accomplishment performs consecration with devotion - it will certainly bear fruit."
    },
    "Siddhikaumaritantram": {
        "default": "What is obtained in a dream or given by a woman - that is accomplished through consecration alone."
    },
    "Tripurasarasamuccaya": {
        "default": "That mantra obtained in a dream becomes fruitful through consecration and through the grace received from devotion to the guru."
    },
    "Vamajalatantram": {
        "default": "The text has reached me through the lineage in three streams. Now by that very stream, obtained in a dream through the lineage. This collected essence extracted from a hundred million tantras - this Bhairava Sarvabhauma tantra is being remembered."
    },
    "Visnuyamalam": {
        "default": "What is obtained in a dream or given by a woman is accomplished through consecration alone."
    },
    "Yoginitantram": {
        "default": "Powerless is the father's mantra, likewise the maternal grandfather's. What is obtained in a dream or given by a woman is purified through consecration alone."
    }
}

def create_combined_json():
    """Create JSON with both Sanskrit and English"""
    
    results = search_svapnalabdha()
    
    # Add English translations to each result
    for result in results:
        text_name = result['text']
        line_num = result['line_number']
        
        # Get the appropriate English translation
        if text_name in english_translations:
            text_trans = english_translations[text_name]
            if isinstance(text_trans, dict):
                # Check for line-specific translation
                if line_num in text_trans:
                    result['english_translation'] = text_trans[line_num]
                else:
                    result['english_translation'] = text_trans.get("default", "Translation not available")
            else:
                result['english_translation'] = text_trans
        else:
            result['english_translation'] = "Translation not available"
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_occurrences": len(results),
        "unique_texts": len(set(r['text'] for r in results)),
        "occurrences": results
    }
    
    with open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_complete_final.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Created svapnalabdha_complete_final.json with {len(results)} occurrences")
    print(f"Unique texts: {output['unique_texts']}")

if __name__ == "__main__":
    create_combined_json()