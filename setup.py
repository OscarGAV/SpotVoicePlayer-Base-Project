import subprocess
import sys


def main():
    print("Installing dependencies...\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\nDone. Run the program with: python run.py")


if __name__ == "__main__":
    main()