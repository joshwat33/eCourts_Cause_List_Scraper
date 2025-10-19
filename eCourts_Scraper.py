# ------------------------ Imports ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import time, re, argparse, sys

# =========================================================
#                   PDF GENERATION FUNCTION
# =========================================================
def save_cause_list_pdf(data, output_path="Cause_List.pdf"):
    """
    Generates a clean, readable PDF file from a list of case data.
    Handles text wrapping, alternating row colors, and formatted headers.
    """
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'Wrapped',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        wordWrap='CJK'
    )

    title = Paragraph("<b>District Court Cause List</b>", styles['Title'])
    elements = [title, Spacer(1, 12)]

    wrapped_data = []
    for row_index, row in enumerate(data):
        wrapped_row = []
        for cell in row:
            if row_index == 0:
                wrapped_row.append(Paragraph(f"<b>{cell}</b>", normal_style))
            else:
                wrapped_row.append(Paragraph(str(cell), normal_style))
        wrapped_data.append(wrapped_row)

    table = Table(
        wrapped_data,
        colWidths=[0.6 * inch, 3.2 * inch, 3.5 * inch, 2.8 * inch]
    )

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f3f3f3")]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])

    table.setStyle(style)
    elements.append(table)
    pdf.build(elements)
    print(f"\n✅ PDF created successfully: {output_path}\n")


# =========================================================
#                   MAIN SCRAPER LOGIC
# =========================================================
def main():
    # ----------- Argument Parser -----------
    parser = argparse.ArgumentParser(description="eCourts Cause List Scraper")
    parser.add_argument("--visible", action="store_true", help="Show browser window")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode for captcha input")
    args = parser.parse_args()

    # ----------- Force visible mode by default -----------
    if not getattr(args, "visible", False):
        args.visible = True
    if not getattr(args, "interactive", False):
        args.interactive = True

    # ----------- Setup Chrome -----------
    chrome_options = Options()
    if not args.visible:
        chrome_options.add_argument("--headless")  # only headless when explicitly told
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # ----------- Open the page -----------
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/index")
    print("\n🌐 eCourts Cause List page opened.")
    print("👉 Please manually select State, District, Court, Date, fill captcha, and click 'View Cause List'.")
    input("\n⏳ After the table has loaded completely, press Enter here to continue scraping...")

    # ----------- Scrape data -----------
    try:
        table = driver.find_element(By.ID, "dispTable")
        rows = table.find_elements(By.TAG_NAME, "tr")

        data = [["Sr No", "Case Info", "Party Name", "Advocate"]]

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if not cols:
                continue

            if len(cols) < 4 or any(td.get_attribute("colspan") for td in cols):
                continue

            sr_no = cols[0].text.strip()
            case_text = cols[1].get_attribute("innerText").replace("\n", " ").strip()
            case_text = re.sub(r"\s{2,}", " ", case_text).replace("View", "").replace("view", "")
            party_info = cols[2].get_attribute("innerText").replace("\n", " ").strip()
            advocate = cols[3].get_attribute("innerText").replace("\n", " ").strip()

            data.append([sr_no, case_text, party_info, advocate])

        if len(data) <= 1:
            print("\n⚠️ No valid case data found. Ensure table is fully loaded before pressing Enter.")
            driver.quit()
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error extracting cause list: {e}")
        driver.quit()
        sys.exit(1)

    driver.quit()
    save_cause_list_pdf(data, "Cause_List.pdf")


if __name__ == "__main__":
    main()
