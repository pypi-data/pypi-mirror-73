#!/usr/bin/env python3
# import argparse
import logging
from snippet_converter import setup, sublime


def run() -> None:
    """Entry point for scli command."""

    if not setup.done():
        setup.run()

    sublime.export()
    variables = setup.read_vars()
    if variables['feedback']:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    logging.info('Sublime snippets successfully exported to VS Code!')


if __name__ == '__main__':
    run()
