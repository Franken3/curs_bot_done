import random
from django.db.models import Q
from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Users, Curs


@sync_to_async
def change_curs():
    usd_random = random.uniform(63.0,72.0)
    aed_random = random.uniform(13.0,23.0)
    eur_random = random.uniform(69.0, 79.0)
    Curs.objects.filter(id=1).update(usd = usd_random, aed = aed_random, eur=eur_random)
    return usd_random, aed_random, eur_random


@sync_to_async
def create_user(user_id):
    Users.objects.get_or_create(user_id=user_id)

@sync_to_async
def all_users_for_push():
    curses = Curs.objects.first()

    usd_users = list(Users.objects.filter(usd__lt=curses.usd))
    aed_users = list(Users.objects.filter(aed__lt=curses.usd))
    eur_users = list(Users.objects.filter(eur__lt=curses.usd))

    print(usd_users,aed_users,eur_users)
    usd_users_res = []
    aed_users_res = []
    eur_users_res = []
    for user in usd_users:
        print(user.usd)
        if user.usd <= curses.usd:
            usd_users_res.append(user.user_id)
    for user in aed_users:
        if user.aed <= curses.aed:
            aed_users_res.append(user.user_id)
    for user in eur_users:
        if user.eur <= curses.eur:
            eur_users_res.append(user.user_id)
    return usd_users_res, aed_users_res, eur_users_res


@sync_to_async()
def add_to_check(user_id, currency, currency_curs):
    Users.objects.filter(user_id=user_id).update(**{currency: currency_curs})

def get_all_currency_for_user(user_id):
    return Users.objects.filter(user_id=user_id).first()
@sync_to_async()
def del_from_check(user_id, currency):
    Users.objects.filter(user_id=user_id).update(**{currency: None})
