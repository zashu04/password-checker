import math
import random
import string
import re

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "1234567", "1234567890",
    "qwerty", "abc123", "million2", "000000", "1234", "iloveyou", "aaron431",
    "password1", "qqww1122", "123123", "omgpop", "123321", "654321", "qwertyuiop",
    "qwerty123", "admin", "letmein", "welcome", "monkey", "dragon", "master",
    "sunshine", "princess", "shadow", "superman", "michael", "football", "baseball",
    "charlie", "donald", "password2", "qwerty1", "123qwe", "zxcvbnm", "1q2w3e4r",
    "hello", "freedom", "whatever", "qazwsx", "trustno1", "jordan23", "harley",
    "ranger", "iwantu", "batman", "soccer", "hockey", "killer", "george",
    "hunter", "buster", "thomas", "robert", "tigger", "cheese", "1q2w3e",
    "pass", "login", "test", "access", "coffee", "asdfgh", "mustang",
    "andrew", "phoenix", "jessica", "pepper", "daniel", "joshua", "samsung",
    "blink182", "myspace1", "dallas", "manchester", "1111111", "222222",
    "333333", "444444", "555555", "666666", "777777", "888888", "999999",
    "11111111", "22222222", "33333333", "55555555", "0987654321", "9876543210",
    "zxcvbn", "asdfghjkl", "fuckyou", "passw0rd", "password123", "p@ssword",
    "p@ssw0rd", "admin123", "root", "toor", "changeme", "secret", "abc",
    "qweasdzxc", "1qaz2wsx", "1qazxsw2", "admin1", "pass123", "pass1234",
    "password!", "iloveyou1", "123abc", "abcd1234", "monkey1", "shadow1"
}


def calculate_entropy(password: str) -> float:
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32
    if charset_size == 0:
        return 0.0
    return len(password) * math.log2(charset_size)


def check_password_strength(password: str) -> dict:
    if not password:
        return {
            "score": 0,
            "label": "None",
            "color": "gray",
            "entropy": 0.0,
            "checks": {},
            "feedback": [],
            "is_common": False,
        }

    checks = {
        "length_8":     len(password) >= 8,
        "length_12":    len(password) >= 12,
        "length_16":    len(password) >= 16,
        "has_lower":    bool(re.search(r'[a-z]', password)),
        "has_upper":    bool(re.search(r'[A-Z]', password)),
        "has_digit":    bool(re.search(r'\d', password)),
        "has_symbol":   bool(re.search(r'[^a-zA-Z0-9]', password)),
        "no_repeating": not bool(re.search(r'(.)\1{2,}', password)),
        "no_sequential": not bool(
            re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij)', password.lower())
        ),
    }

    is_common = password.lower() in COMMON_PASSWORDS

    score = 0
    feedback = []

    # Length scoring (up to 35 pts)
    if checks["length_16"]:
        score += 35
    elif checks["length_12"]:
        score += 25
    elif checks["length_8"]:
        score += 15
    else:
        score += len(password) * 2
        feedback.append("Use at least 8 characters")

    # Character variety (up to 40 pts)
    variety_points = sum([checks["has_lower"], checks["has_upper"], checks["has_digit"], checks["has_symbol"]]) * 10
    score += variety_points

    if not checks["has_lower"]:
        feedback.append("Add lowercase letters")
    if not checks["has_upper"]:
        feedback.append("Add uppercase letters")
    if not checks["has_digit"]:
        feedback.append("Add numbers")
    if not checks["has_symbol"]:
        feedback.append("Add special characters (!@#$...)")

    # Pattern penalties (up to 25 pts bonus)
    if checks["no_repeating"]:
        score += 12
    else:
        feedback.append("Avoid repeating characters (e.g. 'aaa')")

    if checks["no_sequential"]:
        score += 13
    else:
        feedback.append("Avoid sequential patterns (e.g. '123', 'abc')")

    # Common password penalty
    if is_common:
        score = min(score, 15)
        feedback.insert(0, "This is a commonly known password — avoid it!")

    score = max(0, min(score, 100))

    entropy = calculate_entropy(password)

    if score >= 75:
        label, color = "Very Strong", "#00e676"
    elif score >= 50:
        label, color = "Strong", "#69f0ae"
    elif score >= 25:
        label, color = "Fair", "#ffab40"
    else:
        label, color = "Weak", "#ff5252"

    return {
        "score": score,
        "label": label,
        "color": color,
        "entropy": round(entropy, 1),
        "checks": checks,
        "feedback": feedback,
        "is_common": is_common,
    }


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    length = max(4, min(length, 128))

    charset = ""
    required_chars = []

    if use_lower:
        charset += string.ascii_lowercase
        required_chars.append(random.choice(string.ascii_lowercase))
    if use_upper:
        charset += string.ascii_uppercase
        required_chars.append(random.choice(string.ascii_uppercase))
    if use_digits:
        charset += string.digits
        required_chars.append(random.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        charset += symbols
        required_chars.append(random.choice(symbols))

    if not charset:
        charset = string.ascii_letters + string.digits

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [random.choice(charset) for _ in range(max(0, remaining_length))]
    random.shuffle(password_chars)

    return "".join(password_chars)
