
# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, maintainability problems, and style violations.

## 2. What did the three tools identify?

Pylint identified code-quality and maintainability issues, including mutable default arguments, naming problems, unused variables, and exception-handling concerns. Bandit identified unsafe coding patterns such as dynamic expression evaluation, shell execution, hardcoded secrets, and insecure random-number generation. Flake8 identified formatting and PEP 8 violations.

## 3. What changes were made?

The program was updated to remove unsafe expression evaluation and shell execution, remove the hardcoded secret, use SHA-256 for passenger hashing, generate boarding PINs with the `secrets` module, improve exception handling, remove unused code, and correct formatting.

## 4. How were the changes verified?

The program was run after the changes. Pylint reported a final score of 10.00/10, Bandit reported zero issues, and Flake8 produced no output.

## 5. What did I learn?

I learned that static analysis tools detect different categories of problems. Using multiple tools helps identify issues that may be missed by a single tool. Fixing these findings improves readability, consistency, and security, while rerunning the tools helps verify that the changes meet the expected standards.
