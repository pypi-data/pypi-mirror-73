import importlib
import pkgutil
import sys

import log
from bullet import Bullet


def main(target=""):
    log.init()

    target = sys.argv[-1]

    package = importlib.import_module(__package__)
    modules = list(pkgutil.iter_modules(package.__path__))
    choices = [m.name for m in modules]

    cli = Bullet(prompt="\nSelect a script to run:", bullet=" ● ", choices=choices,)
    if target not in choices:
        target = cli.launch()

    module = importlib.import_module(f"{__package__}.{target}")
    module.main()


if __name__ == "__main__":
    main()
