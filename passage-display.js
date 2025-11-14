// Passage Display JavaScript
// Handles expansion/collapse of text nodes with passages

/**
 * Toggle passages visibility for a text node
 * @param {HTMLElement} headerElement - The header element that was clicked
 */
function togglePassages(headerElement) {
    // Prevent event propagation to parent tree nodes
    event.stopPropagation();

    // Find the passages container
    const textNode = headerElement.closest('.text-node-with-passages');
    const passagesContainer = textNode.querySelector('.passages-container');
    const toggleIcon = headerElement.querySelector('.toggle-passages');

    // Toggle expansion
    if (passagesContainer.classList.contains('expanded')) {
        passagesContainer.classList.remove('expanded');
        toggleIcon.classList.remove('rotated');
    } else {
        passagesContainer.classList.add('expanded');
        toggleIcon.classList.add('rotated');
    }
}

/**
 * Render a text node with passages
 * @param {Object} textData - Data object containing text information
 * @returns {string} HTML string for the text node
 */
function renderTextWithPassages(textData) {
    const { name, period, passages } = textData;
    const passageCount = Object.keys(passages).length;

    let passagesHTML = '';

    // Generate HTML for each passage
    for (const [key, passage] of Object.entries(passages)) {
        passagesHTML += renderPassageCard(passage);
    }

    return `
        <div class="text-node-with-passages">
            <div class="text-header" onclick="togglePassages(this)">
                <div class="text-header-left">
                    <div class="text-title-main">• ${name} (${period})</div>
                </div>
                <div class="text-meta-info">
                    <span class="passage-count">${passageCount} passage${passageCount > 1 ? 's' : ''}</span>
                    <span class="toggle-passages">▼</span>
                </div>
            </div>
            <div class="passages-container">
                ${passagesHTML}
            </div>
        </div>
    `;
}

/**
 * Render a single passage card
 * @param {Object} passage - Passage data object
 * @returns {string} HTML string for the passage card
 */
function renderPassageCard(passage) {
    const { reference, categories, translator, translated, verses, context } = passage;

    // Generate category tags
    const categoryTags = categories.map(cat => {
        const tagClass = cat.replace('&', '').toLowerCase();
        return `<span class="tag ${tagClass}">${cat}</span>`;
    }).join('');

    // Generate translator/untranslated tag
    const translatorTag = translated
        ? `<span class="tag translator">${translator}</span>`
        : `<span class="tag untranslated">Untranslated (AI)</span>`;

    // Generate verses HTML for Sanskrit column
    const sanskritVersesHTML = verses.map(verse => `
        <div class="verse">
            <span class="verse-number">${verse.number}</span>
            <span class="verse-text">${verse.sanskrit}</span>
        </div>
    `).join('');

    // Generate verses HTML for Translation column
    const translationVersesHTML = verses.map(verse => `
        <div class="verse">
            <span class="verse-number">${verse.number}</span>
            <span class="verse-text">${verse.translation}</span>
        </div>
    `).join('');

    return `
        <div class="passage-card">
            <div class="passage-header">
                <div class="passage-reference">${reference}</div>
                <div class="tags">
                    ${categoryTags}
                    ${translatorTag}
                </div>
            </div>
            <div class="passage-content">
                <div class="sanskrit-column">
                    <div class="column-header">Sanskrit (Transliterated)</div>
                    ${sanskritVersesHTML}
                </div>
                <div class="translation-column">
                    <div class="column-header">${translated ? 'Translation' : 'Translation (AI Generated)'}</div>
                    ${translationVersesHTML}
                </div>
            </div>
            <div class="passage-summary">
                <strong>Context:</strong> ${context}
            </div>
        </div>
    `;
}

/**
 * Initialize passage displays on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Passage display system initialized');

    // Optional: Auto-expand first text with passages for demo
    const firstTextNode = document.querySelector('.text-node-with-passages');
    if (firstTextNode) {
        const passagesContainer = firstTextNode.querySelector('.passages-container');
        const toggleIcon = firstTextNode.querySelector('.toggle-passages');
        if (passagesContainer) {
            // Uncomment to auto-expand on load:
            // passagesContainer.classList.add('expanded');
            // toggleIcon.classList.add('rotated');
        }
    }
});
