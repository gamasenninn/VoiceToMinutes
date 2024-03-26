import sys
import glob
import os
import json
from dotenv import load_dotenv
from replace_text import load_replacement_dict,replace_words
import re

load_dotenv()
REPLACEMENT_DICT  = os.environ["REPLACEMENT_DICT"]
title = "議事録（AI自動起草）\n"

def remove_decimal_from_time(time_data):
    """Remove the decimal part from the given time data."""
    # Splitting the time data on '-'
    start_time, end_time = time_data.split('-')

    # Removing the decimal part
    start_time = start_time.split('.')[0]
    end_time = end_time.split('.')[0]

    # Rejoining the time data
    formatted_time_data = f"{start_time}-{end_time}"
    return formatted_time_data

def format_minute_item(item, replacement_dict):
    replaced_title = replace_words(item['title'], replacement_dict)
    #time_str = item['times']
    time_str = remove_decimal_from_time(item['times'])

    # 'content' がリストの場合は結合して文字列にする
    if isinstance(item['contents'], list):
        content_str = ' - ' + '\n - '.join(item['contents'])
    else:
        # 'content' がリストでない場合（例えば、文字列の場合）はそのまま使用
        content_str = '- '+item['contents']

    content_str += f"\n【問題点】{item['problem']}" if item.get('problem') else ""
    content_str += f"\n【TODO】{item['todo']}" if item.get('todo') else ""

    replaced_content = replace_words(content_str, replacement_dict)

    return "## {}:\n[{}]\n【議事】\n{}\n".format(replaced_title, time_str,replaced_content)


def format_youtube_description(item, replacement_dict):
    replaced_title = replace_words(item['title'], replacement_dict)
    #time_str = item['times']
    time_str = remove_decimal_from_time(item['times'])

    # 'content' がリストの場合は結合して文字列にする
    if isinstance(item['contents'], list):
        content_str = ' - ' + '\n - '.join(item['contents'])
    else:
        # 'content' がリストでない場合（例えば、文字列の場合）はそのまま使用
        content_str = '- '+item['contents']

    content_str += f"\n【問題点】{item['problem']}" if item.get('problem') else ""
    content_str += f"\n【TODO】{item['todo']}" if item.get('todo') else ""

    replaced_content = replace_words(content_str, replacement_dict)

    return "{}: {}\n".format(time_str,replaced_title )


def make_minutes(dir_path):
    files = glob.glob(os.path.join(dir_path, "*_segment_*.json"))
        # ファイル名でリストを並べ替え
    files = sorted(files)
    output_file =  os.path.join(dir_path, "summary.txt")

    # 読み替え辞書をファイルから読み込む
    replacement_dict = load_replacement_dict(REPLACEMENT_DICT)

  # 正規表現で日付部分を抽出（yyyy_mm_dd形式）
    match = re.search(r'(\d{4})_(\d{2})_(\d{2})', dir_path)
    if match:
        year, month, day = match.groups()
        formatted_date = f"{year}年{int(month)}月{int(day)}日"
        print(formatted_date)
    else:
        print("日付形式が見つかりません。")  
        return False

    # ファイルを最初に上書きモードで開き、空にする
    open(output_file, 'w', encoding='utf-8').close()

    # 各ファイルを読み込み、出力ファイルに追記
    for i,file in enumerate(files):
        print(file)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_minutes = [format_minute_item(item, replacement_dict) for item in data['minutes']]                         

            # この時点でファイルを追記モードで開く
            with open(output_file, 'a', encoding='utf-8') as out_file:
                if i==0:
                    out_file.write(f"# {formatted_date} {title} \n")    
                for minute in combined_minutes:
                    print(i,minute)
                    out_file.write(minute + "\n")
    return True

def make_youtube_description(dir_path):
    files = glob.glob(os.path.join(dir_path, "*_segment_*.json"))
        # ファイル名でリストを並べ替え
    files = sorted(files)
    output_file =  os.path.join(dir_path, "summary_youtube.txt")

    # 読み替え辞書をファイルから読み込む
    replacement_dict = load_replacement_dict(REPLACEMENT_DICT)

  # 正規表現で日付部分を抽出（yyyy_mm_dd形式）
    match = re.search(r'(\d{4})_(\d{2})_(\d{2})', dir_path)
    if match:
        year, month, day = match.groups()
        formatted_date = f"{year}年{int(month)}月{int(day)}日"
        print(formatted_date)
    else:
        print("日付形式が見つかりません。")  
        return False

    # ファイルを最初に上書きモードで開き、空にする
    open(output_file, 'w', encoding='utf-8').close()

    # 各ファイルを読み込み、出力ファイルに追記
    for i,file in enumerate(files):
        print(file)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_minutes = [format_youtube_description(item, replacement_dict) for item in data['minutes']]                         

            # この時点でファイルを追記モードで開く
            with open(output_file, 'a', encoding='utf-8') as out_file:
                if i==0:
                    out_file.write(f"# {formatted_date} {title} \n")    
                for minute in combined_minutes:
                    print(i,minute)
                    out_file.write(minute + "\n")
    return True


if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        print("Usage: python make_minutes.py <video_dirpath>")
        sys.exit(1)

    # コマンドライン引数からビデオファイルのあるディレクトリを取得
    dir_path = sys.argv[1]

    # 
    if make_minutes(dir_path):
        print("議事録を作成しました。")

    if make_youtube_description(dir_path):
        print("youtube概要欄を作成しました。")
