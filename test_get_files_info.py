# test_get_files_info.py

from functions.get_files_info import get_files_info

def test_dir(working_dir, directory):
    if directory == ".":
        print(f"Result for current directory:\n{get_files_info(working_dir, directory)}")
    else:
        print(f"Result for '{directory}' directory:\n{get_files_info(working_dir, directory)}")

def main():
    test_dir("calculator", ".")
    test_dir("calculator", "pkg")
    test_dir("calculator", "/bin")
    test_dir("calculator", "../")

main()