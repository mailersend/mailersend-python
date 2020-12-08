import mailersend
import unittest


class BasicTests(unittest.TestCase):
    def test_api_base_not_none(self):
        """
        Basic checking
        """
        self.assertIsNotNone(mailersend.API_BASE)

    def test_can_instantiate_object(self):
        self.assertIsNotNone(mailersend.NewApiClient())

    def test_can_make_api_call(self):
        pass


if __name__ == "__main__":
    unittest.main()
