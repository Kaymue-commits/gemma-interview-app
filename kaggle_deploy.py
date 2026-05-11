#!/usr/bin/env python3
"""
Kaggle Kernel deployment for Gemma Interview App.
This script:
1. Installs Flask in the Kaggle kernel environment
2. Starts the Flask app with Groq API
3. Uses python-dotenv to load env vars
"""
import subprocess
import sys

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "flask", "requests", "python-dotenv"])

# Now run the app
from app import app
import os

# Get port from environment (Kaggle sets KAGGLE_KERNEL_COMMIT_ID)
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
