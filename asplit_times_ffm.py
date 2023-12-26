import subprocess
import sys
import os
import glob

def split_audio_times(audio_file, split_times):
    """
    audio_file: 分割するオーディオファイルのパス
    split_times: 分割する時間点のリスト (形式: ["1:30:00", "3:50:05", ...])
    """

    base_dir = os.path.dirname(audio_file)
    filename = os.path.splitext(audio_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp3')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 分割処理
    previous_time = "0:0:0"
    for i, split_time in enumerate(split_times, 1):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i}.mp3')
        #subprocess.run(["ffmpeg", "-i", audio_file, "-map", "0:a:0","-ss", previous_time, "-to", split_time, "-c", "copy", 
        # segment_file_path])
        subprocess.run([
            "ffmpeg", 
            "-i", audio_file, 
            "-q:a", "0", "-map", "a", 
            "-ss", previous_time, 
            "-to", split_time,
            segment_file_path
        ])
        print(f"Segment {i} saved as {segment_file_path}")
        previous_time = split_time

if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) < 3:
        print("Usage: python script.py <audio_file> <split_time1> [<split_time2> ...]")
        sys.exit(1)

    # コマンドライン引数から音声ファイル名と分割時間を取得
    input_audio_file = sys.argv[1]
    split_times = sys.argv[2:]

    # 音声ファイルの分割
    split_audio_times(input_audio_file, split_times)
