from functions.get_files_info import get_files_info


result = get_files_info("calculator", ".")
print("Result for current directory:")
print(f"  - {result.replace('\n','\n  - ')}")
result1 =get_files_info("calculator", "pkg")
print("Result for current directory:")
print(f"  - {result1.replace('\n','\n  - ')}")
result2 =get_files_info("calculator", "/bin")
print("Result for current directory:")
print(f"  - {result2.replace('\n','\n  - ')}")
result3 =get_files_info("calculator", "../")
print("Result for current directory:")
print(f"  - {result3.replace('\n','\n  - ')}")