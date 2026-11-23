import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
LONG_NUMBER = re.compile(r"(?<!\w)\+?\d(?:[ -]?\d){8,18}(?!\w)")     # 9 to 19 digits, spaces or dashes allowed


def scrub(text: str) -> str:
    text = EMAIL.sub("[email]", text)
    return LONG_NUMBER.sub("[number]", text)          # names still need a separate step (see the guide)
