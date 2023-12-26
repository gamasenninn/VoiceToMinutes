import subprocess
import sys
import os

def convert_mp4_to_mp3(mp4_file):
    base_name = os.path.splitext(mp4_file)[0]
    mp3_file = base_name + ".mp3"
    subprocess.run(["ffmpeg", "-i", mp4_file, "-q:a", "0", "-map", "a", mp3_file])
    print(f"Converted {mp4_file} to {mp3_file}")

if __name__ == "__main__":
    # コマンドライン引数から入力ファイル名を取得
    if len(sys.argv) < 2:
        print("Usage: python mp43mp3.py <input.mp4>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_mp4_to_mp3(input_file)
