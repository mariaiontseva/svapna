#!/usr/bin/env python3

import json
from datetime import datetime

# Load existing translations
existing = json.load(open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_accurate_translations.json'))

# New accurate translations for occurrences 6-10
new_translations = {
    "Diiksaaprakaasa_137": """According to the Yogini Tantra:
For the dream-obtained (mantra), one should establish the guru's life-force in a vessel.
Writing with saffron on a fig leaf, the receiving becomes auspicious.
Then one attains accomplishment, otherwise it would be fruitless.""",
    
    "Diiksaaprakaasa_193": """Tara is Om. The palace is Hom. The compressed syllable is the root mantra.
Dream-obtained, woman-given, in garland mantras and three-syllabled ones,
Among all Vedic ones, one need not purify from the accomplished ones and others.""",
    
    "Durgarcanasrti_3179": """For worshippers of Shiva's lotus feet, both enjoyment and liberation are in hand.
One who desires enjoyment and liberation from other doctrines -
If through dream-obtained wealth one becomes wealthy, like the illusion of silver in mother-of-pearl,
O Parvati! Similarly from other doctrines one desires enjoyment and liberation.""",
    
    "Jnanarnavatantra_2155": """Obtained through the great mantra of the noble lord, it is well established (verse 16-126).
This has been said, O Great Goddess, having abandoned other excellent doctrines:
Dream-obtained, woman-given, in garland mantras with three seeds (verse 16-127).
O Goddess, purification from the accomplished ones does not exist for them.
In the place of Sri Vidya worship, in the king of chakras, O Great Goddess (verse 16-128).""",
    
    "Kriyasara_49": """For the greater pleasure, I, for the good-minded ones of the world, this essence of good practices,
I make, Nilakantha (Blue-throated Shiva), a collection of all the scriptures, the words of Supreme Shiva.
Remember again and again, contemplate repeatedly the mind's teaching obtained in dreams (verse 7).
If a person becomes endowed with the linga and limbs, then indeed when possessed of limbs..."""
}

# Update the translations structure
for item in existing['translations']:
    if item['text'] == 'Diiksaaprakaasa':
        # Update Diiksaaprakaasa occurrences
        for occ in item['occurrences']:
            if occ['line'] == 137:
                occ['english'] = new_translations["Diiksaaprakaasa_137"]
            elif occ['line'] == 193:
                occ['english'] = new_translations["Diiksaaprakaasa_193"]
    
    elif item['text'] == 'Durgarcanasrti':
        # This text has single occurrence, update it
        item['english'] = new_translations["Durgarcanasrti_3179"]
    
    elif item['text'] == 'Jnanarnavatantra':
        # This text has single occurrence, update it
        item['english'] = new_translations["Jnanarnavatantra_2155"]
    
    elif item['text'] == 'Kriyasara':
        # This text has single occurrence, update it
        item['english'] = new_translations["Kriyasara_49"]

# Update timestamp and note
existing['timestamp'] = datetime.now().isoformat()
existing['note'] = "First 10 occurrences have accurate translations, remaining are placeholders"

# Save the updated translations
with open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_accurate_translations.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print("Updated translations for occurrences 6-10")
print("Total texts with accurate translations: 10")