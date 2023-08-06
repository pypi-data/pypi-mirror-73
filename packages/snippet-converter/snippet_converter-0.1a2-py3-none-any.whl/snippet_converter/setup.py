#!/usr/bin/env python3
import os
import json


def run() -> None:
    """Set up variables.json file with defaults."""

    variables = {}
    variables['SUBLIME_SNIPPET_PATH'] = os.path.expanduser(
        '~') + '/.config/sublime-text-3/Packages/User/Snippets'
    variables['CODE_SNIPPET_PATH'] = os.path.expanduser(
        '~') + '/.config/Code/User/snippets'
    variables['scopes'] = {
        'source.c++': 'cpp',
        'source.python': 'python',
        'source.java': 'java'
    }

    variables_file = open('snippet_converter/variables.json', 'w')
    json.dump(variables, variables_file, indent=2)
    variables_file.close()


if __name__ == '__main__':
    run()
