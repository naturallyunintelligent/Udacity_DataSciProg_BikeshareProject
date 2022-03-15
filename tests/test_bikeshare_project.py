# following testing tutorial: https://realpython.com/python-testing/

import unittest

# from src.bikeshare_project import tidy_input
import src.bikeshare_project as bp

# TODO: Some kind of issue with path here?,
#  as when running test it can't find constants.py? more info?...
# https://stackoverflow.com/questions/51049663/
# python3-6-error-modulenotfounderror-no-module-named-src
# https://realpython.com/lessons/package-initialization/


class TestTidyInput(unittest.TestCase):
    def test_whitespace(self):
        self.assertEqual(
            bp.tidy_input("whitespace  "), "whitespace", "Not removing whitespace?"
        )


if __name__ == "__main__":
    unittest.main()
