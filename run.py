"""
run.py
------
Entry point for Hand Mouse Controller.

Usage:
    python run.py
"""

import os
from dotenv import load_dotenv
load_dotenv()

from hand_mouse_controller.config import Config
from hand_mouse_controller.voice import VoiceController


def main():
    cfg = Config()

    print("=" * 50)
    print("  HAND MOUSE CONTROLLER")
    print("=" * 50)
    print(f"  Click command : '{cfg.CLICK_COMMAND}'")
    print(f"  Voice language: {cfg.VOICE_LANGUAGE}")
    print("=" * 50 + "\n")

    state = {
        "active": True,
        "last_click": 0,
    }

    voice = VoiceController(state, cfg)

    try:
        voice.run()
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")
    finally:
        state["active"] = False
        print("[INFO] Program terminated.")


if __name__ == "__main__":
    main()