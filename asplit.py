import sys
import argparse
from pydub import AudioSegment
import glob
import os

def split_audio(audio_file, segment_duration_min):

    # 分をミリ秒に変換
    segment_duration_ms = int(segment_duration_min * 60 * 1000)

    # 元のファイルのディレクトリを取得
    base_dir = os.path.dirname(audio_file)
    filename = os.path.splitext(audio_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp3')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 音声ファイルの読み込み
    audio = AudioSegment.from_file(audio_file)

    # 重複する持続時間（例：5秒 = 5000ミリ秒）
    overlap_duration_ms = 5000

    # オーディオの全長（ミリ秒）
    original_audio_length_ms = len(audio)

    # 重複を含むセグメントでオーディオを分割
    overlapping_segments = []

    for start_ms in range(0, original_audio_length_ms, segment_duration_ms):
        end_ms = start_ms + segment_duration_ms
        # 前のセグメントからの重複を含めるために開始時間を調整
        start_with_overlap = max(0, start_ms - overlap_duration_ms)
        # 最後のセグメントがオーディオの長さを超えないようにする
        end_ms = min(end_ms, original_audio_length_ms)
        
        # 重複を含むセグメントを抽出
        segment = audio[start_with_overlap:end_ms]
        overlapping_segments.append(segment)

    # 重複セグメントをファイルに保存
    for i, segment in enumerate(overlapping_segments):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i+1:02d}.mp3')  # 保存するファイル名
        segment.export(segment_file_path, format="mp3")
        print(f"Segment {i+1} saved as {segment_file_path}")

if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='Split an audio file into segments.')
    parser.add_argument('audio_file', type=str, help='The audio file to split.')
    parser.add_argument('--sptime', type=float, default=2, help='Duration of each segment in minutes (can be a decimal).')
    args = parser.parse_args()

    # 音声ファイルの分割
    split_audio(args.audio_file, args.sptime)
