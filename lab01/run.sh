if [ $# -eq 0 ]; then
    echo "Usage: $0 <file_path1> [file_path2] ..." >&2
    exit 1
fi

file_paths=("$@")

python3 word_counter.py "${file_paths[@]}"