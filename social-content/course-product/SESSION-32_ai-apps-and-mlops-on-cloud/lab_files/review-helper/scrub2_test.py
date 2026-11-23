from scrub2 import scrub
cases = {"call 9876543210 now":"[number]", "+91 98765 43210":"[number]", "98765-43210":"[number]", "card 4111111111111111":"[number]",
 "card 4111 1111 1111 1111":"[number]", "card 4111-1111-1111-1111":"[number]", "id 12345678901 here":"[number]",
 "email asha@example.com ok":"[email]", "Room 204, 3 nights, paid 5000":"Room 204, 3 nights, paid 5000", "booked on 2026-11-23":"booked on 2026-11-23",
 "ref ABC1234567890":"ref ABC1234567890", "Name Asha Verma":"Name Asha Verma"}
for t, must in cases.items():
    out = scrub(t); print("OK " if must in out else "BAD", repr(t), "->", repr(out))
