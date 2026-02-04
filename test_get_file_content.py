from functions.get_file_content import get_file_content

def test(sandbox, target):
    print(f'Result for {"current" if target == "." else target} file:')
    print(get_file_content(sandbox, target), "\n")

test("calculator", "lorem.txt")
test("calculator", "main.py")
test("calculator", "pkg/calculator.py")
test("calculator", "/bin/cat")
test("calculator", "pkg/does_not_exist.py")
