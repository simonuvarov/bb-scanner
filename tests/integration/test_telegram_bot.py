import unittest

from lib.notifier.telegram import Bot


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.bot = Bot("")

    def test_send_message(self):
        self.bot.send_message("Hi")

if __name__ == '__main__':
    unittest.main()