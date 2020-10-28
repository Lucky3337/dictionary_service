from django.contrib import admin

from .models import (
    User,
    UserToken,
    EnglishWord,
    RussianWord,
    TranslationRussianEnglish,
    TranslationEnglishRussian
)


admin.site.register(User)
admin.site.register(UserToken)
admin.site.register(EnglishWord)
admin.site.register(RussianWord)
admin.site.register(TranslationRussianEnglish)
admin.site.register(TranslationEnglishRussian)
