import argparse
from sys import stdin
from os.path import exists, isfile, getsize

def get_stdin_details():
    """
    Return a dict containing details
    """
    data = stdin.read()
    details = {
            "err": False,
            "new_lines": 0,
            "words": 0,
            "bytes": len(data.encode("utf-8")),
            "chars": 0,
            "max_length": 0,
            }
    curr_line_length = 0
    in_word = 0
    for c in data:
        details["chars"] += 1
        if c == "\n":
            details["max_length"] = max(details["max_length"], curr_line_length)
            curr_line_length = 0
            details["new_lines"] += 1
            details["words"] += in_word
            in_word = 0
            continue
        if c.isspace():
            details["words"] += in_word
            in_word = 0
        else:
            in_word = 1
        curr_line_length += 1
        
    return details

def get_file_details(path):
    """
    Return a dict containing details
    """

    details = {
            "err": False,
            "new_lines": 0,
            "words": 0,
            "bytes": 0,
            "chars": 0,
            "max_length": 0,
            }

    try:
        details["bytes"] = getsize(path)
        file = open(path)
        for line in file:
            details["max_length"] = max(details["max_length"], len(line[:-1]))
            in_word = 0
            for c in line:
                details["chars"] += 1
                if c == "\n":
                    details["new_lines"] += 1
                    details["words"] += in_word
                    in_word = 0
                if c.isspace():
                    details["words"] += in_word
                    in_word = 0
                else:
                    in_word = 1

    except Exception:
        print(f"Something went wrong while processing file: {path}")
        details["err"] = True
    finally:
        try:
            file.close()
        except Exception:
            pass 
    
    return details

def is_valid_file(path):
    """
    Return True if path exists and points to file
    """

    if not exists(path):
        print(f"No such file or directory: {path}")
        return False
    if not isfile(path):
        print(f"Path is not a file: {path}")
        return False
    return True

def main():
    # Get command line arguments
    parser = argparse.ArgumentParser(description="A rewrite of Unix wc utility in python")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-L", "--max-line-length", action="store_true", help="print the maximum display width")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("FILE", type=str, nargs="*", help="With no FILE, or when FILE is -, read standard input")

    # Parse arguments
    args = parser.parse_args()

    if len(args.FILE) == 0:
        stdin_details = get_stdin_details()
        print(stdin_details["new_lines"], stdin_details["words"], stdin_details["bytes"], stdin_details["max_length"])
    
    for path in args.FILE:
        if path == "-":
            stdin_details = get_stdin_details()
            print(stdin_details["new_lines"], stdin_details["words"], stdin_details["bytes"], stdin_details["max_length"], path)
        
        elif is_valid_file(path):
            file_details = get_file_details(path)
            if not file_details["err"]:
                print(file_details["new_lines"], file_details["words"], file_details["bytes"], file_details["max_length"], path)

if __name__ == "__main__":
    main()
