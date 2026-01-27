# PPT Quality Check (QC) System

## Overview
This project validates PowerPoint presentations using semantic analysis.
It checks whether required concepts are present and generates a QC report.

## Features
- Slide-wise content extraction
- Semantic embedding based validation
- Rule-driven QC engine
- Excel report generation

## Folder Structure
- config/ : QC rules
- src/ppt/ : PPT reading logic
- src/qc/ : Analysis & embeddings
- src/report/ : Report generation

## How It Works
1. Load PPT
2. Extract slide text
3. Apply QC rules
4. Perform semantic matching
5. Generate Excel report

## Input
- `.pptx` file

## Output
- `QC_Report.xlsx`

## Run
```bash
python app.py



Steps to setup :

1. Create an Python env : python -m venv venv 
2. run the environment : venv\Scripts\activate
3. Install the dependancy by using command : pip install -r requirements.text
4. Run the project using command : streamlit run app.py
 