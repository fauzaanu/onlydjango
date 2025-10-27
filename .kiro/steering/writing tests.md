---
inclusion: fileMatch
fileMatchPattern: "{**/tests.py,**/tests/*.py}"
---

# Guide for writing tests

For every View a test class must exist. This class will inherit from a base testcase or TestCase directly.

When logins are involved creating a base TestCase makes perfect sense as we wont have to repeat them over and over again.

If a view has post and get methods we must also have atleast 2 test functions within that views test class. More tests are always better.

>TLDR: For each view have a seperate test class