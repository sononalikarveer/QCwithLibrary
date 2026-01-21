import pandas as pd
from io import BytesIO

def create_excel(results):
    df = pd.DataFrame(results)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
