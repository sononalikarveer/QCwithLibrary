import pandas as pd
from io import BytesIO

def generate_excel_report(results):
    df = pd.DataFrame(results)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
