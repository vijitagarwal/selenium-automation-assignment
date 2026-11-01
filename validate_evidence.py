from pathlib import Path
import sys

from run_all import TESTS


ROOT = Path(__file__).resolve().parent


def validate():
    failures = []
    tests = TESTS[:2] if "--pilot" in sys.argv else TESTS
    for number, folder in tests:
        case_dir = ROOT / folder
        required = [
            case_dir / "test_case.py",
            case_dir / "terminal" / "terminal_result.png",
            case_dir / "execution.log",
        ]
        if not required[0].is_file() or required[0].stat().st_size == 0:
            failures.append(f"{folder}: missing test_case.py")
        if not list((case_dir / "screenshots").glob("*.png")):
            failures.append(f"{folder}: missing browser screenshot")
        for path in required[1:]:
            if not path.is_file() or path.stat().st_size == 0:
                failures.append(f"{folder}: missing {path.name}")
        log = required[2]
        if log.is_file():
            try:
                contents = log.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                contents = log.read_text(encoding="utf-16")
            if "RESULT: " not in contents:
                failures.append(f"{folder}: execution status not recorded")
    if failures:
        print("\n".join(failures))
        return 1
    print("All evidence files are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
