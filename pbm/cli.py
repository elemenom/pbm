import sys, os, shutil, time

from time import perf_counter
from typing import Callable, Final

from .get_pbm import get_pbm, get_base
from .pbm import logger, mkdir, choice_map

CREDITS: Final[str] = """
pbm {v} since 2024 by @elemenom on github
build on {b}

    pip install pbm-root

[*] https://github.com/elemenom
[*] https://pypi.org/user/elemenom

[-] https://github.com/elemenom/pbm
[-] https://pypi.org/project/pbm-root

pbm is licensed under a gnu general public license v3
more info at https://www.gnu.org/licenses/gpl-3.0.en.html
"""

def main() -> None:
    try:
        command: str = (sys.argv[1] if len(sys.argv) > 1 else "__not_provided__").lower()

        if get_pbm().get_version() != get_pbm().latest_version:
            logger.warning(f"this pbm repo is outdated. (current='{get_pbm().get_version()}' latest='{get_pbm().latest_version}')")
            logger.warning("use `pbm reinit` to upgrade.")

        match command:
            case "init":
                get_pbm().init()

            case "reinit":
                get_pbm().reinit()

            case "destroy":
                get_pbm().destroy()

            case "commit":
                get_base().build(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base(), message=sys.argv[3] if len(sys.argv) > 3 else None, build_src="--no-src" not in sys.argv)

            case "commit-src":
                get_base().build_src(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "check":
                get_base().check(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "create-base":
                get_base().new_base(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "set-info":
                get_base().set_desc(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base(), sys.argv[3] if len(sys.argv) > 3 else "")

                logger.info("description updated successfully.")

            case "info":
                for i in get_base().get_desc(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base()).split("\n"):
                    logger.info(i)

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

            case "test":
                base: str = sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base()

                logger.debug(f"testing base '{base}' through executable")
                start: float = time.perf_counter()
                get_base().run(base)
                exec_time: float = (perf_counter() - start) * 1000
                logger.debug(f"took {exec_time:.6f}ms to run through executable")

                logger.debug(f"testing base '{base}' through src")
                start = time.perf_counter()
                get_base().run_src(base)
                src_time: float = (perf_counter() - start) * 1000
                logger.debug(f"took {src_time:.6f}ms to run through src")

                logger.debug(f"on average, running through {"executable" if src_time > exec_time else "src"} ran faster than {"executable" if src_time < exec_time else "src"} in this test.")

            case "dist":
                base: str = sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base()

                mkdir("dist")
                shutil.copy(f".pbm/bases/{base}/main.exe", "./dist/dist.exe")

                logger.info(f"created distribution of base '{base}' in dist/")

            case "run-src":
                get_base().run_src(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "fetch":
                get_base().fetch(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "status":
                get_pbm().status()

            case "write":
                logger.info("pbm write uses neovim to simulate a simple command-line ide for you to code in.")
                logger.info("if you do not have neovim installed, you can install it here:")
                logger.info("[-] https://github.com/neovim/neovim/blob/master/INSTALL.md")
                logger.info("have neovim installed, but write isn't working?")
                logger.info("try running pbm write in a different terminal (windows terminal should work well).")

                os.system(f"nvim {sys.argv[2] if len(sys.argv) > 2 else "main.py"}")

            case "set-default-base":
                get_pbm().set_default_base_endpoint(sys.argv[2] if len(sys.argv) > 2 else get_pbm().get_default_base())

            case "help":
                subject: str = sys.argv[3] if len(sys.argv) > 3 else ""

                if subject == "":
                    logger.info("please enter a subject you need help with.")

                try:
                    sector: Callable | None = {
                        "pbm": get_pbm,
                        "base": get_base
                    }.get(sys.argv[2] if len(sys.argv) > 2 else "pbm")

                    if sector is None:
                        logger.error(f"'{sys.argv[2]}' is an invalid sector")

                    print((getattr(sector(), subject).__doc__ or f"no provided help for 'pbm/{subject}'. sorry!").lower())

                except AttributeError:
                    logger.error(f"r'{subject}' is an invalid subject")

            case "panel":
                logger.warning("panel is deprecated. it will not receive bug fixes, or updates of any kind")
                logger.warning("except for security fixes. new features will not be implemented to panel.")

                logger.info("opening pbm control panel. panel is in alpha, so not many visual features are implemented. have a nice day!")

                from .desktop import launch_pbm_desktop

                launch_pbm_desktop()

            case "console":
                logger.error("console is deprecated and no longer works. this is because of security risks.")

            case "report":
                logger.info("a new tab should have opened in your browser.")

                os.system("start https://github.com/elemenom/pbm/issues")

            case "github":
                logger.info("a new tab should have opened in your browser.")

                os.system("start https://github.com/elemenom/pbm")

            case "pypi":
                logger.info("a new tab should have opened in your browser.")

                os.system("start https://pypi.org/project/pbm-root")

            case "uninstall":
                logger.info("pbm uninstall guide:\n")

                logger.info("1. your pbm repos will not be deleted, but may fall out of date.")
                logger.info("2. you will not be able to use pbm commands to modify or init repos. this also applies to destroying them.")
                logger.info("3. once you have made up your mind, run `pip uninstall pbm-root -y` to uninstall pbm.")

            case "credits":
                global CREDITS

                for credit in CREDITS.format(
                    v=get_pbm().latest_version,
                    b=get_pbm().build_date
                ).split("\n"):
                    logger.info(credit)

            case "__not_provided__":
                logger.error(f"no command provided. usage: `pbm <command> [arg1] [arg2] [arg3] [...]`")

            case _:
                logger.error(f"unknown command: '{command}'")

    except Exception as err:
        try:
            logger.error(f"pbm encountered an unexpected error: {type(err).__name__}")
            logger.error("use `pbm report` to report this to pbm developers and get help.")

            if input("press enter to exit ") == "verbose":
                raise err

            exit(1)

        except KeyboardInterrupt:
            ...

        exit(1)
