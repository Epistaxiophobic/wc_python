import argparse
from os.path import exists, isfile

def get_details(path):
    """
    Return a dict containing details
    """

    details = {
            "err": False,
            "new_lines": 0,
            }

    try:
        
        file = open(path)
        for line in file:
            for c in line:
                if c == "\n":
                    details["new_lines"] += 1
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
    parser.add_argument("FILE", type=str, nargs="*", help="With no FILE, or when FILE is -, read standard input")

    # Parse arguments
    args = parser.parse_args()

    for path in args.FILE:
        if is_valid_file(path):
            file_details = get_details(path)
            if not file_details["err"]:
                print(file_details["new_lines"], path)

if __name__ == "__main__":
    main()
