def get_text(emotion_class):
    if emotion_class == 1:
        return 'Плохое настроение'
    elif emotion_class == 0:
        return 'Отличное настроение'
    else:
        return 'Лицо не распознано, попробуйте снова'


def emotion_history_text(emotion_info, date_range=None):
    intro = {
        None: 'За все время у Вас было:\n',
        '7 days': 'За последнюю неделю у Вас было:\n',
        '1 month': 'За последний месяц у Вас было:\n'
    }

    if len(emotion_info) == 0:
        return 'Наблюдения не найдены'
    elif len(emotion_info) == 1:
        emotion, count = emotion_info[0]
        neg, pos = (count, 0) if emotion == 'negative' else (0, count)
    else:
        neg, pos = emotion_info[0][1], emotion_info[1][1]

    history = f'▫Хорошее настроение: {pos} {"раза" if 2 <= pos <= 4 else "раз"}\n' \
              f'▫Плохое настроение: {neg} {"раза" if 2 <= neg <= 4 else "раз"}'

    return intro[date_range] + history
