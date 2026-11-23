import re

SECRET = re.compile(
    r"""(?ix)
      (?:password|passwd|token|secret|api[_-]?key|authorization)\s*[=:]\s*(?:"[^"]*"|'[^']*'|bearer\s+\S+|\S+)   # key = value
    | AKIA[0-9A-Z]{16}                                   # AWS access key id
    | -----BEGIN\ [A-Z\ ]*PRIVATE\ KEY-----              # start of a private key block
    | (?<=://)[^/\s:@]+:[^/\s@]+(?=@)                    # user:password inside a URL
    """)


def redact(text: str) -> str:
    return SECRET.sub("[redacted]", text)
