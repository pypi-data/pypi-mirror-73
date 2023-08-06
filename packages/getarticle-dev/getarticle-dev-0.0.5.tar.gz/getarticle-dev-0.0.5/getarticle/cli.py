# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
from getarticle import GetArticle
import appscript
import os

def parse_args():
    parser = ArgumentParser(description='getarticle CLI')
    parser.add_argument('-i', '--input', required=False, \
        help='article DOI or website')
    parser.add_argument('-o', '--output', required=False, \
        help='download direction')
    parser.add_argument('-so', '--setoutput', required=False, \
        help='set default output direction')
    args = parser.parse_args()
    return args


def main(args):
    if args.setoutput:
        open(".getarticle.ini", "wb").write(args.setoutput.encode())
        os.system("pwd")
        return
    ga = GetArticle()
    if not args.input:
        args.input = appscript.app("Safari").windows.first.current_tab.URL()
    ga.input_article(args.input)
    ga.download(direction=args.output)


def entry_point():
    args = parse_args()
    main(args)


if __name__ == '__main__':
    entry_point()
