import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.flows import run_case

if __name__ == "__main__":
    run_case(4, "Logout User", Path.cwd())
