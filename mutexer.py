import telebot
from telebot import types

bot = telebot.TeleBot("5532472004:AAH74-qByrleRayEA6a2LqQy0fyfzx_YSNU")


START_TEXT = """Hello! I am simple locker bot.\nYou can write /lock to lock me or /unlock to unlock me.\n
Where can i be helpful? If you share some resource with your friends (netflix account for example), you can manage\
 usage of this resource with help of me.\nIf you start using resource - write /lock and you friends must do the same.\
If resource is already locked by someone, there is no opportunity to lock it again until the user locked it enters /unlock command.
If user writes /lock, when resource is locked, I will write error message.\n
Common process:\n[UserA, UserB] - share netflix account\n1. UserA enters /lock (mutex is locked - means he/she uses netflix)\n2. UserB enters /lock (gets error because mutex is locked already)
3. UserA enters /unlock (mutex unlocked - he/she does not uses netflix)\n4. UserB enter /lock (mutex locked - UserB uses netflix account)"""

"""
* Contains chat locks.
* syntax: {chat_id: {"locker": True|False}}
"""
lockers = {}

def init_locker(message):
	"""
	* inits locker for chat if it is not inited.
	"""
	if message.chat.id not in lockers:
		lockers[message.chat.id] = {"locker": False}

@bot.message_handler(commands=["start", "help"])
def start_cmd_handler(message):
	init_locker(message)
	bot.send_message(message.chat.id, START_TEXT)

@bot.message_handler(commands=["lock"])
def start_cmd_handler(message):
	init_locker(message)
	if lockers[message.chat.id]["locker"] == True:
		bot.send_message(message.chat.id, "I can not lock mutex. It is already locked by someone! Try again later")
	else:
		lockers[message.chat.id]["locker"] = True
		bot.send_message(message.chat.id, "Mutex is locked!")


@bot.message_handler(commands=["unlock"])
def start_cmd_handler(message):
	init_locker(message)
	if lockers[message.chat.id]["locker"] == False:
		bot.send_message(message.chat.id, "Mutex is already unlocked!")
	else:
		lockers[message.chat.id]["locker"] = False
		bot.send_message(message.chat.id, "Mutex is unlocked now")


bot.polling()