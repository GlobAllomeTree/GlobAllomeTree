#!/usr/bin/env python
import os
import sys

# PROJECT_PATH = os.path.join(os.path.dirname(__file__))
# sys.path.insert(1, os.path.join(PROJECT_PATH, 'globallometree'))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "globallometree.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
