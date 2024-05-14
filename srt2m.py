import sys
import os
import subprocess

def main():
    # コマンドライン引数を確認
    if len(sys.argv) < 2:
        print("パラメータが指定されていません。")
        sys.exit(1)

    fullpath = sys.argv[1]
    path, filename_with_ext = os.path.split(fullpath)
    filename, extension = os.path.splitext(filename_with_ext)

    # 結果を表示
    print(f"fullpath: {fullpath}")
    print(f"path: {path}")
    print(f"filename: {filename}")
    print(f"ext: {extension}")

    # 新しいファイル名の生成
    path_filename_mp3 = os.path.join(path, f"{filename}.mp3")
    path_filename_srt = os.path.join(path, f"{filename}.srt")
    print(f"path_filname_mp3: {path_filename_mp3}")
    print(f"path_filname_srt: {path_filename_srt}")

    # 各種スクリプトを実行
    #print("----- MP4からMP3に変換 ---------")
    #run_script('mp42mp3.py', fullpath)

    #print("----- 文字起こしをしてSRT形式のテキストに変換 ---------")
    #run_script('tran_gladia.py', path_filename_mp3)

    print("----- セグメントのシナリオを作成する ---------")
    run_script('srt2seg.py', path_filename_srt)

    print("----- セグメントから議事録を起こす---------")
    run_script('seg2txt.py', path_filename_srt)

    print("----- 議事録とyouubeキャプチャーを作成する ---------")
    run_script('make_minutes.py', path)

def run_script(script_name, argument):
    # スクリプトを実行
    try:
        subprocess.run(['python', script_name, argument], check=True)
    except subprocess.CalledProcessError as e:
        print(f"スクリプトの実行に失敗しました: {script_name}")
        print(e)

if __name__ == "__main__":
    main()
