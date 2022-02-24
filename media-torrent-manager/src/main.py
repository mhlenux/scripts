from argparse import ArgumentParser, ArgumentError
import os
from shutil import copyfile

import logging 
logging_format = logging.Formatter('%(asctime)s %(message)s')

# config.py
from pathlib import Path
home = str(Path.home())
cwd = os.path.dirname(os.path.realpath(__file__))
if not cwd:
    raise Exception('CWD parsing failed, CWD is needed')
cwd = Path(cwd)
parent_cwd = str(cwd.parent)

EXCEPTION_LOG_PATH = os.path.join(parent_cwd, 'critical.log')
DEBUG_LOG_PATH = os.path.join(parent_cwd, 'debug.log')
MOVIES_PATH = os.path.join(home, "Videos/Movies/")
TV_PATH = os.path.join(home, "Videos/TV/")
UFC_PATH = os.path.join(home, "Videos/UFC/")
EXTENSIONS = ["mkv", "avi", "mp4"]
CATEGORIES = ["TV", "MOVIES", "UFC"]
#ENDCONFIG

def create_logger(logger_name, log_file, level=logging.DEBUG):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging_format)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

exception_logger = create_logger(
    'exception_logger', 
    EXCEPTION_LOG_PATH,
    logging.WARNING)
logger = create_logger(
    'debug_logger', 
    DEBUG_LOG_PATH)


def create_parser():
    """ 
    For Qbitorrent: %R is -r AND -c is %L 
    Examples
    -r = %R [/home/user/Downloads/ItemRoot] 
    -c = %L [TV]
    """
    parser = ArgumentParser()
    parser.add_argument('--rootpath', '-r', help="root path of the downloaded item", required=True)
    parser.add_argument('--category', '-c', help="movie or tv", required=True)

    return parser


def list_files_recursively(currentPath, found, extensions):
    for (dirpath, dirnames, filenames) in os.walk(currentPath):
        if not dirnames:
            finished = True
        for file in filenames:
            extension = file.split(".")[-1]
            if extension in extensions:
                fullPath = os.path.join(dirpath, file)
                found.append(fullPath)
    
    if finished:
        logger.debug(f"all_files_found: {found}")
        return found
    else:
        list_files_recursively(currentPath, found, extensions)


def print_log_exceptions(msg):
        print(msg)
        exception_logger.exception(msg)
        logger.debug(msg)


def main():
    args = create_parser().parse_args()
    logger.debug(f"parsed args: {args}")

    category = str(args.category).upper()

    if category not in CATEGORIES:
        print_log_exceptions(f"ERROR: Invalid category. ({category})")
        exit(1)

    extensions = EXTENSIONS
    all_files = list_files_recursively(args.rootpath, [], extensions)
    
    for copyFrom in all_files:
        fileName = copyFrom.split("/")[-1]
        copyTo = ""

        try:
            if category == "MOVIE":
                copyTo = MOVIES_PATH + fileName
                copyfile(copyFrom, copyTo)
            elif category == "TV":
                copyTo = TV_PATH + fileName
                copyfile(copyFrom, copyTo)
        except FileNotFoundError as e:
            print_log_exceptions(f"ERROR: File coping failed: '{e}'")
            exit(1)
        logger.debug(f"copied file from '{copyFrom}' TO '{copyTo}'")

if __name__ == '__main__':
    main()