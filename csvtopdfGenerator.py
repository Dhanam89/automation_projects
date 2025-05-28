import pandas as pd 
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

# Define path for output files
path = "100 Sales Records.csv"
bar_chart_path = "total_profit_by_region.png"
pie_chart_item_path = "total_profit_by_item_type.png"
pie_chart_channel_path = "unit_sold_by_sales_channel.png"
output_pdf_path = "Sales_Report_With_Charts.pdf"

def extract_data(path):
    data = pd.read_csv(path)
    df =  pd.DataFrame(data)
    return df

def analyse_data(df):
    region_profit = df.groupby("Region")["Total Profit"].sum().sort_values()
    item_profit = df.groupby("Item Type")["Total Profit"].sum()
    total_sales = df.groupby("Sales Channel")["Units Sold"].sum()
    return region_profit, item_profit, total_sales

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Sales Dashboard Report", ln=True, align="C")
        self.ln(10)

    def add_summary_cards(self, sales, installs):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(90, 10, f"Total Sales: {sales:,}", border=1, fill=True)
        self.cell(0, 10, f"Installations: {installs:,}", border=1, fill=True, ln=True)
        self.ln(5)

    def add_image(self, path, w=180):
        self.image(path, x=15, w=w)
        self.ln(10)
    
def plot_bar_chart(data, title, path):
    plt.figure(figsize=(10, 4))
    data.plot(kind="bar", color="#004466", legend=False)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_pie_chart(data, title, path):
    plt.figure(figsize=(8, 8))
    data.plot(kind="pie", autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.ylabel("")  # Hide y-label
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def generate_pdf_report(csv_path):
    # Load real data
    df = extract_data(path)
    region_profit, item_profit, total_sales = analyse_data(df)

    # Generate bar chart - Total sales by region
    
    plot_bar_chart(region_profit, "Total Sales by Region", bar_chart_path)
    
    # Generate Pie chart - Total sales vs Item type 
    
    plot_pie_chart(item_profit, "Total sales vs Item type ", pie_chart_item_path)
    
    # Generate Pie chart - Sales channel vs Units sold
    plot_pie_chart(total_sales, "Sales channel vs Units sold", pie_chart_channel_path)
    
    #Create PDF
    pdf = PDF()
    pdf.add_page()
    # Set title
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sales Visualizations", ln=True)

    # Bar chart - Total Profit by Region
    pdf.image(bar_chart_path, x=10, y=25, w=180)

    # Pie chart 1 - Total Profit by Item Type
    pdf.image(pie_chart_item_path, x=10, y=120, w=85)

    # Pie chart 2 - Units Sold by Sales Channel
    pdf.image(pie_chart_channel_path, x=110, y=120, w=85)

    # Save the PDF
    pdf.output(output_pdf_path)

if __name__ == '__main__':
   
    generate_pdf_report(path)
