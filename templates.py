start = """
Привет!
Я игровой бот Bunker

Мои команды:
Помощь
/start
/help

Присоединиться к игре
/join
/join код

Выйти из игры
/leave

Заупстить игру
/run

Проголосовать за игрока
/vote номер
"""

specialization = [
    "Маляр",
    "Программист",
    "Художник",
    "Кладовщик",
    "Тренер",
    "Вожатый",
    "Кассир",
    "Руководитель",
    "Детектив"
]

bio = (
    "Женщина",
    "Женщина, беременна",
    "Мужчина",
    "Трансексуал",
    "Вертолёт Апачи"
)

age = tuple(range(16, 90))

sex = [
    "Асексульный",
    "Бисексуальный",
    "Гетеросексуальный"
]

health = (
    "Косоглазие",
    "Спид",
    "Аритмия",
    "Однорукий",
    "Одноглазый",
    "Шизофрения"
)

hobby = (
    "Дайвинг",
    "Прогулки",
    "Поесть",
    "Качалка",
    "Музыкант",
    "Сигары"
)

phobia = (
    "Пауки",
    "Жуки",
    "Нет фобии",
    "Собаки"
)

personality = (
    "Назойливый",
    "Душнила",
    "Спокойный",
    "Хладнокровный",
    "Бедовый"
)

info = (
    "Клянётся, что видел НЛО",
    "У Вас трясуться руки",
    "Нет"
)

knowledge = (
    "Координаты с продовольствием",
    "Координаты лаборатории",
    "Координаты другого бункера",
    "Координаты продуктовой базы",
    "Координаты города"
)

inventory = (
    "Нож",
    "Продовольствие",
    "Рация",
    "Верёвка",
    "Химзащита",
    "Галоши",
    "Средства против насекомых",
    "Открывашка"
)

action = (
    "Один раз за игру выбранный игрок забывает знание",
    "Один раз за игру выбранный игрок будет молчать этот раунд",
    # "Вы можете вернуть игрока в игру"
    # "Один раз за игру Вы можете голосовать дважды"
)

condition = (
    "Когда Вы выбываете в бункере появляются пауки",
    "Когда Вы выбываете в бункере появляются жуки",
    "Когда Вы выбываете в бункере теряется продовольствие",
    "Нет"
)

stats = """
Профессия: \n{specialization}\n
Био: \n{bio}\n
Здоровье: \n{health}\n
Хобби: \n{hobby}\n
Фобия: \n{phobia}\n
Характер: \n{personality}\n
Доп. информация: \n{info}\n
Знание: \n{knowledge}\n
Багаж: \n{inventory}\n
Действие: \n{action}\n
Условие: \n{condition}\n
"""