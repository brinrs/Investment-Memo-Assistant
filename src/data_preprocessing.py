import os
import chardet
from bs4 import BeautifulSoup

def extract_text_from_html(html_path):
    """
    Extracts text from a html file using BeautifulSoup.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text from the PDF.
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
    return chunks

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

    #chunks = simple_chunking()

