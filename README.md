# Selenium Assignment Final

This project automates the official Automation Exercise test cases with visible
Chrome and Selenium. The pilot execution currently covers TC-01 and TC-02.

## Setup

1. Create a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Keep the local password in `.env`.
4. Run a pilot test from its folder, for example:

```powershell
Set-Location .\TC-01_Register_User
python test_case.py
```

`run_all.py` is the sequential execution controller. It writes each test's
output to `execution.log`; terminal screenshot capture and report generation
are completed after the pilot is verified.
