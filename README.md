# Playlist Assistant - Setup & Run Guide

🎵 A music playlist management application powered by Google Gemini AI.

## Overview

The **Playlist Assistant** is an AI-powered app that helps you manage music playlists intelligently. You describe a song and how it makes you feel, and the AI analyzes it to place it into matching playlists. The app can even suggest creating new playlists when nothing fits!
Originally this was a music recommendation application. The application used a basic weight score recommender system to group songs by their genre, mood and energy. Recommendation reasoning was also incorporated into the final response for transparency.


## Project Goals

- Build an end-to-end AI-assisted playlist manager that combines natural-language song descriptions with structured playlist metadata.
- Use Gemini to make explainable playlist decisions (not just keyword matching).
- Give users final control over additions by separating **strong** and **borderline** matches.
- Persist all data locally in JSON so the system is easy to run, inspect, and demo.

## New Features Implemented

- **Explainable AI recommendations** with reasoning for each playlist match.
- **Strong vs. borderline match categories** so users can review confidence before saving.
- **New playlist suggestions** when no existing playlist is a good fit.
- **Interactive playlist management UI** for creating playlists and removing songs.
- **Preloaded starter data** so the app is immediately demo-ready.

### Key Features

- **Smart Song Analysis**: Describe a song's vibe, and Gemini AI generates mood tags and finds perfect playlist matches
- **Playlist Management**: Create, view, and manage playlists with detailed metadata
- **Strong/Borderline Matching**: AI classifies matches with reasoning, so you decide what goes where
- **New Playlist Suggestions**: When no playlist fits, get AI suggestions for new playlists (with songs that also fit!)
- **Beautiful Dark UI**: Clean, modern Streamlit interface with dark theme
- **JSON-Based Storage**: All playlists stored locally in `playlists.json` (no database needed)

---

## Setup

### 1. Prerequisites

- Python 3.9+
- A valid Google Gemini API key (free tier available)

### 2. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This installs:
- **streamlit** — Web UI framework
- **google-genai** — Gemini API client
- **python-dotenv** — Load environment variables
- **pandas** — Data handling
- **pytest** — Testing framework

### 3. Configure Your Gemini API Key

1. Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or open `.env` in the project root
3. Add your API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

✅ **Your API key is already configured in `.env`** — you're ready to go!

Reference `.env.example` for optional settings.

---

## Running the App

### Start the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser (usually `http://localhost:8501`).

### First Launch

On first launch, the app loads with **5 pre-populated playlists** and ~20 songs:

- **Late Night Chill** — Mellow, introspective tracks (Flume, Bon Iver, Tycho, etc.)
- **Workout Motivation** — High-energy bangers (Kanye, Dua Lipa, Survivor, etc.)
- **Romantic Evening** — Sensual, intimate songs (Frank Ocean, Sade, Adele, etc.)
- **Indie Discovery** — Quirky, artistic indie tracks (Tame Impala, Mac DeMarco, etc.)
- **Morning Energy** — Uplifting, feel-good vibes (Pharrell, Katrina & The Waves, etc.)

---

## How to Use

## Sample Input / Output

Use the following example to demonstrate expected behavior.

### Sample Input (user form)

```text
Song title: Nights
Artist: Frank Ocean
How it feels: introspective, moody, emotional late-night drive energy
```

### Sample Output (AI analysis result shown in app)

```json
{
   "generated_mood_tags": ["moody", "introspective", "late-night", "emotional"],
   "matches": {
      "strong": [
         {
            "playlist": "Late Night Chill",
            "reason": "The reflective and nocturnal vibe aligns directly with this playlist's mood profile."
         }
      ],
      "borderline": [
         {
            "playlist": "Romantic Evening",
            "reason": "Emotionally intimate tone overlaps, but overall energy is less romantic-focused."
         }
      ]
   },
   "suggest_new_playlist": null
}
```

### Sample Final System Behavior

- The app pre-checks **Late Night Chill** as a strong match.
- The app leaves **Romantic Evening** unchecked as borderline.
- After clicking **Confirm & Add Song**, a success message confirms the song was saved to selected playlists.

### Mode 1: Add a Song (Default)

1. **Enter Song Details:**
   - Song title
   - Artist name
   - Description of how it makes you feel (e.g., "uplifting, chill vibes, perfect for morning runs")

2. **Click "Find where this belongs"**
   - Gemini analyzes the song and generates mood tags
   - Shows matching playlists with **💚 Strong** and **🟡 Borderline** matches
   - Each match includes reasoning from the AI

3. **Review Matches:**
   - Strong matches are pre-checked
   - Borderline matches are unchecked (you decide)
   - Or accept the suggestion to create a new playlist

4. **Confirm & Add:**
   - Click "Confirm & Add Song"
   - Song is saved to all checked playlists
   - Success message shows how many playlists were updated

### Mode 2: View Playlist Details

1. **Click any playlist in the sidebar** to see:
   - Playlist name, vibe description, and mood tags
   - All songs with their vibes and mood tags
   - Option to remove songs

2. **Click "← Back to Add Song"** to return to the main view

### Create a New Playlist

1. **In the sidebar**, expand **"➕ Create New Playlist"**
2. Enter:
   - Playlist name
   - Vibe description (what's the feeling/purpose?)
   - Select mood tags
3. **Click "Create Playlist"** — now it's ready to receive songs!

---

## File Structure

```
playlist-assistant/
├── app.py                 # Main Streamlit app (UI and controls)
├── src/
│   ├── __init__.py       # Package marker
│   ├── agent.py          # Gemini API integration
│   ├── playlist_manager.py  # JSON read/write operations
│   ├── main.py           # (Original music recommender)
│   └── recommender.py    # (Original music recommender)
├── playlists.json        # Playlist data (auto-created with starter data)
├── requirements.txt      # Python dependencies
├── .env                  # API keys (NEVER commit this!)
├── .env.example          # Template for .env
└── README.md             # Original project README
```

---

## API Integration (Gemini)

The app uses **Google Gemini 2.5 Flash** to analyze songs. Here's what happens:

1. **You describe a song's vibe** (e.g., "melancholy, reflective, great for late night")
2. **Gemini receives:**
   - The song title and artist
   - Your description
   - Your entire playlist library (with all songs and vibes)
3. **Gemini responds with JSON:**
   - Generated mood tags for the song
   - Playlist matches (strong/borderline) with reasoning
   - Optional suggestion for a new playlist
4. **The app displays results** and lets you confirm/adjust before saving

The system prompt guides Gemini to think deeply about vibes and feelings, not just keyword matching.

---

## Troubleshooting

### "Missing GEMINI_API_KEY" Error

**Solution:** Ensure `.env` exists in the project root with:
```env
GEMINI_API_KEY=your_api_key_here
```

### Streamlit imports not found

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "Invalid JSON from Gemini" Error

**Solution:** The app retries once automatically. If it still fails, check:
- Your API key is valid
- You have credit/quota on your Gemini account
- Network connection is stable

### Playlists not persisting

**Solution:** Ensure `playlists.json` has write permissions in the project root.

---

## Development

### Running Tests

```bash
pytest
```

### Adding Features

- **Modify `agent.py`** to change Gemini behavior or prompt
- **Modify `playlist_manager.py`** to add new data operations
- **Modify `app.py`** to change the UI or add new views

### Resetting to Starter Data

Delete `playlists.json` and restart the app — it will auto-regenerate with starter data.

---

## Notes

- **No database required** — all data stored in a simple JSON file
- **No login system** — perfect for personal/classroom use
- **Privacy** — your playlists and descriptions are only sent to Gemini; not stored externally
- **Free Tier** — Google's Gemini API has a free tier with generous limits

---

## Architecture

```
User Input (Streamlit UI)
         ↓
    app.py (renders UI, manages state)
         ↓
    agent.py (talks to Gemini API)
         ↓
    Google Gemini (analyzes song)
         ↓
    Parse JSON response
         ↓
    playlist_manager.py (save to JSON)
         ↓
    playlists.json (persistent storage)
```

---

## Reflection

- **AI During Development** — During the Design and Development proccess of the project I used Claused to help me craft the playlist JSON and how it was structured. I found that my original design of the JSON structure was unessesarily complicated, but Claude helped me restrucutre it.

- **Future Improvments** — If I were to expand aupon this project I would try to find a way to load the users spotify or apple music library. This would make the application legitamatley usable and much more impactful.


🎵 **Enjoy your AI-powered playlist assistant!**
