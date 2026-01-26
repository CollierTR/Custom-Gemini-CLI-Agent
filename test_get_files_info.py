from functions.get_files_info import get_files_info

def test(sandbox, target):
    print(f'Result for {"current" if target == "." else target} directory:')
    print(get_files_info(sandbox, target), "\n")

test("calculator", ".")
test("calculator", "pkg")
test("calculator", "/bin")
test("calculator", "../")
