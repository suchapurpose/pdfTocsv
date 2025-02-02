import PyPDF2
import re
import csv
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    return text

def clean_term(term):
    return re.sub(r'\s*-\s*', '-', term)

def create_glossary(text):
    glossary = {}
    lines = text.split('\n')
    
    for line in lines:
        # Split the line into words
        words = re.findall(r'\S+(?:-\S+)*', line.strip())
        if len(words) >= 2:
            # Find the index of the first Chinese character
            chinese_start = next((i for i, word in enumerate(words) if re.search(r'[\u4e00-\u9fff]', word)), None)
            
            if chinese_start is not None:
                english_term = clean_term(' '.join(words[:chinese_start]))
                chinese_term = ' '.join(words[chinese_start:])
                chinese_term = re.sub(r'\s*\d+$', '', chinese_term)
                glossary[english_term] = chinese_term
    
    return glossary

def save_glossary_to_csv(glossary, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['English Term', 'Chinese Term'])
        for english_term, chinese_term in glossary.items():
            writer.writerow([english_term, chinese_term])

def find_pdf(directory):
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            return os.path.join(directory, file)
    return None

pdf_dir = 'pdf2csv/static/'
pdf_path = find_pdf(pdf_dir)

if pdf_path:
    extracted_text = extract_text_from_pdf(pdf_path)
    glossary = create_glossary(extracted_text)

    #Save the glossary to a CSV file
    csv_path = os.path.splitext(pdf_path)[0] + '.csv'
    save_glossary_to_csv(glossary, csv_path)
else:
    print('No PDF file found in the directory')