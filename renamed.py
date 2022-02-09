import os
import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default=r'C:\Users\1080176', )
    parser.add_argument('-n', '--name', default='File')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    save = os.getcwd()

    os.chdir(f"{namespace.path}")

    for i, t in enumerate(os.listdir()):
        os.rename(t, f"{namespace.name} {i}")

    os.chdir(save)
