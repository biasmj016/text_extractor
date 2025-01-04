import os
from PIL import Image
import pytesseract
import pandas as pd
import fitz

def extract_text_from_file(file_path):
    if file_path.lower().endswith(('png', 'jpg', 'jpeg')):
        return pytesseract.image_to_string(Image.open(file_path), lang='eng')
    elif file_path.lower().endswith(('xls', 'xlsx')):
        return extract_text_from_excel(file_path)
    elif file_path.lower().endswith('pdf'):
        return extract_text_from_pdf(file_path)
    return None

def extract_text_from_excel(file_path):
    """엑셀 파일 텍스트 추출 시작."""
    text = ""
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        text += df.to_string(index=False)
    return text

def extract_text_from_pdf(file_path):
    """PDF 파일 텍스트 추출 시작."""
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_directory(directory_path):
    """디렉토리 내의 모든 파일에서 텍스트를 추출하고 txt 파일로 저장합니다."""
    if not os.path.exists(directory_path):
        print(f"디렉토리 '{directory_path}'가 존재하지 않습니다.")
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                text = extract_text_from_file(file_path)
                if text:
                    output_file = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"{filename}에서 텍스트를 추출하여 {output_file}에 저장했습니다.")
            except Exception as e:
                print(f"{filename} 처리 실패: {e}")

if __name__ == "__main__":
    input_directory = os.path.abspath('resources')
    print("파일 처리 중...")
    extract_text_from_directory(input_directory)
    print("처리 완료.")