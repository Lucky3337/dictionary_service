from django.test import TestCase
from django.core.exceptions import ValidationError

from dictionary.validators import only_english_character, only_russian_character


class ValidatorTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_only_english_character(self):
        res = only_english_character('dddd')
        self.assertIsNone(res)
        res = only_english_character('Apple is lorem IpSUSM ')
        self.assertIsNone(res)

        error = False
        try:
            res = only_english_character('s22 dasdfsfff 2 asd')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

        error = False
        try:
            res = only_english_character('Привет ')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

    def test_only_russian_character(self):
        res = only_russian_character('Привет')
        self.assertIsNone(res)
        res = only_russian_character('Привет как дела Шо как сам')
        self.assertIsNone(res)

        error = False
        try:
            res = only_russian_character('=Прривет ')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

        error = False
        try:
            res = only_russian_character('ааа33фы Hello ')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

