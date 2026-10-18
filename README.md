# README: Run & Build Instructions

## Requirements
- Python 3.12+
- pip

## Install
1. Create virtualenv:
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
2. Install dependencies:
   pip install -r requirements.txt

## Run (development)
python -m src.main

## Tests
pytest -q

## Build Windows executable (PyInstaller)
1. Install pyinstaller: pip install pyinstaller
2. Build: pyinstaller --onefile --windowed -n JunkyardAssistant src/main.py
3. The exe will be in dist/ on success.


## Notes
- This application intentionally does not automate the Roblox client. All in-game actions must be performed by the player and recorded in the app.
