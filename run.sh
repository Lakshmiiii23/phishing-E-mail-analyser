#!/bin/bash
# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "Installing python requirements..."
pip install -r requirements.txt

echo "Starting Streamlit application..."
streamlit run app/app.py
