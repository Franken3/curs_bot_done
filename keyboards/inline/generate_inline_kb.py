from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_all_currency_for_user
# from sql.users_sql import get_all_currency_for_user
from utils.texts.texts import Texts

curs_btn = InlineKeyboardButton(Texts['curs_btn_text'], callback_data='curs_state')
push_btn = InlineKeyboardButton(Texts['push_btn_text'], callback_data='push_state')

usd_btn = InlineKeyboardButton('USD', callback_data='usd_state')
aed_btn = InlineKeyboardButton('AED', callback_data='aed_state')
eur_btn = InlineKeyboardButton('EUR', callback_data='eur_state')

cnf_btn = InlineKeyboardButton('Подтвердить', callback_data='confirm')
cnf_push_btn = InlineKeyboardButton('Подтвердить', callback_data='confirm')


def gen_puch_kb(user_id):
    res = get_all_currency_for_user(user_id)
    print(res)
    print(res.eur, res.usd, res.aed, res.user_id)
    inline_kb = InlineKeyboardMarkup(row_width=1)
    text_none = "У вас нет отслеживаемых курсов"
    text_good = "Нажмите на валюту, что бы удалить ее из отслеживаемых.\n" \
                "В данный момент вы отслеживаете:"
    if res.usd is None and res.aed is None and res.eur is None:
        return inline_kb, text_none
    if res.usd is not None:
        usd_push_btn = InlineKeyboardButton(f'USD выше {res.usd} RUB', callback_data='usd_push_state')
        inline_kb.add(usd_push_btn)
    if res.aed is not None:
        aed_push_btn = InlineKeyboardButton(f'AED выше {res.aed} RUB', callback_data='aed_push_state')
        inline_kb.add(aed_push_btn)
    if res.eur is not None:
        eur_push_btn = InlineKeyboardButton(f'EUR выше {res.eur} RUB', callback_data='eur_push_state')
        inline_kb.add(eur_push_btn)
    return inline_kb, text_good


def gen_puch_all_kb(cuurency: str):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    usd_push_btn = InlineKeyboardButton(f'Убрать отслеживание', callback_data=f'{cuurency}_push_state')
    inline_kb.add(usd_push_btn)
    return inline_kb


def gen_confirm_kb():
    inline_kb = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton(Texts['back_btn'], callback_data='curs_state')
    inline_kb.add(cnf_btn, back_btn)
    return inline_kb


def gen_confirm_when_push_kb():
    inline_kb = InlineKeyboardMarkup(row_width=1)
    back_btn = InlineKeyboardButton(Texts['back_btn'], callback_data='curs_state')
    inline_kb.add(cnf_btn, back_btn)
    return inline_kb


def gen_inl_kb(back=False, start=False, curs=None, push=False, user_id=None, prev_state=None, currency=None):
    inline_kb = InlineKeyboardMarkup(row_width=1)
    if start:
        inline_kb.add(curs_btn, push_btn)
    elif curs:
        inline_kb.add(usd_btn, aed_btn, eur_btn)
    elif push:
        inline_kb, text = gen_puch_kb(user_id)
        back_btn = InlineKeyboardButton(Texts['back_btn'], callback_data=prev_state)
        inline_kb.add(back_btn)
        return inline_kb, text
    if back:
        back_btn = InlineKeyboardButton(Texts['back_btn'], callback_data=prev_state)
        inline_kb.add(back_btn)
    if currency:
        text = f'Введите "Выше n", где n интересующий Вас курс {currency}.\n' \
               f'Примеры вашего сообщения:\nВыше 71.2\nвыше 62'
        return inline_kb, text
    return inline_kb
