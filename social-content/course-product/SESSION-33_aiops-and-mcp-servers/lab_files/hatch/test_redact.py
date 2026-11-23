import pytest
from redact import redact

@pytest.mark.parametrize("line,leaked", [
    ("password=abc123", "abc123"), ("Password: abc123", "abc123"), ("token=abc123 tail", "abc123"), ("api_key=abc123", "abc123"),
    ('password="abc 123"', "123"), ("password='abc 123'", "123"), ("Authorization: Bearer abc123", "abc123"),
    ("key AKIAIOSFODNN7EXAMPLE used", "AKIAIOSFODNN7EXAMPLE"), ("postgres://app:abc123@db/x", "abc123"),
    ("-----BEGIN RSA PRIVATE KEY-----", "PRIVATE KEY"),
])
def test_secrets_are_removed(line, leaked):
    assert leaked not in redact(line)

@pytest.mark.parametrize("line", ["tokens=3 used", "booking ok id=1", "retrying in 5s", "user asha logged in", "https://example.com/path"])
def test_normal_lines_untouched(line):
    assert redact(line) == line
