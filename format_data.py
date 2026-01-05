import os
import csv
import re
from tqdm import tqdm
from datetime import datetime


SOURCE_DIR = "data/blogs/"
OUTPUT_FILE = "data/blog_authorship_corpus.csv"


def format_date(date_str):
    try:
        date_str = date_str.strip()
        dt = datetime.strptime(date_str, "%d,%B,%Y")
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return date_str


def clean_blog_text(text):
    text = re.sub(r'urlLink', '', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_blogs():
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.xml')]

    columns = ['id', 'gender', 'age', 'topic', 'sign', 'date', 'text']
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for filename in tqdm(files):
            parts = filename.replace('.xml', '').split('.')
            if len(parts) < 5: continue
            
            meta = {
                'id': parts[0], 'gender': parts[1], 'age': parts[2],
                'topic': parts[3], 'sign': parts[4]
            }

            try:
                with open(os.path.join(SOURCE_DIR, filename), 'r', encoding='latin-1') as f:
                    content = f.read()

                items = re.findall(r'<date>(.*?)</date>\s*<post>(.*?)</post>', content, re.DOTALL)

                for raw_date, raw_text in items:
                    writer.writerow({
                        **meta,
                        'date': format_date(raw_date),
                        'text': clean_blog_text(raw_text)
                    })
            except Exception:
                continue


if __name__ == "__main__":
    process_blogs()
