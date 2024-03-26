import os
from dotenv import load_dotenv
import argparse
from replace_text import load_replacement_dict,replace_words
import requests
import json
import time
import sys

# OpenAI APIキーを設定
load_dotenv()
galadia_api_key = os.environ["GLADIA_API_KEY"]
replacement_dict_path = os.environ.get("REPLACEMENT_DICT")
replacement_dict = load_replacement_dict(replacement_dict_path)



# コマンドライン引数の解析と説明
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='音声ファイルをテキストに文字起こしし、要約するスクリプト。\n'
                    'OpenAIのWhisperとGPTモデルを使用。',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'file',
        help='処理する音声ファイルのパス(mp3)。\n'
             'ワイルドカード（*）を使用して複数のファイルを一括で処理できます。'
    )
    parser.add_argument(
        '--nosum',
        action='store_true',
        help='このオプションを指定すると、要約処理をスキップします。'
    )
    return parser.parse_args()

def upload_file(file_path):
    url = "https://api.gladia.io/v2/upload"
    headers = {'x-gladia-key': galadia_api_key}

    with open(file_path, 'rb') as file:
        files = [('audio', (os.path.basename(file_path), file, 'audio/mpeg'))]
        response = requests.request("POST", url, headers=headers, files=files)

        if response.ok:
            return response.text
        else:
            return f"Error: {response.status_code} {response.reason}"

def stt(yt_link, fmt='json'):
    st = time.time()

    headers = {
        'accept': 'application/json',
        'x-gladia-key': galadia_api_key,
    }

    data = {
            "audio_url": yt_link,
            "translation": True,
            "translation_config": {
                "model": "base",
                "target_languages": ["jp", "en"]
            },
            "subtitles": True,
            "subtitles_config": {
                "formats": ["srt"]
            },
            "language": "jp",
            "detect_language": False,
            "enable_code_switching": False,
            "diarization": False
        }

    response = requests.post(
        'https://api.gladia.io/v2/transcription/', 
        headers=headers, 
        json=data)

    et = time.time()
    elapsed_time = et - st


    res_dict =  json.loads(response.text)
    result_url = res_dict['result_url']
    print("id:",res_dict['id'])
    print("result_url:",result_url)


    for i in range(60):
        time.sleep(2)
        response = requests.get(
            result_url, 
            headers=headers) 

        res_dict =  json.loads(response.text)
        print("status=",res_dict['status'],i)
        if res_dict['status'] == 'done':
            break

    # Save the response to a file
    with open('response.json', 'w',encoding='utf8') as f:
        f.write(response.text)

    return response, elapsed_time


if __name__ == "__main__":
    args = parse_arguments()

    # コマンドライン引数からファイル名と要約スキップフラグを取得
    filename = args.file

    #print("文字起こしを開始します・・・・・\n")
    print(filename)
    response = upload_file(filename)
    res_dict =  json.loads(response)
    result_url = res_dict['audio_url']

    response,tt = stt(result_url)  

    res_dict = json.loads(response.text)


    # srt字幕データを探します。
    subtitles = res_dict.get('result', {}).get('transcription', {}).get('subtitles', [])

    # srtフォーマットの字幕を見つけます。
    srt_subtitles = [subtitle['subtitles'] for subtitle in subtitles if subtitle['format'] == 'srt']

    # 最初のsrt字幕を取得します（複数ある場合）。
    first_srt_subtitle = srt_subtitles[0] if srt_subtitles else None

    # first_srt_subtitle には、必要なsrtデータが含まれています。
    # 文字起こし結果をファイルに保存
    out_file_name, _ = os.path.splitext(filename)
    out_file_name += ".srt"
    with open(out_file_name, "w", encoding="utf-8") as text_file:
        if first_srt_subtitle:
            for subtitle in first_srt_subtitle:
                # \nを実際の改行に置き換え
                subtitle = subtitle.replace("\\n", "\n")
                subtitle = replace_words(subtitle, replacement_dict)
                text_file.write(subtitle)



