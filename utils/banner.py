"""Logging banner."""

from utils    import ARGS

# Predetermined line
line = f"+{'-'*108}+"

# Banner title
banner_title = ("""
+============================================================================================================+
|                                                                                                            |
|  █████╗ ██████╗ ██╗   ██╗██╗███████╗ ██████╗ ██████╗  ██████╗ ████████╗                                    |
| ██╔══██╗██╔══██╗██║   ██║██║██╔════╝██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝                                    |
| ███████║██║  ██║██║   ██║██║███████╗██║   ██║██████╔╝██║   ██║   ██║                                       | 
| ██╔══██║██║  ██║╚██╗ ██╔╝██║╚════██║██║   ██║██╔══██╗██║   ██║   ██║                                       |
| ██║  ██║██████╔╝ ╚████╔╝ ██║███████║╚██████╔╝██████╔╝╚██████╔╝   ██║    v1.0.0                             |
| ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝    Copyright © 2023 Gabriel C. Trahan |
+============================================================================================================+
""")

# Banner with arguments/configurations list
BANNER =    (
    f"{banner_title}"
    f"|{'CREDENTIALS':<25} | {f'Path: ':<10}{ARGS.credentials_path:<28} | {f'Key: ':<10}{ARGS.config_key:<28} |\n"
    f"|{'COURSES':<25} | {f'Path: ':<10}{ARGS.courses_path:<28} | {f'':<10}{'':<28} |\n"
    f"{line}\n"
    f"|{'LOGGING:':<25} | {f'Path: ':<10}{ARGS.logging_path:<28} | {f'Level: ':<10}{ARGS.logging_level:<28} |\n"
    f"+{'='*108}+"
)