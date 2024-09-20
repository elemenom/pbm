import sys, os, shutil, logging

from .get_pbm import get_pbm, get_base, get_block
from . import logger

def main() -> None:
    if len(sys.argv) < 2:
        logger.fatal("missing command, use `python -m -pbm <command> [args]`")

        return

    for arg in sys.argv[1].split(","):
        match arg:
            case "init":
                get_pbm().init(sys.argv[2] if len(sys.argv) > 2 else ".")

            case "reinit":
                get_pbm().reinit()

            case "destroy":
                get_pbm().destroy()

            case "build":
                get_base().build(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base(), sys.argv[3] if len(sys.argv) > 3 else "main.py")

            case "create-base":
                get_base().new_base(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "delete-base":
                get_base().delete_base(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "export":
                get_base().export_base(sys.argv[2] if len(sys.argv) > 2 else ".", sys.argv[3] if len(sys.argv) > 3 else "*")

            case "import":
                get_base().import_base(sys.argv[2] if len(sys.argv) > 2 else "0000", sys.argv[3] if len(sys.argv) > 3 else get_pbm().get_default_base(), sys.argv[4] if len(sys.argv) > 4 else ".")

            case "detonate":
                get_base().detonate(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "run":
                get_pbm().run(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "status":
                get_pbm().status()

            case "write":
                os.system(f"nvim {sys.argv[2] if len(sys.argv) > 2 else "main.py"}")

            case _:
                logger.fatal(f"unknown command: {arg}")