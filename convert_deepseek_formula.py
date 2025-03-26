#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re


def convert_deepseek_formula(filepath):
    # 定义替换规则
    replacements = {
        "[1mm]": "",
        "\\[": "\n$$",
        "\\]": "$$\n",
        "\\( ": " $",
        " \\)": "$ ",
        "\\(": " $",
        "\\)": "$ ",
        "** $": "**$",
        "$ **": "$**",
        "•": "-",
    }

    # 读取文件内容
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 执行替换
    for old, new in replacements.items():
        content = content.replace(old, new)

    # for every line of the content, remove any white space at the end of the line
    content = "\n".join([line.rstrip() for line in content.split("\n")])

    # 写回文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert DeepSeek output markdown formula"
    )
    parser.add_argument("file_path", nargs="+", type=str, help="Path to the file")
    args = parser.parse_args()

    for file_path in args.file_path:
        print(f"Processing {file_path}...")
        if not os.path.isfile(file_path):
            print(f"Error: {file_path} is not a file.")
            sys.exit(1)
        convert_deepseek_formula(file_path)
    print("Done!")
