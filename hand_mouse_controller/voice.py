"""
voice.py
--------
Handles continuous microphone listening in a background thread.

Commands:
  - 'enter'                                      → left click
  - 'cerrar/cierra programa'                     → quit
  - 'reproduce/pon/escucha <cancion> en spotify' → play on Spotify
"""

import re
import time
import pyautogui
import speech_recognition as sr

from hand_mouse_controller.config import Config


class VoiceController:
    def __init__(self, state: dict, config: Config = None):
        self.state = state
        self.cfg = config or Config()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.cfg.ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6

    def _extract_song(self, text: str) -> str | None:
        trigger_pattern = "|".join(self.cfg.SPOTIFY_TRIGGER_WORDS)

        match = re.search(rf"(?:{trigger_pattern})\s+(.+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return None

    def run(self):
        from hand_mouse_controller.spotify_player import play_song as spotify_play

        print("[VOICE] Starting microphone...")

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[VOICE] Ready.")
            print("  - Say 'enter' to click")
            print("  - Say 'reproduce <song>' to play on Spotify")
            print("  - Say 'cerrar/cierra programa' to exit\n")

            while self.state["active"]:
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=8)
                    text = self.recognizer.recognize_google(
                        audio, language=self.cfg.VOICE_LANGUAGE
                    ).lower()
                    print(f"[VOICE] Heard: '{text}'")

                    is_quit = (
                        any(t in text for t in self.cfg.QUIT_TRIGGER_WORDS)
                        and all(k in text for k in self.cfg.QUIT_KEYWORDS)
                    )
                    is_spotify = any(t in text for t in self.cfg.SPOTIFY_TRIGGER_WORDS)

                    if is_quit:
                        print("[VOICE] Quit command received. Closing program...")
                        self.state["active"] = False
                        break
                    elif is_spotify:
                        song = self._extract_song(text)
                        if song:
                            print(f"[VOICE] Spotify → searching '{song}'...")
                            msg = spotify_play(song)
                            print(f"[VOICE] {msg}")
                        else:
                            print("[VOICE] Could not extract song name.")
                    elif self.cfg.CLICK_COMMAND in text:
                        now = time.time()
                        if now - self.state.get("last_click", 0) >= self.cfg.CLICK_COOLDOWN:
                            self.state["last_click"] = now
                            pyautogui.click()
                            print("[VOICE] Click executed!")

                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"[VOICE] Connection error: {e}")
                    time.sleep(2)
                except Exception as e:
                    print(f"[VOICE] Unexpected error: {e}")

        print("[VOICE] Voice controller stopped.")