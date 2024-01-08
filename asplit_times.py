import sys
from pydub import AudioSegment
import glob
import os

def split_audio_times(audio_file, split_times):
    """
    audio_file: 分割するオーディオファイルのパス
    split_times: 分割する時間点のリスト (形式: ["1:30:00", "3:50:05", ...])
    """

    def convert_to_ms(timestring):
        """ 時間文字列(HH:MM:SS)をミリ秒に変換 """
        hours, minutes, seconds = map(int, timestring.split(':'))
        return (hours * 3600 + minutes * 60 + seconds) * 1000

    # 元のファイルのディレクトリを取得
    base_dir = os.path.dirname(audio_file)
    filename = os.path.splitext(audio_file)[0]

    # 同じディレクトリ内の既存の分割ファイルを削除する
    for file in glob.glob(os.path.join(base_dir, f'{filename}_segment*.mp3')):
        os.remove(file)
        print(f"Deleted existing file: {file}")

    # 音声ファイルの読み込み
    audio = AudioSegment.from_file(audio_file)

    # 分割時間点をミリ秒に変換
    split_points_ms = [convert_to_ms(time) for time in split_times]
    split_points_ms.append(len(audio))  # 最後の部分を含むために追加

    # オーディオの分割
    start_ms = 0
    for i, end_ms in enumerate(split_points_ms):
        segment = audio[start_ms:end_ms]
        segment_file_path = os.path.join(base_dir, f'{filename}_segment_{i+1:02d}.mp3')  # 保存するファイル名
        segment.export(segment_file_path, format="mp3")
        print(f"Segment {i+1} saved as {segment_file_path}")
        start_ms = end_ms  # 次のセグメントの開始点を更新

if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) < 3:
        print("Usage: python asplit_times.py <audio_file> <split_time1> [<split_time2> ...]")
        sys.exit(1)

    # コマンドライン引数から音声ファイル名と分割時間を取得
    input_audio_file = sys.argv[1]
    split_times = sys.argv[2:]

    # 音声ファイルの分割
    split_audio_times(input_audio_file, split_times)
