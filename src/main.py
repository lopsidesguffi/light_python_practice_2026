import os
import sys

def print_help():
    print("""
Использование:
    python main.py <путь> [расширение]

Примеры:
    python main.py test_data
    python main.py test_data .py
""")

def walk_directory(path, level=0, ext_filter=None):
    try:
        items = os.listdir(path)
    except PermissionError:
        print("Нет доступа к:", path)
        return

    for item in items:
        full_path = os.path.join(path, item)

        if os.path.isdir(full_path):
            print("    " * level + f"[DIR] {item}")
            walk_directory(full_path, level + 1, ext_filter)

        else:
            if ext_filter and not item.endswith(ext_filter):
                continue

            size = os.path.getsize(full_path)
            print("    " * level + f"[FILE] {item} ({size} bytes)")

def collect_stats(path, ext_filter=None):
    file_count = 0
    dir_count = 0
    total_size = 0

    def recursive_stats(current_path, level=0):
        nonlocal file_count, dir_count, total_size
        try:
            items = os.listdir(current_path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            if os.path.isdir(full_path):
                dir_count += 1
                recursive_stats(full_path, level + 1)
            else:
                if ext_filter and not item.endswith(ext_filter):
                    continue
                try:
                    size = os.path.getsize(full_path)
                    file_count += 1
                    total_size += size
                except (PermissionError, FileNotFoundError):
                    continue

    recursive_stats(path)
    return file_count, dir_count, total_size

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    path = sys.argv[1]
    ext_filter = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(path):
        print("Ошибка: путь не существует")
        return

    if not os.path.isdir(path):
        print("Ошибка: это не папка")
        return

    print(f"\nСКАНИРОВАНИЕ: {path}\n")

    walk_directory(path, 0, ext_filter)

    file_count, dir_count, total_size = collect_stats(path, ext_filter)

    print("\nОТЧЕТ")
    print(f"Файлов: {file_count}")
    print(f"Папок: {dir_count}")
    print(f"Общий размер: {total_size} байт")

if __name__ == "__main__":
    main()