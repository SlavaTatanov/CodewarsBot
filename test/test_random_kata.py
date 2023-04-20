from unittest import TestCase
from CodewarsTelegramBot.random_kata import get_lang_list, get_lang_levels, create_lang_dict, create_random_kata,\
    random_kata
from CodewarsTelegramBot.database.models import Langs


class TestRandomKata(TestCase):
    def test_get_lang_list(self):
        test_item_1 = {"Python": {"min": 8, "max": 6, "priority": "High"},
                       "JavaScript": {"min": 7, "max": 4, "priority": "Normal"},
                       "Haskell": {"min": 7, "max": 4, "priority": "Very High"}}
        self.assertEqual(get_lang_list(test_item_1), ["Python", "Python", "JavaScript",
                                                      "Haskell", "Haskell", "Haskell"])

    def test_get_lang_levels(self):
        test_item = {"Haskell": {"min": 8, "max": 6, "priority": "High"},
                     "Python": {"min": 7, "max": 4, "priority": "Normal"}}
        self.assertEqual(get_lang_levels(test_item), {"Haskell": [6, 7, 8], "Python": [4, 5, 6, 7]})

    def test_create_lang_dict(self):
        test_item1 = Langs(lang="Python", lang_min=6, lang_max=4, lang_priority="Normal")
        test_item2 = [test_item1, Langs(lang="Haskell", lang_min=8, lang_max=6, lang_priority="High")]
        self.assertEqual(create_lang_dict([test_item1]), {"Python": {"min": 6, "max": 4, "priority": "Normal"}})
        self.assertEqual(create_lang_dict(test_item2), {"Python": {"min": 6, "max": 4, "priority": "Normal"},
                                                        "Haskell": {"min": 8, "max": 6, "priority": "High"}})

    def test_create_random_kata(self):
        test_langs = ["Python", "Python", "Haskell", "Haskell", "Haskell"]
        test_levels = {"Haskell": [6, 7, 8], "Python": [4, 5, 6, 7]}
        for res in [create_random_kata(test_langs, test_levels),
                    random_kata([Langs(lang="Python", lang_min=6, lang_max=4, lang_priority="Normal")])]:
            self.assertEqual(type(res), dict)
            self.assertTrue("Haskell" == res["lang"] or "Python" == res["lang"])
            self.assertTrue("lang" in res.keys() and "level" in res.keys())

