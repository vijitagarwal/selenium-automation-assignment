import subprocess
import time
from pathlib import Path

from PIL import ImageGrab
import win32gui
import win32process
import win32con


ROOT = Path(__file__).resolve().parent
CASES = ["TC-01_Register_User", "TC-02_Login_Correct"]


def window_for_process(pid):
    found = []
    powershell_windows = []

    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if "PowerShell" in title or "pwsh" in title.lower():
            powershell_windows.append(hwnd)
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        if window_pid == pid and title:
            found.append(hwnd)

    win32gui.EnumWindows(callback, None)
    if found:
        return found[0]
    if powershell_windows:
        return powershell_windows[-1]
    raise RuntimeError(f"Could not find PowerShell window for process {pid}.")


def window_for_title(title):
    for _ in range(20):
        matches = []

        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == title:
                matches.append(hwnd)

        win32gui.EnumWindows(callback, None)
        if matches:
            return matches[0]
        time.sleep(1)
    raise RuntimeError(f"Could not find PowerShell window titled {title}.")


def capture_case(folder):
    case_dir = ROOT / folder
    title = f"Selenium {folder} PowerShell"
    command = (
        f"$host.UI.RawUI.WindowTitle = '{title}'; "
        f"Set-Location -LiteralPath '{case_dir}'; "
        "Write-Host ('PS ' + (Get-Location).Path + '> python test_case.py'); "
        "python test_case.py; "
        "Write-Host ''; "
        "Start-Sleep -Seconds 5"
    )
    process = subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-NoExit", "-Command", command],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    try:
        time.sleep(45)
        hwnd = window_for_title(title)
        win32gui.ShowWindow(hwnd, 3)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )
        time.sleep(2)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        image = ImageGrab.grab(bbox=(left, top, right, bottom))
        target = case_dir / "terminal" / "terminal_result.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target)
        print(f"Saved genuine PowerShell screenshot: {target}")
    finally:
        if process.poll() is None:
            process.terminate()


if __name__ == "__main__":
    for case in CASES:
        capture_case(case)
