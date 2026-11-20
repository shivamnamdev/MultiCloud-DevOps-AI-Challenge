from datetime import date


def nights(check_in: str, check_out: str) -> int:
    """How many nights between two ISO dates (YYYY-MM-DD)."""
    a = date.fromisoformat(check_in)
    b = date.fromisoformat(check_out)
    if b <= a:
        raise ValueError("check_out must be after check_in")
    return (b - a).days
