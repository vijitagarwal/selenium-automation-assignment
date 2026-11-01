from pathlib import Path


def save_screenshot(driver, folder, name):
    path = Path(folder) / "screenshots" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if not driver.save_screenshot(str(path)):
        raise RuntimeError(f"Could not save screenshot: {path}")
    return path
