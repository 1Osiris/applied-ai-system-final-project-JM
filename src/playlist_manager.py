"""
Playlist Manager Module

Handles all reads and writes to playlists.json.
Provides functions for managing playlists and songs.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path


PLAYLISTS_FILE = Path(__file__).parent.parent / "playlists.json"


def load_playlists() -> Dict[str, Any]:
    """Load playlists from JSON file.
    
    Returns:
        dict: The full playlists structure with all data
    """
    if not PLAYLISTS_FILE.exists():
        return {"playlists": {}}
    
    try:
        with open(PLAYLISTS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {PLAYLISTS_FILE} is corrupted. Returning empty playlists.")
        return {"playlists": {}}


def save_playlists(data: Dict[str, Any]) -> None:
    """Save playlists to JSON file.
    
    Args:
        data (dict): The playlists structure to save
    """
    with open(PLAYLISTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_playlist(name: str, vibe: str, moods: List[str]) -> str:
    """Create a new playlist and return its ID.
    
    Args:
        name (str): Display name of the playlist
        vibe (str): Natural language description of the playlist's purpose/feeling
        moods (List[str]): List of mood tags
        
    Returns:
        str: The generated playlist ID
    """
    # Generate slug-style ID from name
    playlist_id = name.lower().replace(" ", "_").replace("-", "_")
    # Remove special characters
    playlist_id = "".join(c for c in playlist_id if c.isalnum() or c == "_")
    
    data = load_playlists()
    
    if playlist_id in data["playlists"]:
        # If ID already exists, append a number
        counter = 1
        original_id = playlist_id
        while playlist_id in data["playlists"]:
            playlist_id = f"{original_id}_{counter}"
            counter += 1
    
    data["playlists"][playlist_id] = {
        "name": name,
        "vibe": vibe,
        "moods": moods,
        "songs": []
    }
    
    save_playlists(data)
    return playlist_id


def get_playlist(playlist_id: str) -> Optional[Dict[str, Any]]:
    """Get a single playlist's data.
    
    Args:
        playlist_id (str): The ID of the playlist
        
    Returns:
        dict or None: The playlist data, or None if not found
    """
    data = load_playlists()
    return data["playlists"].get(playlist_id)


def get_all_playlists() -> Dict[str, Dict[str, Any]]:
    """Get all playlists.
    
    Returns:
        dict: All playlists indexed by ID
    """
    data = load_playlists()
    return data["playlists"]


def add_song_to_playlists(
    song: Dict[str, Any],
    playlist_ids: List[str]
) -> Dict[str, bool]:
    """Add a song to multiple playlists, skipping duplicates.
    
    Args:
        song (dict): Song data with keys: title, artist, vibe, moods
        playlist_ids (List[str]): List of playlist IDs to add the song to
        
    Returns:
        dict: Mapping of playlist_id -> bool (success or skipped due to duplicate)
    """
    data = load_playlists()
    results = {}
    
    # Generate a unique song ID
    song_id = f"{song['title'].lower().replace(' ', '_')}_{song['artist'].lower().replace(' ', '_')}"
    song_id = "".join(c for c in song_id if c.isalnum() or c == "_")
    
    song_entry = {
        "id": song_id,
        "title": song["title"],
        "artist": song["artist"],
        "vibe": song["vibe"],
        "moods": song["moods"],
        "added_at": datetime.now().isoformat()
    }
    
    for playlist_id in playlist_ids:
        if playlist_id not in data["playlists"]:
            results[playlist_id] = False
            continue
        
        # Check for duplicates
        existing_songs = data["playlists"][playlist_id]["songs"]
        is_duplicate = any(
            s["title"].lower() == song["title"].lower() and 
            s["artist"].lower() == song["artist"].lower()
            for s in existing_songs
        )
        
        if is_duplicate:
            results[playlist_id] = False  # Skipped (duplicate)
        else:
            data["playlists"][playlist_id]["songs"].append(song_entry)
            results[playlist_id] = True  # Added successfully
    
    save_playlists(data)
    return results


def remove_song_from_playlist(playlist_id: str, song_id: str) -> bool:
    """Remove a song from a playlist.
    
    Args:
        playlist_id (str): The ID of the playlist
        song_id (str): The ID of the song to remove
        
    Returns:
        bool: True if removed, False if not found
    """
    data = load_playlists()
    
    if playlist_id not in data["playlists"]:
        return False
    
    original_count = len(data["playlists"][playlist_id]["songs"])
    data["playlists"][playlist_id]["songs"] = [
        s for s in data["playlists"][playlist_id]["songs"]
        if s["id"] != song_id
    ]
    
    if len(data["playlists"][playlist_id]["songs"]) < original_count:
        save_playlists(data)
        return True
    
    return False


def update_playlist_metadata(
    playlist_id: str,
    name: Optional[str] = None,
    vibe: Optional[str] = None,
    moods: Optional[List[str]] = None
) -> bool:
    """Update a playlist's metadata.
    
    Args:
        playlist_id (str): The ID of the playlist
        name (str, optional): New name
        vibe (str, optional): New vibe description
        moods (List[str], optional): New mood tags
        
    Returns:
        bool: True if updated, False if playlist not found
    """
    data = load_playlists()
    
    if playlist_id not in data["playlists"]:
        return False
    
    if name is not None:
        data["playlists"][playlist_id]["name"] = name
    if vibe is not None:
        data["playlists"][playlist_id]["vibe"] = vibe
    if moods is not None:
        data["playlists"][playlist_id]["moods"] = moods
    
    save_playlists(data)
    return True


def delete_playlist(playlist_id: str) -> bool:
    """Delete a playlist.
    
    Args:
        playlist_id (str): The ID of the playlist to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    data = load_playlists()
    
    if playlist_id not in data["playlists"]:
        return False
    
    del data["playlists"][playlist_id]
    save_playlists(data)
    return True


def get_song_count(playlist_id: str) -> int:
    """Get the number of songs in a playlist.
    
    Args:
        playlist_id (str): The ID of the playlist
        
    Returns:
        int: Number of songs, or 0 if playlist not found
    """
    playlist = get_playlist(playlist_id)
    if playlist is None:
        return 0
    return len(playlist["songs"])


def search_songs(query: str) -> List[Dict[str, Any]]:
    """Search for songs across all playlists.
    
    Args:
        query (str): Search query (matches title or artist)
        
    Returns:
        list: List of matching songs with their playlist context
    """
    data = load_playlists()
    results = []
    query_lower = query.lower()
    
    for playlist_id, playlist in data["playlists"].items():
        for song in playlist["songs"]:
            if (query_lower in song["title"].lower() or 
                query_lower in song["artist"].lower()):
                results.append({
                    **song,
                    "playlist_id": playlist_id,
                    "playlist_name": playlist["name"]
                })
    
    return results
