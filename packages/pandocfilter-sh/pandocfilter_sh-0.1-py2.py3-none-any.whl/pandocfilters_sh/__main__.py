import site
import sys


DESCRIPTION = """Pandocfilters wrapper project to install as a script

Useful to being able to install pandocfilters with something like pipx
"""


def main():
    if "--python" in sys.argv:
        print(site.getsitepackages()[0])
    else:
        print(DESCRIPTION)


if __name__ == "__main__":
    main()
