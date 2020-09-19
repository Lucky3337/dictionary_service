import uuid

from django.db import models

from dictionary.validators import only_english_character, only_russian_character


class TimestampMixin(models.Model):
    """Abstract class with datetime of create_at and update_at"""
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AbstractBaseModel(models.Model):
    """Abstract class with primary key of id"""
    id = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class User(AbstractBaseModel, TimestampMixin):
    """Telegram users"""
    telegram_id = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)


class UserToken(AbstractBaseModel, TimestampMixin):
    """Token for telegram users"""
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class EnglishWord(AbstractBaseModel, TimestampMixin):
    """Words are english"""
    word = models.CharField(max_length=120, unique=True, validators=[only_english_character])

    def __str__(self):
        return self.word


class RussianWord(AbstractBaseModel, TimestampMixin):
    """Translations for english words"""
    word = models.CharField(max_length=120, unique=True, validators=[only_russian_character])

    def __str__(self):
        return self.word


class TranslationRussianEnglish(AbstractBaseModel, TimestampMixin):
    """Translation words pair russian to english"""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    russian_word = models.ForeignKey("RussianWord", on_delete=models.CASCADE)
    english_word = models.ManyToManyField("EnglishWord")

    class Meta:
        unique_together = [['user', 'russian_word']]


class TranslationEnglishRussian(AbstractBaseModel, TimestampMixin):
    """Translation words pair english to russian"""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    english_word = models.ForeignKey("EnglishWord", on_delete=models.CASCADE)
    russian_word = models.ManyToManyField("RussianWord")

    class Meta:
        unique_together = [['user', 'english_word']]