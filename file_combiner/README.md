# File Combiner

File Combiner is a Python package that processes files in a folder and combines them into a single output file, suitable for use with Large Language Models (LLMs).

## Installation

You can install File Combiner using pip:

```
pip install file_combiner
```

## Usage

After installation, you can use the `file-combiner` command from anywhere in your terminal:

```
file-combiner /path/to/folder --output combined_output.txt --extensions .py .txt --ignore venv .git
```

### Arguments:

- `folder_path`: Path to the folder to process (required)
- `--output`: Name of the output file (default: output.txt)
- `--extensions`: File extensions to include (e.g., .py .txt)
- `--ignore`: Folders to ignore (e.g., git node_modules)(default: ['.git', 'node_modules', '__pycache__'])

## License

This project is licensed under the MIT License.