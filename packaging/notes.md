# packaging/notes.md

Steps to produce a production Windows build using PyInstaller:

1. On a Windows machine with Python 3.12 installed, create and activate a virtualenv.
2. Install dependencies: pip install -r requirements.txt pyinstaller
3. Run: pyinstaller --onefile --windowed -n JunkyardAssistant src/main.py
4. Copy the dist/JunkyardAssistant.exe to the user's machine. Ensure the data.db (or configured path) is placed alongside it if you want existing data.

Notes:
- Test the executable in a clean VM to ensure all PySide6 runtime dependencies are included.
- Alternatively, use briefcase or nuitka for different packaging strategies.
