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
            model="gpt-3.5-turbo-0125",  # gpt-3.5-turbo-1106からの変更
            #model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": "次の記録から議事録を起こしていきます。"
                                "議事の流れの中で、内容的に区切れる部分を探し、連続した時間で20程度のパートに分割してください。記録を最後まで全部読んで最後の議事の最終時間になるまで出力してください。"
                                "出力は下記のような配列としての純粋なJSON形式でお願いします。" 
                                "{segments=[{"
                                    "title:タイトル（20文字以内で内容に最も適したタイトル）," 
                                    "start_time:この議題の開始時間(00:00:00)," 
                                    "end_time:この議題の終了時間(00:00:00)" 
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
        description='SRTファイルからタイトルと時間を抽出する。\n'
                    'OpenAIのGPTモデルを使用。',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'file',
        help='処理するSRTファイルのパス\n'
             'ワイルドカード（*）を使用して複数のファイルを一括で処理できます。'
    )
    #parser.add_argument(
    #    '--nosum',
    #    action='store_true',
    #    help='このオプションを指定すると、要約処理をスキップします。'
    #)
    return parser.parse_args()

def read_srt_from_file(file_path):

    # ファイルから文字起こしテキストを読み込む
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def save_to_file(transcription, original_file_path):
    # 元のファイル名から拡張子を除外し、新しいファイル名を作成
    base_name = os.path.splitext(original_file_path)[0]
    new_file_path = f"{base_name}_time.json"

    # 文字起こし結果をファイルに保存
    with open(new_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(transcription)

if __name__ == "__main__":
    args = parse_arguments()

    # コマンドライン引数からファイル名と要約スキップフラグを取得
    filename = args.file
    skip_summary = args.nosum

    srt_text = read_srt_from_file(filename)
    part = make_part(srt_text)
    print(part)
    save_to_file(part,filename)