import sys
from pydub import AudioSegment
import glob
import os

def split_audio(audio_file):

    # 元のファイルのディレクトリを取得
    base_dir = os.path.dirname(audio_file)

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for filename in glob.glob(os.path.join(base_dir, 'overlapping_segment*.mp3')):
        os.remove(filename)
        print(f"Deleted existing file: {filename}")

    # 音声ファイルの読み込み
    audio = AudioSegment.from_file(audio_file)

    # 各セグメントの持続時間（1分 = 60,000ミリ秒）
    #segment_duration_ms = 60000
    segment_duration_ms = 10*60000

    # 重複する持続時間（例：5秒 = 5000ミリ秒）
    overlap_duration_ms = 5000

    # オーディオの全長（ミリ秒）
    original_audio_length_ms = len(audio)

    # 重複を含む1分間隔でオーディオを分割
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
        segment_file_path = os.path.join(base_dir, f'overlapping_segment_{i+1}.mp3')  # 保存するファイル名
        segment.export(segment_file_path, format="mp3")
        print(f"Segment {i+1} saved as {segment_file_path}")

if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio_file>")
        sys.exit(1)

    # コマンドライン引数から音声ファイル名を取得
    input_audio_file = sys.argv[1]

    # 音声ファイルの分割

    split_audio(input_audio_file)
