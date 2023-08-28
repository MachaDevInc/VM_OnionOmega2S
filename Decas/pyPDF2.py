import fitz
from tabulate import tabulate

# Open the PDF file
pdf_file = fitz.open('D:\Stripe\Decas\GoodsDescription.pdf')

# Initialize a list variable to hold the table data
table_data = []

# Loop through each page in the PDF file
for page_num in range(pdf_file.page_count):
    # Get the current page object
    page_obj = pdf_file.load_page(page_num)

    # Extract the table from the page object
    table = page_obj.get_table()

    # Check if the table exists on the page
    if table:
        # Append the table data to the overall table_data variable
        table_data += table

# Print the extracted table in a table format
print(tabulate(table_data, headers="firstrow"))

# Close the PDF file
pdf_file.close()

# pip uninstall PyMuPDF
# pip install PyMuPDF