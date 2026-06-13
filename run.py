import os
import sys
import subprocess

def run_cmd(args, cwd=None):
    print(f"Running: {' '.join(args)}")
    result = subprocess.run(args, cwd=cwd)
    if result.returncode != 0:
        print(f"Error executing command: {' '.join(args)}")
        sys.exit(result.returncode)

def main():
    # 1. Get script dir and set as current working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Set working directory to: {script_dir}")

    # 2. Check and install dependencies
    print("Installing python requirements...")
    run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # 3. Ensure directories exist
    os.makedirs("models", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # 4. Check if models/datasets are built, if not, train/build them
    if not os.path.exists("models/phishing_model.pkl") or not os.path.exists("data/processed/train.csv"):
        print("Training datasets and models not found. Building them now...")
        if os.path.exists("data/phishing_email.csv"):
            run_cmd([sys.executable, "src/prepare_dataset.py"])
            run_cmd([sys.executable, "train_model.py"])
        else:
            print("Warning: data/phishing_email.csv not found, skipping ML training.")

    if not os.path.exists("models/faiss_index.bin"):
        print("FAISS index not found. Building knowledge index now...")
        run_cmd([sys.executable, "src/build_faiss.py"])

    # 5. Launch Streamlit app
    print("Starting Streamlit application...")
    run_cmd([sys.executable, "-m", "streamlit", "run", "app/app.py"])

if __name__ == "__main__":
    main()
