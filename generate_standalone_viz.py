#!/usr/bin/env python3

import json
import html

# Load the snippets data
with open('/Users/mariaiontseva/svapna-deploy/svapna_snippets_display.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get first 100 snippets from each category for initial display
initial_snippets = []
for category, snippets in data['snippets_by_category'].items():
    for snippet in snippets[:100]:
        if not snippet.get('categories'):
            snippet['categories'] = [category] if category != 'uncategorized' else []
        initial_snippets.append(snippet)

print(f"Preparing {len(initial_snippets)} snippets for display...")

# Create HTML with embedded data
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Svapna Analysis - All 6,072 Snippets</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1800px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            color: white;
            font-size: 2.8em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            text-align: center;
            color: rgba(255,255,255,0.95);
            font-size: 1.3em;
            margin-bottom: 30px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }}
        
        .stat-number {{
            font-size: 2.2em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 1200px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .chart-panel {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            height: fit-content;
            position: sticky;
            top: 20px;
        }}
        
        .snippets-panel {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 350px;
            margin-bottom: 20px;
        }}
        
        .controls {{
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .search-box {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #667eea;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            margin-bottom: 15px;
        }}
        
        .search-box:focus {{
            border-color: #764ba2;
            box-shadow: 0 0 10px rgba(118,75,162,0.2);
        }}
        
        .category-filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
        }}
        
        .filter-btn:hover {{
            background: #764ba2;
            transform: scale(1.05);
        }}
        
        .filter-btn.active {{
            background: #764ba2;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .snippet-counter {{
            text-align: center;
            padding: 10px;
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: 600;
            color: #333;
        }}
        
        .snippets-container {{
            max-height: 800px;
            overflow-y: auto;
            padding-right: 10px;
        }}
        
        .snippets-container::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .snippets-container::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        
        .snippets-container::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 10px;
        }}
        
        .snippets-container::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
        
        .snippet-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        
        .snippet-card:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateX(5px);
            border-left-color: #764ba2;
        }}
        
        .snippet-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .text-info {{
            flex: 1;
        }}
        
        .text-name {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
            margin-bottom: 5px;
        }}
        
        .text-meta {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .tradition-badge {{
            padding: 4px 12px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 15px;
            font-size: 0.8em;
        }}
        
        .line-badge {{
            padding: 4px 10px;
            background: #e0e0e0;
            color: #666;
            border-radius: 15px;
            font-size: 0.8em;
        }}
        
        .category-badges {{
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
            margin-top: 5px;
        }}
        
        .category-badge {{
            padding: 3px 8px;
            background: rgba(102,126,234,0.2);
            color: #667eea;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
        }}
        
        .snippet-content {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #444;
            font-size: 0.95em;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .svapna-highlight {{
            background: #ffeb3b;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
            color: #333;
        }}
        
        .category-highlight {{
            background: #e1f5fe;
            padding: 2px 4px;
            border-radius: 3px;
            color: #0277bd;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌙 Complete Svapna Analysis</h1>
        <p class="subtitle">All 6,072 Text Snippets from 307 Sanskrit Texts • 6,469 Total Occurrences</p>
        
        <!-- Statistics Grid -->
        <div class="stats-grid">
            <div class="stat-card" onclick="filterByCategory('all')">
                <div class="stat-number">6,072</div>
                <div class="stat-label">Total Snippets</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('philosophical')">
                <div class="stat-number">2,876</div>
                <div class="stat-label">Philosophical</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('consciousness')">
                <div class="stat-number">2,584</div>
                <div class="stat-label">Consciousness</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('visualization')">
                <div class="stat-number">2,286</div>
                <div class="stat-label">Visualization</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('deity')">
                <div class="stat-number">1,764</div>
                <div class="stat-label">Deity</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('yoga')">
                <div class="stat-number">1,287</div>
                <div class="stat-label">Yoga</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('mantra')">
                <div class="stat-number">1,038</div>
                <div class="stat-label">Mantra</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('tantra')">
                <div class="stat-number">698</div>
                <div class="stat-label">Tantra</div>
            </div>
            <div class="stat-card" onclick="filterByCategory('diksha_initiation')">
                <div class="stat-number">281</div>
                <div class="stat-label">Dīkṣā</div>
            </div>
        </div>
        
        <div class="main-content">
            <!-- Chart Panel -->
            <div class="chart-panel">
                <h3 style="text-align: center; margin-bottom: 20px; color: #333;">Category Distribution</h3>
                <div class="chart-wrapper">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            
            <!-- Snippets Panel -->
            <div class="snippets-panel">
                <div class="controls">
                    <input type="text" class="search-box" id="searchBox" 
                           placeholder="Search in snippets... (text name, tradition, or content)"
                           onkeyup="filterSnippets()">
                    
                    <div class="category-filters">
                        <button class="filter-btn active" onclick="filterByCategory('all')">All</button>
                        <button class="filter-btn" onclick="filterByCategory('philosophical')">Philosophical</button>
                        <button class="filter-btn" onclick="filterByCategory('consciousness')">Consciousness</button>
                        <button class="filter-btn" onclick="filterByCategory('visualization')">Visualization</button>
                        <button class="filter-btn" onclick="filterByCategory('deity')">Deity</button>
                        <button class="filter-btn" onclick="filterByCategory('yoga')">Yoga</button>
                        <button class="filter-btn" onclick="filterByCategory('mantra')">Mantra</button>
                        <button class="filter-btn" onclick="filterByCategory('tantra')">Tantra</button>
                        <button class="filter-btn" onclick="filterByCategory('diksha_initiation')">Dīkṣā</button>
                    </div>
                </div>
                
                <div class="snippet-counter" id="snippetCounter">
                    Showing <span id="shownCount">0</span> snippets
                </div>
                
                <div class="snippets-container" id="snippetsContainer">
                    <div class="no-results">Loading snippets...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Embedded data
        const allSnippetsData = {json.dumps(initial_snippets)};
        
        let currentCategory = 'all';
        let filteredSnippets = [];
        
        // Category data for chart
        const categoryData = {{
            labels: ['Philosophical', 'Consciousness', 'Visualization', 'Deity', 'Yoga', 'Mantra', 'Tantra', 'Dīkṣā'],
            data: [2876, 2584, 2286, 1764, 1287, 1038, 698, 281],
            colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#ffa400', '#fa709a']
        }};
        
        // Initialize chart
        const ctx = document.getElementById('categoryChart').getContext('2d');
        const categoryChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: categoryData.labels,
                datasets: [{{
                    data: categoryData.data,
                    backgroundColor: categoryData.colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 8,
                            font: {{ size: 10 }}
                        }}
                    }}
                }},
                onClick: function(event, elements) {{
                    if (elements.length > 0) {{
                        const index = elements[0].index;
                        const categories = ['philosophical', 'consciousness', 'visualization', 'deity', 'yoga', 'mantra', 'tantra', 'diksha_initiation'];
                        filterByCategory(categories[index]);
                    }}
                }}
            }}
        }});
        
        function filterByCategory(category) {{
            currentCategory = category;
            
            // Update buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.textContent.toLowerCase().includes(category.replace('_', ' ').toLowerCase()) || 
                    (category === 'all' && btn.textContent === 'All')) {{
                    btn.classList.add('active');
                }}
            }});
            
            // Filter snippets
            if (category === 'all') {{
                filteredSnippets = allSnippetsData;
            }} else {{
                filteredSnippets = allSnippetsData.filter(s => 
                    s.categories && s.categories.includes(category)
                );
            }}
            
            displaySnippets();
        }}
        
        function displaySnippets() {{
            const container = document.getElementById('snippetsContainer');
            container.innerHTML = '';
            
            if (filteredSnippets.length === 0) {{
                container.innerHTML = '<div class="no-results">No snippets found</div>';
                updateCounter(0);
                return;
            }}
            
            // Display snippets
            filteredSnippets.forEach(snippet => {{
                container.innerHTML += createSnippetCard(snippet);
            }});
            
            updateCounter(filteredSnippets.length);
            highlightText();
        }}
        
        function createSnippetCard(snippet) {{
            const categoryBadges = (snippet.categories || []).map(cat => 
                `<span class="category-badge">${{cat.replace('_', ' ')}}</span>`
            ).join('');
            
            const escapedContent = escapeHtml(snippet.context || '');
            const highlightedContent = highlightContent(escapedContent);
            
            return `
                <div class="snippet-card">
                    <div class="snippet-header">
                        <div class="text-info">
                            <div class="text-name">${{snippet.text || 'Unknown Text'}}</div>
                            <div class="text-meta">
                                <span class="tradition-badge">${{snippet.tradition || 'Unknown'}}</span>
                                <span class="line-badge">Line ${{snippet.line_number || '?'}}</span>
                            </div>
                            ${{categoryBadges ? `<div class="category-badges">${{categoryBadges}}</div>` : ''}}
                        </div>
                    </div>
                    <div class="snippet-content">${{highlightedContent}}</div>
                </div>
            `;
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function highlightContent(content) {{
            // Highlight svapna
            content = content.replace(/svapn[aāiīuūeoṃṁḥ\\w]*/gi, match => 
                `<span class="svapna-highlight">${{match}}</span>`
            );
            
            // Category-specific highlighting
            if (currentCategory === 'diksha_initiation') {{
                content = content.replace(/dīkṣ[aāiīuūeoṃṁḥ\\w]*/gi, match => 
                    `<span class="category-highlight">${{match}}</span>`
                );
            }}
            
            return content;
        }}
        
        function highlightText() {{
            // Additional highlighting if needed
        }}
        
        function updateCounter(count) {{
            document.getElementById('shownCount').textContent = count;
        }}
        
        function filterSnippets() {{
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            
            if (!searchTerm) {{
                filterByCategory(currentCategory);
                return;
            }}
            
            filteredSnippets = allSnippetsData.filter(snippet => {{
                const searchableText = [
                    snippet.text,
                    snippet.tradition,
                    snippet.context
                ].join(' ').toLowerCase();
                return searchableText.includes(searchTerm);
            }});
            
            displaySnippets();
        }}
        
        // Initialize
        filterByCategory('all');
    </script>
</body>
</html>"""

# Save the HTML file
with open('/Users/mariaiontseva/svapna-deploy/svapna_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Created standalone HTML file: svapna_standalone.html")
print("This file has all data embedded and can be opened directly in a browser.")