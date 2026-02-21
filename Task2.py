import pandas as pd
from fpdf import FPDF
import os

# --- 1. Data Generation (Creating Sample CSV) ---
def create_sample_csv(filename="sales_data.csv"):
    data = {
        'Product': ['Laptops', 'Monitors', 'Keyboards', 'Mice', 'Headsets', 'Webcams'],
        'Units_Sold': [120, 250, 430, 500, 180, 150],
        'Unit_Price': [800, 200, 50, 25, 75, 60],
        'Revenue': [96000, 50000, 21500, 12500, 13500, 9000]
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

# --- 2. Data Analysis ---
def analyze_data(csv_file):
    df = pd.read_csv(csv_file)
    
    # Calculating Key Statistics
    stats = {
        'Total Revenue': df['Revenue'].sum(),
        'Average Unit Price': df['Unit_Price'].mean(),
        'Max Sales Product': df.loc[df['Units_Sold'].idxmax(), 'Product'],
        'Total Units Sold': df['Units_Sold'].sum(),
        'Min Revenue Product': df.loc[df['Revenue'].idxmin(), 'Product']
    }
    return df, stats

# --- 3. PDF Report Generation ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Monthly Sales Performance Report', border=False, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(df, stats, output_file):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Key Statistics Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Executive Summary Statistics", ln=True)
    pdf.set_font("Arial", size=11)
    
    for key, value in stats.items():
        # Formatting numbers for readability
        val_str = f"${value:,.2f}" if isinstance(value, float) else str(value)
        pdf.cell(0, 7, f"- {key}: {val_str}", ln=True)
    
    pdf.ln(10)

    # Data Table Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Detailed Product Data Table", ln=True)
    
    # Table Header
    pdf.set_fill_color(200, 220, 255)
    cols = list(df.columns)
    col_width = pdf.w / 4.5
    
    for col in cols:
        pdf.cell(col_width, 10, col, border=1, fill=True, align='C')
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        pdf.cell(col_width, 10, str(row['Product']), border=1)
        pdf.cell(col_width, 10, str(row['Units_Sold']), border=1)
        pdf.cell(col_width, 10, f"${row['Unit_Price']}", border=1)
        pdf.cell(col_width, 10, f"${row['Revenue']}", border=1)
        pdf.ln()

    pdf.output(output_file)
    print(f"Report successfully generated: {output_file}")

# --- 4. Main Execution ---
if __name__ == "__main__":
    # Setup files
    csv_path = create_sample_csv()
    
    # Run Analysis
    data_df, summary_stats = analyze_data(csv_path)
    
    # Create PDF
    generate_pdf(data_df, summary_stats, "Sales_Summary_Report.pdf")
