# test_get_file_content.py

from functions.get_file_content import get_file_content

def main():
    lorem_file = get_file_content("calculator", "lorem.txt")
    print(str(len(lorem_file)) + " characters " + lorem_file[10001:])
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

main()