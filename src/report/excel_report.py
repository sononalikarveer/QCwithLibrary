from io import BytesIO
import pandas as pd

def create_excel(rows, summary):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(
            writer,
            sheet_name="Slide Point Analysis",
            index=False
        )
        pd.DataFrame(summary).to_excel(
            writer,
            sheet_name="Summary Review",
            index=False
        )

    output.seek(0)
    return output
