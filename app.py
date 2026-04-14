"""
Playlist Assistant Streamlit App

A music playlist management application powered by Google Gemini AI.
Lets users analyze songs and intelligently place them into matching playlists.
"""

import json
import streamlit as st
from datetime import datetime

from src.agent import analyze_song_for_playlists, format_agent_response_for_ui
from src.playlist_manager import (
    load_playlists,
    get_all_playlists,
    create_playlist,
    get_playlist,
    add_song_to_playlists,
    remove_song_from_playlist,
)


# Configure Streamlit page
st.set_page_config(
    page_title="Playlist Assistant",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme styling
st.markdown("""
<style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .main {
        background-color: #0d1117;
    }
    .sidebar {
        background-color: #161b22;
    }
    h1 {
        color: #79c0ff;
        font-weight: bold;
    }
    h2 {
        color: #79c0ff;
    }
    h3 {
        color: #a371f7;
    }
    .stButton > button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #2ea043;
    }
    .mood-pill {
        display: inline-block;
        background-color: #a371f7;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .strong-match {
        border-left: 4px solid #3fb950;
    }
    .borderline-match {
        border-left: 4px solid #f0883e;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if "current_view" not in st.session_state:
        st.session_state.current_view = "add_song"  # "add_song" or "playlist_detail"
    
    if "selected_playlist" not in st.session_state:
        st.session_state.selected_playlist = None
    
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    
    if "pending_song" not in st.session_state:
        st.session_state.pending_song = None
    
    if "checked_playlists" not in st.session_state:
        st.session_state.checked_playlists = {}


init_session_state()


def render_mood_pills(moods: list):
    """Render mood tags as colored pills."""
    if not moods:
        return
    
    html = '<div style="margin-bottom: 1rem;">'
    colors = ["#a371f7", "#79c0ff", "#79c0ff", "#f0883e", "#3fb950"]
    for i, mood in enumerate(moods):
        color = colors[i % len(colors)]
        html += f'<span style="display: inline-block; background-color: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; margin-right: 0.5rem; margin-bottom: 0.5rem; font-size: 0.9rem;">{mood}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with playlists and create new playlist section."""
    st.sidebar.title("🎵 My Playlists")
    
    playlists = get_all_playlists()
    
    # Playlist buttons
    if playlists:
        st.sidebar.markdown("---")
        for playlist_id, playlist in playlists.items():
            song_count = len(playlist["songs"])
            button_label = f"{playlist['name']} ({song_count})"
            
            if st.sidebar.button(button_label, key=f"playlist_{playlist_id}", use_container_width=True):
                st.session_state.current_view = "playlist_detail"
                st.session_state.selected_playlist = playlist_id
                st.rerun()
    else:
        st.sidebar.info("No playlists yet. Create one below!")
    
    st.sidebar.markdown("---")
    
    # Create new playlist section
    with st.sidebar.expander("➕ Create New Playlist"):
        new_name = st.text_input("Playlist Name", key="new_playlist_name")
        new_vibe = st.text_area("Playlist Vibe Description", key="new_playlist_vibe", height=100)
        new_moods = st.multiselect(
            "Mood Tags",
            ["happy", "sad", "energetic", "chill", "romantic", "angry", "peaceful", "creative", "nostalgic", "funky"],
            key="new_playlist_moods"
        )
        
        if st.button("Create Playlist", key="create_playlist_btn"):
            if new_name and new_vibe:
                create_playlist(new_name, new_vibe, new_moods)
                st.success(f"Playlist '{new_name}' created!")
                st.rerun()
            else:
                st.error("Please enter both a name and vibe description.")


def render_add_song_mode():
    """Render the 'Add a Song' mode."""
    st.header("🎧 Add a New Song")
    
    # Input section
    col1, col2 = st.columns(2)
    with col1:
        song_title = st.text_input("Song Title", key="song_title")
    with col2:
        artist = st.text_input("Artist", key="artist")
    
    vibe_description = st.text_area(
        "How does this song make you feel?",
        key="vibe_description",
        height=120,
        placeholder="Describe the mood, emotion, energy, or any feeling this song gives you..."
    )
    
    analyze_btn = st.button("🔍 Find where this belongs", use_container_width=True)
    
    # Analysis handling
    if analyze_btn:
        if not song_title or not artist or not vibe_description:
            st.error("Please fill in all fields.")
        else:
            # Store pending song info
            st.session_state.pending_song = {
                "title": song_title,
                "artist": artist,
                "vibe": vibe_description
            }
            
            with st.spinner("🤔 Analyzing with Gemini..."):
                try:
                    playlists_data = load_playlists()
                    raw_response = analyze_song_for_playlists(
                        song_title,
                        artist,
                        vibe_description,
                        playlists_data
                    )
                    
                    formatted = format_agent_response_for_ui(raw_response)
                    st.session_state.analysis_results = {
                        "raw": raw_response,
                        "formatted": formatted
                    }
                    
                    # Initialize checked playlists (strong matches pre-checked)
                    st.session_state.checked_playlists = {}
                    for match in formatted["strong_matches"]:
                        st.session_state.checked_playlists[match["playlist_id"]] = True
                    for match in formatted["borderline_matches"]:
                        st.session_state.checked_playlists[match["playlist_id"]] = False
                    
                except Exception as e:
                    st.error(f"Error analyzing song: {e}")
                    st.session_state.analysis_results = None
    
    # Display analysis results
    if st.session_state.analysis_results:
        st.markdown("---")
        st.subheader("✨ Analysis Results")
        
        formatted = st.session_state.analysis_results["formatted"]
        
        # Song mood tags
        st.markdown("**Generated Mood Tags:**")
        render_mood_pills(formatted["moods"])
        
        # Strong matches
        if formatted["strong_matches"]:
            st.markdown("#### 💚 Strong Matches")
            for match in formatted["strong_matches"]:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        playlist = get_playlist(match["playlist_id"])
                        playlist_name = playlist["name"] if playlist else "Unknown Playlist"
                        st.markdown(f"**{playlist_name}**")
                        st.caption(match["reasoning"])
                    with col2:
                        checked = st.checkbox(
                            "Add",
                            value=True,
                            key=f"check_{match['playlist_id']}",
                            label_visibility="collapsed"
                        )
                        st.session_state.checked_playlists[match["playlist_id"]] = checked
        
        # Borderline matches
        if formatted["borderline_matches"]:
            st.markdown("#### 🟡 Borderline Matches")
            for match in formatted["borderline_matches"]:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        playlist = get_playlist(match["playlist_id"])
                        playlist_name = playlist["name"] if playlist else "Unknown Playlist"
                        st.markdown(f"**{playlist_name}**")
                        st.caption(match["reasoning"])
                    with col2:
                        checked = st.checkbox(
                            "Add",
                            value=False,
                            key=f"check_{match['playlist_id']}",
                            label_visibility="collapsed"
                        )
                        st.session_state.checked_playlists[match["playlist_id"]] = checked
        
        # New playlist suggestion
        if formatted["new_playlist"]:
            st.markdown("#### 🆕 Suggested New Playlist")
            suggestion = formatted["new_playlist"]
            with st.container(border=True):
                st.markdown(f"**{suggestion['name']}**")
                st.write(f"*Vibe:* {suggestion['vibe']}")
                st.markdown("*Mood Tags:*")
                render_mood_pills(suggestion["moods"])
                
                if st.checkbox("Create this playlist and add song", key="create_new_playlist_checkbox"):
                    st.session_state.checked_playlists["__new_playlist__"] = {
                        "data": suggestion,
                        "create": True
                    }
        
        # Confirm and add button
        if st.button("✅ Confirm & Add Song", use_container_width=True):
            if not any(st.session_state.checked_playlists.values()):
                st.error("Please select at least one playlist.")
            else:
                # Collect playlists to add to
                target_playlists = []
                new_playlist_to_create = None
                
                for playlist_id, checked in st.session_state.checked_playlists.items():
                    if playlist_id == "__new_playlist__" and isinstance(checked, dict):
                        if checked.get("create"):
                            new_playlist_to_create = checked["data"]
                    elif checked:
                        target_playlists.append(playlist_id)
                
                # Create new playlist if needed
                if new_playlist_to_create:
                    new_id = create_playlist(
                        new_playlist_to_create["name"],
                        new_playlist_to_create["vibe"],
                        new_playlist_to_create["moods"]
                    )
                    target_playlists.append(new_id)
                
                # Add song to playlists
                song_data = {
                    "title": st.session_state.pending_song["title"],
                    "artist": st.session_state.pending_song["artist"],
                    "vibe": st.session_state.pending_song["vibe"],
                    "moods": formatted["moods"]
                }
                
                results = add_song_to_playlists(song_data, target_playlists)
                
                # Show results
                success_count = sum(1 for v in results.values() if v)
                skip_count = sum(1 for v in results.values() if not v)
                
                st.success(f"🎉 Added to {success_count} playlist(s)!")
                if skip_count > 0:
                    st.info(f"⏭️ Skipped {skip_count} playlist(s) (duplicate detected)")
                
                # Clear form
                st.session_state.analysis_results = None
                st.session_state.pending_song = None
                st.session_state.checked_playlists = {}


def render_playlist_detail_mode():
    """Render the playlist detail view."""
    playlist_id = st.session_state.selected_playlist
    playlist = get_playlist(playlist_id)
    
    if not playlist:
        st.error("Playlist not found.")
        return
    
    # Back button
    if st.button("← Back to Add Song"):
        st.session_state.current_view = "add_song"
        st.session_state.selected_playlist = None
        st.rerun()
    
    # Playlist header
    st.header(f"🎵 {playlist['name']}")
    st.markdown(f"**Vibe:** {playlist['vibe']}")
    
    st.markdown("**Mood Tags:**")
    render_mood_pills(playlist["moods"])
    
    st.markdown("---")
    
    # Songs table
    songs = playlist["songs"]
    if songs:
        st.subheader(f"🎧 Songs ({len(songs)})")
        
        for song in songs:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{song['title']}** by *{song['artist']}*")
                    if song.get("vibe"):
                        st.caption(f"✨ {song['vibe']}")
                    
                    if song.get("moods"):
                        render_mood_pills(song["moods"])
                    
                    st.caption(f"Added: {song.get('added_at', 'Unknown')}")
                
                with col2:
                    if st.button("🗑️", key=f"remove_{song['id']}", help="Remove song"):
                        remove_song_from_playlist(playlist_id, song["id"])
                        st.success("Song removed!")
                        st.rerun()
    else:
        st.info("No songs in this playlist yet. Add one from the main view!")


def main():
    """Main app logic."""
    render_sidebar()
    
    # Main content area
    if st.session_state.current_view == "add_song":
        render_add_song_mode()
    elif st.session_state.current_view == "playlist_detail":
        render_playlist_detail_mode()


if __name__ == "__main__":
    main()
