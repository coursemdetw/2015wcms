#@+leo-ver=5-thin
#@+node:2014spring.20140628104046.1744: * @file manage.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:2014spring.20140628104046.1745: ** manage declarations
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
#@-others
#@-leo
