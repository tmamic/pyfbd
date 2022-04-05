"""
@what:  Utility for running all tests at once.
@why:   QA is important.
@who:   TM
@when:  2022-04-05
"""

# built-in
import glob
import unittest

if __name__ != "__main__":
    raise Exception("Don't import me!")

targets = glob.glob("*_tests.py")
module_names = (name.split(".")[0] for name in targets)
tests = (unittest.defaultTestLoader.loadTestsFromName(name) for name in module_names)
suite = unittest.TestSuite(tests)
runner = unittest.TextTestRunner()
runner.run(suite)