#!/usr/bin/env python3
import sys, json, math, re, string

def entropy(password):
    chars = 0
    if re.search(r'[a-z]', password): chars += 26
    if re.search(r'[A-Z]', password): chars += 26
    if re.search(r'[0-9]', password): chars += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): chars += 32
    if chars == 0: return 0
    return len(password) * math.log2(chars)

def common_patterns(password):
    patterns = []
    common_passwords = {"password", "123456", "12345678", "qwerty", "admin", "letmein", "welcome", "monkey", "dragon", "master", "passw0rd", "iloveyou", "sunshine", "princess", "football"}
    if password.lower() in common_passwords:
        patterns.append("common_password")
    if re.search(r'(.)\1{2,}', password):
        patterns.append("repeated_chars")
    if re.search(r'(123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
        patterns.append("sequential_chars")
    if len(set(password)) < len(password) * 0.5:
        patterns.append("low_uniqueness")
    return patterns

def audit(password):
    e = entropy(password)
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    patterns = common_patterns(password)

    if length < 8: strength = "VERY_WEAK"
    elif length < 10: strength = "WEAK"
    elif e < 40: strength = "WEAK"
    elif e < 60: strength = "MODERATE"
    elif e < 80: strength = "STRONG"
    else: strength = "VERY_STRONG"

    if patterns:
        strength = "WEAK" if strength in ("MODERATE", "STRONG", "VERY_STRONG") else strength

    crack_time = "instantly" if e < 28 else "seconds" if e < 36 else "minutes" if e < 44 else "hours" if e < 52 else "days" if e < 60 else "months" if e < 68 else "years" if e < 76 else "centuries"

    return {
        "password_length": length,
        "entropy_bits": round(e, 1),
        "has_lowercase": has_lower,
        "has_uppercase": has_upper,
        "has_digit": has_digit,
        "has_special": has_special,
        "patterns_detected": patterns,
        "strength": strength,
        "estimated_crack_time": crack_time,
        "recommendations": []
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        password = input("Enter password to audit: ")
    else:
        password = sys.argv[1]
    result = audit(password)
    result["recommendations"] = []
    if result["strength"] in ("VERY_WEAK", "WEAK"):
        result["recommendations"] = [
            "Use at least 12 characters",
            "Mix upper, lower, digits and special chars",
            "Avoid common words and patterns",
            "Use a password manager"
        ]
    print(json.dumps(result, indent=2))
