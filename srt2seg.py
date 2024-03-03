import openai
import sys
import os
from dotenv import load_dotenv
import glob
import argparse
from replace_text import load_replacement_dict,replace_words

# OpenAI APIキーを設定
load_dotenv()
openai.api_key = os.environ["OPEN_API_KEY"]
replacement_dict_path = os.environ.get("REPLACEMENT_DICT")
replacement_dict = load_replacement_dict(replacement_dict_path)

#要約処理（openai API）
def make_part(text):
 

    response = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo-0125",  # gpt-3.5-turbo-1106からの変更
            model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": "次の記録から議事録を起こしていきます。"
                                "議事の流れの中で、内容的に区切れる部分を探し、10以上のパートを作りたいです。"
                                "出力は純粋な配列のJSON形式でお願いします。" 
                                "{segments=[{"
                                    "title:タイトル（20文字以内で内容に最も適したタイトル）," 
                                    "contents:[内容(具体的な詳細内容や決定事項、売上や買掛の数字などに注目して箇条書きにしてください)]," 
                                    "start_times:この議題の開始時間00:00:00" 
                                    "start_times:この議題の終了時間00:00:00," 
                                "},]}"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
        )
    # 要約されたテキストを取得
    new_summary = response.choices[0].message.content.strip()

    return new_summary



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

def read_srt_from_file(file_path):

    # ファイルから文字起こしテキストを読み込む
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    args = parse_arguments()

    # コマンドライン引数からファイル名と要約スキップフラグを取得
    filename = args.file
    skip_summary = args.nosum

    srt_text = read_srt_from_file(filename)
    part = make_part(srt_text)
    print(part)