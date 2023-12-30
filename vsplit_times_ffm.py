import subprocess
import sys
import os
import glob

def split_video_times(video_file, split_times):
    """
    video_file: 分割するビデオファイルのパス
    split_times: 分割する時間点のリスト (形式: ["1:30:00", "3:50:05", ...])
    """

    base_dir = os.path.dirname(video_file)
    filename = os.path.splitext(video_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp4')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 分割処理
    previous_time = "0:0:0"
    for i, split_time in enumerate(split_times, 1):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i}.mp4')
        subprocess.run([
            "ffmpeg", 
            "-i", video_file, 
            "-c", "copy", 
            "-ss", previous_time, 
            "-to", split_time, 
            segment_file_path
        ])
        print(f"Segment {i} saved as {segment_file_path}")
        previous_time = split_time

if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) < 3:
        print("Usage: python script.py <video_file> <split_time1> [<split_time2> ...]")
        sys.exit(1)

    # コマンドライン引数からビデオファイル名と分割時間を取得
    input_video_file = sys.argv[1]
    split_times = sys.argv[2:]

    # ビデオファイルの分割
    split_video_times(input_video_file, split_times)
