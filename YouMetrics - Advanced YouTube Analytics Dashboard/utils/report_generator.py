from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def generate_pdf_report(df):
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.cell(200, 10, txt="YouTube Trending Videos Report", ln=1, align='C')
    pdf.ln(10)
    
    # Summary stats
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Summary Statistics", ln=1)
    pdf.set_font("Arial", size=10)
    
    stats = df.describe().round(2)
    for col in stats.columns:
        pdf.cell(200, 6, txt=f"{col}: mean={stats[col]['mean']}, max={stats[col]['max']}", ln=1)
    
    # Add plots
    plt.figure(figsize=(8, 4))
    df['category_name'].value_counts().plot(kind='bar')
    plt.title('Videos by Category')
    plt.tight_layout()
    plt.savefig('temp_plot.png')
    pdf.image('temp_plot.png', x=10, y=pdf.get_y(), w=180)
    os.remove('temp_plot.png')
    
    # Save PDF
    report_path = "reports/youtube_report.pdf"
    pdf.output(report_path)
    return report_path

def generate_excel_report(df):
    report_path = "reports/youtube_data.xlsx"
    
    with pd.ExcelWriter(report_path) as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Summary sheet
        summary = df.describe().round(2)
        summary.to_excel(writer, sheet_name='Summary Stats')
        
        # Category analysis
        cat_stats = df.groupby('category_name').agg({
            'view_count': ['mean', 'count'],
            'like_count': 'mean',
            'comment_count': 'mean'
        })
        cat_stats.to_excel(writer, sheet_name='Category Analysis')
    
    return report_path