import re


def is_email(val, allow_none = True):
	if allow_none and len(val) == 0:
		return True
	return re.match(r"[^@]+@[^@]+\.[^@]+", val)


def is_phone(val, allow_none = True):
	if allow_none and len(val) == 0:
		return True
	return re.match(r"\d{3}-\d{3}-\d{3}", val)