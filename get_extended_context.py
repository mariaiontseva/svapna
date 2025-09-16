#!/usr/bin/env python3

import json
import sqlite3
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_extended_context(filename, search_term, line_number=None, context_lines=10, display_name=None):
    """Get extended context from the database"""
    try:
        # Connect to database
        conn = sqlite3.connect('/Users/mariaiontseva/muktabodha_texts.db')
        cursor = conn.cursor()
        
        # If display_name is provided, get the filename
        if display_name and not filename:
            cursor.execute("""
                SELECT si.filename 
                FROM search_index si 
                JOIN texts t ON si.filename = t.filename
                WHERE t.display_name = ?
                LIMIT 1
            """, (display_name,))
            filename_result = cursor.fetchone()
            if filename_result:
                filename = filename_result[0]
        
        # Get the full text
        cursor.execute("""
            SELECT content 
            FROM search_index 
            WHERE filename = ?
        """, (filename,))
        
        result = cursor.fetchone()
        if not result:
            return None
            
        full_text = result[0]
        lines = full_text.split('\n')
        
        # Find the line with search term near the given line number
        if line_number:
            # Search around the given line number
            search_start = max(0, line_number - 20)
            search_end = min(len(lines), line_number + 20)
        else:
            search_start = 0
            search_end = len(lines)
        
        # Find the line containing the search term
        target_line = -1
        for i in range(search_start, search_end):
            if search_term.lower() in lines[i].lower():
                target_line = i
                break
        
        if target_line == -1:
            # Search entire text if not found near line number
            for i, line in enumerate(lines):
                if search_term.lower() in line.lower():
                    target_line = i
                    break
        
        if target_line == -1:
            return None
        
        # Extract context lines
        start = max(0, target_line - (context_lines // 2))
        end = min(len(lines), target_line + (context_lines // 2) + 1)
        
        context_lines_text = lines[start:end]
        
        # Add line numbers
        result_lines = []
        for i, line in enumerate(context_lines_text, start=start+1):
            result_lines.append(f"[{i}] {line}")
        
        conn.close()
        return '\n'.join(result_lines)
        
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/extended_context', methods=['POST', 'OPTIONS'])
def extended_context_api():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json
    filename = data.get('filename')
    display_name = data.get('display_name')
    search_term = data.get('search_term')
    line_number = data.get('line_number')
    context_lines = data.get('context_lines', 10)
    
    context = get_extended_context(filename, search_term, line_number, context_lines, display_name)
    
    if context:
        return jsonify({'extended_context': context})
    else:
        return jsonify({'error': 'Context not found'}), 404

if __name__ == '__main__':
    # Test mode
    if len(sys.argv) > 1:
        if sys.argv[1] == 'serve':
            print("Starting Extended Context API on port 5001...")
            app.run(port=5001, debug=True)
        else:
            # Test with command line args
            filename = sys.argv[1] if len(sys.argv) > 1 else 'Agnipuranam.xml'
            search_term = sys.argv[2] if len(sys.argv) > 2 else 'svapna'
            
            context = get_extended_context(filename, search_term)
            if context:
                print(context)
            else:
                print("No context found")
    else:
        print("Starting Extended Context API on port 5001...")
        app.run(port=5001, debug=True)