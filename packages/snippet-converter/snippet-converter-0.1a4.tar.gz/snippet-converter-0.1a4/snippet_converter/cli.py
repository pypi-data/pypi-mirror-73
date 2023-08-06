#!/usr/bin/env python3
# import argparse
from snippet_converter import setup, sublime


def run() -> None:
    setup.run()
    sublime.export()


if __name__ == '__main__':
    run()
