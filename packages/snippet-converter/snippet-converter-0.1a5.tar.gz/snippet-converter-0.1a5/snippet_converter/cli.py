#!/usr/bin/env python3
# import argparse
from snippet_converter import setup, sublime


def run() -> None:
    """Entry point for scli command."""

    if not setup.done():
        setup.run()
    sublime.export()


if __name__ == '__main__':
    run()
