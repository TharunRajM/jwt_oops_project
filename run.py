import sys
from pathlib import Path

# Add 'src' directory to Python module search path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from file_upload import app

if __name__ == "__main__":
    app.run(debug=True, port=8000)
