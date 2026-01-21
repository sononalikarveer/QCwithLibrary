import yaml
from src.ppt.ppt_reader import read_ppt
from src.qc.chunking_validator import validate_slide
from report.excel_report import generate_excel_report

PPT_PATH = "data/input_ppt/sample.pptx"
REPORT_PATH = "data/output_reports/qc_report.xlsx"
RULES_PATH = "config/qc_rules.yaml"

def load_rules():
    with open(RULES_PATH, "r") as f:
        return yaml.safe_load(f)

def main():
    rules = load_rules()
    slides = read_ppt(PPT_PATH)

    results = []
    for slide in slides:
        qc_result = validate_slide(slide, rules)
        results.append(qc_result)

    generate_excel_report(results, REPORT_PATH)
    print("QC Report generated successfully")

if __name__ == "__main__":
    main()
