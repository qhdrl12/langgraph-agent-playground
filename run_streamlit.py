"""Run the KShop Streamlit application."""

import subprocess
import sys
from pathlib import Path


def run_streamlit():
    """Run the Streamlit application."""
    main_py = Path(__file__).parent / "main.py"
    
    if not main_py.exists():
        print("Error: main.py not found!")
        sys.exit(1)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(main_py),
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--theme.base", "light"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStreamlit application stopped.")

if __name__ == "__main__":
    run_streamlit()