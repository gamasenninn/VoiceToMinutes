import json
import pprint
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

def read_file(file_path):
    """Reads and returns the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def time_to_seconds(time_str):
    """Converts a time string to seconds."""
    #print(time_str)
    hours, minutes, seconds = map(float, time_str.replace(',', '.').split(':'))
    return hours * 3600 + minutes * 60 + seconds

def extract_segment(transcript_data, start_time, end_time):
    """Extracts and returns the text segment from the transcript that corresponds to the given start and end time."""
    extracted_segment = ""
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    for transcript in transcript_data.split("\n\n"):
        # Splitting the transcript into its components
        parts = transcript.split('\n')
        if len(parts) > 1:
            # Extracting the time range from the transcript
            time_range = parts[1]
            if ' --> ' in time_range:
                transcript_start_time, transcript_end_time = time_range.split(' --> ')
                transcript_start_seconds = time_to_seconds(transcript_start_time)
                transcript_end_seconds = time_to_seconds(transcript_end_time)
                
                # Check if the segment time overlaps with the transcript time
                if not (transcript_end_seconds < start_seconds or transcript_start_seconds > end_seconds):
                    extracted_segment += transcript + "\n\n"

    return extracted_segment
def process_files(time_file_path, transcript_file_path):
    """Processes the time file and transcript file to extract relevant segments."""
    # Reading files
    time_file_data = json.loads(read_file(time_file_path))
    transcript_file_data = read_file(transcript_file_path)

    # Extracting segments
    extracted_segments = []
    for segment in time_file_data["segments"]:
        start_time = segment["start_time"] 
        end_time = segment["end_time"] 
        extracted_text = extract_segment(transcript_file_data, start_time, end_time)
        extracted_segments.append(
            {
             "title": segment["title"], 
             "text": extracted_text,
             "start_time": segment["start_time"],
             "end_time": segment["end_time"]
            }
        )

    return extracted_segments

# コマンドライン引数の解析と説明
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='セグメントファイルから時間を抽出し、要約処理を行う。\n'
                    'OpenAIのGPTモデルを使用。',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'transcript_file',
        help='処理するトランスクリプトファイルのパス(SRT)。'
    )
    #parser.add_argument(
    #    '--nosum',
    #    action='store_true',
    #    help='このオプションを指定すると、要約処理をスキップします。'
    #)
    return parser.parse_args()

#要約処理（openai API）
def summarize_text(text):
   
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",  # gpt-3.5-turbo-1106からの変更
            #model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system",
                    "content": "議事録の下書きを作成してください。"
                                "議事録ですのでタイトルと内容をセットにして詳細にそれごとに複数書いてください"
                                "出力は純粋な配列のJSON形式でお願いします。" 
                                "{minutes:["
                                    "{"
                                        "title:タイトル（20文字以内で内容に最も適したタイトル）,\n" 
                                        "contents:[内容(具体的な詳細内容や決定事項、売上や買掛の数字などに注目して箇条書きにしてください)],\n" 
                                        "times:この議題の開始時間00:00:00-終了時間00:00:00\n" 

                                    "},"
                                "]}"
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


if __name__ == "__main__":
    args = parse_arguments()

    # Assuming the transcript file path is provided
    transcript_file_path = args.transcript_file

    # Removing the extension from the transcript file path and appending '_time.json'
    time_file_base = os.path.splitext(transcript_file_path)[0]
    time_file_path = f"{time_file_base}_time.json"

    # Check if the time file exists
    if not os.path.exists(time_file_path):
        print(f"Time file not found: {time_file_path}")
        sys.exit(1)
    # Process the files and get the extracted segments
    extracted_segments = process_files(time_file_path, args.transcript_file)

    for i, segment in enumerate(extracted_segments):
        #pprint.pprint(segment.get("text"))
        out_file_path = f"{time_file_base}_segment_{i:02d}.json"
        transcription = summarize_text(segment.get("text"))
        replaced_text = replace_words(transcription, replacement_dict)
        # 文字起こし結果をファイルに保存
        with open(out_file_path, "w", encoding="utf-8") as text_file:
            print(replaced_text)
            text_file.write(replaced_text)

        


