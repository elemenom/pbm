import sys, os, shutil, logging

from random import randint

def mkdir(path: str) -> bool:
    if os.path.exists(path):
        return False

    os.mkdir(path)

    return True

def rmdir(path: str) -> bool:
    if not os.path.exists(path):
        return False

    shutil.rmtree(path)

    return True

def choice_map(message: str, *choices: str, explicit_case: bool = False) -> str:
    while True:
        inp: str = input(f"\n\n\n{message}\n      :").strip()

        inp = inp if explicit_case else inp.lower()

        if inp in choices:
            return inp

def confirmation() -> bool:
    if "-y" in sys.argv or "--yes" in sys.argv:
        print("      :autofilled 'y'")

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
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

CX_FREEZE_SETUP = """
from cx_Freeze import setup, Executable

build_options = {{
    "packages": [],
    "excludes": [
        "PyQt6",
        "PyQt5"
    ]
}}

setup(name="pbm repo",
      version = "1",
      description = "PBM build",
      options = {{"build_exe": build_options}},
      executables = [Executable("./{}")]
)
"""


class PBM:
    latest_version: str = "v1.3.2.2"

    def init(self, path: str | None = None) -> None:
        """
        Command: `pbm init [location]`

        Initializes a new PBM blank repository at the specified [location] (. by default).
        Running this creates the following paths on your system:
        [location]/.pbm/
        [location]/.pbm/bases/
        [location]/.pbm/bases/main/
        [location]/.pbm/cx_freeze_setup.py
        [location]/.pbm/init-version
        [location]/.pbm/default-base
        (i) paths that end with '/' are directories, any other paths are files
        """

        try:
            path = path or sys.argv[2]
        except IndexError:
            logger.error(paint("&rmissing pbm repo path, use `pbm init <path>` instead, or `pbm init .` to initialize the current directory."))

            return

        if ".pbm" not in os.listdir(path):
            mkdir(f"{path}/.pbm")
            mkdir(f"{path}/.pbm/bases")
            mkdir(f"{path}/.pbm/bases/main")

            logger.info(paint("&gpbm repo initialized successfully"))

            with open(".pbm/cx_freeze_setup.py", "w") as file:
                file.write(CX_FREEZE_SETUP.format("main.py"))

            self.set_version(self.latest_version)
            self.set_default_base("main")

            self.status()

        else:
            logger.error(paint("&ralready a pbm repo in '.', cannot initialize again. use `pbm reinit` instead."))

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

    @staticmethod
    def get_default_base() -> str:
        with open(".pbm/default-base") as file:
            return file.read()

    @staticmethod
    def set_default_base(cont: str) -> None:
        with open(".pbm/default-base", "w") as file:
            file.write(cont)

    def set_default_base_endpoint(self, name: str | None = None) -> None:
        """
        Command: `pbm set-default-base <base>`

        Sets the default base for PBM to use as the default.
        Only applies to the PBM repo this command was used in.
        """

        name = name or "main"

        logger.warning(paint("&ythis will rename the physical default base directory as well as defaults in commands"))
        logger.warning(paint(f"&yfrom '{self.get_default_base()}' to '{name}'. this action cannot be undone."))
        logger.warning(paint(f"&yyour bases will be saved and won't be lost during the refactoring."))

        if confirmation():
            self.set_default_base(name)

    @staticmethod
    def ensure_pbm_dir() -> None:
        if not os.path.exists(".pbm"):
            logger.fatal(paint("&rnot a pbm repo, no .pbm directory."))
            exit(1)

    def destroy(self) -> bool:
        """
        Command: `pbm destroy`

        Deletes (destroys) the PBM repository at .
        Removes all files and directories added by `pbm init` for a full cleanup (except manually exported files).
        This also deletes the bases and builds of the repository.

        KEEP IN MIND: A path cannot be specified to this command, it always deletes from .!
        """

        self.ensure_pbm_dir()

        logger.warning(paint("&rthis will also detonate all bases of the pbm repo IN THE ./ (CURRENT) DIRECTORY. consider using `pbm base export . *` to back up your bases."))
        logger.warning(paint("&yare you sure you want to continue?"))

        if confirmation():
            rmdir(".pbm")
            logger.info(paint("&gpbm repo destroyed successfully"))

            return True

        else:
            logger.warning(paint("&ycancelled pbm repo destruction"))

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
            self.init(".")
            new_version = self.get_version()

            logger.info(paint(f"&gpbm repo reinitialized successfully"))
            logger.info(paint(f"&r{old_version}&0 -> &g{new_version}"))
        else:
            logger.warning(paint("&ycancelled pbm repo reinitialization"))

    class Base:
        def __init__(self, pbm_instance: "PBM") -> None:
            self.pbm: PBM = pbm_instance

        def build(self, base: str | None = None, fn: str | None = None) -> None:
            """
            Command: `pbm build [base] [file]`

            Builds [file] from . to [base].
            [file] is 'main.py' by default.

            Use `pbm run` to run your builds.
            """

            logger.warning(paint(f"&ythis will overwrite your '{base}' build"))

            if confirmation():
                self.pbm.ensure_pbm_dir()

                fn = fn or "main.py"

                with open(".pbm/cx_freeze_setup.py", "w") as file:
                    file.write(CX_FREEZE_SETUP.format(fn))

                os.system(f"python .pbm/cx_freeze_setup.py build_exe --build-exe .pbm/bases/{base}")

                logger.info(paint("&gbuild completed successfully"))

            else:
                logger.warning(paint("&ycancelled standard build"))

        def new_base(self, base: str) -> None:
            """
            Command: `pbm create-base <base>`

            Creates a new base in the PBM repository at .
            """

            self.pbm.ensure_pbm_dir()

            if os.path.exists(f".pbm/bases/{base}"):
                logger.warning(paint(f"&ybase '{base}' already exists"))
            else:
                mkdir(f".pbm/bases/{base}")
                logger.info(paint(f"&gbase '{base}' created successfully"))

        def export_all(self, location: str) -> None:
            self.pbm.ensure_pbm_dir()

            export_id: int = randint(0, 99999)

            mkdir(f".pbm/global_export_{export_id}")
            shutil.make_archive(f"{location.strip('/\\')}/export_g{export_id}", "zip",
                                f".pbm/global_export_{export_id}")
            shutil.copytree(f".pbm/bases", f"{location.strip('/\\')}/g{export_id}.pbm")
            rmdir(f".pbm/global_export_{export_id}")

            logger.info(paint(f"&gsuccessfully created global export 'g{export_id}'"))

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
            shutil.copytree(f".pbm/bases/{base}", f"{location.strip('/\\')}/{export_id}.pbm")

            logger.info(paint(f"&gsuccessfully created export '{export_id}'"))

        def import_base(self, export_id: str, base: str, location: str | None = None) -> None:
            """
            Command: `pbm import <id> [base|*] [location]

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

            logger.warning(paint("&ythis may also detonate all bases of this pbm repo (and replace them with the imported ones) if a global export is being imported. consider creating a new pbm repo in a separate directory, and merging manually."))

            if confirmation():
                location = location or "."
                source_path = f"{location}/{export_id}.pbm"

                if not os.path.exists(source_path):
                    logger.error(paint(f"&rimport failed: {source_path} does not exist."))
                    return

                if export_id.startswith("g"):
                    target_path = ".pbm/bases"
                    if os.path.exists(target_path):
                        rmdir(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(paint(f"&gsuccessfully imported global export '{export_id}'"))
                else:
                    target_path = f".pbm/bases/{base}"
                    if os.path.exists(target_path):
                        rmdir(target_path)
                    shutil.copytree(source_path, target_path)
                    logger.info(paint(f"&gsuccessfully imported base '{base}' from export '{export_id}'"))
            else:
                logger.warning(paint("&ycancelled base import"))

        def delete_base(self, base: str | None = None) -> None:
            """
            Command: `pbm delete-base [base]`

            Self-explanatory, deletes base [base] from the PBM repository at .
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            logger.warning(paint(f"&ythis will delete your '{base}' build. consider using `pbm export . {base}` to back up this build."))
            logger.warning(paint("&yare you sure you want to continue?"))

            if confirmation():
                try:
                    rmdir(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(paint(f"&rthat base '{base}' does not exist."))
                    return

                logger.info(paint("&gbase deleted successfully"))
            else:
                logger.warning(paint("&ycancelled base deletion"))

        def detonate(self, base: str | None = None) -> None:
            """
            Command: `pbm detonate [base]`

            Doesn't necessarily delete base [base], but detonates (deletes)
            the build within it. Useful for memory-efficiency and cleanup.
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            logger.warning(paint(f"&ythis will detonate your '{base}' build"))
            logger.warning(paint("&yare you sure you want to continue?"))

            if confirmation():
                try:
                    rmdir(f".pbm/bases/{base}")
                except FileNotFoundError:
                    logger.error(paint(f"&rthat base '{base}' does not exist."))
                    return

                mkdir(f".pbm/bases/{base}")
                logger.info(paint("&gbase detonated successfully"))

            else:
                logger.warning(paint("&ycancelled base detonation"))
                
        def run(self, base: str | None = None) -> None:
            """
            Command: `pbm run [base]`

            Runs the build in base [base].
            """

            self.pbm.ensure_pbm_dir()

            base = base or self.pbm.get_default_base()

            try:
                exe_file: str = [f for f in os.listdir(f".pbm/bases/{base}") if f.endswith(".exe")][0]

                logger.info(paint(f"&grunning '{base}' build\n\n"))
                os.system(f".pbm\\bases\\{base}\\{exe_file}")

            except IndexError:
                logger.error(paint(f"&rbase '{base}' is not built."))

    def status(self) -> None:
        self.ensure_pbm_dir()

        version: str = self.get_version()
        default_base: str = self.get_default_base()
        builds: list[str] = os.listdir(".pbm/bases")

        logger.info(paint("&gpbm repository in './': diagnosis"))
        logger.info(paint(f"&gversion: {version} ({f"outdated by {self.latest_version}" if self.get_version() != self.latest_version else "up to date"})"))
        logger.info(paint(f"&gdefault base: {default_base}"))
        logger.info(paint(f"&gavailable bases: [{", ".join(builds) if builds else "no bases available"}]"))

    @staticmethod
    def write() -> None: # EMPTY METHOD JUST FOR THE HELP FUNCTIONALITY
        """
        Command: `pbm write [file]`

        Starts a neovim instance at [file] (or 'main.py' by default)

        NEOVIM BASICS:
        - Press 'i' to switch to insert mode
        - Press 'Esc' to switch to command mode
        - Press ':' to enter command mode and type your command

        :wq - save and quit
        :q! - quit neovim WITHOUT saving
        """
        ...