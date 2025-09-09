#!/usr/bin/env python3

import json
from datetime import datetime

# Complete English translations for all svapnalabdha occurrences
translations = [
    {
        "text": "AcaraBhedaTantra",
        "english": "In the Vaishampayana collection addressed to Shaunaka, in the words of Vyasa, verse 72: In the Yogini Tantra it states - powerless is the mantra from one's father, likewise from the maternal grandfather. That which is obtained in a dream or given by a woman becomes pure only through proper consecration, verse 73. But that woman who is virtuous and of good conduct, devoted to the guru, with controlled senses, knowledgeable in all mantra meanings and principles, of good character, engaged in worship - she should be considered worthy as a guru."
    },
    {
        "text": "Agnipuranam", 
        "occurrences": [
            {
                "line": 3602,
                "english": "Seeing a blazing fire, worshipping Shiva, or Vishnu - one who obtains a mantra in a dream sees the accomplishment of that mantra."
            },
            {
                "line": 7773,
                "english": "One who sees or obtains a mantra in a dream while sleeping, that mantra quickly bears fruit for them."
            }
        ]
    },
    {
        "text": "Anandbhairav Kalpa",
        "occurrences": [
            {
                "line": 813,
                "english": "Through the mouth of the guru I obtained the knowledge called dream-obtained. He who seeks accomplishment in illusion magic without mantra and meditation - the sages say he is confused by delusion, fallen from the authority of scriptures."
            },
            {
                "line": 2165,
                "english": "Dream-obtained means gained through a dream - that knowledge which he obtained. The fool who seeks accomplishment in the supreme tantra filled with meditation on Brahman without mantra and meditation is confused by delusion. Fallen from scriptural authority means one who lacks the eligibility described in scripture. Accomplishment in illusion magic can also be accomplished through this dream-obtained supreme knowledge alone."
            }
        ]
    },
    {
        "text": "Bhutadamaratantra", 
        "english": "One should offer meat, liquor and other substances to one's mantra. That which is obtained in a dream, heard, or seen - all that should be concealed."
    },
    {
        "text": "Brahmayamalam",
        "occurrences": [
            {
                "line": 8975,
                "english": "Even thousands and millions of mantras obtained in dreams do not succeed. Because I have compassion for you, I speak what brings welfare to all people."
            },
            {
                "line": 21562,
                "english": "In sleep, what is obtained in a dream from the guru's mouth becomes fruitful. And that mantra given by a woman is successful, so say the best of the twice-born. I speak of the mantra that bestows all accomplishments, there is no doubt in this."
            }
        ]
    },
    {
        "text": "Durgarcanasrti",
        "english": "That mantra obtained in a dream or given by a woman becomes accomplished through consecration alone. After knowing one's own mantra, one should perform consecration and purification."
    },
    {
        "text": "Gautama Tantram",
        "english": "A valiant hero free from sorrow, with five faces. That which is dream-obtained or woman-given becomes pure through consecration alone."
    },
    {
        "text": "JayaSamhita",
        "english": "That which is obtained in a dream is purified through consecration alone. And that given by a woman also becomes pure through consecration."
    },
    {
        "text": "Kaksaputtantra",
        "english": "That which is obtained in a dream or given by a woman is purified through consecration alone. But a woman who is virtuous, of good conduct, devoted to the guru, with controlled senses, knowing all mantra meanings and principles, of good character, engaged in worship - she should be worthy as a guru."
    },
    {
        "text": "Kalivilasatantra",
        "english": "What is obtained in a dream or given by a woman is accomplished through proper ritual consecration. But that woman should be initiated, a great practitioner, intent on repeating her received mantra, of good qualities, knowing the meaning of mantras, devoted to the guru, and with conquered senses."
    },
    {
        "text": "Kamadhenutantra",
        "english": "That given by a woman or obtained in a dream - the practitioner accomplishes it quickly through consecration alone."
    },
    {
        "text": "Kaulajnananirnaya",
        "english": "The highest secret mantra, whether obtained in a dream or given by a woman, for one who desires accomplishment - that certainly becomes fruitful through consecration. I have obtained the vidya mantra in a dream, received from the guru's lotus mouth."
    },
    {
        "text": "Kularatnoddyota",
        "english": "What is obtained in a dream or given by a woman - that great mantra is accomplished through consecration alone."
    },
    {
        "text": "Mahakalasamhita Guhyakalikhanda",
        "english": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    {
        "text": "Mahakalasaṃhita Kamakalakhanda",
        "english": "What is obtained in a dream or given by a woman should be consecrated by the practitioner."
    },
    {
        "text": "MahanirvaNatantram",
        "english": "What is obtained in a dream or given by a woman - that mantra becomes fruitful through consecration."
    },
    {
        "text": "Matasara",
        "english": "Through these five consecrations, what is obtained in a dream and what is woman-given becomes pure - thus it is remembered in the tradition."
    },
    {
        "text": "Merutantram",
        "english": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    {
        "text": "Niruttaratantram",
        "english": "What is obtained in a dream or given by a woman is purified through consecration alone."
    },
    {
        "text": "Prapancasaratantram",
        "english": "Through effort alone, Parvati, the mantras that are self-arisen, obtained in dreams, or given by women become accomplished."
    },
    {
        "text": "Rudrayamalam",
        "occurrences": [
            {
                "line": 17839,
                "english": "What is obtained in a dream or given by a woman is purified through consecration alone."
            },
            {
                "line": 25309,
                "english": "What is obtained in a dream or given by a woman becomes fruitful through consecration. What is self-arisen also becomes accomplished through consecration."
            }
        ]
    },
    {
        "text": "Samvarodayatantram",
        "english": "By the accomplished yogini, a garland equal to pearls was made. Having purified the supreme essence through various tantras and obtained in a dream from the lineage - thus having been accomplished, this is now being composed by me."
    },
    {
        "text": "Saradatilaka",
        "english": "Even the supreme mantra, when obtained in a dream or given by a woman, if one desiring accomplishment performs consecration with devotion - it will certainly bear fruit."
    },
    {
        "text": "Siddhikaumaritantram",
        "english": "What is obtained in a dream or given by a woman - that is accomplished through consecration alone."
    },
    {
        "text": "Tripurasarasamuccaya",
        "english": "That mantra obtained in a dream becomes fruitful through consecration and through the grace received from devotion to the guru."
    },
    {
        "text": "Vamajalatantram",
        "english": "The text has reached me through the lineage in three streams. Now by that very stream, obtained in a dream through the lineage. This collected essence extracted from a hundred million tantras - this Bhairava Sarvabhauma tantra is being remembered."
    },
    {
        "text": "Visnuyamalam",
        "english": "What is obtained in a dream or given by a woman is accomplished through consecration alone."
    },
    {
        "text": "Yoginitantram",
        "english": "Powerless is the father's mantra, likewise the maternal grandfather's. What is obtained in a dream or given by a woman is purified through consecration alone."
    }
]

def create_final_json():
    """Create the final JSON with proper English translations"""
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "translations": translations
    }
    
    with open('/Users/mariaiontseva/svapna-deploy/svapnalabdha_english_only.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Created svapnalabdha_english_only.json with complete English translations")

if __name__ == "__main__":
    create_final_json()