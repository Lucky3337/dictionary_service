from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from dictionary.models import (
    User,
    UserToken,
    EnglishWord,
    RussianWord,
    TranslationRussianEnglish,
    TranslationEnglishRussian
)


class ModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(telegram_id=123)
        self.user_token = UserToken.objects.create(user=self.user)

        self.russian_word1 = RussianWord.objects.create(word='Ручка')
        self.english_word1 = EnglishWord.objects.create(word='Hand')
        self.russian_english = TranslationRussianEnglish.objects.create(
            user=self.user,
            russian_word=self.russian_word1
        )
        self.russian_english.english_word.add(self.english_word1)

        self.russian_word2 = RussianWord.objects.create(word='дверь')
        self.english_word2 = EnglishWord.objects.create(word='door')
        self.english_russian = TranslationEnglishRussian.objects.create(
            user=self.user,
            english_word=self.english_word2
        )
        self.english_russian.russian_word.add(self.russian_word2)

    def test_unique_user_by_telegram_id(self):
        error = False
        try:
            user = User.objects.create(telegram_id=123)
        except IntegrityError:
            error = True
        self.assertEqual(error, True)

    def test_unique_user_token_by_user(self):
        error = False
        try:
            user_token = UserToken.objects.create(user=self.user)
        except IntegrityError:
            error = True
        self.assertEqual(error, True)

    def test_english_word(self):
        error = False
        try:
            word = EnglishWord.objects.create(word='ёЖИК')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

        error = False
        try:
            word = EnglishWord.objects.create(word='Apple')
        except ValidationError:
            error = True
        self.assertEqual(error, False)
        word = EnglishWord.objects.create(word='tree')
        self.assertEqual(word.word, 'tree')

        error = False
        try:
            word = EnglishWord.objects.create(word='tree')
        except IntegrityError:
            error = True
        self.assertEqual(error, True)

    def test_russian_word(self):
        word = RussianWord.objects.create(word='ЁЖИК')
        self.assertEqual(word.word, 'ЁЖИК')

        error = False
        try:
            word = RussianWord.objects.create(word='Apple')
        except ValidationError:
            error = True
        self.assertEqual(error, True)

        error = False
        try:
            word = RussianWord.objects.create(word='ЁЖИК')
        except IntegrityError:
            error = True
        self.assertEqual(error, True)

    def test_unique_user_and_russian_word(self):
        russian, _ = RussianWord.objects.get_or_create(word='Ручка')

        english, _ = EnglishWord.objects.get_or_create(word='Hand')
        error = False
        try:
            russian_english = TranslationRussianEnglish.objects.create(
                user=self.user,
                russian_word=russian
            )
        except IntegrityError:
            error = True
        self.assertEqual(error, True)

    def test_unique_user_and_english_word(self):
        russian, _ = RussianWord.objects.get_or_create(word='дверь')

        english, _ = EnglishWord.objects.get_or_create(word='door')
        error = False
        try:
            english_russian = TranslationEnglishRussian.objects.create(
                user=self.user,
                english_word=english
            )
        except IntegrityError:
            error = True
        self.assertEqual(error, True)


