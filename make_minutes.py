import sys
import glob
import os
import json
from dotenv import load_dotenv

load_dotenv()
REPLACEMENT_DICT  = os.environ["REPLACEMENT_DICT"]

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

def format_minute_item(item, replacement_dict):
    replaced_title = replace_words(item['title'], replacement_dict)

    # 'content' がリストの場合は結合して文字列にする
    if isinstance(item['contents'], list):
        content_str = '\n'.join(item['contents'])
    else:
        # 'content' がリストでない場合（例えば、文字列の場合）はそのまま使用
        content_str = item['contents']

    replaced_content = replace_words(content_str, replacement_dict)

    return "## {}:\n{}\n".format(replaced_title, replaced_content)


def make_minutes(dir_path):
    files = glob.glob(os.path.join(dir_path, "*.json"))
    output_file =  os.path.join(dir_path, "summary.txt")

    # 読み替え辞書をファイルから読み込む
    replacement_dict = load_replacement_dict(REPLACEMENT_DICT)

    # ファイルを最初に上書きモードで開き、空にする
    open(output_file, 'w', encoding='utf-8').close()

    # 各ファイルを読み込み、出力ファイルに追記
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_minutes = [format_minute_item(item, replacement_dict) for item in data['minutes']]                         

            # この時点でファイルを追記モードで開く
            with open(output_file, 'a', encoding='utf-8') as out_file:
                for minute in combined_minutes:
                    print(minute)
                    out_file.write(minute + "\n")
                   
if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        print("Usage: python make_minutes.py <video_dirpath>")
        sys.exit(1)

    # コマンドライン引数からビデオファイルのあるディレクトリを取得
    dir_path = sys.argv[1]

    # 
    make_minutes(dir_path)
