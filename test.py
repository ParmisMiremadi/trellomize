import unittest
from user import is_valid_email, is_valid_username, is_valid_password


class test(unittest.TestCase):
    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertFalse(is_valid_email("testexample.com"))
        self.assertFalse(is_valid_email("test@examplecom"))
        self.assertFalse(is_valid_email("testexamplecom"))


    def test_is_valid_username(self):
        self.assertTrue(is_valid_username("test1234"))
        self.assertFalse(is_valid_username("test"))


    def test_is_valid_password(self):
        self.assertTrue(is_valid_password("12349876"))
        self.assertFalse(is_valid_username("fg65"))

        
if __name__ == "__main__":
    unittest.main()

