# PBM : Python Build Manager

PBM is a lightweight console-oriented CLI and package for building python projects
as EXE files, creating memory-efficient back-ups, managing dependencies and
running them.

## Installation

### 1. Using `pip` (RECOMMENDED`):
```commandline
pip install pbm_r
```

- [Click here](https://bit.ly/get-pbm) for more information on how to install PBM.

*No other installation methods at the moment*

## CLI Commands

- `python -m -pbm init <path>` - Initialize a PBM repository. PBM repositories are
required to be initialized to perform most PBM actions.
- `python -m -pbm destroy` - Destroy the PBM repository in the current path.
- `python -m -pbm reinit` - Re-initialize the PBM repository in the current path.
This can be useful when upgrading your PBM, and completely wipes the current
PBM repository.
- `python -m -pbm create-base <name>` - Create a base in the current PBM repository.
- `python -m -pbm delete-base <name>` - Delete the base in the current PBM repository.
- `python -m -pbm build <base>` - Build `./main.py` in the current PBM repository.
- `python -m -pbm run <base>` - Run the newest build in the current PBM repository.
- `python -m -pbm status` - View info about the current PBM repository.
- `python -m -pbm detonate <base>` - Delete all build files in the base.
- `python -m -pbm export <location> <base|*>` - Export the base as a .zip file and .pbm file.
- `python -m -pbm import <export-id> <base>` - Load from an export's .pbm file using the export ID.
