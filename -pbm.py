import sys, os, shutil, logging

from .pbm import PBM, logger

def main() -> None:
    if len(sys.argv) < 2:
        logger.fatal("missing command, use `python -m -pbm <command> [args]`")

        return

    for arg in sys.argv[1].split(","):
        match arg:
            case "init":
                PBM.init(sys.argv[2] if len(sys.argv) > 2 else ".")

            case "reinit":
                PBM.reinit()

            case "destroy":
                PBM.destroy()

            case "build":
                PBM.build.build(sys.argv[2] if len(sys.argv) > 2 else "main", sys.argv[3] if len(sys.argv) > 3 else "main.py")

            case "create-base":
                PBM.build.new_base(sys.argv[2] if len(sys.argv) > 2 else "main")

            case "delete-base":
                PBM.build.delete_base(sys.argv[2] if len(sys.argv) > 2 else "main")

            case "export":
                PBM.build.export_base(sys.argv[2] if len(sys.argv) > 2 else ".", sys.argv[3] if len(sys.argv) > 3 else "*")

            case "import":
                PBM.build.import_base(sys.argv[2] if len(sys.argv) > 2 else "0000", sys.argv[3] if len(sys.argv) > 3 else "main", sys.argv[4] if len(sys.argv) > 4 else ".")

            case "detonate":
                PBM.build.detonate(sys.argv[2] if len(sys.argv) > 2 else "main")

            case "run":
                PBM.run(sys.argv[2] if len(sys.argv) > 2 else "main")

            case "status":
                PBM.status()

            case "write":
                os.system(f"nvim {sys.argv[2] if len(sys.argv) > 2 else "main.py"}")

            case _:
                logger.fatal(f"unknown command: {arg}")

if __name__ == "__main__":
    main()