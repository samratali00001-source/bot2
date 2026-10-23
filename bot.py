import os
import random
import re
import sqlite3
import threading
import urllib.parse
from datetime import date, datetime
from flask import Flask
from gtts import gTTS
import requests
import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# --- RENDER WEB SERVER WRAPPER ---
app = Flask('')


@app.route('/')
def home():
  return 'Mega All-in-One Super Bot is running live on Render!'


def run_web():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# --- CONFIGURATION ---
TOKEN = '8944416320:AAEpQrzPWGmBfnzeoSerHq4WmJRXU1-UMog'  # Replace with your Telegram Bot Token
ADMIN_ID = 8729108422 # Replace with your Telegram User ID (For /broadcast)
ADMIN_GROUP_ID =-1003850262852  # Replace with your Private Admin Group ID
CHANNELS = ['@DarkBugBountyHunter', '@pythonJavalanguage', '@fullstackwebdeveloperx']  # 3 Channels

bot = telebot.TeleBot(TOKEN)

# --- QUIZ DATA ---
QUIZ_QUESTIONS = [
    {
        'q': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'ans': 'Paris',
    },
    {
        'q': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'ans': 'Mars',
    },
    {
        'q': 'What is 12 x 12?',
        'options': ['122', '144', '148', '160'],
        'ans': '144',
    },
    {
        'q': 'Which element has chemical symbol O?',
        'options': ['Gold', 'Oxygen', 'Silver', 'Iron'],
        'ans': 'Oxygen',
    },
]

# --- 5 LANGUAGES DICTIONARY ---
TRANSLATIONS = {
    'en': {
        'btn_ai': '🤖 AI Assistant',
        'btn_image': '🎨 Image AI',
        'btn_qr': '📷 QR Code',
        'btn_short': '🔗 Short URL',
        'btn_tts': '🗣️ Text to Speech',
        'btn_math': '🧮 Math Solver',
        'btn_quote': '💡 Daily Quote',
        'btn_bonus': '🎁 Daily Bonus',
        'btn_quiz': '🎮 Quiz Game',
        'btn_font': '✨ Fancy Font',
        'btn_weather': '🌤️ Weather',
        'btn_translate': '🌐 Translator',
        'btn_pass': '🔐 Password Gen',
        'btn_ref': '🔗 Referral',
        'btn_profile': '📊 My Profile',
        'btn_lang': '🗣️ Language',
        'welcome': (
            '🎉 Welcome! Subscription verified. Select a feature from below:'
        ),
        'sub_warning': '⚠️ Join all 3 channels to use the bot!',
    },
    'bn': {
        'btn_ai': '🤖 এআই চ্যাট',
        'btn_image': '🎨 ইমেজ জেনারেটর',
        'btn_qr': '📷 কিউআর কোড',
        'btn_short': '🔗 লিংক ছোট করুন',
        'btn_tts': '🗣️ লেখা থেকে ভয়েস',
        'btn_math': '🧮 ম্যাথ সলভার',
        'btn_quote': '💡 মোটিভেশনাল কোটস',
        'btn_bonus': '🎁 ডেইলি বোনাস',
        'btn_quiz': '🎮 কুইজ গেম',
        'btn_font': '✨ স্টাইলিশ ফন্ট',
        'btn_weather': '🌤️ আবহাওয়া',
        'btn_translate': '🌐 অনুবাদক',
        'btn_pass': '🔐 পাসওয়ার্ড জেনারেটর',
        'btn_ref': '🔗 রেফারেল লিংক',
        'btn_profile': '📊 আমার প্রোফাইল',
        'btn_lang': '🗣️ ভাষা পরিবর্তন',
        'welcome': '🎉 স্বাগতম! সাবস্ক্রিপশন ভেরিফাইড। অপশন বেছে নিন:',
        'sub_warning': '⚠️ প্রথমে ৩টি চ্যানেলে জয়েন করুন!',
    },
    'ru': {
        'btn_ai': '🤖 ИИ Ассистент',
        'btn_image': '🎨 ИИ Картинки',
        'btn_qr': '📷 QR Код',
        'btn_short': '🔗 Короткая ссылка',
        'btn_tts': '🗣️ Текст в речь',
        'btn_math': '🧮 Калькулятор',
        'btn_quote': '💡 Цитата дня',
        'btn_bonus': '🎁 Бонус',
        'btn_quiz': '🎮 Викторина',
        'btn_font': '✨ Красивый шрифт',
        'btn_weather': '🌤️ Погода',
        'btn_translate': '🌐 Переводчик',
        'btn_pass': '🔐 Генератор паролей',
        'btn_ref': '🔗 Реф. ссылка',
        'btn_profile': '📊 Профиль',
        'btn_lang': '🗣️ Язык',
        'welcome': '🎉 Добро пожаловать! Выберите функцию:',
        'sub_warning': '⚠️ Подпишитесь на 3 канала!',
    },
    'ar': {
        'btn_ai': '🤖 مساعد الذكاء',
        'btn_image': '🎨 منشئ الصور',
        'btn_qr': '📷 رمز الاستجابة',
        'btn_short': '🔗 تقصير الرابط',
        'btn_tts': '🗣️ تحويل النص لصوت',
        'btn_math': '🧮 حاسبة',
        'btn_quote': '💡 حكم اليوم',
        'btn_bonus': '🎁 المكافأة',
        'btn_quiz': '🎮 لعبة المسابقات',
        'btn_font': '✨ خطوط مميزة',
        'btn_weather': '🌤️ الطقس',
        'btn_translate': '🌐 المترجم',
        'btn_pass': '🔐 مولد كلمة السر',
        'btn_ref': '🔗 رابط الإحالة',
        'btn_profile': '📊 ملفي',
        'btn_lang': '🗣️ اللغة',
        'welcome': '🎉 أهلاً بك! اختر ميزة من القائمة:',
        'sub_warning': '⚠️ يجب الانضمام إلى القنوات الـ 3 أولاً!',
    },
    'ko': {
        'btn_ai': '🤖 AI 어시스턴트',
        'btn_image': '🎨 AI 이미지',
        'btn_qr': '📷 QR 코드',
        'btn_short': '🔗 URL 단축',
        'btn_tts': '🗣️ 음성 변환',
        'btn_math': '🧮 수학 계산',
        'btn_quote': '💡 오늘의 명언',
        'btn_bonus': '🎁 보너스',
        'btn_quiz': '🎮 퀴즈 게임',
        'btn_font': '✨ 예쁜 폰트',
        'btn_weather': '🌤️ 날씨',
        'btn_translate': '🌐 번역기',
        'btn_pass': '🔐 비밀번호 생성기',
        'btn_ref': '🔗 추천 링크',
        'btn_profile': '📊 내 프로필',
        'btn_lang': '🗣️ 언어',
        'welcome': '🎉 환영합니다! 메뉴를 선택하세요:',
        'sub_warning': '⚠️ 3개 채널에 가입하세요!',
    },
}

# --- DATABASE SETUP ---
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        referred_by INTEGER,
        points INTEGER DEFAULT 0,
        language TEXT DEFAULT 'en',
        state TEXT DEFAULT 'IDLE',
        joined_date TEXT,
        last_bonus TEXT
    )
""")
conn.commit()


# --- EXACT ADMIN LOGGING FORMAT ---
def log_user_action(message, action_text):
  try:
    name = message.from_user.first_name or 'User'
    username = message.from_user.username
    username_str = f'@{username}' if username else '@None'
    user_id = message.from_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_msg = (
        f'🔍 User Activity Log\n'
        f'👤 User: {name} ({username_str})\n'
        f'🆔 ID: {user_id}\n'
        f'⚡ Action: {action_text}\n'
        f'⏰ Time: {timestamp}'
    )
    bot.send_message(ADMIN_GROUP_ID, log_msg)
  except Exception as e:
    print('Admin log error:', e)


def get_stats():
  cursor.execute('SELECT COUNT(*) FROM users')
  total = cursor.fetchone()[0]
  current_month = datetime.now().strftime('%Y-%m')
  cursor.execute(
      'SELECT COUNT(*) FROM users WHERE joined_date LIKE ?', (f'{current_month}%',)
  )
  monthly = cursor.fetchone()[0]
  return total, monthly


def update_bot_description():
  try:
    total, monthly = get_stats()
    desc = f'🤖 Mega All-In-One Telegram Bot!\n👥 Total Users: {total} (New this month: +{monthly})\n👇 Tap Start below.'
    bot.set_my_description(desc)
  except Exception as e:
    print('Description update error:', e)


def check_subscriptions(user_id):
  for channel in CHANNELS:
    try:
      member = bot.get_chat_member(channel, user_id)
      if member.status not in ['creator', 'administrator', 'member']:
        return False
    except Exception:
      return False
  return True


# --- FANCY FONT GENERATOR HELPER ---
def make_fancy_text(text):
  normal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  fancy = '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
  trans_table = str.maketrans(normal, fancy)
  return text.translate(trans_table)


# --- KEYBOARDS ---
def main_menu_keyboard(lang):
  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
  markup = ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(KeyboardButton(t['btn_ai']), KeyboardButton(t['btn_image']))
  markup.add(KeyboardButton(t['btn_qr']), KeyboardButton(t['btn_short']))
  markup.add(KeyboardButton(t['btn_tts']), KeyboardButton(t['btn_math']))
  markup.add(KeyboardButton(t['btn_quiz']), KeyboardButton(t['btn_font']))
  markup.add(KeyboardButton(t['btn_weather']), KeyboardButton(t['btn_translate']))
  markup.add(KeyboardButton(t['btn_pass']), KeyboardButton(t['btn_bonus']))
  markup.add(KeyboardButton(t['btn_quote']), KeyboardButton(t['btn_profile']))
  markup.add(KeyboardButton(t['btn_ref']), KeyboardButton(t['btn_lang']))
  return markup


def subscription_keyboard():
  markup = InlineKeyboardMarkup()
  for i, ch in enumerate(CHANNELS, 1):
    markup.add(
        InlineKeyboardButton(
            f'📢 Join Channel {i}', url=f'https://t.me/{ch[1:]}'
        )
    )
  markup.add(
      InlineKeyboardButton('✅ I Have Joined (Check)', callback_data='check_join')
  )
  return markup


# --- GROUP HELPER (WELCOME & ANTI-LINK) ---
@bot.message_handler(
    content_types=['new_chat_members'],
    func=lambda message: message.chat.type in ['group', 'supergroup'],
)
def welcome_group_members(message):
  for user in message.new_chat_members:
    welcome_text = (
        f'👋 Welcome {user.first_name} to **{message.chat.title}**!\nEnjoy your'
        ' stay and obey rules.'
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')


@bot.message_handler(
    func=lambda message: message.chat.type in ['group', 'supergroup']
)
def group_moderation(message):
  text = message.text or ''
  if re.search(r'http[s]?://|t\.me/', text):
    try:
      bot.delete_message(message.chat.id, message.message_id)
      bot.send_message(
          message.chat.id,
          f'⚠️ @{message.from_user.username or message.from_user.first_name},'
          ' links are not allowed here!',
      )
      log_user_action(message, f'Link deleted in Group: {message.chat.title}')
    except Exception:
      pass


# --- /START COMMAND ---
@bot.message_handler(commands=['start'])
def start_command(message):
  if message.chat.type in ['group', 'supergroup']:
    bot.send_message(
        message.chat.id, '🤖 Hello! I am active as a Group Helper Bot.'
    )
    return

  user_id = message.from_user.id
  args = message.text.split()
  referred_by = (
      int(args[1])
      if len(args) > 1 and args[1].isdigit() and int(args[1]) != user_id
      else None
  )

  cursor.execute(
      'SELECT user_id, language FROM users WHERE user_id = ?', (user_id,)
  )
  user_data = cursor.fetchone()

  if not user_data:
    joined_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'INSERT INTO users (user_id, referred_by, language, state, joined_date)'
        " VALUES (?, ?, 'en', 'IDLE', ?)",
        (user_id, referred_by, joined_date),
    )
    conn.commit()
    update_bot_description()
    log_user_action(message, 'New User Registered')

    if referred_by:
      cursor.execute(
          'UPDATE users SET points = points + 1 WHERE user_id = ?',
          (referred_by,),
      )
      conn.commit()
      log_user_action(message, f'Joined via Referral of ID: {referred_by}')
    lang = 'en'
  else:
    lang = user_data[1]
    cursor.execute(
        "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    log_user_action(message, 'Restarted the bot (/start)')

  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
  if not check_subscriptions(user_id):
    bot.send_message(
        message.chat.id, t['sub_warning'], reply_markup=subscription_keyboard()
    )
  else:
    bot.send_message(
        message.chat.id, t['welcome'], reply_markup=main_menu_keyboard(lang)
    )


# --- BROADCAST COMMAND ---
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
  if message.from_user.id != ADMIN_ID:
    return
  msg_to_send = message.text.replace('/broadcast', '').strip()
  if not msg_to_send:
    bot.send_message(
        message.chat.id, 'Usage: `/broadcast Your Message`', parse_mode='Markdown'
    )
    return

  cursor.execute('SELECT user_id FROM users')
  all_users = cursor.fetchall()
  count = 0
  for u in all_users:
    try:
      bot.send_message(u[0], msg_to_send)
      count += 1
    except Exception:
      pass
  bot.send_message(
      message.chat.id, f'✅ Broadcast sent successfully to {count} users!'
  )


# --- CALLBACK HANDLER ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  user_id = call.from_user.id
  cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
  row = cursor.fetchone()
  lang = row[0] if row else 'en'

  if call.data == 'check_join':
    if check_subscriptions(user_id):
      bot.answer_callback_query(call.id, '✅ Verified!')
      bot.send_message(
          call.message.chat.id,
          'Welcome to Main Menu:',
          reply_markup=main_menu_keyboard(lang),
      )
      log_user_action(call.message, 'Verified channel subscriptions')
    else:
      bot.answer_callback_query(
          call.id, '❌ Not joined all channels yet!', show_alert=True
      )

  elif call.data.startswith('lang_'):
    new_lang = call.data.split('_')[1]
    cursor.execute(
        'UPDATE users SET language = ? WHERE user_id = ?', (new_lang, user_id)
    )
    conn.commit()
    bot.answer_callback_query(call.id, 'Language updated!')
    bot.send_message(
        call.message.chat.id,
        'Main Menu:',
        reply_markup=main_menu_keyboard(new_lang),
    )
    log_user_action(call.message, f'Changed language to: {new_lang.upper()}')

  elif call.data.startswith('quiz_'):
    ans = call.data.split('_')[1]
    correct_ans = call.data.split('_')[2]
    if ans == correct_ans:
      cursor.execute(
          'UPDATE users SET points = points + 10 WHERE user_id = ?', (user_id,)
      )
      conn.commit()
      bot.answer_callback_query(
          call.id, '🎉 Correct Answer! You earned +10 Points!', show_alert=True
      )
      log_user_action(call.message, 'Solved Quiz correctly (+10 Points)')
    else:
      bot.answer_callback_query(
          call.id, f'❌ Wrong Answer! Correct was: {correct_ans}', show_alert=True
      )


# --- MAIN TEXT & FEATURE HANDLER ---
@bot.message_handler(
    func=lambda message: message.chat.type == 'private',
    content_types=['text', 'photo', 'document', 'video'],
)
def handle_private_text(message):
  user_id = message.from_user.id

  if not check_subscriptions(user_id):
    bot.send_message(
        message.chat.id,
        '⚠️ Join required channels first!',
        reply_markup=subscription_keyboard(),
    )
    return

  # File to Link Converter
  if message.content_type in ['photo', 'document', 'video']:
    try:
      file_id = (
          message.photo[-1].file_id
          if message.content_type == 'photo'
          else (
              message.document.file_id
              if message.document
              else message.video.file_id
          )
      )
      file_info = bot.get_file(file_id)
      direct_link = (
          f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
      )
      bot.reply_to(
          message,
          f'📁 **Direct Download Link:**\n`{direct_link}`',
          parse_mode='Markdown',
      )
      log_user_action(message, f'Generated File Link ({message.content_type})')
    except Exception:
      bot.reply_to(message, '❌ Failed to generate file link.')
    return

  text = message.text
  cursor.execute(
      'SELECT state, language, points, last_bonus FROM users WHERE user_id = ?',
      (user_id,),
  )
  row = cursor.fetchone()
  state, lang, points, last_bonus = row if row else ('IDLE', 'en', 0, None)
  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])

  # --- BUTTON CLICK CHECKS ---
  if text in [t['btn_ai'], '🤖 AI Assistant', '🤖 এআই চ্যাট']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_AI' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '🤖 Ask me anything! Send your question:')
    log_user_action(message, 'Opened AI Assistant')

  elif text in [t['btn_short'], '🔗 Short URL', '🔗 লিংক ছোট করুন']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_SHORT' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '🔗 Send long URL to shorten:')
    log_user_action(message, 'Opened URL Shortener')

  elif text in [t['btn_tts'], '🗣️ Text to Speech', '🗣️ লেখা থেকে ভয়েস']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_TTS' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(
        message.chat.id, '🗣️ Send text to convert into voice audio:'
    )
    log_user_action(message, 'Opened Text to Speech')

  elif text in [t['btn_font'], '✨ Fancy Font', '✨ স্টাইলিশ ফন্ট']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_FONT' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(
        message.chat.id, '✨ Send text to convert into stylish fancy font:'
    )
    log_user_action(message, 'Opened Fancy Font Generator')

  elif text in [t['btn_weather'], '🌤️ Weather', '🌤️ আবহাওয়া']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_WEATHER' WHERE user_id = ?",
        (user_id,),
    )
    conn.commit()
    bot.send_message(
        message.chat.id, '🌤️ Send city name to check live weather (e.g. Dhaka):'
    )
    log_user_action(message, 'Opened Weather Check')

  elif text in [t['btn_translate'], '🌐 Translator', '🌐 অনুবাদক']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_TRANS' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(
        message.chat.id, '🌐 Send text to translate into English:'
    )
    log_user_action(message, 'Opened Text Translator')

  elif text in [t['btn_pass'], '🔐 Password Gen', '🔐 পাসওয়ার্ড জেনারেটর']:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    new_pass = ''.join(random.choice(chars) for _ in range(12))
    bot.send_message(
        message.chat.id,
        f'🔐 **Your Generated Secure Password:**\n`{new_pass}`',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Generated Secure Password')

  elif text in [t['btn_quiz'], '🎮 Quiz Game', '🎮 কুইজ গেম']:
    q_data = random.choice(QUIZ_QUESTIONS)
    markup = InlineKeyboardMarkup()
    for opt in q_data['options']:
      markup.add(
          InlineKeyboardButton(
              opt, callback_data=f"quiz_{opt}_{q_data['ans']}"
          )
      )
    bot.send_message(
        message.chat.id, f"🎮 **Quiz:** {q_data['q']}", reply_markup=markup
    )
    log_user_action(message, 'Started Quiz Game')

  elif text in [t['btn_quote'], '💡 Daily Quote', '💡 মোটিভেশনাল কোটস']:
    try:
      res = requests.get('https://api.quotable.io/random', timeout=5).json()
      quote = f"💡 *\"{res['content']}\"*\n\n— _{res['author']}_"
      bot.send_message(message.chat.id, quote, parse_mode='Markdown')
    except Exception:
      bot.send_message(
          message.chat.id,
          '💡 *\"Believe you can and you\'re halfway there.\"*\n\n— _Theodore'
          ' Roosevelt_',
          parse_mode='Markdown',
      )
    log_user_action(message, 'Requested Daily Quote')

  elif text in [t['btn_bonus'], '🎁 Daily Bonus', '🎁 ডেইলি বোনাস']:
    today = str(date.today())
    if last_bonus == today:
      bot.send_message(
          message.chat.id,
          '⚠️ You have already claimed today\'s bonus! Come back tomorrow.',
      )
    else:
      cursor.execute(
          'UPDATE users SET points = points + 5, last_bonus = ? WHERE user_id'
          ' = ?',
          (today, user_id),
      )
      conn.commit()
      bot.send_message(
          message.chat.id,
          '🎉 **Congratulations!** You received +5 Bonus Points today!',
      )
      log_user_action(message, 'Claimed Daily Bonus (+5 Points)')

  elif text in [t['btn_qr'], '📷 QR Code', '📷 কিউআর কোড']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_QR' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '📷 Send text or URL for QR Code:')
    log_user_action(message, 'Opened QR Code Generator')

  elif text in [t['btn_image'], '🎨 Image AI', '🎨 ইমেজ জেনারেটর']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_IMAGE' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '🎨 Send English prompt for Image AI:')
    log_user_action(message, 'Opened Image Generator')

  elif text in [t['btn_math'], '🧮 Math Solver', '🧮 ম্যাথ সলভার']:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_MATH' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '🧮 Send math expression (e.g. 50 * 2):')
    log_user_action(message, 'Opened Math Solver')

  elif text in [t['btn_profile'], '📊 My Profile', '📊 আমার প্রোফাইল']:
    bot.send_message(
        message.chat.id,
        f'📊 **Your Profile:**\n\n🆔 User ID: `{user_id}`\n⭐ Points:'
        f' {points}\n🗣️ Language: {lang.upper()}\n📢 Status: Verified ✅',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Checked Profile')

  elif text in [t['btn_ref'], '🔗 Referral', '🔗 রেফারেল লিংক']:
    bot_info = bot.get_me()
    bot.send_message(
        message.chat.id,
        f'🔗 **Referral Link:**\n`https://t.me/{bot_info.username}?start={user_id}`\n\nShare'
        ' with friends to earn points!',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Requested Referral Link')

  elif text in [t['btn_lang'], '🗣️ Language', '🗣️ ভাষা পরিবর্তন']:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('English 🇬🇧', callback_data='lang_en'),
        InlineKeyboardButton('Bengali 🇧🇩', callback_data='lang_bn'),
        InlineKeyboardButton('Russian 🇷🇺', callback_data='lang_ru'),
        InlineKeyboardButton('Arabic 🇸🇦', callback_data='lang_ar'),
        InlineKeyboardButton('Korean 🇰🇷', callback_data='lang_ko'),
    )
    bot.send_message(
        message.chat.id, '🗣️ Select your language:', reply_markup=markup
    )
    log_user_action(message, 'Opened Language Settings Menu')

  # --- USER STATE PROCESSORS ---
  else:
    if state == 'WAITING_FONT':
      fancy_res = make_fancy_text(text)
      bot.send_message(
          message.chat.id,
          f'✨ **Stylish Font:**\n`{fancy_res}`',
          parse_mode='Markdown',
      )
      log_user_action(message, f'Generated Fancy Font for: {text}')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_WEATHER':
      try:
        res = requests.get(
            f'https://wttr.in/{urllib.parse.quote(text)}?format=3', timeout=5
        ).text
        bot.send_message(message.chat.id, f'🌤️ **Weather Info:**\n{res}')
        log_user_action(message, f'Checked Weather for: {text}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to fetch weather info.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_TRANS':
      try:
        res = requests.get(
            'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='
            + urllib.parse.quote(text),
            timeout=5,
        ).json()
        translated_text = res[0][0][0]
        bot.send_message(
            message.chat.id, f'🌐 **Translated (English):**\n{translated_text}'
        )
        log_user_action(message, f'Translated text: {text}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to translate text.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_AI':
      bot.send_message(message.chat.id, '🤖 Thinking...')
      try:
        res = requests.get(
            'https://api.simsimi.vn/v1/simtalk?text='
            f'{urllib.parse.quote(text)}&lc=en',
            timeout=5,
        ).json()
        reply = res.get('message', 'Sorry, I could not process that.')
        bot.send_message(message.chat.id, f'🤖 **AI:** {reply}')
        log_user_action(message, f'AI Chat Query: {text}')
      except Exception:
        bot.send_message(
            message.chat.id, '🤖 I am busy right now. Try again later.'
        )
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_SHORT':
      try:
        res = requests.get(
            'https://is.gd/create.php?format=json&url='
            f'{urllib.parse.quote(text)}',
            timeout=5,
        ).json()
        short_url = res.get('shorturl', 'Invalid URL')
        bot.send_message(message.chat.id, f'🔗 **Shortened URL:**\n{short_url}')
        log_user_action(message, f'Shortened URL for: {text}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to shorten URL.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_TTS':
      try:
        tts = gTTS(text=text, lang='en')
        filename = f'tts_{user_id}.mp3'
        tts.save(filename)
        with open(filename, 'rb') as audio:
          bot.send_voice(message.chat.id, audio)
        os.remove(filename)
        log_user_action(message, f'Text to Speech Audio: {text}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to convert text to speech.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_QR':
      qr_url = (
          'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data='
          f'{urllib.parse.quote(text)}'
      )
      bot.send_photo(message.chat.id, qr_url, caption='✨ QR Code Generated')
      log_user_action(message, f'Generated QR Code for: {text}')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_IMAGE':
      bot.send_message(message.chat.id, '🎨 Generating image...')
      image_url = (
          f'https://image.pollinations.ai/prompt/{urllib.parse.quote(text)}'
      )
      bot.send_photo(message.chat.id, image_url, caption=f'✨ Prompt: {text}')
      log_user_action(message, f'Text to Image Prompt: {text}')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_MATH':
      try:
        allowed = set('0123456789+-*/(). ')
        if all(c in allowed for c in text):
          bot.send_message(
              message.chat.id,
              f'🧮 **Result:** `{eval(text)}`',
              parse_mode='Markdown',
          )
          log_user_action(message, f'Math Solved: {text}')
        else:
          bot.send_message(
              message.chat.id, '❌ Invalid characters in expression.'
          )
      except Exception:
        bot.send_message(message.chat.id, '❌ Invalid math expression.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    else:
      bot.send_message(
          message.chat.id, t['welcome'], reply_markup=main_menu_keyboard(lang)
      )


# --- RUN BOT ---
if __name__ == '__main__':
  t = threading.Thread(target=run_web)
  t.daemon = True
  t.start()
  print('Mega All-in-One Super Bot is running live on Render...')
  bot.infinity_polling(skip_pending=True)
