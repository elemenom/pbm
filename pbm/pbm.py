import sys, os, shutil, logging, stat, subprocess
from datetime import datetime

from random import randint
from typing import Callable


def mkdir(path: str) -> bool:
    if os.path.exists(path):
        return False

    os.mkdir(path)

    return True

def rm_readonly(func: Callable, path: str, _) -> None:
    os.chmod(path, stat.S_IWRITE)

    func(path)

def rmdir(path: str) -> bool:
    if not os.path.exists(path):
        return False

    shutil.rmtree(path, onerror=rm_readonly)

    return True

def choice_map(message: str, *choices: str, explicit_case: bool = False) -> str:
    while True:
        inp: str = input(f"\n\n\n{message}\n      :").strip()

        inp = inp if explicit_case else inp.lower()

        if inp in choices:
            return inp

def confirmation() -> bool:
    if "-y" in sys.argv or "--yes" in sys.argv:
        print("[y]es (confirm) | [n]o (cancel)\n      :autofill 'y'")

        return True

    return choice_map("[y]es (confirm) | [n]o (cancel)", "y", "n") == "y"

def paint(cont: str) -> str:
    return cont\
        .replace("&g", "\033[32m")\
        .replace("&r", "\033[31m")\
        .replace("&y", "\033[33m")\
        .replace("&b", "\033[34m")\
        .replace("&m", "\033[35m")\
        .replace("&c", "\033[36m")\
        .replace("&w", "\033[37m")\
        .replace("&0", "\033[0m")\
        .replace("&bold", "\033[1m")\
        .replace("&underline", "\033[4m")\
        .replace("&italic", "\033[3m")\
        .replace("&blink", "\033[5m")\
        .replace("&reverse", "\033[7m")\
        .replace("&hide", "\033[8m")\
        .replace("&reset", "\033[0m")\
        + "\033[0m"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

class ColoredFormatter(logging.Formatter):
    COLORS: dict[str, str] = {
        "DEBUG": "&c",
        "INFO": "&g",
        "WARNING": "&y",
        "ERROR": "&r",
        "CRITICAL": "&m"
    }

    def format(self, record) -> str:
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname = record.levelname.lower()  # Use lowercase
            colored_msg = f"{self.COLORS[record.levelname]}{record.msg}&0"  # Add color
            record.msg = colored_msg
            record.levelname = levelname
        
        return paint(super().format(record))

logger: logging.Logger = logging.getLogger(__name__)
handler: logging.StreamHandler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
logger.handlers = []
logger.addHandler(handler)

logger.propagate = False

CX_FREEZE_SETUP: str = r"""
import os, sys

from cx_Freeze import setup, Executable

build_options = {{
    "packages": [],
    "excludes": [
        "PyQt6",
        "PyQt5"
    ],
    "bin_includes": [
        r"C:\path\to\dll1.dll",
        r"C:\path\to\dll2.dll"
    ]
}}

setup(name="pbm repo",
      version = "1",
      description = "PBM build",
      options = {{"build_exe": build_options}},
      executables = [Executable("./{}", base="Win32GUI")]
)
"""


class PBM:
    latest_version: str = "v1.8"

    def init(self) -> None:
        """
        Command: `pbm init`

        Initializes a new blank PBM repository at .

        Running this creates the following paths on your system:
        ./.pbm/
        ./.pbm/bases/
        ./.pbm/bases/main/
        ./.pbm/init-version
        ./.pbm/default-base
        (i) paths that end with '/' are directories, any other paths are files
        """

        if ".pbm" not in os.listdir("."):
            mkdir(f"./.pbm")
            mkdir(f"./.pbm/bases")
            mkdir(f"./.pbm/bases/main")

            logger.info("pbm repo initialized successfully")

            self.set_version(self.latest_version)
            self.set_default_base("main")

            self.status()

        else:
            logger.error("already a pbm repo in '.', cannot initialize again. use `pbm reinit` instead.")

    @staticmethod
    def get_version() -> str:
        try:
            with open(".pbm/init-version") as file:
                return file.read()

        except FileNotFoundError:
            return PBM.latest_version

    @staticmethod
    def set_version(cont: str) -> None:
        with open(".pbm/init-version", "w") as file:
            file.write(cont)

    def get_default_base(self) -> str:
        self.ensure_pbm_dir()

        with open(".pbm/default-base") as file:
            return file.read()

    @staticmethod
    def set_default_base(cont: str) -> None:
        with open(".pbm/default-base", "w") as file:
            file.write(cont)

    def get_log(self, base: str | None) -> list[str]:
        with open(f".pbm/bases/{base or self.get_default_base()}/logs") as file:
            return file.read().split("\n")

    def add_log(self, base: str | None, message: str | None = None, time: str | None = None) -> None:
        with open(f".pbm/bases/{base or self.get_default_base()}/logs", "a") as file:
            file.write(f"\n{time or datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: build \"{message or f"unmarked commit "+str(randint(0, 9999))}\"")

    def set_default_base_endpoint(self, name: str | None = None) -> None:
        """
        Command: `pbm set-default-base <base>`

        Sets the default base for PBM to use as the default.
        Only applies to the PBM repo this command was used in.
        """

        name = name or "main"

        logger.warning("this will rename the physical default base directory as well as defaults in commands")
        logger.warning(f"from '{self.get_default_base()}' to '{name}'. this action cannot be undone.")
        logger.warning(f"your bases will be saved and won't be lost during the refactoring.")

        if confirmation():
            self.set_default_base(name)

    @staticmethod
    def ensure_pbm_dir() -> None:
        if not os.path.exists(".pbm"):
            logger.fatal("not a pbm repo, no .pbm directory.")

            exit(1)

    def destroy(self, **_) -> bool:
        """
        Command: `pbm destroy`

        Deletes (destroys) the PBM repository at .
        Removes all files and directories added by `pbm init` for a full cleanup (except manually exported files).
        This also deletes the bases and builds of the repository.

        KEEP IN MIND: A path cannot be specified to this command, it always deletes from .!
        """

        self.ensure_pbm_dir()

        logger.warning(
            "this will also detonate all bases of the pbm repo IN THE ./ (CURRENT) DIRECTORY. consider using `pbm base export . *` to back up your bases.")
        logger.warning("are you sure you want to continue?")

        if confirmation():
            rmdir(".pbm")
            logger.info("pbm repo destroyed successfully")

            return True

        else:
            logger.warning("cancelled pbm repo destruction")

        return False

    def reinit(self) -> None:
        """
        Command: `pbm reinit`

        Reinitialize the PBM repo at .

        Reinitializing a PBM repo destroys it, and then initializes it again (duh)
        Reinitializing can be useful for upgrading PBM.

        KEEP IN MIND: Like with `pbm destroy`, a path cannot be specified to this command, it always works in .
        """

        self.ensure_pbm_dir()

        old_version = self.get_version()

        if self.destroy():
            self.init()
            new_version = self.get_version()

            logger.info(f"pbm repo reinitialized successfully")
            logger.info(f"{old_version} -> {new_version}")
        else:
            logger.warning("cancelled pbm repo reinitialization")

    class Base:
        def __init__(self, pbm_instance: "PBM") -> None:
            self.pbm: PBM = pbm_instance

        def build(self,
            base: str | None = None,
            fn: str | None = None,
            build_src: bool = True,
            message: str | None = None,
            **_
        ) -> None:
            """
            Command: `pbm build [base]`

            Builds main.py from . to [base].

            PBM v1.8+ enforces that all repos' entrypoints are 'main.py'.

            UPDATED IN v1.6:
                Building now creates a copy of all files in a hidden 'src'
                directory to allow for fetch functionality. Use the '--no-src' option to
                stop this from happening. This will also make this base
                unfetchable.

            Use `pbm run` to run your builds.
            """

            self.pbm.ensure_pbm_dir()
            base = base or self.pbm.get_default_base()

            if not os.path.exists(f".pbm/bases/{base}"):
                logger.error("cannot build in a base that does not exist")

                return

            logger.warning(f"this will overwrite your '{base}' build")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                fn = fn or "main.py"

                rmdir(f".pbm/bases/{base}")
                mkdir(f".pbm/bases/{base}")

                if fn not in os.listdir():
                    logger.error("pbm v1.8+ enforces that all repos' entrypoints are 'main.py'.")
                    logger.error("please add a 'main.py' file to your repo's root directory.")

                    return

                with open(".pbm/cx_freeze_setup.py", "w") as file:
                    file.write(CX_FREEZE_SETUP.format(fn))

                os.system(f"python .pbm/cx_freeze_setup.py build_exe --build-exe .pbm/bases/{base}")

                logger.info("build completed successfully")

                if build_src:
                    self.build_src(base, True)

                self.pbm.add_log(base, message)

                logger.info("commit was successful.")

            else:
                logger.warning("cancelled standard build")

        @staticmethod
        def ignore_pbm_dir(_, cont: list[str]) -> list[str]:
            return [d for d in cont if d == ".pbm"]

        def build_src(self, base: str | None = None, skip_conf: bool = False) -> None:
            self.pbm.ensure_pbm_dir()

            if not skip_conf:
                logger.warning(f"this will overwrite the src of your '{base}' build")
                logger.warning("are you sure you want to continue?")

                if not confirmation():
                    logger.error("operation cancelled.")

                    return

            logger.info("building src...")

            rmdir(f".pbm/bases/{base}/src")
            shutil.copytree(".", f".pbm/bases/{base}/src", ignore=lambda src, cont: [".pbm"])

            logger.info("src built successfully")

        def check(self, base: str | None = None) -> None:
            self.pbm.ensure_pbm_dir()
            base = base or self.pbm.get_default_base()

            logger.info(f"pbm repository in {os.getcwd()} base {base}: diagnosis")
            logger.info(f"built: {"yes" if os.listdir(f".pbm/bases/{base}") else "no"}")
            logger.info(f"src built: {"yes" if "src" in os.listdir(f".pbm/bases/{base}") else "no"}")
            logger.info(f"commits on this base:")
            for log in self.pbm.get_log(base):
                logger.info(log)

        def new_base(self, base: str) -> None:
            """
            Command: `pbm create-base <base>`

            Creates a new base in the PBM repository at .

            WARNING: `create-base` is deprecated, but can still be used.
                     Consider detonating a new branch using
                     `pbm detonate [branch]` instead.

                     This is because unlike `create-base`, `detonate`
                     takes some extra security measures to ensure
                     that the base is up and running properly when created.

                     You may still use `create-base` if you want,
                     but it's discouraged for large repos where
                     file safety is key.
            """

            self.pbm.ensure_pbm_dir()

            if os.path.exists(f".pbm/bases/{base}"):
                logger.error(f"base '{base}' already exists")

            else:
                mkdir(f".pbm/bases/{base}")
                logger.info(f"base '{base}' created successfully")

        def export_all(self, location: str) -> None:
            self.pbm.ensure_pbm_dir()

            export_id: int = randint(0, 99999)

            mkdir(f".pbm/global_export_{export_id}")
            shutil.make_archive(f"{location.strip('/\\')}/export_g{export_id}", "zip",
                                f".pbm/global_export_{export_id}")
            shutil.copytree(f".pbm/bases", f"{location.strip('/\\')}/g{export_id}.pbm")
            rmdir(f".pbm/global_export_{export_id}")

            logger.info(f"successfully created global export 'g{export_id}'")

        def export_base(self, location: str, base: str) -> None:
            """
            Command: `pbm export [location] [base|*]`

            Exports the selected base into a .zip file and id.pbm directory*

            Exported files can be imported again using `pbm import`.

            *id.pbm directories are exported directories used when importing.
            You cannot automatically import from the .zip file provided.
            id.pbm directories cannot be renamed, as they are distinguished
            using a unique id. (the part before .pbm).

            [base|*], as the name implies, can either be a base,
            or '*' which exports all bases in a "global" export.

            Global exports' ids' first numeral is replaced
            with a 'g' character for 'global'. Global exports
            can be imported same as non-global exports, but with
            the 'g' at the start.

            For more information about importing, see `pbm help base import_base`
            """

            self.pbm.ensure_pbm_dir()

            export_id: int = randint(0, 999999)

            if base == "*":
                self.export_all(location)
                return

            shutil.make_archive(f"{location.strip('/\\')}/export_{export_id}", "zip", f".pbm/bases/{base}")
            shutil.copytree(f".pbm/bases/{base}", f"{location.strip("/\\")}/{export_id}.pbm")

            logger.info(f"successfully created export '{export_id}'")

        def import_base(self, export_id: str, base: str, location: str | None = None) -> None:
            """
            Command: `pbm import <id> [base|*] [location]`

            Import an exported id.pbm* directory.
            Importing a base overwrites that base with the imported material.
            Bulk importing/importing global id.pbm directories will overwrite
            ALL bases, no matter if they're modified or not.
            ALWAYS export to back up before importing.

            *id.pbm directories are exported directories used when importing.
            You cannot automatically import from the .zip file provided.
            id.pbm directories cannot be renamed, as they are distinguished
            using a unique id. (the part before .pbm).

            For more information about exporting, see `pbm help base export_base`
            """

            self.new_base(base)
            self.pbm.ensure_pbm_dir()

            logger.warning(
                "this may also detonate all bases of this pbm repo (and replace them with the imported ones) if a global export is being imported. consider creating a new pbm repo in a separate directory, and merging manually.")

            if confirmation():
                location = location or "."
                source_path = f"{location}/{export_id}.pbm"

                if not os.path.exists(source_path):
                    logger.error(f"import failed: {source_path} does not exist.")
                    return

                if export_id.startswith("g"):
                    target_path = ".pbm/bases"
                    if os.path.exists(target_path):
                        rmdir(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported global export '{export_id}'")
                    
                else:
                    target_path = f".pbm/bases/{base}"
                    if os.path.exists(target_path):
                        rmdir(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported base '{base}' from export '{export_id}'")
            else:
                logger.warning("cancelled base import")

        def delete_base(self, base: str | None = None) -> None:
            """
            Command: `pbm delete-base [base]`

            Self-explanatory, deletes base [base] from the PBM repository at .
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            logger.warning(f"this will delete your '{base}' build. consider using `pbm export . {base}` to back up this build.")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    rmdir(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(f"that base '{base}' does not exist.")
                    return

                logger.info("base deleted successfully")
            else:
                logger.warning("cancelled base deletion")

        def detonate(self, base: str | None = None) -> None:
            """
            Command: `pbm detonate [base]`

            Doesn't necessarily delete base [base], but detonates (deletes)
            the build within it. Useful for memory-efficiency and cleanup.

            Detonating a non-existent base will in turn create it.
            This is the recommended approach for creating bases.
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            logger.warning(f"this will detonate your '{base}' build")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    rmdir(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(f"that base '{base}' does not exist.")
                    return

                mkdir(f".pbm/bases/{base}")
                logger.info("base detonated successfully")

            else:
                logger.warning("cancelled base detonation")
                
        def run(self, base: str | None = None) -> None:
            """
            Command: `pbm run [base]`

            Runs the build in base [base].
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            try:
                try:
                    exe_file: str = [f for f in os.listdir(f".pbm/bases/{base}") if f.endswith(".exe")][0]

                except FileNotFoundError:
                    logger.error(f"base '{base}' does not exist.")

                    return

                logger.info(f"running '{base}' build...\n\n")
                result: subprocess.CompletedProcess = subprocess.run(
                    f".pbm\\bases\\{base}\\{exe_file}",
                    capture_output=True,
                    text=True
                )
                print(result.stdout)

            except IndexError:
                logger.error(f"base '{base}' is not built.")

        def run_src(self, base: str | None = None) -> None:
            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            if os.path.exists(f".pbm/bases/{base}/src"):
                if "main.py" not in os.listdir(f".pbm/bases/{base}/src"):
                    logger.error(f"the 'src' of base '{base}' is not built on 'main.py'.")

                    return

                logger.info(f"running src of '{base}' build...\n\n")

                os.system(f"python .pbm/bases/{base}/src/main.py")

                print()

            else:
                logger.error(f"base '{base}' does not exist, or does not have a built 'src'.")

        def fetch(self, base: str | None = None) -> None:
            """
            Command: `pbm fetch [base]`

            Discards changes made to all files and overwrites them with their
            respective files in [base]/src. Fetching cannot be undone.
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            base = base or self.pbm.get_default_base()

            logger.warning(f"this will overwrite all files in . with their respective files in the src of '{base}'.")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                if os.path.exists(f".pbm/bases/{base}/src"):
                    for file in os.listdir(f".pbm/bases/{base}/src"):
                        shutil.copy(f".pbm/bases/{base}/src/{file}", file)

                    logger.info(f"successfully fetched from '{base}'")

                else:
                    logger.error(f"{base} either doesn't exist, is not built, or is built without a 'src'.")

            else:
                logger.error("operation cancelled.")

    def status(self, _: None = None) -> None:
        self.ensure_pbm_dir()

        version: str = self.get_version()
        default_base: str = self.get_default_base()
        builds: list[str] = os.listdir(".pbm/bases")

        logger.info(f"pbm repository in {os.getcwd()}: diagnosis")
        logger.info(f"version: {version} ({f"outdated by {self.latest_version}" if self.get_version() != self.latest_version else "up to date"})")
        logger.info(f"default base: {default_base}")
        logger.info(f"available bases: [{", ".join(builds) if builds else "no bases available"}]")

    @staticmethod
    def write() -> None: # EMPTY METHOD JUST FOR THE HELP FUNCTIONALITY
        """
        Command: `pbm write [file]`

        Starts a neovim instance at [file] (or 'main.py' by default)

        NEOVIM BASICS:
        - Press 'i' to switch to insert mode
        - Press 'Esc' to switch to command mode
        - Press ':' to type a command whilst in command mode

        - :wq - save and quit
        - :q! - quit neovim WITHOUT saving
        """
        ...

    def console(self) -> None:
        logger.info("entered pbm console. use 'exit' or press 'ctrl + c' to quit.")
        logger.info("")
        logger.info("pbm by @elemenom on github")
        logger.info(f"    distribution {self.latest_version}")
        logger.info(f"open in '{os.getcwd()}'")
        print()

        while True:
            try:
                action: str = input(paint("&italic&g{}:pbm ").format(os.getcwd())).strip()

                if action == "":
                    ...

                elif action == "exit":
                    raise KeyboardInterrupt("manual exit")

                elif action == "clear":
                    os.system("clear")

                elif action.startswith("echo "):
                    print(action[5:])

                elif action.startswith("rm "):
                    logger.warning(f"this would delete the file '{action[3:]}'. this action may be permanent.")

                    if confirmation():
                        os.remove(action[3: ])

                elif action.startswith("rmdir "):
                    logger.warning(f"this would delete the directory and it's children '{action[3:]}'. this action may be permanent.")

                    if confirmation():
                        os.remove(action[6:])

                elif action.startswith("cd "):
                    try:
                        os.chdir(action[3:])
                    except FileNotFoundError:
                        logger.error(f"{action[3:]}: no such file or directory")

                elif action.startswith("read "):
                    with open(action[5:]) as file:
                        print(file.read())

                elif action.startswith("tree "):
                    os.system(f"tree {action[5:]}")

                elif action.startswith("ls "):
                    print("\n".join(os.listdir(action[3:])))

                elif action.startswith("dir "):
                    print(",".join(os.listdir(action[4:])))

                else:
                    os.system(f"python -m pbm {action}")

            except KeyboardInterrupt:
                print()
                logger.info("exiting pbm console...")

                return

            except Exception as err:
                logger.error(f"error: {str(err)}")