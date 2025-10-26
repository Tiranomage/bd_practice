import sys
import re
from collections import Counter

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='cp1251') as f:
            content = f.read()
        return content
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            print(f"Файл {file_path} прочитан в utf-8-sig (возможно, был BOM).", file=sys.stderr)
            return content
        except UnicodeDecodeError:
            pass

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Файл {file_path} прочитан в utf-8.", file=sys.stderr)
            return content
        except UnicodeDecodeError:
            pass 
        print(f"Ошибка декодирования файла {file_path} (cp1251, utf-8-sig, utf-8).", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла {file_path}: {e}", file=sys.stderr)
        return ""

def extract_words(text):
    words = re.findall(r'\b[а-яёa-z]+\b', text, re.IGNORECASE)
    words = [word.lower() for word in words]
    words = [word for word in words if len(word) >= 4]
    return words

def count_words(file_paths):
    total_counter = Counter()
    for file_path in file_paths:
        content = read_file_content(file_path)
        if content:
            words = extract_words(content)
            total_counter.update(words)
    return total_counter

def filter_and_sort(counter):
    filtered_items = [(word, count) for word, count in counter.items() if count >= 10]
    sorted_items = sorted(filtered_items, key=lambda item: (-item[1], item[0]))
    return sorted_items

def print_results(sorted_items):
    for word, count in sorted_items:
        print(f"{word} - {count}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python word_counter.py <file_path1> [file_path2] ...", file=sys.stderr)
        sys.exit(1)

    file_paths = sys.argv[1:]
    counter = count_words(file_paths)
    sorted_items = filter_and_sort(counter)
    print_results(sorted_items)

if __name__ == "__main__":
    main()