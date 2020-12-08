import mailersend
import unittest


class BasicTests(unittest.TestCase):
    def test_api_base_not_none(self):
        """
        Basic version checking
        """
        self.assertIsNotNone(mailersend.API_BASE)


if __name__ == "__main__":
    unittest.main()
