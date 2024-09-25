import sys, os
from typing import Callable

from .get_pbm import get_pbm, get_base
from .pbm import logger

def main() -> None:
    if len(sys.argv) < 2:
        logger.error("missing command, use `pbm <command> [args]`")

        return

    if get_pbm().get_version() != get_pbm().latest_version:
        logger.warning(f"this pbm repo is outdated. (current='{get_pbm().get_version()}' latest='{get_pbm().latest_version}')")
        logger.warning("&ruse `pbm reinit` to upgrade.")

    for arg in sys.argv[1].split(","):
        match arg:
            case "init":
                get_pbm().init()

            case "reinit":
                get_pbm().reinit()

            case "destroy":
                get_pbm().destroy()

            case "build":
                get_base().build(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base(), sys.argv[3] if len(sys.argv) > 3 else "main.py")

            case "create-base":
                logger.warning("&create-base is deprecated, but can still be used. for more information, see `pbm help base new_base`")

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
                get_base().run(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "status":
                get_pbm().status()

            case "write":
                logger.warning("&pbm write uses neovim to simulate a simple command-line ide for you to code in.")
                logger.warning("&bif you do not have neovim installed, you can install it here:")
                logger.warning("&b[-] https://github.com/neovim/neovim/blob/master/INSTALL.md")
                logger.warning("&have neovim installed, but write isn't working?")
                logger.warning("&try running pbm write in a different terminal (windows terminal should work well).")

                os.system(f"nvim {sys.argv[2] if len(sys.argv) > 2 else "main.py"}")

            case "set-default-base":
                get_pbm().set_default_base_endpoint(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "help":
                subject: str = sys.argv[3] if len(sys.argv) > 3 else ""

                if subject == "":
                    logger.info("&please enter a subject you need help with.")

                try:
                    sector: Callable | None = {
                        "pbm": get_pbm,
                        "base": get_base
                    }.get(sys.argv[2] if len(sys.argv) > 2 else "pbm")

                    if sector is None:
                        logger.error(f"&r'{sys.argv[2]}' is an invalid sector")

                    print((getattr(sector(), subject).__doc__ or f"no provided help for 'pbm/{subject}'. sorry!").lower())

                except AttributeError:
                    logger.error(f"&r'{subject}' is an invalid subject")

            case _:
                logger.error(f"&unknown command: '{arg}'")