import os

import tkinter as tk
from tkinter import filedialog, messagebox

from .get_pbm import get_pbm, get_base
from .pbm import logger

def continue_in_terminal_popup(_ = None) -> None:
    messagebox.showinfo("message", "please continue in the terminal.")

def fetch_input(*find: str) -> tuple[str, ...]:
    continue_in_terminal_popup()

    r: list[str] = []

    for f in find:
        r.append(input(f"please enter the {f} >> "))

    return (*r,)

def open_pbm_project(path: str) -> None:
    logs: list[str] = [
        f"info: a path was passed to pbm.ui successfully: '{path}'"
    ]

    if not path.lower().startswith("c:"):
        messagebox.showerror("error", f"'{path}' is not supported. please enter an absolute path ('c:/...')")

        return

    os.chdir(path)
    logs.append(f"info: changed working directory to '{path}'")

    if ".pbm" in os.listdir(path):
        logs.append("info: found .pbm directory")

    else:
        logs.append("info: .pbm directory not found, initializing...")

        get_pbm().init(path)

    logs.append("info: created root tkinter window")
    logs.append("info: creating elements...")
    logs.append("info: tkinter window elements created successfully")
    logs.append("info: running mainloop...")

    messagebox.showinfo("logs", "\n".join(logs))

    home: tk.Tk = tk.Tk()
    home.title(f"pbm control panel ({path})")
    home.geometry("500x1000")

    tk.Label(home, text="-- build and run --", font="arial 15 bold").pack(pady=20)
    tk.Button(home, text=f"run '{get_pbm().get_default_base()}' base", command=lambda: get_base().run(), foreground="#00cc00", background="#aaaaaa").pack(pady=10)
    tk.Button(home, text=f"build '{get_pbm().get_default_base()}' base with entrypoint 'main.py'", command=lambda: get_base().build(_=continue_in_terminal_popup()),foreground="#00cc00", background="#aaaaaa").pack(pady=10)
    tk.Button(home, text="run a different base", command=lambda: get_base().run(*fetch_input("base name")), foreground="#00aa00").pack(pady=10)
    tk.Button(home, text="build a different base or entrypoint", command=lambda: get_base().build(*fetch_input("base name", "file to build from", "answer. would you like to also build\n"
        "a 'src' with this build? (recommended).\n"
        "this cannot be done later")),
    foreground="#00aa00").pack(pady=10)

    tk.Label(home, text="-- manage bases --", font="arial 15 bold").pack(pady=20)
    tk.Button(home, text="create new base", command=lambda: get_base().new_base(*fetch_input("base name")), foreground="#7777ff").pack(pady=10)
    tk.Button(home, text="export base", command=lambda: get_base().export_base(*fetch_input("export path", "base name")), foreground="#7777ff").pack(pady=10)
    tk.Button(home, text="import base", command=lambda: get_base().import_base(*fetch_input("id", "base name", "destination base")), foreground="#7777ff").pack(pady=10)

    tk.Label(home, text="-- misc --", font="arial 15 bold").pack(pady=20)
    tk.Button(home, text="write 'main.py'", command=lambda: continue_in_terminal_popup(os.system(f"nvim ./main.py"))).pack(pady=10)
    tk.Button(home, text="write", command=lambda: os.system(f"nvim {fetch_input("file to write")[0]}")).pack(pady=10)

    tk.Label(home, text="-- danger zone /!\\ --", font="arial 15 bold", foreground="#ff0000").pack(pady=20)
    tk.Button(home, text="detonate a base (irreversible)", command=lambda: get_base().detonate(*fetch_input("base name")), foreground="#ff0000").pack(pady=10)
    tk.Button(home, text="delete a base (irreversible)", command=lambda: get_base().delete_base(*fetch_input("base name")), foreground="#ff0000").pack(pady=10)
    tk.Button(home, text=f"destroy repo at '{path}' (irreversible)", command=lambda: (get_pbm().destroy if fetch_input("answer. are you sure you want to continue?\n"
        "this action is irreversible. [y/n]") == "y" else lambda _: None
    ), foreground="#ff0000").pack(pady=10)

    home.mainloop()

    messagebox.showinfo("message", f"closed project '{path}' safely.")

def launch_pbm_desktop() -> None:
    root: tk.Tk = tk.Tk()
    root.title("pbm control panel (no directory open)")

    tk.Label(root, text="open or init a project", font="arial 20 bold").pack(pady=10)
    tk.Label(root, text="choose a path:").pack(pady=20)
    entry: tk.Entry = tk.Entry(root, width=60)
    entry.pack(pady=10)
    tk.Button(root, text="open", command=lambda: open_pbm_project(entry.get())).pack(pady=10)
    tk.Label(root, text="-- or --", font="arial 13 bold").pack(pady=10)
    tk.Button(root, text="choose in explorer", command=lambda: open_pbm_project(filedialog.askdirectory(
        title="choose a directory for pbm"
    ))).pack(pady=10)
    tk.Label(root, text="-- or --", font="arial 13 bold").pack(pady=10)
    tk.Button(root, text="continue in terminal", command=lambda: get_pbm().console(continue_in_terminal_popup())).pack(pady=10)

    root.mainloop()

    logger.info("successfully concluded pbm control panel session")