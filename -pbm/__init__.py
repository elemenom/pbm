import sys, os, shutil, logging

def choice_map(message: str, *choices: str, explicit_case: bool = False) -> str:
    while True:
        inp: str = input(f"\n\n\n{message}{"".join(" " * 80)}:").strip()

        inp = inp if explicit_case else inp.lower()

        if inp in choices:
            return inp

def confirmation() -> bool:
    return choice_map("[y]es (confirm) | [n]o (cancel)", "y", "n") == "y"

from random import randint

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
      description = "PyForge build",
      options = {{"build_exe": build_options}},
      executables = [Executable("./{}")]
)
"""

class PBM:
    latest_version: str = "v1.2"

    @staticmethod
    def init(path: str | None = None) -> None:
        try:
            path = path or sys.argv[2]
        except IndexError:
            logger.fatal(
                "missing pbm repo path, use `python -m -pbm init <path>` instead, or `python -m -pbm init .` to initialize the current directory.")
            return

        PBM.ensure_pbm_dir()

        logger.fatal("already a pbm repo in '.', cannot initialize again. use `python -m -pbm reinit` instead.")

        else:
            os.mkdir(f"{path}/.pbm")
            os.mkdir(f"{path}/.pbm/builds")
            os.mkdir(f"{path}/.pbm/builds/main")

            logger.info("pbm repo initialized successfully")

            with open(".pbm/cx_freeze_setup.py", "w") as file:
                file.write(CX_FREEZE_SETUP.format("main.py"))

            with open(f".pbm/init_version", "w") as file:
                file.write(PBM.latest_version)

    def __getattribute__(self, attribute: str) -> None:
        if self._get_version() != PBM.latest_version:
            logger.warning("this pbm repo is outdated.")
            logger.warning("use `python -m -pbm reinit` to upgrade.")

    @staticmethod
    def get_version():
        with open(".pbm/init_version", "r") as file:
            return file.read()

    @staticmethod
    def ensure_pbm_dir() -> None:
        if not os.path.exists(".pbm"):
            logger.fatal("not a pbm repo, no .pbm directory.")

            exit(1)

    @staticmethod
    def destroy() -> bool:
        PBM.ensure_pbm_dir()

        logger.warning(
            "this will also detonate all builds of this pbm repo. consider using `python -m -pbm base export . *` to back up your builds.")
        logger.warning("are you sure you want to continue?")

        if confirmation():
            shutil.rmtree(".pbm")

            logger.info("pbm repo destroyed successfully")

            return True

        else:
            logger.warning("cancelled pbm repo destruction")

        return False

    @staticmethod
    def reinit() -> None:
        PBM.ensure_pbm_dir()

        old_version = PBM._get_version()

        if PBM.destroy():
            PBM.init(".")

            new_version = PBM._get_version()

            logger.info(f"pbm repo reinitialized successfully")
            logger.info(f"{old_version} -> {new_version}")

        else:
            logger.warning("cancelled pbm repo reinitialization")

    class build:
        @staticmethod
        def build(base: str | None = None, fn: str | None = None) -> None:
            logger.warning(f"this will overwrite your '{base}' build")

            if confirmation():
                PBM.ensure_pbm_dir()

                fn = fn or "main.py"

                with open(".pbm/cx_freeze_setup.py", "w") as file:
                    file.write(CX_FREEZE_SETUP.format(fn))

                os.system(f"python .pbm/cx_freeze_setup.py build_exe --build-exe .pbm/builds/{base}/{fn}")

                logger.info("build completed successfully")

            else:
                logger.warning("cancelled standard build")

        @staticmethod
        def new_base(base: str) -> None:
            PBM.ensure_pbm_dir()

            if os.path.exists(f".pbm/builds/{base}"):
                logger.warning(f"base '{base}' already exists")
            else:
                os.mkdir(f".pbm/builds/{base}")

                logger.info(f"base '{base}' created successfully")

        @staticmethod
        def export_all(location: str) -> None:
            export_id: int = randint(0, 99999)

            os.mkdir(f".pbm/global_export_{export_id}")
            shutil.make_archive(f"{location.strip("/\\")}/export_g{export_id}", "zip",
                                f".pbm/global_export_{export_id}")
            shutil.copytree(f".pbm/builds", f"{location.strip("/\\")}/g{export_id}.pbm")
            shutil.rmtree(f".pbm/global_export_{export_id}")

            logger.info(f"successfully created global export 'g{export_id}'")


        @staticmethod
        def export_base(location: str, base: str) -> None:
            PBM.ensure_pbm_dir()

            export_id: int = randint(0, 999999)

            if base == "*":
                PBM.build.export_all(location)

                return

            shutil.make_archive(f"{location.strip("/\\")}/export_{export_id}", "zip", f".pbm/builds/{base}")
            shutil.copytree(f".pbm/builds/{base}", f"{location.strip("/\\")}/{export_id}.pbm")

            logger.info(f"successfully created export '{export_id}'")

        @staticmethod
        def import_base(export_id: str, base: str, location: str | None = None) -> None:
            PBM.build.new_base(base)

            PBM.ensure_pbm_dir()
            logger.warning(
                "this will also detonate all builds of this pbm repo (and replace them with the imported ones). consider creating a new pbm repo in a separate directory, and merging manually.")

            if confirmation():
                location = location or "."

                source_path = f"{location}/{export_id}.pbm"

                if not os.path.exists(source_path):
                    logger.error(f"import failed: {source_path} does not exist.")

                    return

                if export_id.startswith("g"):
                    target_path = ".pbm/builds"

                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)

                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported global export '{export_id}'")

                else:
                    target_path = f".pbm/builds/{base}"

                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)

                    shutil.copytree(source_path, target_path)
                    logger.info(f"successfully imported base '{base}' from export '{export_id}'")

            else:
                logger.warning("cancelled base import")

        @staticmethod
        def delete_base(base: str | None = None) -> None:
            PBM.ensure_pbm_dir()

            base = base or "main"

            logger.warning(
                f"this will delete your '{base}' build. consider using `python -m -pbm export . {base}` to back up this build.")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    shutil.rmtree(f".pbm/builds/{base}")

                except FileNotFoundError:
                    logger.error(f"that base '{base}' does not exist.")

                    return

                logger.info("base deleted successfully")

            else:
                logger.warning("cancelled base deletion")

        @staticmethod
        def detonate(base: str | None = None) -> None:
            base = base or "main"

            logger.warning(f"this will detonate your '{base}' build")
            logger.warning("are you sure you want to continue?")

            if confirmation():
                try:
                    shutil.rmtree(f".pbm/builds/{base}")

                except FileNotFoundError:
                    logger.error(f"that build '{base}' does not exist.")

                    return

                os.mkdir(f".pbm/builds/{base}")

                logger.info("base detonated successfully")

            else:
                logger.warning("cancelled base detonation")

    @staticmethod
    def run(base: str | None = None) -> None:
        base = base or "main"

        PBM.ensure_pbm_dir()
        print("\n")

        if os.path.exists(f".pbm/builds/{base}/main.py/main.exe"):
            os.system(f".\\.pbm\\builds\\{base}\\main.py\\main.exe")

        else:
            logger.fatal(f"either that base '{base}' does not exist, or is not built.")

        print("\n")

    @staticmethod
    def status() -> None:
        PBM.ensure_pbm_dir()

        print(f"{os.getcwd()} is a pbm repo.")
        print(f"bases: [{", ".join(os.listdir('.pbm/builds'))}]")
        print(f"current version: {PBM._get_version()}")