import glob
import os
import sys

def parse_time(time_str):
    """ 時間文字列を秒に変換する """
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

def format_time(seconds):
    """ 秒を時間文字列に変換する """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

def main(directory):
    file_path = os.path.join(directory, "*_*.txt")
    file_list = sorted(glob.glob(file_path))

    accumulated_time = 0

    for file in file_list:
        updated_content = []
        with open(file, 'r', encoding='utf8') as f:
            content = f.read()
            segments = content.split("\n\n")[1:]  # ヘッダを除外

            for segment in segments:
                parts = segment.split('\n', 1)
                if len(parts) < 2:
                    continue  # 時間とテキストの両方がない場合は無視

                times, text = parts
                start_time, end_time = times.split(' --> ')
                start_time = parse_time(start_time) + accumulated_time
                end_time = parse_time(end_time) + accumulated_time
                updated_content.append(f"{format_time(start_time)} --> {format_time(end_time)}\n{text}")

                accumulated_time = end_time  # ここを変更

        print(f"file: {file}")
        print("summary:")
        print("\n\n".join(updated_content))
        print("-----------------")

if __name__ == '__main__':
    directory = '/path/to/your/directory'  # ディレクトリを指定
    main(directory)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        main(directory)
    else:
        print("Please provide a directory as an argument.")
