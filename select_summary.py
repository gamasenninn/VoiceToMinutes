import glob
import os
import re
import sys
from dotenv import load_dotenv

def main(directory):
    load_dotenv()

    file_path = os.path.join(directory, "*_*.txt")
    file_list = glob.glob(file_path)

    #from_num = 47023
    #to_num = 47043

    #pattern = re.compile(r'sum_(\d+)\.txt')

    for file in file_list:
        with open(file, 'r', encoding='utf8') as f:
            content = f.read()
            print(f"file: {file}")
            print(f"summary:\n{content}")
            print("-----------------")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        main(directory)
    else:
        print("Please provide a directory as an argument.")
