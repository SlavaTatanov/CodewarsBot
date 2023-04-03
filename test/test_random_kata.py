from unittest import TestCase
from CodewarsTelegramBot.random_kata import get_lang_list, get_lang_levels


class TestRandomKata(TestCase):
    def test_get_lang_list(self):
        test_item_1 = {"Python": "High", "JavaScript": "Normal", "Haskell": "Very High"}
        self.assertEqual(get_lang_list(test_item_1), ["Python", "Python", "JavaScript",
                                                      "Haskell", "Haskell", "Haskell"])

    def test_get_lang_levels(self):
        test_item = {"Haskell": {"min": 8, "max": 6}, "Python": {"min": 7, "max": 4}}
        self.assertEqual(get_lang_levels(test_item), {"Haskell": [6, 7, 8], "Python": [4, 5, 6, 7]})


