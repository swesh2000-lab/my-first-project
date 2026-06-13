import os
import re
import time
import subprocess nagi hikaru

def clear():
    os.system("clear")

def color(text, c):
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "cyan": "\033[96m", "white": "\033[97m", "bold": "\033[1m",
        "dim": "\033[2m", "reset": "\033[0m", "magenta": "\033[95m"
    }
    return colors.get(c,"") + str(text) + colors["reset"]

PYTHON_ERRORS = {
    "SyntaxError": {
        "what": "Your code has a syntax mistake — Python cannot understand it.",
        "causes": [
            "Missing colon : at end of if / for / while / def / class",
            "Mismatched brackets or parentheses",
            "Wrong quotes or unclosed string",
            "Typo in keyword like prin instead of print",
        ],
        "fixes": [
            "Check the line number shown in the error",
            "Look for missing : at end of if/for/while/def",
            "Make sure all ( ) [ ] are opened and closed",
            "Check all strings have matching quotes",
        ],
        "example": "if x == 5    # missing coloumn"
    },
    "IndentationError": {
        "what": "Python is strict about spaces. Your indentation is wrong.",
        "causes": [
            "Mixed tabs and spaces",
            "Wrong number of spaces inside if/for/while/def",
            "Code that should be indented is not",
        ],
        "fixes": [
            "Use 4 spaces for each level of indentation",
            "Never mix tabs and spaces — use only spaces",
            "Check that code inside if/for/def is indented",
        ],
        "example": "def greet():\nprint('hi')  # should be indented"
    },
    "NameError": {
        "what": "You used a variable or function that does not exist.",
        "causes": [
            "Typo in variable name",
            "Variable used before it was created",
            "Function called before it was defined",
            "Wrong capitalisation — Python is case sensitive",
        ],
        "fixes": [
            "Check spelling of variable name",
            "Make sure variable is created before use",
            "Check capitalisation — Name and name are different",
        ],
        "example": "print(nmae)  # typo — should be name"
    },
    "TypeError": {
        "what": "You used the wrong type of data for an operation.",
        "causes": [
            "Adding string and number together without converting",
            "Calling a non-function as a function",
            "Wrong number of arguments to a function",
            "Using None where a value is expected",
        ],
        "fixes": [
            "Convert types — use int(), str(), float()",
            "Check function arguments match what it expects",
            "Check variable is not None before using it",
        ],
        "example": "age = 18\nprint('Age: ' + age)  # need str(age)"
    },
    "ValueError": {
        "what": "Right type of data but wrong value.",
        "causes": [
            "Converting a non-number string to int",
            "Unpacking wrong number of values",
            "Passing invalid value to a function",
        ],
        "fixes": [
            "Check the value before converting",
            "Use try/except when converting user input",
            "Validate data before passing to functions",
        ],
        "example": "int('hello')  # cannot convert text to number"
    },
    "IndexError": {
        "what": "You tried to access a position in a list that does not exist.",
        "causes": [
            "List has 3 items but you tried index 5",
            "Empty list but tried to access index 0",
            "Off by one — list ends at index 4 not 5",
        ],
        "fixes": [
            "Check list length with len() before accessing",
            "Remember lists start at index 0 not 1",
            "Use len(list) - 1 for last item or list[-1]",
        ],
        "example": "items = [1,2,3]\nprint(items[5])  # only 0,1,2 exist"
    },
    "KeyError": {
        "what": "You tried to access a key in a dictionary that does not exist.",
        "causes": [
            "Typo in key name",
            "Key was deleted or never added",
            "Case mismatch — Name vs name",
        ],
        "fixes": [
            "Use dict.get('key') instead of dict['key']",
            "Check key exists with: if 'key' in dict",
            "Print dict.keys() to see what keys exist",
        ],
        "example": "d = {'name': 'Ali'}\nprint(d['age'])  # age key missing"
    },
    "AttributeError": {
        "what": "You tried to use a method or property that does not exist on this object.",
        "causes": [
            "Typo in method name",
            "Wrong object type — calling list method on string",
            "Variable is None so has no methods",
        ],
        "fixes": [
            "Check spelling of method name",
            "Check variable type before calling methods",
            "Check variable is not None",
        ],
        "example": "x = 5\nx.append(3)  # int has no append method"
    },
    "ImportError": {
        "what": "Python could not find the module you tried to import.",
        "causes": [
            "Module not installed",
            "Typo in module name",
            "Wrong Python version",
        ],
        "fixes": [
            "Install it: pip3 install module_name",
            "Check spelling of import name",
            "Make sure you are using python3 not python",
        ],
        "example": "import numppy  # typo — should be numpy"
    },
    "ModuleNotFoundError": {
        "what": "The module you imported is not installed on your system.",
        "causes": [
            "Package not installed",
            "Installed for wrong Python version",
            "Virtual environment issue",
        ],
        "fixes": [
            "Run: pip3 install module_name",
            "Run: pip3 install module_name --break-system-packages",
            "Check: pip3 list | grep module_name",
        ],
        "example": "import pandas  # run: pip3 install pandas"
    },
    "FileNotFoundError": {
        "what": "Python could not find the file you specified.",
        "causes": [
            "Wrong file path",
            "File does not exist",
            "Wrong directory",
            "Typo in filename",
        ],
        "fixes": [
            "Check file path is correct",
            "Use os.path.exists('file') to verify",
            "Use full path instead of relative path",
            "Run ls to see files in current directory",
        ],
        "example": "open('data.txt')  # file does not exist here"
    },
    "ZeroDivisionError": {
        "what": "You tried to divide a number by zero.",
        "causes": [
            "Dividing by a variable that happens to be 0",
            "Formula that results in division by zero",
        ],
        "fixes": [
            "Check divisor is not zero before dividing",
            "Use: result = a / b if b != 0 else 0",
        ],
        "example": "print(10 / 0)  # cannot divide by zero"
    },
    "RecursionError": {
        "what": "A function called itself too many times without stopping.",
        "causes": [
            "Missing base case in recursive function",
            "Base case never reached",
        ],
        "fixes": [
            "Add a base case that stops the recursion",
            "Check the condition that stops the function",
        ],
        "example": "def f(): return f()  # calls itself forever"
    },
    "MemoryError": {
        "what": "Your program ran out of memory.",
        "causes": [
            "Creating an extremely large list or object",
            "Infinite loop building up data",
            "Loading a huge file all at once",
        ],
        "fixes": [
            "Process data in smaller chunks",
            "Use generators instead of lists for large data",
            "Close files and free variables when done",
        ],
        "example": "x = list(range(10**10))  # too large"
    },
    "PermissionError": {
        "what": "Python does not have permission to access that file or folder.",
        "causes": [
            "File is owned by root or another user",
            "File is read-only",
            "Trying to write to a system directory",
        ],
        "fixes": [
            "Run with sudo if needed: sudo python3 script.py",
            "Change file permissions: chmod 644 file.txt",
            "Write to home directory instead",
        ],
        "example": "open('/etc/passwd', 'w')  # no write permission"
    },
}

LINUX_ERRORS = {
    "command not found": {
        "what": "The command you typed does not exist or is not installed.",
        "causes": [
            "Typo in command name",
            "Program not installed",
            "Program not in PATH",
        ],
        "fixes": [
            "Check spelling of command",
            "Install it: sudo apt install program_name",
            "Use which command_name to check if installed",
        ],
        "example": "pythn3 script.py  # typo — should be python3"
    },
    "permission denied": {
        "what": "You do not have permission to run or access this.",
        "causes": [
            "File is not executable",
            "File owned by another user",
            "Need administrator access",
        ],
        "fixes": [
            "Make executable: chmod +x filename",
            "Run as admin: sudo command",
            "Check ownership: ls -la filename",
        ],
        "example": "./script.sh  # need: chmod +x script.sh first"
    },
    "no such file or directory": {
        "what": "The file or folder you specified does not exist.",
        "causes": [
            "Wrong path",
            "Typo in filename",
            "File was deleted or moved",
            "Wrong directory",
        ],
        "fixes": [
            "Run ls to see what files exist here",
            "Run pwd to check current directory",
            "Use full path: /home/user/file.py",
            "Check spelling of filename",
        ],
        "example": "cd Downlods  # typo — should be Downloads"
    },
    "broken pipe": {
        "what": "The program receiving output stopped before the sender finished.",
        "causes": [
            "Piped command closed early",
            "Network connection dropped",
        ],
        "fixes": [
            "Usually harmless — just run the command again",
            "Check network connection if network related",
        ],
        "example": "cat bigfile.txt | head -5  # head closes pipe early"
    },
    "disk quota exceeded": {
        "what": "You have used all your allowed disk space.",
        "causes": [
            "Too many files",
            "Very large files",
            "Log files filling up space",
        ],
        "fixes": [
            "Check usage: du -sh ~/*",
            "Delete unused files: rm filename",
            "Empty trash",
        ],
        "example": "cp bigfile.iso ~/  # disk full"
    },
    "connection refused": {
        "what": "Could not connect — the server or port is not accepting connections.",
        "causes": [
            "Server is not running",
            "Wrong port number",
            "Firewall blocking connection",
        ],
        "fixes": [
            "Check if service is running: sudo systemctl status service",
            "Check port number is correct",
            "Check firewall: sudo ufw status",
        ],
        "example": "curl http://localhost:8080  # server not started"
    },
    "too many open files": {
        "what": "Your program opened more files than the system allows.",
        "causes": [
            "Files opened in loop but never closed",
            "System limit reached",
        ],
        "fixes": [
            "Always close files after use: file.close()",
            "Use with open() which closes automatically",
            "Increase limit: ulimit -n 4096",
        ],
        "example": "for i in range(10000): open('f.txt')  # never closed"
    },
    "address already in use": {
        "what": "Another program is already using that network port.",
        "causes": [
            "Previous instance of your program still running",
            "Another app using same port",
        ],
        "fixes": [
            "Find what is using it: sudo lsof -i :PORT",
            "Kill it: sudo kill -9 PID",
            "Use a different port number",
        ],
        "example": "python3 server.py  # port 8000 already taken"
    },
    "killed": {
        "what": "Your process was killed by the system, usually due to too much memory.",
        "causes": [
            "Program used too much RAM",
            "System ran out of memory",
            "Manually killed with kill command",
        ],
        "fixes": [
            "Optimise memory usage",
            "Process data in smaller chunks",
            "Check RAM: free -h",
        ],
        "example": "python3 heavy_script.py  # uses too much RAM"
    },
}

def print_banner():
    clear()
    print(color("=" * 60, "dim"))
    print(color("  ERROR DETECTOR  --  Python & Linux", "cyan"))
    print(color("=" * 60, "dim"))
    print()

def print_menu():
    print(color("  WHAT DO YOU WANT TO DO?", "yellow"))
    print(color("  " + "-" * 30, "dim"))
    print("  " + color("1)", "cyan") + " Paste an error message -- I will explain it")
    print("  " + color("2)", "cyan") + " Run a Python file -- I will catch and explain errors")
    print("  " + color("3)", "cyan") + " Browse all Python errors")
    print("  " + color("4)", "cyan") + " Browse all Linux errors")
    print("  " + color("q)", "cyan") + " Quit")
    print()

def detect_error(text):
    text_lower = text.lower()
    matched = []

    for err_name, info in PYTHON_ERRORS.items():
        if err_name.lower() in text_lower:
            matched.append(("Python", err_name, info))

    for err_phrase, info in LINUX_ERRORS.items():
        if err_phrase in text_lower:
            matched.append(("Linux", err_phrase, info))

    return matched

def print_error_info(etype, ename, info):
    print(color("  ERROR TYPE : ", "dim") + color(etype, "magenta"))
    print(color("  ERROR NAME : ", "dim") + color(ename, "red"))
    print()
    print(color("  WHAT IT MEANS", "yellow"))
    print("  " + info["what"])
    print()
    print(color("  COMMON CAUSES", "yellow"))
    for c in info["causes"]:
        print(color("  - ", "dim") + c)
    print()
    print(color("  HOW TO FIX", "yellow"))
    for i, f in enumerate(info["fixes"], 1):
        print("  " + color(str(i) + ".", "green") + " " + f)
    print()
    print(color("  EXAMPLE", "yellow"))
    print(color("  " + info["example"], "dim"))
    print()
    print(color("  " + "=" * 56, "dim"))
    print()

def paste_error():
    print_banner()
    print(color("  Paste your error message below.", "yellow"))
    print(color("  Type END on a new line when done.", "dim"))
    print()
    lines = []
    while True:
        line = input("  ")
        if line.strip().upper() == "END":
            break
        lines.append(line)
    text = "\n".join(lines)
    if not text.strip():
        print(color("  No input received.", "red"))
        time.sleep(1)
        return
    matched = detect_error(text)
    clear()
    print_banner()
    if not matched:
        print(color("  Could not identify a known error in your message.", "red"))
        print(color("  Try copying just the error line e.g. SyntaxError: ...", "dim"))
        print()
    else:
        print(color("  Found " + str(len(matched)) + " matching error(s):", "green"))
        print()
        for etype, ename, info in matched:
            print_error_info(etype, ename, info)
    input(color("  Press Enter to go back...", "dim"))

def run_python_file():
    print_banner()
    print(color("  Enter the full path to your Python file.", "yellow"))
    print(color("  Example: /home/user/Downloads/my_script.py", "dim"))
    print()
    path = input(color("  File path: ", "cyan")).strip()
    if not os.path.exists(path):
        print(color("  File not found: " + path, "red"))
        time.sleep(2)
        return
    print()
    print(color("  Running " + path + "...", "dim"))
    print(color("  " + "-" * 56, "dim"))
    print()
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    if result.returncode == 0:
        print(color("  No errors! Output:", "green"))
        print()
        print(result.stdout)
    else:
        error_output = result.stderr
        print(color("  Error detected:", "red"))
        print()
        print(color(error_output, "red"))
        print(color("  " + "-" * 56, "dim"))
        print()
        matched = detect_error(error_output)
        if matched:
            print(color("  EXPLANATION", "yellow"))
            print()
            for etype, ename, info in matched:
                print_error_info(etype, ename, info)
        else:
            print(color("  Could not match a known error pattern.", "dim"))
    input(color("  Press Enter to go back...", "dim"))

def browse_errors(error_dict, label):
    while True:
        print_banner()
        print(color("  " + label + " ERRORS -- Choose one to learn about it", "yellow"))
        print(color("  " + "-" * 40, "dim"))
        keys = list(error_dict.keys())
        for i, k in enumerate(keys, 1):
            print("  " + color(str(i) + ")", "cyan") + " " + k)
        print("  " + color("b)", "cyan") + " Back")
        print()
        choice = input(color("  Choose: ", "cyan")).strip().lower()
        if choice == "b":
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                key = keys[idx]
                clear()
                print_banner()
                print_error_info(label, key, error_dict[key])
                input(color("  Press Enter to continue...", "dim"))
        except:
            pass

def main():
    while True:
        print_banner()
        print_menu()
        choice = input(color("  Choose (1/2/3/4/q): ", "cyan")).strip().lower()
        if choice == "q":
            print()
            print(color("  Goodbye!\n", "cyan"))
            break
        elif choice == "1":
            paste_error()
        elif choice == "2":
            run_python_file()
        elif choice == "3":
            browse_errors(PYTHON_ERRORS, "PYTHON")
        elif choice == "4":
            browse_errors(LINUX_ERRORS, "LINUX")
        else:
            print(color("  Invalid choice.", "red"))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\n  Goodbye!\n", "cyan"))import numpy as np
np.array([1, 2, 3])

