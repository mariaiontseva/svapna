#!/usr/bin/env python3
"""
Verify that every text from the source list is correctly attributed in the Śaiva taxonomy tree.
"""

import re
from bs4 import BeautifulSoup

# Source list of texts (from user's document)
SOURCE_TEXTS = [
    {
        "name": "Niśvāsatattvasaṃhitā",
        "period": "c. 450-550 CE",
        "category": "Śaiva",
        "expected_location": "Śaiva Siddhānta (dualist)"
    },
    {
        "name": "Brahmayāmala",
        "period": "c. 650-750 CE",
        "category": "Śākta",
        "expected_location": "Yāmala-tantras"
    },
    {
        "name": "Mālinīvijayottaratantra",
        "period": "7th-8th century",
        "category": "Śaiva/Trika",
        "expected_location": "Trika"
    },
    {
        "name": "Svacchandatantra",
        "period": "7th-10th century",
        "category": "Śaiva/Bhairava",
        "expected_location": "Mantrapīṭha (early Bhairava Tantras)"
    },
    {
        "name": "Netratantra",
        "period": "700-850 CE",
        "category": "Śaiva",
        "expected_location": "Mantrapīṭha (early Bhairava Tantras)"
    },
    {
        "name": "Tantrasadbhāvatantra",
        "period": "8th-9th century",
        "category": "Śaiva",
        "expected_location": "Trika"
    },
    {
        "name": "Śivasūtra",
        "period": "c. 800-850 CE",
        "category": "Śaiva/Kashmir Śaivism",
        "expected_location": "KASHMIR ŚAIVISM (Post-scriptural)"
    },
    {
        "name": "Vijñānabhairavatantra",
        "period": "c. 850 CE",
        "category": "Śaiva/Kashmir Śaivism",
        "expected_location": "Trika"
    },
    {
        "name": "Spandakārikā",
        "period": "c. 850-900 CE",
        "category": "Śaiva/Kashmir Śaivism",
        "expected_location": "KASHMIR ŚAIVISM (Post-scriptural)"
    },
    {
        "name": "Manthānabhairavatantra",
        "period": "10th-12th century",
        "category": "Śākta/Kubjikā",
        "expected_location": "Paścimāmnāya (Western Transmission)"
    },
    {
        "name": "Kubjikāmatatantra",
        "period": "10th-11th century",
        "category": "Śākta/Kubjikā",
        "expected_location": "Paścimāmnāya (Western Transmission)"
    },
    {
        "name": "Tantrāloka",
        "period": "c. 1000-1020 CE",
        "category": "Śaiva/Kashmir Śaivism",
        "expected_location": "Pūrvāmnāya (Eastern Transmission)"
    },
    {
        "name": "Kulārṇavatantra",
        "period": "11th-14th century",
        "category": "Śākta/Kaula",
        "expected_location": "Pūrvāmnāya (Eastern Transmission)"
    },
    {
        "name": "Svapnacintāmaṇi",
        "period": "c. 1175 CE",
        "category": "Dream Manual",
        "expected_location": "DREAM MANUALS"
    },
    {
        "name": "Śiva Saṃhitā",
        "period": "14th-15th century",
        "category": "Yoga/Haṭha",
        "expected_location": "YOGA & HAṬHA TEXTS"
    },
    {
        "name": "Yoginī Tantra",
        "period": "16th-17th century",
        "category": "Śākta/Assamese",
        "expected_location": "ASSAMESE ŚĀKTA TRADITIONS"
    },
    {
        "name": "Bṛhaantrasāra",
        "period": "18th century",
        "category": "Śākta/Bengal",
        "expected_location": "BENGAL ŚĀKTA TRADITIONS"
    },
    {
        "name": "Mahānirvāṇatantra",
        "period": "18th-19th century",
        "category": "Śākta/Bengal",
        "expected_location": "BENGAL ŚĀKTA TRADITIONS"
    }
]


def normalize_text(text):
    """Normalize text for comparison (remove diacritics variations, spaces, etc.)"""
    # Simple normalization - can be expanded
    text = text.lower()
    text = re.sub(r'\s+', '', text)
    # Remove common variations
    text = text.replace('ś', 's').replace('ṣ', 's').replace('ṛ', 'r')
    text = text.replace('ṃ', 'm').replace('ṅ', 'n').replace('ñ', 'n')
    text = text.replace('ā', 'a').replace('ī', 'i').replace('ū', 'u')
    text = text.replace('ḍ', 'd').replace('ṭ', 't').replace('ḥ', 'h')
    return text


def extract_tree_structure(html_content):
    """Extract the tree structure from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')

    tree_structure = {}

    # Find all text nodes (those with •)
    text_nodes = soup.find_all('div', class_='node-title', string=re.compile(r'•'))

    for node in text_nodes:
        text_title = node.get_text(strip=True).replace('•', '').strip()

        # Find the parent branch by traversing up
        parent_titles = []
        current = node.parent
        while current:
            if 'tree-node' in current.get('class', []):
                title_div = current.find('div', class_='node-title', recursive=False)
                if title_div:
                    title_text = title_div.get_text(strip=True)
                    # Remove toggle icons and badges
                    title_text = re.sub(r'►|✓|✗', '', title_text).strip()
                    if title_text and '•' not in title_text:
                        parent_titles.insert(0, title_text)
            current = current.parent
            if current and 'root' in current.get('class', []):
                break

        # Store location
        location_path = " → ".join(parent_titles) if parent_titles else "ROOT"
        tree_structure[text_title] = location_path

    return tree_structure


def find_text_in_tree(text_name, tree_structure):
    """Find a text in the tree structure"""
    normalized_search = normalize_text(text_name)

    for tree_text, location in tree_structure.items():
        if normalized_search in normalize_text(tree_text):
            return location

    return None


def verify_attribution():
    """Main verification function"""
    print("=" * 80)
    print("ŚAIVA TAXONOMY TEXT ATTRIBUTION VERIFICATION")
    print("=" * 80)
    print()

    # Read HTML file
    with open('/Users/mariaiontseva/svapna/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract tree structure
    tree_structure = extract_tree_structure(html_content)

    # Verify each text
    correctly_placed = []
    misplaced = []
    missing = []

    for text in SOURCE_TEXTS:
        location = find_text_in_tree(text['name'], tree_structure)

        if location:
            # Check if it's in the expected location
            if text['expected_location'] in location:
                correctly_placed.append({
                    'text': text,
                    'location': location,
                    'status': '✓ CORRECT'
                })
            else:
                misplaced.append({
                    'text': text,
                    'found_location': location,
                    'expected_location': text['expected_location'],
                    'status': '⚠ MISPLACED'
                })
        else:
            missing.append({
                'text': text,
                'status': '✗ MISSING'
            })

    # Print results
    print(f"\n📊 SUMMARY: {len(SOURCE_TEXTS)} total texts\n")
    print(f"  ✓ Correctly placed: {len(correctly_placed)}")
    print(f"  ⚠ Misplaced: {len(misplaced)}")
    print(f"  ✗ Missing: {len(missing)}")
    print()

    # Print correctly placed
    if correctly_placed:
        print("\n" + "=" * 80)
        print("✓ CORRECTLY ATTRIBUTED TEXTS")
        print("=" * 80)
        for item in correctly_placed:
            text = item['text']
            print(f"\n{text['name']} ({text['period']})")
            print(f"  Category: {text['category']}")
            print(f"  Location: {item['location']}")

    # Print misplaced
    if misplaced:
        print("\n" + "=" * 80)
        print("⚠ MISPLACED TEXTS (need review)")
        print("=" * 80)
        for item in misplaced:
            text = item['text']
            print(f"\n{text['name']} ({text['period']})")
            print(f"  Category: {text['category']}")
            print(f"  Expected: {item['expected_location']}")
            print(f"  Found at: {item['found_location']}")
            print(f"  ⚠ ACTION NEEDED: Move or verify placement")

    # Print missing
    if missing:
        print("\n" + "=" * 80)
        print("✗ MISSING TEXTS (not found in tree)")
        print("=" * 80)
        for item in missing:
            text = item['text']
            print(f"\n{text['name']} ({text['period']})")
            print(f"  Category: {text['category']}")
            print(f"  Expected: {text['expected_location']}")
            print(f"  ✗ ACTION NEEDED: Add to tree")

    # Print tree structure for reference
    print("\n" + "=" * 80)
    print("COMPLETE TREE STRUCTURE (for reference)")
    print("=" * 80)
    for text, location in sorted(tree_structure.items()):
        print(f"{text}")
        print(f"  → {location}")

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

    return {
        'correctly_placed': correctly_placed,
        'misplaced': misplaced,
        'missing': missing,
        'total': len(SOURCE_TEXTS)
    }


if __name__ == "__main__":
    verify_attribution()
