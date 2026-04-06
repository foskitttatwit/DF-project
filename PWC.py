import hashlib
import re
import sys

#Function to load common passwords from a file into a set for quick lookup
def load_common_passwords(filename="PsswdTest.txt"):
    try:
        with open(filename, "r") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Using empty list.")
        return set()
    
#define a global variable to hold the common passwords set
COMMON_PASSWORDS = load_common_passwords()

#get the password input from the user
def get_password():
   pwd = input("Enter password: ")
   return pwd

#Function to allow user to select hashing algorithm
def select_algorithm():
    choices = {
        "1": "MD5",
        "2": "SHA-1",
        "3": "SHA-256",
        "4": "SHA-512",
        "5": "No Hash",
        "md5": "MD5",
        "sha1": "SHA-1",
        "sha256": "SHA-256",
        "sha512": "SHA-512",
        "no hash": "No Hash",
    }
    prompt = (
        "Select hashing algorithm:\n"
        "  1) MD5\n"
        "  2) SHA-1\n"
        "  3) SHA-256\n"
        "  4) SHA-512\n"
        "  5) No Hash\n"
        "Enter choice (1-5 or name): "
    )
    while True:
        choice = input(prompt).strip().lower()
        if choice in choices:
            return choices[choice]
        print("Invalid selection. Try again.")

#Function to compute the hash of the password using the selected algorithm
def compute_hash(password: str, algorithm: str) -> str:
    data = password.encode("utf-8")
    alg = algorithm.lower().replace("-", "")
    if alg == "md5":
        h = hashlib.md5(data)
    elif alg == "sha1":
        h = hashlib.sha1(data)
    elif alg == "sha256":
        h = hashlib.sha256(data)
    elif alg == "sha512":
        h = hashlib.sha512(data)
    elif alg == "no hash":
        return "No Hash"
    else:
        raise ValueError("Unsupported algorithm")
    return h.hexdigest()

#Function to check for repeated characters in the password
def has_repeated_chars(password: str) -> bool:
    if len(password) < 4:
        return False
    return len(set(password)) <= max(1, len(password) // 3)

#Function to check for common sequential patterns in the password
def has_sequential_pattern(password: str) -> bool:
    sequences = [
        "123", "234", "345", "456", "567", "678", "789",
        "abc", "bcd", "cde", "def", "efg",
        "qwe", "wer", "ert", "rty", "tyu", "yui"
    ]
    pwd_lower = password.lower()
    return any(seq in pwd_lower for seq in sequences)

#Function to check if the password is a common password or contains common patterns
def is_common_password(password: str) -> bool:
    pwd_lower = password.lower()
    return pwd_lower in COMMON_PASSWORDS or any(common in pwd_lower for common in COMMON_PASSWORDS)

#Function to evaluate password strength and risk factors
def evaluate_password(password: str):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))
    common_match = is_common_password(password)
    repeated_chars = has_repeated_chars(password)
    sequential_pattern = has_sequential_pattern(password)

    #start with a base risk score of 0 and add points based on various factors
    risk = 0

    if length < 4:
        risk += 60
    elif length < 6:
        risk += 40
    elif length <= 8:
        risk += 15
    elif length <= 11:
        risk += 5
    #if missing character types, add 10 points for each missing type
    missing = 0
    for present in (has_lower, has_upper, has_digit, has_special):
        if not present:
            missing += 1.5
    risk += missing * 10  # up to +60

    #if the password is common or contains common patterns, add a significant risk
    if common_match:
        risk += 40

    #if the password has repeated characters or sequential patterns, add additional risk
    if repeated_chars:
        risk += 15
    if sequential_pattern:
        risk += 15

    risk = min(100, risk)

    complexity = {
        "lowercase": has_lower,
        "uppercase": has_upper,
        "digits": has_digit,
        "special": has_special,
    }

    return {
        "length": length,
        "complexity": complexity,
        "is_common": common_match,
        "repeated_chars": repeated_chars,
        "sequential_pattern": sequential_pattern,
        "password_risk": risk,
    }
#Function to assign a risk score to the selected hashing algorithm
def hash_risk_score(algorithm: str):
    alg = algorithm.upper()
    if alg == "NO HASH":
        return 100
    if alg == "MD5":
        return 60
    if alg == "SHA-1":
        return 45
    if alg == "SHA-256":
        return 20
    if alg == "SHA-512":
        return 10
    return 50

#add up the password risk and hash risk with a weighted average to get an overall risk score
#password is more important than the hash choice, so we weight it at 70% and the hash risk at 30%
def combine_risks(password_risk: int, hash_risk: int):
    overall = int(min(100, password_risk * 0.7 + hash_risk * 0.3))
    return overall

#define risk level labels based on the overall risk score
def risk_level_label(score: int):
    if score <= 10:
        return "Negligible"
    if score <= 33:
        return "Low"
    if score <= 66:
        return "Medium"
    if score <= 99:
        return "High"
    return "Critical Vulnerability"

#define password strength labels based on the password risk score
def password_strength_label(score: int):
    if score <= 25:
        return "Strong"
    if score <= 55:
        return "Moderate"
    return "Weak"

#recommendations based on the evaluation results and selected algorithm
def recommendations(eval_res, alg):
    recs = []

    if eval_res["length"] < 12:
        recs.append("Use a longer password or passphrase (12+ characters).")

    missing = [k for k, v in eval_res["complexity"].items() if not v]
    if missing:
        recs.append("Increase complexity by including: " + ", ".join(missing) + ".")

    if eval_res["is_common"]:
        recs.append("Avoid common or easily guessed passwords.")

    if eval_res["repeated_chars"]:
        recs.append("Avoid repeated or overly predictable character patterns.")

    if eval_res["sequential_pattern"]:
        recs.append("Avoid sequential patterns such as '123' or 'abc'.")

    alg_upper = alg.upper()
    if alg_upper in ("MD5"):
        recs.append("Use a stronger algorithm, MD5 is fast but vulnerable.")
    elif alg_upper in ("SHA-1"):
        recs.append("Use a stronger algorithm, SHA-1 has been deprecated because of vulnerabilities.")
    elif alg_upper in ("SHA-256"):
        recs.append("Good choice! SHA-256 is considered secure and is the industry standard.")
    elif alg_upper in ("SHA-512"):
        recs.append("Excellent choice! SHA-512 is one of the most secure hashing algorithms available.")
    elif alg_upper == "NO HASH":
        recs.append("Not hashing the password is not recommended.")


    return recs

#print a detailed report of the password evaluation, including all factors and recommendations
def print_report(password_eval, algorithm, hashed, hash_risk, overall_score, psswd):
    print("\n--- Password Security Report ---")
    print(f"Password entered: {psswd}")
    print(f"Password length: {password_eval['length']}")
    print(f"Password strength: {password_strength_label(password_eval['password_risk'])}")

    comp = password_eval["complexity"]
    print("Complexity:")
    print(f"  Lowercase: {'Yes' if comp['lowercase'] else 'No'}")
    print(f"  Uppercase: {'Yes' if comp['uppercase'] else 'No'}")
    print(f"  Digits:    {'Yes' if comp['digits'] else 'No'}")
    print(f"  Special:   {'Yes' if comp['special'] else 'No'}")

    print(f"Common password pattern: {'Yes' if password_eval['is_common'] else 'No'}")
    print(f"Repeated character pattern: {'Yes' if password_eval['repeated_chars'] else 'No'}")
    print(f"Sequential pattern: {'Yes' if password_eval['sequential_pattern'] else 'No'}")
    print(f"Selected hash algorithm: {algorithm}")
    print(f"Generated hash: {hashed}")
    print(f"Password risk score (0-100): {password_eval['password_risk']}")
    print(f"Hash algorithm risk (0-100): {hash_risk}")
    print(f"Final overall risk score (0-100): {overall_score}")
    print(f"Risk level: {risk_level_label(overall_score)}")

    print("\nRecommendations:")
    for r in recommendations(password_eval, algorithm):
        print(" -", r)
    print("--------------------------------\n")

#main function to orchestrate the password evaluation process
def main():
    pwd = get_password()
    if pwd == "":
        print("No password entered. Exiting.")
        sys.exit(1)

    alg = select_algorithm()
    hashed = compute_hash(pwd, alg)
    eval_res = evaluate_password(pwd)
    h_risk = hash_risk_score(alg)
    overall = combine_risks(eval_res["password_risk"], h_risk)

    print_report(eval_res, alg, hashed, h_risk, overall, pwd)

if __name__ == "__main__":
    main()