"""
PDF receipt / invoice generator.
Saves receipts to a dedicated 'receipts/' folder inside the project.
"""

import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from datetime import datetime

# Create receipts directory next to this file's parent
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECEIPTS_DIR = os.path.join(_PROJECT_ROOT, "receipts")
os.makedirs(RECEIPTS_DIR, exist_ok=True)


def generate_pdf_receipt(cart, total):
    """Generate a styled PDF receipt and return the full file path."""

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"invoice_{timestamp}.pdf"
    filepath = os.path.join(RECEIPTS_DIR, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Header
    elements.append(Paragraph("SUPERMARKET INVOICE", styles["Title"]))
    elements.append(
        Paragraph(
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 10 * mm))

    # Table data
    data = [["Product", "Qty", "Unit Price", "Total"]]

    for item in cart:
        item_total = item["price"] * item["quantity"]
        data.append([
            item["name"],
            str(item["quantity"]),
            f"{item['price']:,.0f} DZD",
            f"{item_total:,.0f} DZD",
        ])

    data.append(["", "", "GRAND TOTAL", f"{total:,.0f} DZD"])

    # Table styling
    table = Table(data, colWidths=[200, 60, 100, 100])
    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#635bff")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING",   (0, 0), (-1, 0), 10),

        # Body rows
        ("FONTSIZE",     (0, 1), (-1, -2), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -2), 6),
        ("TOPPADDING",   (0, 1), (-1, -2), 6),

        # Total row
        ("BACKGROUND",   (0, -1), (-1, -1), colors.HexColor("#f0f0f5")),
        ("FONTNAME",     (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",     (0, -1), (-1, -1), 12),
        ("TOPPADDING",   (0, -1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),

        # Grid
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ALIGN",        (1, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15 * mm))
    elements.append(Paragraph("Thank you for shopping with us!", styles["Normal"]))

    doc.build(elements)
    return filepath