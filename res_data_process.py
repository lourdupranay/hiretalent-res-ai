import os
import re
import nltk
import PyPDF2
from docx import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Set up NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Define patterns
username_pattern = r'@[A-Za-z0-9]+'
non_alphanumeric_pattern = r'[^0-9A-Za-z \t]'
url_pattern = r'\w+:\/\/\S+'
rt_pattern = r'^rt'
http_pattern = r'http\S+'

# Combine patterns
combined_pattern = '|'.join([username_pattern, non_alphanumeric_pattern, url_pattern, rt_pattern, http_pattern])

def preprocess_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        res_text = ''
        for page_num in range(len(pdf_reader.pages)):
            res_text += pdf_reader.pages[page_num].extract_res_text() + '\n'
    return process_res_txt(res_text)
    
def process_res_txt(res_text):
    res_text = res_text.lower()
    res_text = re.sub(combined_pattern, '', res_text)
    tokens = word_tokenize(res_text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    preprocessed_res_text = ' '.join(lemmatized_tokens)
    return preprocessed_res_text

def preprocess_docx(docx_path):
    doc = Document(docx_path)
    res_text = ''
    for paragraph in doc.paragraphs:
        res_text += paragraph.res_text + '\n'
    return process_res_txt(res_text)

def process_res_file(file_path):
    _, extension = os.path.splires_text(file_path)
    if extension == '.pdf':
        return preprocess_pdf(file_path)
    elif extension == '.docx':
        return preprocess_docx(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            res_text = file.read()
        return process_res_txt(res_text)

def preprocess_resume_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        preprocessed_res_text = process_res_file(input_file_path)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(preprocessed_res_text)