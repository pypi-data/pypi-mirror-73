import argparse
import os
from pathlib import Path

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('subprogram', type=str, help='start new project')
    parser.add_argument('-n', '--name', type=str)

    args = parser.parse_args()
    destination = Path(os.getcwd())
    dirname = destination/args.name
    if args.subprogram in ["start", "add"]:
        os.mkdir(dirname)
        os.mknod(dirname/"__init__.py")
        for folder in ["data","panels","plots","views"]:
            os.mkdir(dirname/folder)
            os.mkdir(dirname/folder/"__init__.py")
    if args.subprogram == "start":
        for f in ["config.py", "main.py", "__init__.py"]:
            os.mknod(f)
