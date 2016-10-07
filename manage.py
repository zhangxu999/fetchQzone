#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os
import sys
if __name__ == "__main__":
    a =1
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line
    if len(sys.argv) == 1:
        sys.argv.append('runserver')


    execute_from_command_line(sys.argv)

