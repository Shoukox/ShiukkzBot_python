import functools
import logging

from telegram import Bot, TelegramError
from telegram.ext import messagequeue as mq, Updater, MessageHandler, CallbackQueryHandler, Filters
from telegram.utils.request import Request

import commands, callback as callb, variables, other, os, datetime, pytz


# def auto_group(method):
#     @functools.wraps(method)
#     def wrapped(self, *args, **kwargs):
#         chat_id = 0
#         if "chat_id" in kwargs:
#             chat_id = kwargs["chat_id"]
#         elif len(args) > 0:
#             try:
#                 chat_id = args[0] if isinstance(args[0], int) else args[1]
#             except:
#                 chat_id = -1
#         is_group = (chat_id < 0)
#         return method(self, *args, **kwargs, isgroup=is_group)
#     return wrapped
#
# class MQBot(Bot):
#     """A subclass of Bot which delegates send method handling to MQ"""
#
#
#     def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
#         super(MQBot, self).__init__(*args, **kwargs)
#         # below 2 attributes should be provided for decorator usage
#         self._is_messages_queued_default = is_queued_def
#         self._msg_queue = mqueue or mq.MessageQueue()
#
#     def __del__(self):
#         try:
#             self._msg_queue.stop()
#         except:
#             pass
#
#     @auto_group
#     @mq.queuedmessage
#     def send_message(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         err = None
#         try:
#             msg = super(MQBot, self).send_message(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#             err = error
#         return msg if err is None else [msg, err]
#
#     @auto_group
#     @mq.queuedmessage
#     def edit_message_text(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         try:
#             msg = super(MQBot, self).edit_message_text(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#         return msg
#
#     @auto_group
#     @mq.queuedmessage
#     def get_chat_members_count(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         try:
#             msg = super(MQBot, self).get_chat_members_count(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#         return msg
#
#     def delete_message(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         err = None
#         try:
#             msg = super(MQBot, self).delete_message(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#             err = error
#         return msg if err is None else [msg, err]
#
#     @auto_group
#     @mq.queuedmessage
#     def send_photo(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         err = None
#         try:
#             msg = super(MQBot, self).send_photo(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#             err = error
#         return msg if err is None else [msg, err]
#
#     @auto_group
#     @mq.queuedmessage
#     def send_audio(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         err = None
#         try:
#             msg = super(MQBot, self).send_audio(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#             err = error
#         return msg if err is None else [msg, err]
#     @auto_group
#     @mq.queuedmessage
#     def pin_chat_message(self, *args, **kwargs):
#         """Wrapped method would accept new `queued` and `isgroup`
#         OPTIONAL arguments"""
#         msg = None
#         err = None
#         try:
#             msg = super(MQBot, self).pin_chat_message(*args, **kwargs)
#         except TelegramError as error:
#             print(error)
#             err = error
#         return msg if err is None else [msg, err]


def add_events():
    def add_msg():
        dp.add_handler(MessageHandler(Filters.text, commands.check, run_async=True))

    def callback():
        dp.add_handler(CallbackQueryHandler(callb.checkCallback, run_async=True))

    def add_timers():
        dp.job_queue.run_daily(other.morning,
                               datetime.time(9, 0, 0, 0, tzinfo=pytz.timezone('Asia/Tashkent')))
        dp.job_queue.run_daily(other.night,
                               datetime.time(0, 0, 0, 0, tzinfo=pytz.timezone('Asia/Tashkent')))

    dp = upd.dispatcher
    callback()
    add_msg()
    add_timers()


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

q = mq.MessageQueue()
request = Request(con_pool_size=8, read_timeout=None, connect_timeout=None)
#bot = MQBot(variables.token, request=request, mqueue=q)
bot = Bot(variables.token, request=request)
upd = Updater(bot=bot, use_context=True)
dp = upd.dispatcher

add_events()

from db import datab
datab.CreateTablesIfNotExist()
other.getDataFromDB()
#"""
PORT = int(os.environ.get('PORT', 5000))

upd.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=variables.token)
upd.bot.setWebhook('https://arcane-fjord-93722.herokuapp.com/' + variables.token)
#"""
#upd.start_polling(clean=True)

upd.idle()
