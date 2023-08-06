# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
from getarticle import GetArticle

def parse_args():
    parser = ArgumentParser(description='getarticle CLI')
    parser.add_argument('-i', '--input', required=True, help='article DOI or website')
    parser.add_argument('-o', '--output', required=False, help='download direction')
    args = parser.parse_args()
    return args


def main(args):
    ga = GetArticle()
    ga.input_article(args.input)
    ga.download(direction=args.output)


def entry_point():
    args = parse_args()
    main(args)


if __name__ == '__main__':
    entry_point()
