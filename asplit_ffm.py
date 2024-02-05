import subprocess
import sys
import os
import glob

def get_audio_length(audio_file):
    """
    オーディオファイルの総再生時間を秒単位で取得する。
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_file],
        text=True, capture_output=True
    )
    duration = float(result.stdout)
    return duration

def generate_split_times(total_seconds, interval=120):
    """
    2分間隔で分割する時間点のリストを生成する。
    """
    times = []
    current_time = interval
    while current_time < total_seconds:
        times.append(current_time)
        current_time += interval
    return times

def split_audio_intervals(audio_file, interval=120):
    """
    audio_file: 分割するオーディオファイルのパス
    interval: 分割する時間間隔 (秒)
    """

    total_seconds = get_audio_length(audio_file)
    split_times = generate_split_times(total_seconds, interval)

    base_dir = os.path.dirname(audio_file)
    filename = os.path.splitext(audio_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp3')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 分割処理
    previous_time = "0"
    for i, split_time in enumerate(split_times, 1):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i:02d}.mp3')
        subprocess.run([
            "ffmpeg", 
            "-i", audio_file, 
            "-q:a", "0", "-map", "a", 
            "-ss", previous_time, 
            "-to", str(split_time),
            segment_file_path
        ])
        print(f"Segment {i} saved as {segment_file_path}")
        previous_time = str(split_time)

    # 最後のセグメント
    if previous_time != str(total_seconds):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i+1:02d}.mp3')
        subprocess.run([
            "ffmpeg", 
            "-i", audio_file, 
            "-q:a", "0", "-map", "a", 
            "-ss", previous_time, 
            segment_file_path
        ])
        print(f"Segment {i+1} saved as {segment_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file>")
        sys.exit(1)

    input_audio_file = sys.argv[1]

    split_audio_intervals(input_audio_file)
