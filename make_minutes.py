import sys
import glob
import os
import json



def make_minutes(dir_path):
    files = glob.glob(os.path.join(dir_path, "*.json"))
    output_file =  os.path.join(dir_path, "summary.txt")

    # ファイルを最初に上書きモードで開き、空にする
    open(output_file, 'w', encoding='utf-8').close()

    # 各ファイルを読み込み、出力ファイルに追記
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_minutes = ["## {}:\n {}\n".format(item['title'], item['content']) for item in data['minutes']]
            
            # この時点でファイルを追記モードで開く
            with open(output_file, 'a', encoding='utf-8') as out_file:
                for minute in combined_minutes:
                    print(minute)
                    out_file.write(minute + "\n")
                      



if __name__ == "__main__":
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        print("Usage: python make_minutes.py <video_dirpath>")
        sys.exit(1)

    # コマンドライン引数からビデオファイルのあるディレクトリを取得
    dir_path = sys.argv[1]

    # 

    make_minutes(dir_path)
