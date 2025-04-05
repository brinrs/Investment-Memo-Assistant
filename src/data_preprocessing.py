import os
import re
#import chardet
from bs4 import BeautifulSoup
from tqdm import tqdm

def extract_text_from_html(html_path):
    """
    Extracts text from a html file using BeautifulSoup.
    Args:
        pdf_path (str): Path to the html file.
    Returns:
        str: Extracted text from the html.
    """
    with open(html_path, 'r', encoding="Windows-1252") as file:
        soup = BeautifulSoup(file, "html.parser")
    text = soup.get_text("\n")
    return text

def simple_chunking(text, chunk_size=500):
    """
    Splits the text into chunks of specified size.
    Args:
        text (str): The text to be chunked.
        chunk_size (int): The size of each chunk.
    Returns:
        list: List of text chunks.
    """
    chunks = []
    start = 0
    total_steps = len(text) // chunk_size + 1
    with tqdm(total=total_steps, desc="Chunking text") as pbar:
        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                end = text.rfind(' ', start, end) 
                if end == -1:
                    end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end
            pbar.update(1)
    return chunks

def clean_text(text):
    """
    Cleans the text by removing extra spaces and newlines.
    Args:
        text (str): The text to be cleaned.
    Returns:
        str: Cleaned text.
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '<NEWLINE>', text)
    text = re.sub(r'[\t]+', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = text.replace('<NEWLINE>', '\n')
    text = text.replace('<NEWLINE>', '\n')
    return text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", 'data', 'TSLA_10k.html')

    #with open(file_path, "rb") as f:
        #raw_data = f.read()
        #result = chardet.detect(raw_data)
        #detected_encoding = result["encoding"]
        #print("Detected encoding:", detected_encoding)

    text = extract_text_from_html(file_path)

    if text:
        print("Extracted text length:", len(text))
    else:
        print("No text extracted. Please check the HTML file.")
    
    clean_text = clean_text(text)
    print("Cleaned text length:", len(clean_text))
    
    limited_text = clean_text[0:100000]
    print("Limited text length for testing", len(limited_text))

    chunks = simple_chunking(limited_text, 5000)
    print("Total chunks:", len(chunks))

    if chunks:
        print("First chunk preview:\n", chunks[1])
