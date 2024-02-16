import sys
import glob
import os
from dotenv import load_dotenv

def load_replacement_dict(file_path):
    replacement_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                replacement_dict[parts[0]] = parts[1]
    return replacement_dict

def replace_words(text, replacement_dict):
    for word, replacement in replacement_dict.items():
        text = text.replace(word, replacement)
    return text

def process_files(dir_path, replacement_dict):
    files = glob.glob(os.path.join(dir_path, "*.txt"))
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        text = replace_words(text, replacement_dict)

        # 元のファイル名から拡張子を除外し、'_rep.txt' を追加して新しいファイル名を作成
        base_name, _ = os.path.splitext(file_path)
        new_file_path = base_name + '_rep.txt'
        
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python replace_text.py <dir_path>")
        sys.exit(1)

    dir_path = sys.argv[1]

    # 環境変数をロード
    load_dotenv()
    replacement_dict_path = os.environ.get("REPLACEMENT_DICT")
    if not replacement_dict_path:
        print("Error: The REPLACEMENT_DICT environment variable is not set.")
        sys.exit(1)

    replacement_dict = load_replacement_dict(replacement_dict_path)
    process_files(dir_path, replacement_dict)