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
        for root, dirs, files in os.walk(path):
            current_level = root.replace(path, "").count(os.sep)

            if root != path:
                print("    " * current_level + f"[DIR] {os.path.basename(root)}")

            for file in files:
                if ext_filter and not file.endswith(ext_filter):
                    continue

                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    print("    " * (current_level + 1) + f"[FILE] {file} ({size} bytes)")
                except (PermissionError, FileNotFoundError):
                    print("    " * (current_level + 1) + f"[FILE] {file} (НЕТ ДОСТУПА)")

    except PermissionError:
        print("Нет доступа к:", path)
        return


def collect_stats(path, ext_filter=None):
    file_count = 0
    dir_count = 0
    total_size = 0

    for root, dirs, files in os.walk(path):
        dir_count += len(dirs)

        for file in files:
            if ext_filter and not file.endswith(ext_filter):
                continue

            file_path = os.path.join(root, file)
            try:
                file_count += 1
                total_size += os.path.getsize(file_path)
            except (PermissionError, FileNotFoundError):
                continue

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