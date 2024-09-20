from typing import Callable, Any

from . import PBM

def get_pbm() -> PBM:
    return PBM()

def get_base() -> PBM.Base:
    pbm: PBM = get_pbm()

    return pbm.Base(pbm)

def get_block() -> PBM.block:
    pbm: PBM = get_pbm()

    return pbm.block(pbm)

def run_pbm(obj: str | Callable, command: str, *args, **kwargs) -> Any:
    obj = eval(obj, {
        "get_pbm": get_pbm,
        "get_base": get_base,
        "get_block": get_block
    })() if isinstance(obj, str) else obj

    return getattr(obj, command)(*args, **kwargs)