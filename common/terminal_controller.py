import subprocess
import time
from pathlib import Path

from PIL import ImageGrab
import win32con
import win32gui


def _window(title):
    for _ in range(60):
        matches = []
        fallback = []

        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return
            text = win32gui.GetWindowText(hwnd)
            if text == title:
                matches.append(hwnd)
            if "PowerShell" in text or "pwsh" in text.lower():
                fallback.append(hwnd)

        win32gui.EnumWindows(callback, None)
        if matches:
            return matches[0]
        if fallback:
            return fallback[-1]
        time.sleep(1)
    raise RuntimeError(f"PowerShell window not found: {title}")


def execute_with_terminal(case_dir):
    title = f"Selenium {case_dir.name} PowerShell"
    log_path = case_dir / "execution.log"
    command = (
        f"$host.UI.RawUI.WindowTitle = '{title}'; "
        f"Set-Location -LiteralPath '{case_dir}'; "
        "Write-Host ('PS ' + (Get-Location).Path + '> python test_case.py'); "
        "python test_case.py 2>&1 | Tee-Object -FilePath execution.log; "
        "if ($LASTEXITCODE -eq 0) { Write-Host 'FINAL RESULT: PASS' } "
        "else { Write-Host 'FINAL RESULT: FAIL' }; "
        "Start-Sleep -Seconds 5"
    )
    process = subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-NoExit", "-Command", command],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    try:
        deadline = time.time() + 45
        completed = False
        while time.time() < deadline:
            if log_path.is_file():
                raw = log_path.read_bytes()
                encoding = "utf-16" if raw.startswith(b"\xff\xfe") else "utf-8-sig"
                text = raw.decode(encoding, errors="replace")
                if "RESULT: " in text or "Traceback" in text:
                    completed = True
                    break
            time.sleep(1)
        if not completed:
            process.terminate()
            with log_path.open("a", encoding="utf-8") as log:
                log.write("\nFINAL RESULT: FAIL (execution timeout)\n")
        hwnd = _window(title)
        win32gui.ShowWindow(hwnd, 3)
        try:
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0,
                0,
                0,
                0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )
        except Exception:
            pass
        time.sleep(1)
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        except Exception:
            left, top, right, bottom = (0, 0, 1295, 735)
        image = ImageGrab.grab(bbox=(left, top, right, bottom))
        target = case_dir / "terminal" / "terminal_result.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target)
        raw = log_path.read_bytes()
        encoding = "utf-16" if raw.startswith(b"\xff\xfe") else "utf-8-sig"
        return "RESULT: PASSED" in raw.decode(encoding, errors="replace")
    finally:
        if process.poll() is None:
            process.terminate()
