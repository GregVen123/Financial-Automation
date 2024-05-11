import pandas as pd
import numpy as np
import pandas as pd
import tabula
from tabula import read_pdf
from openpyxl import *

input_pdf_loc = input("Paste the PDF file location here: ")
num_doc = int(input("How many tables do you want? : "))

for i in range(1,(num_doc+1)):
    page = int(input(f"What page is table {i} on?: "))
    df = (tabula.read_pdf(input_pdf_loc, pages=page, stream=True))
    tabula.convert_into(input_pdf_loc,(f"output{i}.csv"), output_format="csv", pages=page)
    df2 = pd.read_csv(f"output{i}.csv")
    df2.to_excel(f"output_{i}.xlsx")


#local locations
#   C:\Users\kingo\Downloads\exhibit-13.pdf
# C:\Users\kingo\PycharmProjects\FinancialAutomation\Annual Report_DG2023.pdf

#44 45 48

