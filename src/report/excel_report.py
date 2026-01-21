import pandas as pd
from pathlib import Path

def generate_excel_report(results, output_path):
    df = pd.DataFrame(results)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)

