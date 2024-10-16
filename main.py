from typing import List, Dict, Tuple, Set, Callable, Self
from random import choice, random, randrange, seed, shuffle
import re
from string import ascii_lowercase
import os, sys

import telebot
from telebot.types import Message

import templates

TOKEN = os.environ.get("TOKEN")

class Player:
    def __init__(self, code, index:int, specialization: str, bio:str, health:str, hobby:str, phobia:str, personality:str, info:str, knowledge:str, inventory:str, action:str, condition):
        self.code = code
        self.index = index
        self.specialization = specialization
        self.bio = bio
        self.health = health
        self.hobby = hobby
        self.phobia = phobia
        self.personality = personality
        self.info = info
        self.knowledge = knowledge
        self.inventory = inventory
        self.action = action
        self.condition = condition
    
    def __str__(self):
        return "Player: " + ", ".join([
            self.code,
            self.index,
            self.specialization,
            self.bio,
            self.health,
            self.hobby,
            self.phobia,
            self.personality,
            self.info,
            self.knowledge,
            self.inventory,
            self.action,
            self.condition
        ])

    def __repr__(self):
        return str(self)

    @classmethod
    def random(cls, code, index:int):
        seed(code + str(index))
        return cls(
            code = code,
            index = index,
            specialization = choice(templates.specialization),
            bio = f"{choice(templates.bio)} / возраст: {choice(templates.age)} / {choice(templates.sex)}",
            health = choice(templates.health),
            hobby = choice(templates.hobby),
            phobia = choice(templates.phobia),
            personality = choice(templates.personality),
            info = choice(templates.info),
            knowledge = choice(templates.knowledge),
            inventory = choice(templates.inventory),
            action = choice(templates.action),
            condition = choice(templates.condition)
        )

class User:
    collection:Set[Self] = set()

    def __init__(self, username:str, chat_id:int):
        self.username = username
        self.chat_id = chat_id
        self.player = None
        self.game = None
        self.cancelled = False
        self.voted = False
        self.votes = 0

    @classmethod
    def create(cls, username:str, chat_id:int):
        user = cls(username, chat_id)
        cls.collection.add(user)
        return user

    @classmethod
    def find(cls, username:str):
        return next((u for u in cls.collection if u.username == username), None)

    @classmethod
    def get(cls, username:str, chat_id:int):
        user = next((u for u in cls.collection if u.username == username), None)
        if user is None:
            user = cls(username, chat_id)
            cls.collection.add(user)
        return user

class Game:
    collection:Set[Self] = set()

    def __init__(self, code:str):
        self.code = code
        self.users:List[User] = []
        self.host:User = None
        self.round = 0
        self.is_started = False
        self.is_finished = False
        self.round = 0
    
    @classmethod
    def create(cls, code:str):
        game = cls(code)
        cls.collection.add(game)
        return game

    @classmethod
    def find(cls, code:str):
        return next((g for g in cls.collection if g.code == code), None)

    @classmethod
    def get(cls, code:str):
        game = next((g for g in cls.collection if g.code == code), None)
        if game is None:
            game = cls(code)
            cls.collection.add(game)
        return game

    @property
    def count(self):
        return len(self.users)

    @property
    def active(self):
        return sum(1 for u in self.users if not u.cancelled)
    
    @property
    def votes(self):
        return sum(1 for u in self.users if u.voted)

    def join(self, user:User):
        user.game = self
        if self.host is None: self.host = user
        self.users.append(user)
        return user

    def leave(self, user:User):
        user.game = None
        user.cancelled = False
        user.voted = False
        user.votes = 0
    
    def cancel(self, user:User):
        user.cancelled = True
        user.voted = False
        user.votes = 0

    def start(self):
        self.is_started = True

    def finish(self):
        self.is_finished = True
        self.host = None
        for u in self.users: self.leave(u)
        if self in Game.collection:
            Game.collection.remove(self)

    def test(self):
        return self.active <= 1 # TODO 2

    def step(self):
        for u in self.users:
            u.voted = False
            u.votes = 0

# Проверки
print("Token:", "FAILED" if TOKEN is None else "OK")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ["help", "start"])
def help(message:Message):
    bot.reply_to(message, templates.start)

@bot.message_handler(commands = ["join"])
def join(message:Message):
    cmd, *args = re.findall("[A-Za-z0-9]+", message.text)

    # Проверка игрока в игре
    user = User.get(message.from_user.full_name, message.chat.id)
    if user.game is not None:
        bot.reply_to(message, "Вы уже в игре: " + user.game.code)
        return

    # Поиск кода
    code = next(iter(args), None)
    if code is None:
        string = ascii_lowercase + "".join(map(str, range(9)))
        code = choice(string) + choice(string) + choice(string)
        bot.reply_to(message, "Код игры не указан")

    # Поиск игры
    game = Game.find(code)
    if game is None:
        game = Game.create(code)
        bot.reply_to(message, "Создана новая игра: " + code)
    
    # Присоединение
    game.join(user)
    for u in user.game.users:
        bot.send_message(u.chat_id, f"<{user.username}> присоединился к игре: {code}")

@bot.message_handler(commands = ["leave", "exit"])
def leave(message:Message):
    # Проверка в игре
    user = User.find(message.from_user.full_name)
    if user is None or user.game is None:
        bot.reply_to(message, "Вы не в игре")
        return

    bot.reply_to(message, "Вы вышли из игры")
    game = user.game

    # Проверка хоста
    if user.game.host == user:
        for u in user.game.users:
            bot.send_message(u.chat_id, "Хост вышел из игры - игра завершена")
        user.game.finish()
        return
    
    # Выход из игры
    game.leave(user)
    game.users.remove(user)
    for u in game.users:
        bot.send_message(u.chat_id, f"<{user.username}> вышел из игры")

@bot.message_handler(commands = ["run"])
def run(message:Message):
    user = User.find(message.from_user.full_name)
    
    # Проверка в игре
    if user is None or user.game is None:
        bot.reply_to(message, "Вы не в игре")
        return
    
    # Проверка хоста
    if user.game.host is not user:
        bot.reply_to(message, f"Только хост <{user.game.host.username}> может начать игру")
        return
    
    # Проверка количества игроков
    # TODO Вернуть
    # if user.game.count < 4:
    #     bot.reply_to(message, "Требуется хотя бы 4 игрока")

    # Запуск
    for i, u in enumerate(user.game.users): u.player = Player.random(user.game.code, i)
    for u in user.game.users:
        bot.send_message(u.chat_id, "Игра запущена")
        bot.send_message(u.chat_id, "\n".join(f"{i.username} {i.player.index}: {i.player.specialization}" for i in user.game.users))
        bot.send_message(u.chat_id, templates.stats.format(
            specialization = u.player.specialization,
            bio = u.player.bio,
            health = u.player.health,
            hobby = u.player.hobby,
            phobia = u.player.phobia,
            personality = u.player.personality,
            info = u.player.info,
            knowledge = u.player.knowledge,
            inventory = u.player.inventory,
            action = u.player.action,
            condition = u.player.condition
        ))
    user.game.start()

@bot.message_handler(commands = ["vote"])
def vote(message:Message):
    # Проверка в игре
    user = User.find(message.from_user.full_name)
    if user is None or user.game is None:
        bot.reply_to(message, "Вы не в игре")

    # Проверка проголосовал
    if user.voted:
        bot.reply_to(message, "Вы уже проголосовали")
        return

    game = user.game

    cmd, *args = re.findall("[A-Za-z0-9]+", message.text)
    vote:User = None
    if not args:
        bot.reply_to(message, "Вы пропустили голосование")
    else:
        # Проверка индекса за границами
        try:
            index = int(args[0])
        except:
            index = None
        vote = next((u for u in game.users if u.player.index == index), None)
        if vote is None or vote.cancelled:
            bot.reply_to(message, "Нет такого игрока, введите номер")
            bot.reply_to(message, "\n".join(f"{i.username} {i.player.index}: {i.player.specialization}" for i in game.users if not i.cancelled))
            return
        bot.reply_to(message, "Вы проголосовали")

    if vote is not None: vote.votes += 1
    user.voted = True

    for u in game.users:
        bot.send_message(u.chat_id, f"Проголосовало: {game.votes}/{game.active}")
    
    if game.votes < game.active: return

    game.round += 1

    # Игрок за которого проголосовало наибольшее количество игроков
    shuffle(game.users)
    least = max((u for u in game.users if not u.cancelled), key = lambda u: u.votes)
    if least.votes == 0: least = None

    # Результат голосования
    if least is None:
        # Голосование не состоялось
        for u in game.users:
            bot.send_message(u.chat_id, "Голоса не были отданы ни за одного игрока")
    else:
        # Игрок выбывает
        for u in game.users:
            bot.send_message(u.chat_id, f"Голосование окончено, выбывает: {least.username}")
            bot.send_message(u.chat_id, templates.stats.format(
                specialization = u.player.specialization,
                bio = u.player.bio,
                health = u.player.health,
                hobby = u.player.hobby,
                phobia = u.player.phobia,
                personality = u.player.personality,
                info = u.player.info,
                knowledge = u.player.knowledge,
                inventory = u.player.inventory,
                action = u.player.action,
                condition = u.player.condition
            ))
        bot.send_message(least.chat_id, "Вы проиграли")
        game.cancel(least)

    # Проверка завершения
    if game.test():
        for u in game.users:
            bot.send_message(u.chat_id, "Игра завершена, остались: " + ", ".join(u.username for u in game.users if not u.cancelled))
        game.finish()
    else:
        for u in game.users:
            if u.cancelled: continue
            bot.send_message(u.chat_id, f"Следующий раунд: {game.round}")
            u.votes = 0
            u.voted = False

print("Running")
bot.infinity_polling()