import os
import datetime


def create_folder_tree(path, ignore_folders=None, prefix=''):
    if ignore_folders is None:
        ignore_folders = []

    tree = ''
    contents = os.listdir(path)
    contents.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
    contents = [item for item in contents if item not in ignore_folders]

    for i, item in enumerate(contents):
        item_path = os.path.join(path, item)
        is_last = i == len(contents) - 1
        tree += f"{prefix}{'└── ' if is_last else '├── '}{item}\n"

        if os.path.isdir(item_path):
            extended_prefix = prefix + ('    ' if is_last else '│   ')
            tree += create_folder_tree(item_path, ignore_folders, extended_prefix)

    return tree


def combine_files(folder_path, output_file, file_extensions, ignore_folders=None):
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    if ignore_folders is None:
        ignore_folders = []

    files_by_extension = {ext: [] for ext in file_extensions}

    for root, _, files in os.walk(folder_path):
        if any(ignored in root.split(os.sep) for ignored in ignore_folders):
            continue
        for filename in files:
            file_ext = os.path.splitext(filename)[1]
            if file_ext in file_extensions:
                files_by_extension[file_ext].append(os.path.join(root, filename))

    for ext in file_extensions:
        files_by_extension[ext].sort()

    all_files = [file for ext in file_extensions for file in files_by_extension[ext]]

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("<file_overview>\n")
        outfile.write(f"Total files: {len(all_files)}\n")
        outfile.write(f"Date generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write("Folder Structure:\n")
        folder_tree = create_folder_tree(folder_path, ignore_folders)
        outfile.write(folder_tree)
        outfile.write("\nFiles included:\n")
        for file_path in all_files:
            relative_path = os.path.relpath(file_path, folder_path)
            outfile.write(f"- {relative_path}\n")
        outfile.write("</file_overview>\n\n")

        for file_path in all_files:
            try:
                relative_path = os.path.relpath(file_path, folder_path)
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                mod_time = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                outfile.write(f'<file path="{relative_path}" size="{file_size}" modified="{mod_time}">\n')

                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()

                outfile.write(content.strip())
                outfile.write("\n</file>\n\n")
            except Exception as e:
                print(f"Error reading file '{file_path}': {str(e)}")

    print(f"All files with extensions {', '.join(file_extensions)} have been combined into '{output_file}'.")


if __name__ == '__main__':
    combine_files("abc", "HttpStuff.txt", [".h", ".cpp"], ['.git', 'node_modules', '__pycache__'])
