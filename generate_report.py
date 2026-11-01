from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as ReportImage,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

from run_all import ROOT, TESTS


NAMES = {number: folder.replace(f"TC-{number:02d}_", "").replace("_", " ") for number, folder in TESTS}


def build_report():
    output = ROOT / "Final_Assignment.pdf"
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle("Code", parent=styles["Code"], fontSize=6, leading=7)
    story = [
        Paragraph("Selenium Automation Assignment", styles["Title"]),
        Paragraph("AutomationExercise.com - 26 Official Test Cases", styles["Heading2"]),
        Spacer(1, 0.3 * inch),
        Paragraph("Prepared by: Vijit Agarwal", styles["Normal"]),
        Paragraph("This report contains the source code and execution evidence for the Selenium tests.", styles["Normal"]),
        PageBreak(),
        Paragraph("Table of Contents", styles["Heading1"]),
    ]
    for number, _ in TESTS:
        story.append(Paragraph(f"TC-{number:02d}: {NAMES[number]}", styles["Normal"]))
    story.append(PageBreak())

    for number, folder in TESTS:
        case_dir = ROOT / folder
        log = case_dir / "execution.log"
        status = "PASS" if log.is_file() and "RESULT: PASSED" in log.read_text(encoding="utf-8-sig", errors="replace") else "FAIL"
        story.append(Paragraph(f"TC-{number:02d}: {NAMES[number]}", styles["Heading1"]))
        story.append(Paragraph(f"<b>Objective:</b> Execute and verify the official AutomationExercise test case. Status: <b>{status}</b>", styles["Normal"]))
        story.append(Paragraph("<b>Expected result:</b> The requested action completes and the site displays the expected result.", styles["Normal"]))
        story.append(Paragraph(f"<b>Actual result:</b> {status} based on the latest execution log.", styles["Normal"]))
        source = (case_dir / "test_case.py").read_text(encoding="utf-8")
        story.append(Paragraph("Python source code", styles["Heading2"]))
        story.append(Preformatted(source, code_style))
        for image_path in sorted((case_dir / "screenshots").glob("*.png")):
            story.append(ReportImage(str(image_path), width=6.4 * inch, height=3.5 * inch))
            story.append(Spacer(1, 0.1 * inch))
        terminal = case_dir / "terminal" / "terminal_result.png"
        if terminal.is_file():
            story.append(Paragraph("PowerShell execution evidence", styles["Heading2"]))
            story.append(ReportImage(str(terminal), width=6.4 * inch, height=3.5 * inch))
        story.append(PageBreak())

    SimpleDocTemplate(str(output), pagesize=A4, rightMargin=36, leftMargin=36).build(story)
    print(output)


if __name__ == "__main__":
    build_report()
