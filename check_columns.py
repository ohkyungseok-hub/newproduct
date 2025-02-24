import pandas as pd

input_file = "상품제안서.xlsx"
df = pd.read_excel(input_file)
print(df.columns)
