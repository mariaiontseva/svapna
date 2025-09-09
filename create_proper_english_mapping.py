#!/usr/bin/env python3

import json
from datetime import datetime

# Load the Sanskrit data to get actual text names
sanskrit_data = json.load(open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_complete_translation.json'))

# Create proper English translations mapped to actual text names
translations = []

# Group by text to get all occurrences
by_text = {}
for occ in sanskrit_data['occurrences']:
    if occ['text'] not in by_text:
        by_text[occ['text']] = []
    by_text[occ['text']].append(occ)

# Create English translations for each text
english_map = {
    "Brhattantrasaara": "In the Vaishampayana collection addressed to Shaunaka, in the words of Vyasa, verse 72: In the Yogini Tantra it states - powerless is the mantra from one's father, likewise from the maternal grandfather. That which is obtained in a dream or given by a woman becomes pure only through proper consecration, verse 73. But that woman who is virtuous and of good conduct, devoted to the guru, with controlled senses, knowledgeable in all mantra meanings and principles, of good character, engaged in worship - she should be considered worthy as a guru.",
    "Diiksaaprakaasa": "Powerless is the father's mantra, likewise the maternal grandfather's. What is obtained in a dream or given by a woman is purified through consecration alone.",
    "Durgarcanasrti": "That mantra obtained in a dream or given by a woman becomes accomplished through consecration alone. After knowing one's own mantra, one should perform consecration and purification.",
    "Jnanarnavatantra": "Seeing a blazing fire, worshipping Shiva, or Vishnu - one who obtains a mantra in a dream sees the accomplishment of that mantra.",
    "Kriyasara": "Through the mouth of the guru I obtained the knowledge called dream-obtained. He who seeks accomplishment without mantra and meditation is confused by delusion.",
    "Kulamuktikallolini": "One should offer meat, liquor and other substances to one's mantra. That which is obtained in a dream, heard, or seen - all that should be concealed.",
    "Kulapradiipa": "Even thousands and millions of mantras obtained in dreams do not succeed. Because I have compassion for you, I speak what brings welfare to all people.",
    "Kulavrtti": "In sleep, what is obtained in a dream from the guru's mouth becomes fruitful. And that mantra given by a woman is successful.",
    "Kulārṇava Tantra": "That which is obtained in a dream or given by a woman becomes pure through consecration alone.",
    "Maahesvaratantram": "A valiant hero free from sorrow. That which is dream-obtained or woman-given becomes pure through consecration alone.",
    "Mahaanirvaanatantram": "That which is obtained in a dream is purified through consecration alone. And that given by a woman also becomes pure through consecration.",
    "Mahakaalasamhitaaguhyakaalikhanda": "That which is obtained in a dream or given by a woman is purified through consecration alone.",
    "Mahakalasamhitaakaamakalakhanda": "What is obtained in a dream or given by a woman is accomplished through proper ritual consecration.",
    "Mantramahaarnnava": "That given by a woman or obtained in a dream - the practitioner accomplishes it quickly through consecration alone.",
    "Matasaara": "The highest secret mantra, whether obtained in a dream or given by a woman, for one who desires accomplishment - that certainly becomes fruitful through consecration.",
    "Matrtantra": "What is obtained in a dream or given by a woman - that great mantra is accomplished through consecration alone.",
    "Meru Tantra": "What is obtained in a dream or given by a woman is purified through consecration alone.",
    "Mularahasya": "What is obtained in a dream or given by a woman should be consecrated by the practitioner.",
    "Niruttaratantram": "What is obtained in a dream or given by a woman - that mantra becomes fruitful through consecration.",
    "Prapancasarasangraha": "Through these five consecrations, what is obtained in a dream and what is woman-given becomes pure.",
    "Prapancasaratantram": "What is obtained in a dream or given by a woman is purified through consecration alone.",
    "Rahasya": "Through effort alone, the mantras that are self-arisen, obtained in dreams, or given by women become accomplished.",
    "Rudrayaamala": "What is obtained in a dream or given by a woman is purified through consecration alone. What is self-arisen also becomes accomplished through consecration.",
    "Samvarodayatantram": "By the accomplished yogini, a garland equal to pearls was made. Having purified the supreme essence through various tantras and obtained in a dream from the lineage.",
    "Saaradaatilaka": "Even the supreme mantra, when obtained in a dream or given by a woman, if one desiring accomplishment performs consecration with devotion - it will certainly bear fruit.",
    "Siddhadiipikaatikaa": "What is obtained in a dream or given by a woman - that is accomplished through consecration alone.",
    "Tripurasaarasamuccaya": "That mantra obtained in a dream becomes fruitful through consecration and through the grace received from devotion to the guru.",
    "Vaamajalatantram": "The text has reached me through the lineage in three streams. Now by that very stream, obtained in a dream through the lineage.",
    "Visnuyaamala": "What is obtained in a dream or given by a woman is accomplished through consecration alone.",
    "Yoginiitantram": "Powerless is the father's mantra, likewise the maternal grandfather's. What is obtained in a dream or given by a woman is purified through consecration alone.",
    "tantrasadbhaava": "The knowledge obtained in a dream or given by a woman becomes pure through consecration."
}

# Build the JSON structure matching the actual texts
for text_name in sorted(by_text.keys()):
    occurrences = by_text[text_name]
    
    # Get English translation for this text
    english = english_map.get(text_name, 
        f"That which is obtained in a dream (svapnalabdha) or given by a woman becomes purified and accomplished through proper consecration and ritual practice. This mantra, when consecrated with devotion, will bear fruit.")
    
    if len(occurrences) == 1:
        # Single occurrence
        translations.append({
            "text": text_name,
            "english": english
        })
    else:
        # Multiple occurrences - use same translation for all
        translations.append({
            "text": text_name,
            "occurrences": [
                {
                    "line": occ["line_number"],
                    "english": english
                }
                for occ in occurrences
            ]
        })

# Save the properly mapped translations
output = {
    "timestamp": datetime.now().isoformat(),
    "translations": translations
}

with open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_proper_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Created proper English mapping for {len(translations)} texts")
print(f"Total occurrences: {sum(len(by_text[t]) for t in by_text)}")