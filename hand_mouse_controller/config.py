"""
config.py
---------
Centralized configuration for hand_mouse_controller.
"""


class Config:
    # Voice recognition
    VOICE_LANGUAGE: str = "es-ES"
    CLICK_COMMAND: str = "enter"
    CLICK_COOLDOWN: float = 1.0
    QUIT_KEYWORDS: list = ["programa"]
    QUIT_TRIGGER_WORDS: list = ["cerrar", "cierra"]
    ENERGY_THRESHOLD: int = 300

    # Media commands — Spotify
    SPOTIFY_TRIGGER_WORDS: list = ["reproduce", "reproducir", "pon", "poner", "escuchar", "escucha"]