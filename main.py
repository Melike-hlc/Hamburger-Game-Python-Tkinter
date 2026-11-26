import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
for folder in ("backend", "frontend", "data"):
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path:
        sys.path.insert(0, path)

import ui

if __name__ == "__main__":
    ui.run_app()
