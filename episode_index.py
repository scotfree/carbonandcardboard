#!/usr/bin/env python3
"""
Episode Index Generator

This script reads transcript HTML files from the episodes directory and generates
an index.html file with links to all episodes.

Usage:
    python episode_index.py

The script will:
1. Scan the 'episodes' directory for transcript_ep*.html files
2. Extract episode information from each file
3. Generate an index.html with a table of all episodes
"""

import os
import re
from pathlib import Path


def find_transcript_files(episodes_dir):
    """
    Find all transcript HTML files in the episodes directory.
    
    Returns:
        list: Sorted list of transcript file paths
    """
    transcript_files = []
    pattern = re.compile(r'^transcript_ep(\d+)\.html$')
    
    for filename in os.listdir(episodes_dir):
        match = pattern.match(filename)
        if match:
            episode_num = int(match.group(1))
            transcript_files.append({
                'filename': filename,
                'episode_num': episode_num,
                'path': os.path.join(episodes_dir, filename)
            })
    
    # Sort by episode number
    transcript_files.sort(key=lambda x: x['episode_num'])
    return transcript_files


def extract_episode_title(file_path):
    """
    Extract the episode title from a transcript HTML file.
    
    Returns:
        str: The episode title (e.g., "Episode 1 Transcript")
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract from the <h1> tag
    h1_match = re.search(r'<h1>(.+?)</h1>', content, re.IGNORECASE)
    if h1_match:
        title = h1_match.group(1)
        # Remove "Carbon and Cardboard - " prefix if present
        title = re.sub(r'^Carbon and Cardboard\s*-\s*', '', title, flags=re.IGNORECASE)
        return title
    
    # Fallback: try to extract from <title> tag
    title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        title = re.sub(r'^Carbon and Cardboard\s*-\s*', '', title, flags=re.IGNORECASE)
        return title
    
    return "Unknown Episode"


def generate_index_html(episodes, output_path, css_file='transcript_styles.css'):
    """
    Generate the index.html file with episode listing.
    """
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Carbon and Cardboard - Episode List</title>',
        f'    <link rel="stylesheet" href="{css_file}">',
        '    <style>',
        '        .episode-table {',
        '            width: 100%;',
        '            border-collapse: collapse;',
        '            margin-top: 20px;',
        '        }',
        '        .episode-table th,',
        '        .episode-table td {',
        '            padding: 15px;',
        '            text-align: left;',
        '            border-bottom: 1px solid rgba(100, 255, 218, 0.2);',
        '        }',
        '        .episode-table th {',
        '            color: #64ffda;',
        '            font-size: 1.1em;',
        '            border-bottom: 2px solid rgba(100, 255, 218, 0.4);',
        '        }',
        '        .episode-table tr:hover {',
        '            background-color: rgba(100, 255, 218, 0.05);',
        '        }',
        '        .episode-name {',
        '            color: #e0e0e0;',
        '            font-weight: 500;',
        '        }',
        '        .link-btn {',
        '            display: inline-block;',
        '            padding: 8px 16px;',
        '            margin: 2px 4px;',
        '            border-radius: 4px;',
        '            text-decoration: none;',
        '            font-size: 0.9em;',
        '            transition: all 0.2s ease;',
        '        }',
        '        .link-transcript {',
        '            background-color: rgba(100, 255, 218, 0.15);',
        '            color: #64ffda;',
        '        }',
        '        .link-transcript:hover {',
        '            background-color: rgba(100, 255, 218, 0.3);',
        '            text-decoration: none;',
        '        }',
        '        .link-spotify {',
        '            background-color: rgba(30, 215, 96, 0.15);',
        '            color: #1ed760;',
        '        }',
        '        .link-spotify:hover {',
        '            background-color: rgba(30, 215, 96, 0.3);',
        '            text-decoration: none;',
        '        }',
        '        .link-youtube {',
        '            background-color: rgba(255, 0, 0, 0.15);',
        '            color: #ff4444;',
        '        }',
        '        .link-youtube:hover {',
        '            background-color: rgba(255, 0, 0, 0.3);',
        '            text-decoration: none;',
        '        }',
        '    </style>',
        '</head>',
        '<body>',
        '    <div class="transcript-container">',
        '        <h1>Carbon and Cardboard - Episode List</h1>',
        '        <table class="episode-table">',
        '            <thead>',
        '                <tr>',
        '                    <th>Episode</th>',
        '                    <th>Links</th>',
        '                </tr>',
        '            </thead>',
        '            <tbody>',
    ]
    
    for episode in episodes:
        episode_num = episode['episode_num']
        title = episode['title']
        transcript_file = episode['filename']
        
        # Placeholder URLs - can be updated later
        spotify_url = f"https://open.spotify.com/show/placeholder-episode-{episode_num}"
        youtube_url = f"https://youtube.com/watch?v=placeholder-episode-{episode_num}"
        
        html_parts.extend([
            '                <tr>',
            f'                    <td class="episode-name">{title}</td>',
            '                    <td>',
            f'                        <a href="{transcript_file}" class="link-btn link-transcript">Transcript</a>',
            f'                        <a href="{spotify_url}" class="link-btn link-spotify" target="_blank">Spotify</a>',
            f'                        <a href="{youtube_url}" class="link-btn link-youtube" target="_blank">YouTube</a>',
            '                    </td>',
            '                </tr>',
        ])
    
    html_parts.extend([
        '            </tbody>',
        '        </table>',
        '    </div>',
        '</body>',
        '</html>'
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))


def main():
    """Main function to generate the episode index."""
    
    # Determine the episodes directory (relative to script location)
    script_dir = Path(__file__).parent
    episodes_dir = script_dir / 'episodes'
    
    if not episodes_dir.exists():
        print(f"Error: Episodes directory '{episodes_dir}' not found.")
        return 1
    
    print(f"Scanning for transcript files in: {episodes_dir}")
    
    # Find transcript files
    transcript_files = find_transcript_files(episodes_dir)
    
    if not transcript_files:
        print("No transcript files found (looking for transcript_ep*.html)")
        return 1
    
    print(f"Found {len(transcript_files)} transcript file(s):")
    
    # Extract episode information
    episodes = []
    for tf in transcript_files:
        title = extract_episode_title(tf['path'])
        episodes.append({
            'filename': tf['filename'],
            'episode_num': tf['episode_num'],
            'title': title
        })
        print(f"  - Episode {tf['episode_num']}: {title}")
    
    # Generate index.html
    output_path = episodes_dir / 'index.html'
    generate_index_html(episodes, output_path)
    
    print(f"\nIndex file generated: {output_path}")
    print(f"Make sure 'transcript_styles.css' is in the same directory!")
    
    return 0


if __name__ == '__main__':
    exit(main())

