import re
from django import template

register = template.Library()

# Список запрещённых слов (можешь дополнить)
CENSORED_WORDS = [
    'редиска',
    'плохой',
    'дурак',
    'балбес',
    # добавь другие слова по необходимости
]

@register.filter(name='censor')
def censor(value):
    """
    Фильтр заменяет все нецензурные слова из списка CENSORED_WORDS
    на формат: первая буква + звёздочки (длина слова - 1).
    Регистр первой буквы сохраняется.
    Применяется только к строкам, иначе вызывает TypeError.
    """
    if not isinstance(value, str):
        raise TypeError(
            f"Фильтр censor применяется только к строковым переменным, "
            f"а получен тип {type(value).__name__}"
        )

    def replace_match(match):
        word = match.group(0)  # найденное слово с исходным регистром
        return word[0] + '*' * (len(word) - 1)

    # Для каждого запрещённого слова создаём регулярку и применяем замену
    result = value
    for word in CENSORED_WORDS:
        # \b – граница слова, re.IGNORECASE – независимо от регистра
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        result = pattern.sub(replace_match, result)
    return result