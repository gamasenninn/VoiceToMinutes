import subprocess
import sys
import os
import glob
import argparse

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

def generate_split_times(total_seconds, interval, overlap):
    """
    指定された間隔と重複時間を考慮して分割する時間点のリストを生成する。
    """
    times = []
    current_time = 0
    while current_time < total_seconds:
        start_time = max(0, current_time - overlap)
        end_time = min(current_time + interval, total_seconds)
        times.append((start_time, end_time))
        current_time += interval
    return times

def split_audio_intervals(audio_file, interval, overlap):
    """
    audio_file: 分割するオーディオファイルのパス
    interval: 分割する時間間隔 (秒)
    overlap: 各セグメント間の重複する時間 (秒)
    """

    total_seconds = get_audio_length(audio_file)
    split_times = generate_split_times(total_seconds, interval, overlap)

    base_dir = os.path.dirname(audio_file)
    filename = os.path.splitext(audio_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp3')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 分割処理
    for i, (start_time, end_time) in enumerate(split_times, 1):
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i:02d}.mp3')
        subprocess.run([
            "ffmpeg", 
            "-i", audio_file, 
            "-q:a", "0", "-map", "a", 
            "-ss", str(start_time), 
            "-to", str(end_time),
            segment_file_path
        ])
        print(f"Segment {i} saved as {segment_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split an audio file into intervals with overlap.')
    parser.add_argument('audio_file', type=str, help='The audio file to split.')
    parser.add_argument('--sptime', type=float, default=2.0, help='Duration of each segment in minutes (can be a decimal).')
    parser.add_argument('--overlap', type=float, default=5.0, help='Overlap duration in seconds between segments.')
    args = parser.parse_args()

    interval_seconds = args.sptime * 60  # 分を秒に変換
    overlap_seconds = args.overlap  # 重複する秒数
    split_audio_intervals(args.audio_file, interval_seconds, overlap_seconds)
