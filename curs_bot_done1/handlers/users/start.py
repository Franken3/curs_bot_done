from aiogram import types, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.generate_inline_kb import gen_inl_kb, gen_confirm_kb, gen_puch_all_kb
from loader import dp, bot
from states.states import UserState
from utils.db_api.db_commands import create_user, add_to_check, del_from_check, change_curs, all_users_for_push
from utils.texts.texts import Texts


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    await create_user(message.from_user.id)
    reply = gen_inl_kb(start=True)
    await change_curs()
    await bot.send_message(chat_id=message.from_user.id,
                           text=Texts['start_text'],
                           reply_markup=reply)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)


@dp.message_handler(commands=['curs'])
async def change_curs_msg(message: types.Message):
    curses = await change_curs()
    reply = gen_inl_kb(start=True)
    await bot.send_message(chat_id=message.from_user.id,
                           text= 'Установил значения курсов:\n'
                                 f'USD:{curses[0]}\n'
                                 f'AED:{curses[1]}\n'
                                 f'EUR:{curses[2]}\n',
                           reply_markup=reply)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)



@dp.message_handler(state=UserState.currency_state)
async def msg_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cuurency, del_it, is_del = data['currency'], data['prev_msg'], data['is_del']
    msg = message.text.lower().split()
    error_flag = False
    if len(msg) == 2:
        up, curs = msg[0], msg[1] if msg[1].isdigit() else None
    else:
        up, curs = None, None
        error_flag = True
    if up != 'выше' or curs is None or error_flag:
        if not is_del:
            print('here!')
            await bot.delete_message(chat_id=message.from_user.id, message_id=del_it)

        send = await bot.send_message(chat_id=message.from_user.id,
                                      text=f'Отправите сообщение в соответствие с примером. Пример:\n'
                                           f'Выше 71.2\n'
                                           f'выше 63\n'
                                           f'Вы ввели: {message.text}',
                                      reply_markup=gen_inl_kb(back=True,
                                                              prev_state='curs_state'))
        await state.update_data(prev_msg=send.message_id)
        await bot.delete_message(message.from_user.id, message_id=message.message_id)
    else:
        if not is_del:
            await bot.delete_message(chat_id=message.from_user.id, message_id=del_it)

        prev_msg = await bot.send_message(message.from_user.id,
                                          text=f'Вы хотите отслеживать {cuurency} выше {msg[1]} RUB.\nВсе верно?\n'
                                               f'Нажмите подтвердить или введите новое значение',
                                          reply_markup=gen_confirm_kb())
        print(prev_msg.message_id)
        await state.update_data(curs=msg[1], prev_msg=prev_msg.message_id)
        data = await state.get_data()
        print(data)
        await bot.delete_message(message.from_user.id, message_id=message.message_id)


@dp.callback_query_handler(state=UserState.currency_state)
async def cnf_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback_query.data == 'confirm':
        currency, curs, is_del = data['currency'], data['curs'], data['is_del']
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f'Теперь вы отслеживаете {currency} выше {curs} RUB.',
                                    reply_markup=gen_inl_kb(back=True,
                                                            prev_state='curs_state'))
        await state.finish()
        await add_to_check(callback_query.from_user.id,
                           currency=currency.lower(),
                           currency_curs=curs)
    else:
        await state.finish()
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=Texts['curs_state_text'],
                                    reply_markup=gen_inl_kb(curs=True, back=True, prev_state='start_state'))


@dp.callback_query_handler(state=UserState.push_state)
async def push_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    print(data)
    match data:
        case 'usd_push_state' | 'aed_push_state' | 'eur_push_state':
            await del_from_check(user_id=callback_query.from_user.id,
                                 currency=data[:3])
            reply, text = gen_inl_kb(push=True,
                                     user_id=callback_query.from_user.id,
                                     prev_state='start_state')
        case _:
            await state.finish()
            reply = gen_inl_kb(start=True)
            text = Texts['start_text']

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=text,
                                reply_markup=reply)


@dp.callback_query_handler(text='usd_push_state')
@dp.callback_query_handler(text='aed_push_state')
@dp.callback_query_handler(text='eur_push_state')
async def push_callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    await del_from_check(user_id=callback_query.from_user.id,
                                 currency=data[:3])

    await bot.delete_message(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)



@dp.callback_query_handler()
async def main_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = Texts['start_text']
    reply = gen_inl_kb(start=True)
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    print(callback_query.data)
    match callback_query.data:
        case 'start_state':
            text = Texts['start_text']
            reply = gen_inl_kb(start=True)
        case 'curs_state':
            text = Texts['curs_state_text']
            reply = gen_inl_kb(curs=True,
                               prev_state='start_state',
                               back=True)
        case 'push_state':
            reply, text = gen_inl_kb(push=True,
                                     user_id=callback_query.from_user.id,
                                     prev_state='start_state')
            await state.set_state(UserState.push_state)
        case 'usd_state':
            await state.set_state(UserState.currency_state)
            await state.update_data(currency='USD',
                                    prev_msg=callback_query.message.message_id,
                                    is_del=False)
            reply, text = gen_inl_kb(back=True,
                                     currency='USD',
                                     prev_state='curs_state')
        case 'aed_state':
            await state.set_state(UserState.currency_state)
            await state.update_data(currency='AED',
                                    prev_msg=callback_query.message.message_id,
                                    is_del=False)
            reply, text = gen_inl_kb(back=True,
                                     currency='AED',
                                     prev_state='curs_state')
        case 'eur_state':
            await state.set_state(UserState.currency_state)
            await state.update_data(currency='EUR',
                                    prev_msg=callback_query.message.message_id,
                                    is_del=False)
            reply, text = gen_inl_kb(back=True,
                                     currency='EUR',
                                     prev_state='curs_state')

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=text,
                                reply_markup=reply)

@dp.message_handler()
async def del_spam(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id=message.message_id)


async def send_curs_push():
    usd_users, aed_users, eur_users = await all_users_for_push()
    print('here', usd_users, aed_users, eur_users)
    if len(usd_users) != 0:
        print(1)
        for user_id in usd_users:
            text = f"USD сейчас выше вашего отслеживаемого порога RUB"
            inline_kb= gen_puch_all_kb('usd')
            await bot.send_message(chat_id=user_id,
                                   text=text,
                                   reply_markup=inline_kb)
            print(3)
    if len(aed_users) != 0:
        for user_id in aed_users:
            text = f"AED сейчас выше вашего отслеживаемого порога RUB"
            inline_kb = gen_puch_all_kb('aed')
            await bot.send_message(chat_id=user_id,
                                   text=text,
                                   reply_markup=inline_kb)
    if len(eur_users) != 0:
        for user_id in eur_users:
            text = f"EUR сейчас выше вашего отслеживаемого порога RUB"
            inline_kb= gen_puch_all_kb('eur')
            await bot.send_message(chat_id=user_id,
                                   text=text,
                                   reply_markup=inline_kb)
