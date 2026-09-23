# Smart Media Analysis Agent — src package
"""
All core pipeline scripts live here.
Paths are resolved relative to the project root (one level up from src/).
"""

import os

# Project root is the parent of this package directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Standard project directories
if os.environ.get("VERCEL"):
    MEDIA_DIR = "/tmp/media"
    DB_DIR = "/tmp/media_db"
else:
    MEDIA_DIR = os.path.join(PROJECT_ROOT, "media")
    DB_DIR = os.path.join(PROJECT_ROOT, "media_db")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
