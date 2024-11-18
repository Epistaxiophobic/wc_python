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
        print(f" Something went wrong while processing file: {path}")
        details["err"] = True
    finally:
        try:
            file.close()
        except Exception:
            pass 
    
    return details

def get_state(args):
    state = 0
    if args.lines:
        state |= 1
    if args.words:
        state |= 2
    if args.bytes:
        state |= 4
    if args.chars:
        state |= 8
    if args.max_line_length:
        state |= 16
    return state if state else 7

def is_valid_file(path):
    """
    Return True if path exists and points to file
    """

    if not exists(path):
        print(f" No such file or directory: {path}")
        return False
    if not isfile(path):
        print(f" Path is not a file: {path}")
        return False
    return True

def report(details, state, path):
    output = " "
    if state & 1:
        output += f"{details['new_lines']}\t"
    if state & 2:
        output += f"{details['words']:4}\t"
    if state & 4:
        output += f"{details['bytes']:4}\t"
    if state & 8:
        output += f"{details['chars']:4}\t"
    if state & 16:
        output += f"{details['max_length']:4}\t"
    print(output, path)

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
    
    # Program state
    state = get_state(args)
    
    # No input FILE
    if len(args.FILE) == 0:
        stdin_details = get_stdin_details()
        report(stdin_details, state, "")
        quit(0)
    
    # Get total info
    total = {
            "new_lines": 0,
            "words": 0,
            "bytes": 0,
            "chars": 0,
            "max_length": 0,
            }

    for path in args.FILE:
        details = {
                "new_lines": 0,
                "words": 0,
                "bytes": 0,
                "chars": 0,
                "max_length": 0,
                }
        if path == "-":
            details = get_stdin_details()
            report(details, state, "-")

        elif is_valid_file(path):
            details = get_file_details(path)
            if not details["err"]:
                report(details, state, path)
        else:
            report(details, state, path)
            continue

        if details.get("err", False) == False:
            for k, v in details.items():
                if k == "err":
                    continue
                if k == "max_length":
                    total[k] = max(total[k], v)
                else:
                    total[k] += v

    if len(args.FILE) > 1:
        report(total, state, "TOTAL")

if __name__ == "__main__":
    main()
