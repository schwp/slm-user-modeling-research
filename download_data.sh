#!/bin/bash

URL="https://huggingface.co/datasets/barilan/blog_authorship_corpus/resolve/main/data/blogs.zip"
ZIP_FILE="data/blogs.zip"

echo "Downloading the data ..."
curl -L "$URL" -o "$ZIP_FILE"

echo "Unzipping files ..."
unzip -q "$ZIP_FILE" -d data/

echo "Cleaning & formating the data "
python3 format_data.py
rm -rf "$ZIP_FILE" data/blogs
