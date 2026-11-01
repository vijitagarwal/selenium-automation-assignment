import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.pending import run_pending

if __name__ == "__main__":
    run_pending("TC-06: Contact Us Form")
