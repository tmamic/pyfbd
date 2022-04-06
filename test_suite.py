"""
@what:  Utility for running all tests at once.
@why:   QA is important.
@who:   TM
@when:  2022-04-05
"""

# built-in
import unittest

if __name__ != "__main__":
    raise Exception("Don't import me!")

suite = unittest.TestLoader().discover('.', pattern = "*_tests.py")
unittest.TextTestRunner(verbosity=2).run(suite)