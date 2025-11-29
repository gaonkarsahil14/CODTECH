import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ------------------------------------------------------
# 1. Load Data from CSV
# ------------------------------------------------------
data_file = "D:/SAHIL CODE IT/data.csv"   # Make sure data.csv is in same folder
df = pd.read_csv(data_file)

# Sample Analysis
avg_score = df['Score'].mean()
max_score = df['Score'].max()
min_score = df['Score'].min()

# ------------------------------------------------------
# 2. Create PDF Report
# ------------------------------------------------------
pdf_file = "generated_report.pdf"
styles = getSampleStyleSheet()
story = []

doc = SimpleDocTemplate(pdf_file, pagesize=A4)

# Title
story.append(Paragraph("Automated Data Analysis Report", styles['Title']))
story.append(Spacer(1, 20))

# Intro
story.append(Paragraph("This report is automatically generated using Python.", styles['BodyText']))
story.append(Spacer(1, 12))

# File Used
story.append(Paragraph(f"Input Data File: {data_file}", styles['BodyText']))
story.append(Spacer(1, 12))

# Analysis Section
story.append(Paragraph("Analysis Summary:", styles['Heading2']))
story.append(Spacer(1, 10))

story.append(Paragraph(f"📌 Average Score: {avg_score:.2f}", styles['BodyText']))
story.append(Paragraph(f"📌 Highest Score: {max_score}", styles['BodyText']))
story.append(Paragraph(f"📌 Lowest Score: {min_score}", styles['BodyText']))
story.append(Spacer(1, 20))

# Completion note
story.append(Paragraph("Report generated successfully using Python and ReportLab.", styles['Italic']))

# Build PDF
doc.build(story)

print("PDF report generated:", pdf_file)
