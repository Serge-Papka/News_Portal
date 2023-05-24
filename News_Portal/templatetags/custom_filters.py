from django import template


class MyExceptions(Exception):
    pass


class NotAString(MyExceptions):
    def __str__(self):
        return """Ошибка! Фильтр 'censor' применяется не к строке"""


# список слов, которые нужно цензуровать
bad_words = ['редиска', 'бяка', 'мудак', 'урод', 'дебил', 'идиот', 'мат_тест']

register = template.Library()


@register.filter()
def censor(some_text, bad=bad_words):
    # print(type(some_text)

    if not isinstance(some_text, str):
        raise NotAString()

    for bad_word in bad:
        i = -2
        while i != -1:
            i = some_text.lower().find(bad_word)
            if i >= 0:
                some_text = some_text[0:i + 1] + '*' * (len(bad_word) - 1) + some_text[i + len(bad_word):]
                print(type(some_text))
    return some_text
