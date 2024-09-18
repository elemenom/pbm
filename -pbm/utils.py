def choice_map(message: str, *choices: str, explicit_case: bool = False) -> str:
    while True:
        inp: str = input(f"\n\n\n{message}{"".join(" " * 80)}:").strip()

        inp = inp if explicit_case else inp.lower()

        if inp in choices:
            return inp

def confirmation() -> bool:
    return choice_map("[y]es (confirm) | [n]o (cancel)", "y", "n") == "y"