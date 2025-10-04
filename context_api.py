#!/usr/bin/env python3
"""
Local API server for getting extended context from texts database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database path
DB_PATH = '/Users/mariaiontseva/muktabodha_texts.db'

def get_extended_context(filename, search_term, line_number=None, context_lines=4):
    """
    Get extended context for a search term from the database
    Returns 4 lines before and 4 lines after the match
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # First try to find by filename in search_index table (which has content)
        cursor.execute("""
            SELECT content
            FROM search_index
            WHERE filename = ?
            LIMIT 1
        """, (filename,))

        result = cursor.fetchone()

        if not result:
            # Try to find the filename from texts table using display_name
            cursor.execute("""
                SELECT filename
                FROM texts
                WHERE display_name = ? OR display_name LIKE ?
                LIMIT 1
            """, (filename, f'%{filename}%'))

            filename_result = cursor.fetchone()

            if filename_result and filename_result[0]:
                # Now get the content from search_index using the filename
                cursor.execute("""
                    SELECT content
                    FROM search_index
                    WHERE filename = ?
                    LIMIT 1
                """, (filename_result[0],))
                result = cursor.fetchone()

        if result and result[0]:
            content = result[0]
            lines = content.split('\n')

            # Find the line containing the search term
            search_lower = search_term.lower()
            matches = []

            for i, line in enumerate(lines):
                if search_lower in line.lower():
                    # Get context: 4 lines before and 4 lines after
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)

                    context_text = []

                    # Add marker if we're not at the beginning
                    if start > 0:
                        context_text.append("... [previous lines omitted] ...\n")

                    # Add the lines with line numbers
                    for j in range(start, end):
                        line_text = lines[j].strip()
                        if line_text:  # Skip empty lines
                            if j == i:
                                # Highlight the matching line
                                context_text.append(f">>> [Line {j+1}] {line_text} <<<")
                            else:
                                context_text.append(f"[Line {j+1}] {line_text}")

                    # Add marker if we're not at the end
                    if end < len(lines):
                        context_text.append("\n... [following lines omitted] ...")

                    matches.append('\n'.join(context_text))

            if matches:
                # Return the first match or the one closest to the line number
                if line_number and line_number > 0:
                    # Find the match closest to the requested line number
                    for match in matches:
                        if f"[Line {line_number}]" in match:
                            return match
                return matches[0]

        conn.close()
        return None

    except Exception as e:
        print(f"Database error: {e}")
        return None

@app.route('/extended_context', methods=['POST'])
def extended_context():
    """API endpoint for getting extended context"""
    data = request.json

    filename = data.get('filename', '')
    display_name = data.get('display_name', '')
    search_term = data.get('search_term', '')
    line_number = data.get('line_number', None)
    context_lines = data.get('context_lines', 4)

    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    # Try with filename first, then display_name
    extended = None
    if filename:
        extended = get_extended_context(filename, search_term, line_number, context_lines)

    if not extended and display_name:
        extended = get_extended_context(display_name, search_term, line_number, context_lines)

    if extended:
        return jsonify({
            'extended_context': extended,
            'source': 'database',
            'context_lines': context_lines
        })
    else:
        return jsonify({
            'error': 'No context found',
            'filename': filename,
            'display_name': display_name
        }), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check if database exists and is accessible
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM texts")
            count = cursor.fetchone()[0]
            conn.close()

            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'texts_count': count
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Database not found'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print(f"Starting context API server...")
    print(f"Database: {DB_PATH}")

    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"WARNING: Database not found at {DB_PATH}")
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM texts")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"Database connected: {count} texts available")
        except Exception as e:
            print(f"Database error: {e}")

    print("Server running at http://localhost:5001")
    print("Endpoints:")
    print("  POST /extended_context - Get extended context for a search term")
    print("  GET /health - Check server status")

    app.run(port=5001, debug=True)