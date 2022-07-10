
# Vezdekod22 - Marusya
# https://64e9-79-137-132-11.ngrok.io/_webhooks/marusya/vezdekodfinal22
import os
import sys
import json
import logging
import random
import logic

from enum import IntEnum
from tabnanny import check

from flask import Flask, request
from flask_cors import CORS

from vk_api import VKApi


DEV = False
CMDS = {
    '10': [
        'сыграем в двадцать одно'
    ]
}


app = Flask(__name__)
cors = CORS(app, resources={
            '/': {"origins": '*',
                  "headers": 'Content-Type, Accept'}})
logging.basicConfig(
    format='[%(asctime)s] (%(levelname)s) %(name)s.%(funcName)s (%(lineno)d) >> %(message)s',
    level=logging.DEBUG if DEV else logging.INFO)
log = logging.getLogger('server')
if 'SKILL_TOKEN' in os.environ:
    vka = VKApi(os.environ.get('SKILL_TOKEN', ''))
    resp = vka.marusia_getPictures()
    if resp:
        log.info('Logged in VK Api as Skill.')
    else:
        log.fatal(f'Can\'t login to VK Api as Skill!\nResponse: {resp}')
        sys.exit(1)


STOP_CMD = [
    'с меня хватит'
]
@app.route('/_webhooks/marusya/vezdekodfinal22/', methods=['GET', 'POST'])
def webhhook():
    req = request.get_json()
    log.debug(f'New request: {req}')
    utter = req['request']['original_utterance'].lower()
    print(utter)
    if utter in STOP_CMD:
        ans = make_welcome(req)
        return json.loads(ans)
    elif utter in ('двадцать одно', 'погнали') or req['state']['session'] and req['state']['session'].get('game') == 'двадцать одно':
        return game1(req)
    elif utter in ('съедобное — несъедобное', 'поехали') or req['state']['session'] and req['state']['session'].get('game') == 'съедобное — несъедобное':
        return game2(req)
    elif utter in ('тетрис', 'полетели') or req['state']['session'] and req['state']['session'].get('game') == 'полетели':
        return game3(req)
    elif utter in ('змейка', 'поползли') or req['state']['session'] and req['state']['session'].get('game') == 'змейка':
        return game4(req)
    elif utter in ('2048', 'помчали') or req['state']['session'] and req['state']['session'].get('game') == '2048':
        return game5(req)
    elif req['session']['new']:
        return make_welcome(req)
    else:
        ans = make_welcome(req)
        return json.loads(ans)
        # return make_echo(req)


def game1_check_status(req: dict, resp: dict, state: dict, users='user') -> bool:
    """
    метод проверяет текущее состояние игры
    :return:
    """
    count_point = sum(state.get(users))
    end_state = False
    if count_point > 21:
        end_state = True
    return end_state


def game1(req: dict) -> str:
    """
    Игра двадцать одно
    1. Если новый игрок, тогда перемешиваются карты
    2. Раздается по одной карте игроку и марусе
    :param req:
    :return:
    """
    koloda = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4
    random.shuffle(koloda)
    utter = req['request']['original_utterance'].lower()
    resp = {
        'response': {},
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    end_state = False
    if req['state']['session'] and utter != 'погнали':
        # пользователь играет
        if utter == 'да':
            # пользователь берет карту
            user_koloda = req['state']['session']['koloda']
            session_state = {
                'user': req['state']['session']['user'] + [user_koloda.pop()],
                'koloda': user_koloda,
                'game': 'двадцать одно'
            }
            end_state = game1_check_status(req, resp, session_state)
            count_point = sum(session_state.get("user"))
            resp['response'] = {
                'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. Еще одну карту?',
                'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. Еще одну карту?',
                'end_session': False,
                'buttons': [
                    {'title': 'Да'},
                    {'title': 'Нет'}
                ]
            }
            resp['session_state'] = session_state
        elif utter == 'нет':
            # пользователь не берет карту, набирает Маруся
            end_state = True
            card = []
            user_koloda = req['state']['session']['koloda']
            user_state = req['state']['session']['user']
            count_point = sum(user_state)
            for i in range(10):
                card.append(user_koloda.pop())
                if sum(card) > 21:
                    break
                elif sum(card) > count_point:
                    break
            session_state = {
                'koloda': user_koloda,
                'user': user_state,
                'marusya': card,
                'game': 'двадцать одно'
            }
            resp['session_state'] = session_state
    elif utter == 'погнали' or not req['state']['session']:
        # пользователь первый раз зашел в игру
        session_state = {
            'user': [koloda.pop(), koloda.pop()],
            'koloda': koloda,
            'game': 'двадцать одно'
        }
        end_state = game1_check_status(req, resp, session_state)
        count_point = sum(session_state.get("user"))
        resp['response'] = {
            'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. Еще одну карту?',
            'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. Еще одну карту?',
            'end_session': False,
            'buttons': [
                {'title': 'Да'},
                {'title': 'Нет'}
            ]
        }
        resp['session_state'] = session_state
    if end_state:
        if sum(resp['session_state']['user']) > 21:
            # Проиграл из-за перебора
            resp['response'] = {
                'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. К сожалению вы проиграли, сыграем еще?',
                'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. К сожалению вы проиграли, сыграем еще?',
                'end_session': False,
                'buttons': [
                    {'title': 'Погнали'},
                    {'title': 'С меня хватит'}
                ]
            }
        elif sum(resp['session_state']['user']) > sum(resp['session_state']['marusya']):
            # Выиграл пользователь
            mar = sum(resp['session_state']['marusya'])
            resp['response'] = {
                'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. А у меня {mar} очков и это меньше. Поздравляю, ты выиграл! Продолжим?',
                'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. А у меня {mar} очков и это меньше. Поздравляю, ты выиграл! Продолжим?',
                'end_session': False,
                'buttons': [
                    {'title': 'Погнали'},
                    {'title': 'С меня хватит'}
                ]
            }
        elif sum(resp['session_state']['user']) < sum(resp['session_state']['marusya']):
            # Выиграла маруся
            mar = sum(resp['session_state']['marusya'])
            resp['response'] = {
                'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. А у меня {mar} очков и это больше, я выиграла! Продолжим?',
                'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. А у меня {mar} очков и это больше, я выиграла! Продолжим?',
                'end_session': False,
                'buttons': [
                    {'title': 'Погнали'},
                    {'title': 'С меня хватит'}
                ]
            }
        elif sum(resp['session_state']['user']) < sum(resp['session_state']['marusya']):
            # Ничья
            resp['response'] = {
                'text': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. К сожалению у нас поровну, попробуем еще?',
                'tts': f'У вас на руке карты: {", ".join(map(str, session_state.get("user")))}. В сумме дают {count_point}. К сожалению у нас поровну, попробуем еще?',
                'end_session': False,
                'buttons': [
                    {'title': 'Погнали'},
                    {'title': 'С меня хватит'}
                ]
            }
    return json.loads(json.dumps(resp))


game_2_info = {
    'Огурец': True,
    'Молоко': True,
    'Фарфор': False,
    'Телефон': False,
    'Пушка': False,
    'Душка': False,
    'Мушка': False,
    'Золото': False,
    'Факел': False,
    'Мясо': True,
    'Олень': True,
    'Мухомор': False,
    'Яблоко': True,
    'Банка': False,
    'Вода': True,
    'Табличка': False,
    'Морковь': True,
    'Фишка': False,
    'Мандарин': True,
    'Стул': False,
    'Фалафель': True,
}


def game2(req: dict) -> str:
    """
    съедобное - не съедобное
    Игра предлагает пользователю варианты и если пользователь выбирает съедобное, тогда ему засчитываются очки
    :param req:
    :return:
    """
    utter = req['request']['original_utterance'].lower()
    resp = {
        'response': {},
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    end_state = False
    if req['state']['session'] and utter != 'поехали':
        # пользователь играет
        if utter == 'съем':
            # пользователь считает, что съедобное
            eat = req['state']['session']['eat']
            point = req['state']['session']['point']
            if game_2_info.get(eat):
                point += 1
            else:
                end_state = True
            choice = random.choice(list(game_2_info.keys()))
            session_state = {
                'eat': choice,
                'prev_eat': eat,
                'point': point,
                'game': 'съедобное — несъедобное'
            }
            resp['response'] = {
                'text': f'Ты прав! {eat} съедобное! Ты заработал {point} очков! А что на счет {choice}?',
                'tts': f'Ты прав! {eat} съедобное! Ты заработал {point} очков! А что на счет {choice}?',
                'end_session': False,
                'buttons': [
                    {'title': 'Съем'},
                    {'title': 'Выброшу'}
                ]
            }
            resp['session_state'] = session_state
        elif utter == 'выброшу':
            # пользователь считает, что не съедобное
            eat = req['state']['session']['eat']
            point = req['state']['session']['point']
            if not game_2_info.get(eat):
                point += 1
            else:
                end_state = True
            choice = random.choice(list(game_2_info.keys()))
            session_state = {
                'eat': choice,
                'prev_eat': eat,
                'point': point,
                'game': 'съедобное — несъедобное'
            }
            resp['response'] = {
                'text': f'Ты прав! {eat} не съедобное! Ты заработал {point} очков! А что на счет {choice}?',
                'tts': f'Ты прав! {eat} не съедобное! Ты заработал {point} очков! А что на счет {choice}?',
                'end_session': False,
                'buttons': [
                    {'title': 'Съем'},
                    {'title': 'Выброшу'}
                ]
            }
            resp['session_state'] = session_state
    elif utter == 'поехали' or not req['state']['session']:
        # пользователь первый раз зашел в игру
        choice = random.choice(list(game_2_info.keys()))
        session_state = {
            'eat': choice,
            'point': 0,
            'game': 'съедобное — несъедобное'
        }
        resp['response'] = {
            'text': f'Сможешь угадать насколько это съедобно? Что на счет {choice}?',
            'tts': f'Сможешь угадать насколько это съедобно? Что на счет {choice}?',
            'end_session': False,
            'buttons': [
                {'title': 'Съем'},
                {'title': 'Выброшу'}
            ]
        }
        resp['session_state'] = session_state
    if end_state:
        choice = resp['session_state']['prev_eat']
        point = resp['session_state']['point']
        resp['response'] = {
            'text': f'К сожалению ты не угадал! {choice} - {"съедобное" if game_2_info.get(choice) else "не съедобное"}. Ты набрал {point} очков. Попробуем еще раз?',
            'tts': f'К сожалению ты не угадал! {choice} - {"съедобное" if game_2_info.get(choice) else "не съедобное"}. Ты набрал {point} очков.  Попробуем еще раз?',
            'end_session': False,
            'buttons': [
                {'title': 'Поехали'},
                {'title': 'С меня хватит'}
            ]
        }

    return json.loads(json.dumps(resp))


from tetris import Board


def draw_tetris(game_board):
    BOARD_HEIGHT = 17
    BOARD_WIDTH = 11
    matrix = [[] * 11] * 17
    for a in range(BOARD_HEIGHT):
        m = []
        for b in range(BOARD_WIDTH):
            if game_board.board[a][b] == 1:
                # matrix[a][b] = " "
                m.append(" ")
                # window.addstr(a + 1, 2 * b + 1, "  ", curses.color_pair(96))
            else:
                # matrix[a][b] = " ."
                m.append(" .")
                # draw net
                # window.addstr(a + 1, 2 * b + 1, " .", curses.color_pair(99))
        matrix.append(m)
    # draw current block
    for a in range(game_board.current_block.size()[0]):
        for b in range(game_board.current_block.size()[1]):
            if game_board.current_block.shape[a][b] == 1:
                x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                y = game_board.current_block_pos[0] + a + 1

                matrix[y][x] = "#"
                # window.addstr(y, x, "  ", curses.color_pair(game_board.current_block.color))
    return matrix

def game3(req: dict) -> str:
    """
    тетрис
    :param req:
    :return:
    """
    utter = req['request']['original_utterance'].lower()
    resp = {
        'response': {},
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    end_state = False
    if req['state']['session'] and utter != 'полетели':
        # пользователь играет
        if utter in ('влево', 'вправо', 'вниз', 'вверх'):
            field = req['state']['session']['field']
            snake = req['state']['session']['snake']

            field = Field(10, field)
            snake = Snake("Маруся", snake)
            snake.set_field(field)
            end_state = snake.move(utter)

            session_state = {
                'field': field.field,
                'snake': snake.coords,
                'game': 'тетрис'
            }
            resp['response'] = {
                'text': '\n'.join(field.render()),
                'tts': f'Игра началась, какой выбор сделаешь?',
                'end_session': False,
                'buttons': [
                    {'title': 'Повернуть'},
                    {'title': 'Вниз'},
                    {'title': 'Вправо'},
                    {'title': 'Влево'},
                    {'title': 'С меня хватит'}
                ]
            }
            resp['session_state'] = session_state
    elif utter == 'полетели' or not req['state']['session']:

        game_board = Board(17, 11)
        game_board.start()
        game_board.move_block("вниз")
        draw_tetris(game_board)
        # пользователь первый раз зашел в игру
        field = Field(10)
        snake = Snake("Маруся")
        snake.set_field(field)
        end_state = snake.move('вправо')


        session_state = {
            'field': field.field,
            'snake': snake.coords,
            'game': 'змейка'
        }
        resp['response'] = {
            'text': '\n'.join(field.render()),
            'tts': f'Игра началась, какой выбор сделаешь?',
            'end_session': False,
            'buttons': [
                {'title': 'Вверх'},
                {'title': 'Вниз'},
                {'title': 'Вправо'},
                {'title': 'Влево'},
                {'title': 'С меня хватит'}
            ]
        }
        resp['session_state'] = session_state
    if end_state:

        resp['response'] = {
                'text': f'Вы проиграли! Еще разок?',
                'tts': f'Вы проиграли! Еще разок?',
                'end_session': False,
                'buttons': [
                    {'title': 'поползли'},
                    {'title': 'С меня хватит'}
                ]
            }
    return json.loads(json.dumps(resp))


from snake import Snake, Field


def game4(req: dict) -> str:
    """
    змейка
    :param req:
    :return:
    """
    commands = {
        "вверх": logic.up,
        "вниз": logic.down,
        "влево": logic.left,
        "вправо": logic.right
    }
    utter = req['request']['original_utterance'].lower()
    resp = {
        'response': {},
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    end_state = False
    if req['state']['session'] and utter != 'поползли':
        # пользователь играет
        if utter in ('влево', 'вправо', 'вниз', 'вверх'):
            field = req['state']['session']['field']
            snake = req['state']['session']['snake']

            field = Field(10, field)
            snake = Snake("Маруся", snake)
            snake.set_field(field)
            end_state = snake.move(utter)

            session_state = {
                'field': field.field,
                'snake': snake.coords,
                'game': 'змейка'
            }
            resp['response'] = {
                'text': '\n'.join(field.render()),
                'tts': f'Игра началась, какой выбор сделаешь?',
                'end_session': False,
                'buttons': [
                    {'title': 'Вверх'},
                    {'title': 'Вниз'},
                    {'title': 'Вправо'},
                    {'title': 'Влево'},
                    {'title': 'С меня хватит'}
                ]
            }
            resp['session_state'] = session_state
    elif utter == 'поползли' or not req['state']['session']:
        # пользователь первый раз зашел в игру
        field = Field(10)
        snake = Snake("Маруся")
        snake.set_field(field)
        end_state = snake.move('вправо')

        session_state = {
            'field': field.field,
            'snake': snake.coords,
            'game': 'змейка'
        }
        resp['response'] = {
            'text': '\n'.join(field.render()),
            'tts': f'Игра началась, какой выбор сделаешь?',
            'end_session': False,
            'buttons': [
                {'title': 'Вверх'},
                {'title': 'Вниз'},
                {'title': 'Вправо'},
                {'title': 'Влево'},
                {'title': 'С меня хватит'}
            ]
        }
        resp['session_state'] = session_state
    if end_state:
        resp['response'] = {
                'text': f'Вы проиграли! Еще разок?',
                'tts': f'Вы проиграли! Еще разок?',
                'end_session': False,
                'buttons': [
                    {'title': 'поползли'},
                    {'title': 'С меня хватит'}
                ]
            }
    return json.loads(json.dumps(resp))


str_grid = """
--------------
|%s|%s|%s|%s|
--------------
|%s|%s|%s|%s|
--------------
|%s|%s|%s|%s|
--------------
|%s|%s|%s|%s|
--------------
"""


class Gameresult:
    commands = {
        "1": logic.up,
        "2": logic.down,
        "3": logic.left,
        "4": logic.right
    }

    def __init__(self):
        self.matrix = logic.new_game(4)
        self.grid = str_grid % tuple([(lambda j: str(j) + " " * (4 - len(str(j))))(j) for i in self.matrix for j in i])

    def exec_command(self, command):
        self.matrix, done = self.commands[command](self.matrix)
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.grid = str_grid % tuple(
                [(lambda j: str(j) + " " * (4 - len(str(j))))(j) for i in self.matrix for j in i])
            if logic.game_state(self.matrix) == 'win':
                return True, False
            elif logic.game_state(self.matrix) == 'lose':
                return False, True
            else:
                return False, False


def game5(req: dict) -> str:
    """
    Игра 2048
    :param req:
    :return:
    """
    commands = {
        "вверх": logic.up,
        "вниз": logic.down,
        "влево": logic.left,
        "вправо": logic.right
    }
    utter = req['request']['original_utterance'].lower()
    resp = {
        'response': {},
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    end_state = False
    if req['state']['session'] and utter != 'помчали':
        # пользователь играет
        if utter in ('влево', 'вправо', 'вниз', 'вверх'):
            matrix = req['state']['session']['matrix']
            matrix, done = commands[utter](matrix)
            if done:
                matrix = logic.add_two(matrix)
            session_state = {
                'matrix': matrix,
                'grid': str_grid % tuple([(lambda j: str(j) + " " * (4 - len(str(j))))(j) for i in matrix for j in i]),
                'game': '2048'
            }
            resp['response'] = {
                'text': f'{session_state.get("grid")}',
                'tts': f'Каков твой следующий ход?',
                'end_session': False,
                'buttons': [
                    {'title': 'Вверх'},
                    {'title': 'Вниз'},
                    {'title': 'Вправо'},
                    {'title': 'Влево'},
                    {'title': 'С меня хватит'}
                ]
            }
            resp['session_state'] = session_state
    elif utter == 'помчали' or not req['state']['session']:
        # пользователь первый раз зашел в игру
        matrix = logic.new_game(4)
        session_state = {
            'matrix': matrix,
            'grid': str_grid % tuple([(lambda j: str(j) + " " * (4 - len(str(j))))(j) for i in matrix for j in i]),
            'game': '2048'
        }
        resp['response'] = {
            'text': f'{session_state.get("grid")}',
            'tts': f'Игра началась, какой выбор сделаешь?',
            'end_session': False,
            'buttons': [
                {'title': 'Вверх'},
                {'title': 'Вниз'},
                {'title': 'Вправо'},
                {'title': 'Влево'},
                {'title': 'С меня хватит'}
            ]
        }
        resp['session_state'] = session_state
    if logic.game_state(resp['session_state']['matrix']) == 'win':
        resp['response'] = {
            'text': f'Поздравляю, ты выиграл!',
            'tts': f'Поздравляю, ты выиграл!',
            'end_session': False,
            'buttons': [
                {'title': 'Помчали'},
                {'title': 'С меня хватит'}
            ]
        }
    elif logic.game_state(resp['session_state']['matrix']) == 'lose':
        resp['response'] = {
            'text': f'Увы увы, ты проиграл!',
            'tts': f'Увы увы, ты проиграл!',
            'end_session': False,
            'buttons': [
                {'title': 'Помчали'},
                {'title': 'С меня хватит'}
            ]
        }

    return json.loads(json.dumps(resp))


def make_app(req: dict) -> str:
    resp = {
        'response': {
            'text': 'Открываю приложение регистрации Вездекода.',
            'tts': 'Открываю приложение регистрации Вездекода.',
            'end_session': True,
            'card': {
                'type': 'MiniApp',
                'url': 'https://vk.com/app7543093'
            }
        },
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    return json.dumps(resp)


def make_welcome(req: dict) -> str:
    resp = {
        'response': {
            'text': 'Привет вездекодерам!\n\n Хочешь сыграть со мной в одну из моих игр?\n Предлагаю тебе поиграть со мной в такие игры:\n "Двадцать одно", "Съедобное - несъедобное", "Змейка" или 2048.',
            'tts': '<speaker audio=marusia-sounds/music-tambourine-120bpm-1>Привет вездекодерам!\n\nХочешь сыграть со мной в одну из моих игр?\n Предлагаю тебе поиграть со мной в такие игры:\n "Двадцать одно", "Съедобное - несъедобное", "Змейка" или 2048.',
            'end_session': False,
            'buttons': [
                {'title': 'Двадцать одно'},
                {'title': 'Съедобное — несъедобное'},
                {'title': 'Змейка'},
                {'title': '2048'}
            ]
        },
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    return json.dumps(resp)


def make_echo(req: dict) -> str:
    resp = {
        'response': {
            'text': req['request']['original_utterance'],
            'tts': req['request']['original_utterance'],
            'end_session': False
        },
        'session': {
            'session_id': req['session']['session_id'],
            'user_id': req['session']['user_id'],
            'message_id': req['session']['message_id'],
            'skill_id': os.environ.get('SKILL_TOKEN', '')
        },
        'version': req['version']
    }
    return json.dumps(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12341)

