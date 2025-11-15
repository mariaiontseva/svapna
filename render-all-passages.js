// Render All Śaiva Passages - Automatic Integration
// This script reads from all-saiva-passages-data.js and renders passage displays

document.addEventListener('DOMContentLoaded', function() {
    // Map of text IDs to their HTML identifiers
    const textMapping = {
        'brahmayamala': 'Brahmayāmala',
        'malinivijayottaratantra': 'Mālinīvijayottaratantra',
        'svacchandatantra': 'Svacchandatantra',
        'netratantra': 'Netratantra',
        'tantrasadbhavatantra': 'Tantrasadbhāvatantra',
        'shivasutra': 'Śivasūtra',
        'vijnanabhairavatantra': 'Vijñānabhairavatantra',
        'spandakarika': 'Spandakārikā',
        'manthanabhairavatantra': 'Manthānabhairavatantra',
        'kubjikamatatantra': 'Kubjikāmatatantra',
        'kularnavatantra': 'Kulārṇavatantra',
        'tantraloka': 'Tantrāloka',
        'yoginitantra': 'Yoginī Tantra',
        'brhattantrasara': 'Bṛhattantrasāra',
        'saktisamgama': 'Śaktisamgama Sundarīkhaṇḍa'
    };

    // Function to count total passages for a text
    function countPassages(textData) {
        return Object.keys(textData.passages).length;
    }

    // Function to determine translator status
    function getTranslatorTags(textData) {
        const passages = Object.values(textData.passages);
        const translatedCount = passages.filter(p => p.translated).length;
        const totalCount = passages.length;

        if (translatedCount === 0) {
            return '<span class="tag untranslated">Untranslated</span>';
        } else if (translatedCount === totalCount) {
            // Get unique translators
            const translators = [...new Set(passages
                .filter(p => p.translator)
                .map(p => p.translator))];

            if (translators.length === 1) {
                return `<span class="tag translator">Tr. by: ${translators[0]}</span>`;
            } else if (translators.length > 1) {
                return '<span class="tag translator">Tr. by: Multiple</span>';
            }
            return '<span class="tag translator">Translated</span>';
        } else {
            return '<span class="tag translator">Partially translated</span>';
        }
    }

    // Function to get unique taxonomy tags across all passages
    function getTaxonomyTags(textData) {
        const passages = Object.values(textData.passages);
        const allCategories = new Set();

        passages.forEach(passage => {
            if (passage.categories && Array.isArray(passage.categories)) {
                passage.categories.forEach(cat => {
                    if (cat) allCategories.add(cat);
                });
            }
        });

        const categories = [...allCategories];

        if (categories.length === 0) {
            return '';
        } else if (categories.length === 1) {
            return `<span class="tag ${categories[0]}">${categories[0]}</span>`;
        } else {
            // Show first category + "+N" indicator
            const first = categories[0];
            const remaining = categories.length - 1;
            return `<span class="tag ${first}">${first}</span><span class="tag" style="background: var(--bg-tertiary); color: var(--text-muted); border-color: var(--border);">+${remaining}</span>`;
        }
    }

    // Function to create passage HTML
    function createPassageHTML(passageId, passageData) {
        const categoryTags = passageData.categories
            .map(cat => `<span class="tag ${cat}">${cat}</span>`)
            .join('');

        const versesHTML = passageData.verses.map(verse => `
            <div class="verse">
                <span class="verse-number">${verse.number}</span>
                <span class="verse-text">${verse.sanskrit}</span>
            </div>
        `).join('');

        const translationsHTML = passageData.verses.map(verse => `
            <div class="verse">
                <span class="verse-number">${verse.number}</span>
                <span class="verse-text">${verse.translation}</span>
            </div>
        `).join('');

        return `
            <div class="passage-card">
                <div class="passage-header">
                    <div class="passage-reference">${passageData.reference}</div>
                    <div class="tags">${categoryTags}</div>
                </div>
                <div class="passage-content">
                    <div class="sanskrit-column">
                        <div class="column-header">Sanskrit (IAST)</div>
                        ${versesHTML}
                    </div>
                    <div class="translation-column">
                        <div class="column-header">Translation</div>
                        ${translationsHTML}
                    </div>
                </div>
                ${passageData.context ? `
                    <div class="passage-summary">
                        <strong>Context:</strong> ${passageData.context}
                    </div>
                ` : ''}
            </div>
        `;
    }

    // Function to replace text node with clickable passage display
    function replaceWithPassageDisplay(textId, textData) {
        const searchName = textMapping[textId];
        if (!searchName) return;

        // Find all nodes containing this text name
        const allNodes = document.querySelectorAll('.node-title');
        let targetNode = null;

        for (const node of allNodes) {
            if (node.textContent.includes(searchName)) {
                targetNode = node;
                break;
            }
        }

        if (!targetNode) {
            console.log(`Could not find node for ${searchName}`);
            return;
        }

        const passageCount = countPassages(textData);
        const translatorTags = getTranslatorTags(textData);
        const taxonomyTags = getTaxonomyTags(textData);

        // Extract original text details (name and period)
        const originalText = targetNode.textContent;

        // Create passages HTML
        const passagesHTML = Object.entries(textData.passages)
            .map(([id, data]) => createPassageHTML(id, data))
            .join('');

        // Create the full clickable structure
        const clickableHTML = `
            <div class="text-node-with-passages">
                <div class="text-header" onclick="togglePassages(this)">
                    <div class="text-header-left">
                        <div class="text-title-main">${originalText}</div>
                        <div class="text-translator-tags">
                            ${translatorTags}
                        </div>
                    </div>
                    <div class="text-meta-info">
                        ${taxonomyTags}
                        <span class="passage-count">${passageCount} passage${passageCount !== 1 ? 's' : ''}</span>
                        <span class="toggle-passages"></span>
                    </div>
                </div>
                <div class="passages-container">
                    ${passagesHTML}
                </div>
            </div>
        `;

        // Replace the simple node with clickable structure
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = clickableHTML;
        targetNode.replaceWith(tempDiv.firstElementChild);

        console.log(`✓ Rendered ${passageCount} passages for ${searchName}`);
    }

    // Render all texts
    console.log('Starting to render all Śaiva passages...');

    if (typeof all_saiva_passages === 'undefined') {
        console.error('all_saiva_passages data not found!');
        return;
    }

    Object.entries(all_saiva_passages).forEach(([textId, textData]) => {
        replaceWithPassageDisplay(textId, textData);
    });

    console.log('Finished rendering all passages');
});
