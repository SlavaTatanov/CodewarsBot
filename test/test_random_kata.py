from unittest import TestCase
from CodewarsTelegramBot.random_kata import get_lang_list


class TestRandomKata(TestCase):
    def test_get_lang_list(self):
        test_item_1 = {"Python": "High", "JavaScript": "Normal", "Haskell": "Very High"}
        self.assertEqual(get_lang_list(test_item_1), ["Python", "Python", "JavaScript",
                                                      "Haskell", "Haskell", "Haskell"])


