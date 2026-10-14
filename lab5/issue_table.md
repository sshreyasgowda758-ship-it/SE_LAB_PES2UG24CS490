
# Lab 5: Static Code Analysis — Issue Table

| Issue | Tool / Type | Original Location | Description | Fix Applied |
|---|---|---|---|---|
| Mutable default argument | Pylint / Bug | `bookFlightSeat` | The default `baggage_tags=[]` could share a mutable list across calls. | Changed the default to `None` and initialized a new list inside the function. |
| Unsafe expression evaluation | Pylint and Bandit / Security | `calculateBaggageFee` | `eval()` could execute arbitrary Python expressions. | Replaced it with a validated numeric surcharge calculation. |
| Shell command execution | Bandit / Security | `exportFlightManifest` | `os.system()` invoked a shell unnecessarily. | Removed the shell call and printed a confirmation directly. |
| Hardcoded secret | Bandit / Security | `main` | An API-like secret was embedded in the source and printed. | Removed the unused hardcoded secret and its print statement. |
| Weak hash algorithm | Bandit / Security | `generatePassengerHash` | MD5 is not appropriate when a stronger cryptographic hash is required. | Replaced MD5 with SHA-256. |
| Insecure random PIN generation | Bandit / Security | `generateBoardingPin` | `random.randint()` is not intended for security-sensitive random values. | Replaced it with `secrets.randbelow()`. |
| Broad exception handling | Pylint / Reliability | `cancelBooking` | A bare `except` hid unexpected errors. | Removed broad exception handling and checked whether the flight exists. |
| Incorrect comparison with `None` | Pylint and Flake8 / Style | `checkSeatAvailability` | Used `== None` instead of an identity comparison. | Changed the check to `is None`. |
| Unused imports and variables | Pylint and Flake8 / Maintainability | Multiple locations | Unused names made the code harder to maintain. | Removed unused imports and variables. |
| Formatting violations | Flake8 / Style | Multiple locations | Extra blank lines and trailing whitespace violated PEP 8. | Applied automatic formatting and reran Flake8. |

## Verification

- Original Pylint score: 4.00/10.
- Final Pylint score: 10.00/10.
- Final Bandit report: zero reported issues.
- Final Flake8 report: no output, indicating no reported violations.
