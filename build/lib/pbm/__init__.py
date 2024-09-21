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