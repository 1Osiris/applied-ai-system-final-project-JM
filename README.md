# Playlist Assistant - Setup & Run Guide

🎵 A music playlist management application powered by Google Gemini AI.

## Overview

The **Playlist Assistant** is an AI-powered app that helps you manage music playlists intelligently. You describe a song and how it makes you feel, and the AI analyzes it to place it into matching playlists. The app can even suggest creating new playlists when nothing fits!

### Original Project (Modules 1-3)

The original project was **Music Mood Recommender (rule-based prototype)**. Its goal was to recommend playlists by scoring songs against genre, mood, and energy metadata using fixed weighting logic. It could produce transparent recommendation reasoning, but it was limited by manual rules and had less flexibility when users described songs in natural language.


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

### Sample Input / Output #2

**Input**

```text
Song title: Titanium
Artist: David Guetta ft. Sia
How it feels: powerful, motivational, high-energy gym song
```

**Output**

```json
{
   "generated_mood_tags": ["energetic", "motivational", "confident", "high-energy"],
   "matches": {
      "strong": [
         {
            "playlist": "Workout Motivation",
            "reason": "Strong tempo and empowering tone align closely with workout-focused high-energy songs."
         }
      ],
      "borderline": [
         {
            "playlist": "Morning Energy",
            "reason": "The uplifting mood is relevant, but intensity is higher than typical morning tracks."
         }
      ]
   },
   "suggest_new_playlist": null
}
```

### Sample Input / Output #3

**Input**

```text
Song title: Daylight Reverie
Artist: Unknown Artist
How it feels: dreamy electronic ambience for focused coding and studying
```

**Output**

```json
{
   "generated_mood_tags": ["ambient", "focus", "dreamy", "electronic"],
   "matches": {
      "strong": [],
      "borderline": [
         {
            "playlist": "Late Night Chill",
            "reason": "Calm reflective texture overlaps, but the song is more concentration-focused than late-night emotional."
         }
      ]
   },
   "suggest_new_playlist": {
      "name": "Deep Focus Flow",
      "vibe": "Steady, low-distraction tracks for coding, writing, or studying."
   }
}
```

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
├── .env                  # API keys 
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

## Design Decisions and Trade-offs

1. **JSON storage instead of a database:** I chose `playlists.json` for simplicity and fast local iteration. The trade-off is weaker scalability and no concurrent multi-user support.
2. **Strong vs. borderline categories:** I separated high-confidence from lower-confidence matches so users keep final control. The trade-off is one extra review step before saving.
3. **Explainable recommendations:** The app requires reasoning strings for each suggested match to improve trust and grading transparency. The trade-off is slightly longer model outputs and occasional verbose explanations.
4. **Gemini-driven mood extraction:** Using natural-language AI improves flexibility versus rigid keyword rules. The trade-off is external API dependency and possible response variability.

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

## Testing Summary

- **What worked:** Core recommendation flow, JSON persistence, and playlist create/remove actions worked in manual testing; unit tests for the recommender logic executed successfully.
- **What did not work at first:** Early prompt versions sometimes returned malformed JSON or overly broad playlist matches.
- **How it was improved:** I added stricter response-format instructions and retry handling for invalid JSON, and clarified confidence boundaries between strong and borderline matches.
- **What I learned:** AI features need defensive parsing, explicit schema expectations, and user confirmation checkpoints to remain reliable.

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

Building this project taught me that AI problem-solving is strongest when model output is treated as a recommendation, not an unquestioned final answer. Prompt design, output constraints, and validation logic were just as important as the model choice itself.

I also learned that explainability improves user trust: showing *why* a match was suggested made the system easier to evaluate and debug. The biggest practical lesson was balancing automation with user control by introducing strong/borderline confidence buckets and explicit confirmation before writing data.

If I continue this project, I would prioritize Spotify/Apple Music import and richer feedback loops so the assistant can learn from accepted/rejected matches over time.

## Limitations, Bias, and Responsible Use

### What are the limitations or biases in this system?

1. The assistant depends on user-provided descriptions, so vague or biased language can produce weak or skewed playlist matches.
2. Mood interpretation is subjective and culturally dependent, so the model may overfit to common Western/pop listening patterns.
3. The system currently lacks personalization memory across sessions, so it cannot fully adapt to an individual user's long-term taste.
4. External API behavior can vary over time, which can affect consistency even for similar inputs.

### Could this AI be misused, and how would misuse be prevented?

Possible misuse includes generating manipulative or inappropriate playlist labels/content, or repeatedly spamming API calls. To reduce this risk, the app keeps users in the loop by requiring manual confirmation before saving results, limits outputs to a structured schema, and can be extended with moderation checks for unsafe text before writing to storage.

### What surprised me while testing reliability?

The most surprising result was that small wording changes in the same song description could move a recommendation from strong to borderline. This showed that reliability is not just a model issue; prompt structure, schema enforcement, and confidence-threshold design strongly influence stability.

## Collaboration with AI During Development

I collaborated with AI as a design and implementation assistant, especially for prompt wording, JSON schema refinement, and edge-case handling.

- **Helpful suggestion:** AI suggested separating matches into **strong** and **borderline** categories, which made the user experience much better by preserving user control instead of auto-adding songs everywhere.
- **Flawed suggestion:** One AI suggestion initially produced overly broad mood tags and occasionally invalid JSON shape for my expected schema. I corrected this by tightening the prompt, adding stricter JSON constraints, and implementing retry/fallback validation logic.


🎵 **Enjoy your AI-powered playlist assistant!**
