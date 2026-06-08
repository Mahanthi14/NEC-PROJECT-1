from fpdf import FPDF
import datetime
import os

def generate_report(
    total_customers,
    total_revenue,
    low_stock_count
):

    os.makedirs("reports", exist_ok=True)

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        18
    )

    pdf.cell(
        200,
        10,
        "AI Customer Intelligence Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.cell(
        200,
        10,
        f"Generated On: {datetime.datetime.now()}",
        ln=True
    )

    pdf.ln(5)

    pdf.cell(
        200,
        10,
        f"Total Customers: {total_customers}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Total Revenue: Rs. {total_revenue}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Low Stock Products: {low_stock_count}",
        ln=True
    )

    file_path = "reports/customer_report.pdf"

    pdf.output(file_path)

    return file_path