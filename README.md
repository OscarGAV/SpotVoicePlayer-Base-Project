# Voice Assistant (Python)

Voice assistant for Windows controlled entirely by voice commands.
No mouse, no keyboard. Integrates with Spotify via the official API.

---

## Technologies

- Python 3.12
- SpeechRecognition — voice capture and Google STT
- PyAudio — microphone input
- PyAutoGUI — mouse click simulation
- Spotipy — Spotify Web API client
- python-dotenv — environment variable management

---

## Features

- Left click by voice command ("enter")
- Play songs on Spotify by voice ("reproduce", "pon", "escucha" + song name)
- Fuzzy song matching — finds the closest result even with partial or imprecise names
- Close the program by voice ("cerrar programa", "cierra el programa")

---

## Project Structure

```
hand_mouse_controller/
├── run.py                            # Entry point
├── setup.py                          # Installs dependencies
├── requirements.txt                  # Dependencies
├── .env                              # Spotify credentials (not committed)
├── .env.example                      # Credentials template
├── README.md
├── hand_mouse_controller/
│   ├── __init__.py
│   ├── config.py                     # All configurable settings
│   ├── voice.py                      # Voice recognition and command handling
│   └── spotify_player.py             # Spotify search and playback
```

---

## Setup

1. Install Python 3.12 and create a virtual environment:

       py -3.12 -m venv .venv312
       .venv312\Scripts\activate

2. Install dependencies:

       python setup.py

3. Configure Spotify credentials.
   Copy .env.example to .env and fill in your credentials:

       SPOTIPY_CLIENT_ID=your_client_id
       SPOTIPY_CLIENT_SECRET=your_client_secret
       SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

   Get your credentials at https://developer.spotify.com/dashboard
   In the app settings, add http://127.0.0.1:8888/callback as a Redirect URI.

4. Run:

       python run.py

---

## Voice Commands

| Say                                   | Action                          |
|---------------------------------------|---------------------------------|
| "enter"                               | Left mouse click                |
| "reproduce Despacito"                 | Search and play on Spotify      |
| "pon algo de Bad Bunny"               | Search and play on Spotify      |
| "escucha Blinding Lights"             | Search and play on Spotify      |
| "cerrar programa"                     | Close the assistant             |
| "cierra el programa"                  | Close the assistant             |

---

## Configuration

All settings are in hand_mouse_controller/config.py.

| Setting               | Default              | Description                              |
|-----------------------|----------------------|------------------------------------------|
| VOICE_LANGUAGE        | "es-ES"              | Language for speech recognition          |
| CLICK_COMMAND         | "enter"              | Word that triggers a left click          |
| CLICK_COOLDOWN        | 1.0                  | Seconds between clicks                   |
| QUIT_TRIGGER_WORDS    | ["cerrar", "cierra"] | Words that trigger quit                  |
| QUIT_KEYWORDS         | ["programa"]         | Keywords required alongside quit trigger |
| SPOTIFY_TRIGGER_WORDS | ["reproduce", ...]   | Words that trigger Spotify search        |
| ENERGY_THRESHOLD      | 300                  | Microphone sensitivity                   |

---

## Notes

- The first time a Spotify command is used, a browser window will open for authentication. After that it stays logged in via a .cache file.
- Requires an active internet connection for speech recognition and Spotify.
- Spotify must be open and playing on any device for playback commands to work.