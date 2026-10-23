import os
import random
import re
import sqlite3
import threading
import urllib.parse
from datetime import date, datetime
from flask import Flask
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
  return 'Multi-Language Super Bot is running live on Render!'


def run_web():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# --- CONFIGURATION ---
TOKEN = '8944416320:AAHHyhCYYrNOOH_LRD_j7tvBDbNlVtCWzO4'  # Put your Telegram Bot Token here
ADMIN_ID = 8729108422  # Put your Personal Telegram ID (for /broadcast)
ADMIN_GROUP_ID = -1003850262852  # Put your Private Admin Group ID
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
    {
        'q': 'How many continents are there on Earth?',
        'options': ['5', '6', '7', '8'],
        'ans': '7',
    },
]

# --- 11 LANGUAGES DICTIONARY ---
TRANSLATIONS = {
    'en': {
        'btn_qr': '📷 QR Code',
        'btn_font': '✨ Fancy Font',
        'btn_math': '🧮 Math Solver',
        'btn_pass': '🔐 Password Gen',
        'btn_quiz': '🎮 Quiz Game',
        'btn_bonus': '🎁 Daily Bonus',
        'btn_ref': '🔗 Referral',
        'btn_profile': '📊 My Profile',
        'btn_lang': '🗣️ Language',
        'welcome': (
            '🎉 Welcome! Subscription verified. Select a feature from below:'
        ),
        'sub_warning': '⚠️ Join all 3 channels to use the bot!',
    },
    'bn': {
        'btn_qr': '📷 কিউআর কোড',
        'btn_font': '✨ স্টাইলিশ ফন্ট',
        'btn_math': '🧮 ম্যাথ সলভার',
        'btn_pass': '🔐 পাসওয়ার্ড জেনারেটর',
        'btn_quiz': '🎮 কুইজ গেম',
        'btn_bonus': '🎁 ডেইলি বোনাস',
        'btn_ref': '🔗 রেফারেল লিংক',
        'btn_profile': '📊 আমার প্রোফাইল',
        'btn_lang': '🗣️ ভাষা পরিবর্তন',
        'welcome': '🎉 স্বাগতম! সাবস্ক্রিপশন ভেরিফাইড। অপশন বেছে নিন:',
        'sub_warning': '⚠️ প্রথমে ৩টি চ্যানেলে জয়েন করুন!',
    },
    'ru': {
        'btn_qr': '📷 QR Код',
        'btn_font': '✨ Красивый шрифт',
        'btn_math': '🧮 Калькулятор',
        'btn_pass': '🔐 Генератор паролей',
        'btn_quiz': '🎮 Викторина',
        'btn_bonus': '🎁 Бонус',
        'btn_ref': '🔗 Реф. ссылка',
        'btn_profile': '📊 Профиль',
        'btn_lang': '🗣️ Язык',
        'welcome': '🎉 Добро пожаловать! Выберите функцию:',
        'sub_warning': '⚠️ Подпишитесь на 3 канала!',
    },
    'ar': {
        'btn_qr': '📷 رمز الاستجابة',
        'btn_font': '✨ خطوط مميزة',
        'btn_math': '🧮 حاسبة',
        'btn_pass': '🔐 مولد كلمة السر',
        'btn_quiz': '🎮 لعبة المسابقات',
        'btn_bonus': '🎁 المكافأة',
        'btn_ref': '🔗 رابط الإحالة',
        'btn_profile': '📊 ملفي',
        'btn_lang': '🗣️ اللغة',
        'welcome': '🎉 أهلاً بك! اختر ميزة من القائمة:',
        'sub_warning': '⚠️ يجب الانضمام إلى القنوات الـ 3 أولاً!',
    },
    'ko': {
        'btn_qr': '📷 QR 코드',
        'btn_font': '✨ 예쁜 폰트',
        'btn_math': '🧮 수학 계산',
        'btn_pass': '🔐 비밀번호 생성기',
        'btn_quiz': '🎮 퀴즈 게임',
        'btn_bonus': '🎁 보너스',
        'btn_ref': '🔗 추천 링크',
        'btn_profile': '📊 내 프로필',
        'btn_lang': '🗣️ 언어',
        'welcome': '🎉 환영합니다! 메뉴를 선택하세요:',
        'sub_warning': '⚠️ 3개 채널에 가입하세요!',
    },
    'zh': {
        'btn_qr': '📷 二维码生成',
        'btn_font': '✨ 花样字体',
        'btn_math': '🧮 数学计算',
        'btn_pass': '🔐 密码生成器',
        'btn_quiz': '🎮 问答游戏',
        'btn_bonus': '🎁 每日奖励',
        'btn_ref': '🔗 推荐链接',
        'btn_profile': '📊 个人资料',
        'btn_lang': '🗣️ 切换语言',
        'welcome': '🎉 欢迎！订阅已验证。请从下方选择功能：',
        'sub_warning': '⚠️ 必须先加入所有3个频道！',
    },
    'id': {
        'btn_qr': '📷 Kode QR',
        'btn_font': '✨ Font Keren',
        'btn_math': '🧮 Matematika',
        'btn_pass': '🔐 Pembuat Kata Sandi',
        'btn_quiz': '🎮 Game Kuis',
        'btn_bonus': '🎁 Bonus Harian',
        'btn_ref': '🔗 Tautan Rujukan',
        'btn_profile': '📊 Profil Saya',
        'btn_lang': '🗣️ Ubah Bahasa',
        'welcome': (
            '🎉 Selamat datang! Langganan diverifikasi. Pilih fitur di bawah:'
        ),
        'sub_warning': '⚠️ Bergabunglah dengan ke-3 saluran terlebih dahulu!',
    },
    'uz': {
        'btn_qr': '📷 QR Kod',
        'btn_font': '✨ Chiroyli Font',
        'btn_math': '🧮 Matematika',
        'btn_pass': '🔐 Parol Generatori',
        'btn_quiz': '🎮 Viktorina',
        'btn_bonus': '🎁 Kunlik Bonus',
        'btn_ref': '🔗 Taklif Havolasi',
        'btn_profile': '📊 Profilim',
        'btn_lang': '🗣️ Tilni Oʻzgartirish',
        'welcome': (
            '🎉 Xush kelibsiz! Obuna tasdiqlandi. Quyidan funksiyani tanlang:'
        ),
        'sub_warning': '⚠️ Avval barcha 3 ta kanalga qoʻshiling!',
    },
    'kk': {
        'btn_qr': '📷 QR Код',
        'btn_font': '✨ Әдемі Шрифт',
        'btn_math': '🧮 Математика',
        'btn_pass': '🔐 Құпия сөз генераторы',
        'btn_quiz': '🎮 Викторина',
        'btn_bonus': '🎁 Күнделікті бонус',
        'btn_ref': '🔗 Реферал сілтеме',
        'btn_profile': '📊 Меңің профилім',
        'btn_lang': '🗣️ Тілді өзгерту',
        'welcome': (
            '🎉 Қош келдіңіз! Жазылым расталды. Төмендегі функцияны таңдаңыз:'
        ),
        'sub_warning': '⚠️ Алдымен барлық 3 арнаға қосылыңыз!',
    },
    'tg': {
        'btn_qr': '📷 Ремзи QR',
        'btn_font': '✨ Шрифти зебо',
        'btn_math': '🧮 Ҳисоби математикӣ',
        'btn_pass': '🔐 Генератори парол',
        'btn_quiz': '🎮 Бозии викторина',
        'btn_bonus': '🎁 Бонуси рӯзона',
        'btn_ref': '🔗 Истиноди даъватӣ',
        'btn_profile': '📊 Профили ман',
        'btn_lang': '🗣️ Интихоби забон',
        'welcome': (
            '🎉 Хуш омадед! Обуна тасдиқ шуд. Имкониятро аз зер интихоб кунед:'
        ),
        'sub_warning': '⚠️ Аввал ба ҳамаи 3 канал обуна шавед!',
    },
    'az': {
        'btn_qr': '📷 QR Kod',
        'btn_font': '✨ Qəşəng Şrift',
        'btn_math': '🧮 Riyaziyyat',
        'btn_pass': '🔐 Parol Generatoru',
        'btn_quiz': '🎮 Viktorina Oyunu',
        'btn_bonus': '🎁 Gündəlik Bonus',
        'btn_ref': '🔗 Dəvət Linki',
        'btn_profile': '📊 Profilim',
        'btn_lang': '🗣️ Dili Dəyiş',
        'welcome': (
            '🎉 Xoş gəldiniz! Abunəlik təsdiqləndi. Aşağıdan funksiya seçin:'
        ),
        'sub_warning': '⚠️ Əvvəlcə bütün 3 kanala qoşulun!',
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


# --- EXACT ADMIN LOGGING ---
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
    desc = f'🤖 All-In-One Telegram Bot!\n👥 Total Users: {total} (New this month: +{monthly})\n👇 Tap Start below.'
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


def make_fancy_text(text):
  normal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  fancy = '𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
  trans_table = str.maketrans(normal, fancy)
  return text.translate(trans_table)


# --- KEYBOARDS ---
def main_menu_keyboard(lang):
  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
  markup = ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(KeyboardButton(t['btn_qr']), KeyboardButton(t['btn_font']))
  markup.add(KeyboardButton(t['btn_math']), KeyboardButton(t['btn_pass']))
  markup.add(KeyboardButton(t['btn_quiz']), KeyboardButton(t['btn_bonus']))
  markup.add(
      KeyboardButton(t['btn_ref']),
      KeyboardButton(t['btn_profile']),
      KeyboardButton(t['btn_lang']),
  )
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


# --- GROUP HELPER ---
@bot.message_handler(
    content_types=['new_chat_members'],
    func=lambda message: message.chat.type in ['group', 'supergroup'],
)
def welcome_group_members(message):
  for user in message.new_chat_members:
    welcome_text = (
        f'👋 Welcome {user.first_name} to **{message.chat.title}**!\nEnjoy your'
        ' stay and follow the rules.'
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


# --- MAIN TEXT HANDLER ---
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

  # --- BUTTON TRIGGERS (MATCHES ALL 11 LANGUAGES) ---
  if text in [
      t['btn_font'],
      '✨ Fancy Font',
      '✨ স্টাইলিশ ফন্ট',
      '✨ Красивый шрифт',
      '✨ خطوط مميزة',
      '✨ 예쁜 폰特',
      '✨ 花样字体',
      '✨ Font Keren',
      '✨ Chiroyli Font',
      '✨ Әдемі Шрифт',
      '✨ Шрифти зебо',
      '✨ Qəşəng Şrift',
  ]:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_FONT' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(
        message.chat.id, '✨ Send text to convert into stylish fancy font:'
    )
    log_user_action(message, 'Opened Fancy Font Generator')

  elif text in [
      t['btn_pass'],
      '🔐 Password Gen',
      '🔐 পাসওয়ার্ড জেনারেটর',
      '🔐 Генератор паролей',
      '🔐 مولد كلمة السر',
      '🔐 비밀번호 생성기',
      '🔐 密码生成器',
      '🔐 Pembuat Kata Sandi',
      '🔐 Parol Generatori',
      '🔐 Құпия сөз генераторы',
      '🔐 Генератори парол',
      '🔐 Parol Generatoru',
  ]:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    new_pass = ''.join(random.choice(chars) for _ in range(14))
    bot.send_message(
        message.chat.id,
        f'🔐 **Your Generated Secure Password:**\n`{new_pass}`',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Generated Secure Password')

  elif text in [
      t['btn_quiz'],
      '🎮 Quiz Game',
      '🎮 কুইজ গেম',
      '🎮 Викторина',
      '🎮 لعبة المسابقات',
      '🎮 퀴즈 게임',
      '🎮 问答游戏',
      '🎮 Game Kuis',
      '🎮 Viktorina',
      '🎮 Бозии викторина',
      '🎮 Viktorina Oyunu',
  ]:
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

  elif text in [
      t['btn_bonus'],
      '🎁 Daily Bonus',
      '🎁 ডেইলি বোনাস',
      '🎁 Бонус',
      '🎁 المكافأة',
      '🎁 보너스',
      '🎁 每日奖励',
      '🎁 Bonus Harian',
      '🎁 Kunlik Bonus',
      '🎁 Күнделікті бонус',
      '🎁 Бонуси рӯзона',
      '🎁 Gündəlik Bonus',
  ]:
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

  elif text in [
      t['btn_qr'],
      '📷 QR Code',
      '📷 কিউআর কোড',
      '📷 QR Код',
      '📷 رمز الاستجابة',
      '📷 QR 코드',
      '📷 二维码生成',
      '📷 Kode QR',
      '📷 QR Kod',
  ]:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_QR' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '📷 Send text or URL for QR Code:')
    log_user_action(message, 'Opened QR Code Generator')

  elif text in [
      t['btn_math'],
      '🧮 Math Solver',
      '🧮 ম্যাথ সলভার',
      '🧮 Калькулятор',
      '🧮 حاسبة',
      '🧮 수학 계산',
      '🧮 数学计算',
      '🧮 Matematika',
      '🧮 Ҳисоби математикӣ',
      '🧮 Riyaziyyat',
  ]:
    cursor.execute(
        "UPDATE users SET state = 'WAITING_MATH' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, '🧮 Send math expression (e.g. 50 * 2):')
    log_user_action(message, 'Opened Math Solver')

  elif text in [
      t['btn_profile'],
      '📊 My Profile',
      '📊 আমার প্রোফাইল',
      '📊 Профиль',
      '📊 ملفي',
      '📊 내 프로필',
      '📊 个人资料',
      '📊 Profil Saya',
      '📊 Profilim',
      '📊 Меңің профилім',
      '📊 Профили ман',
  ]:
    bot.send_message(
        message.chat.id,
        f'📊 **Your Profile:**\n\n🆔 User ID: `{user_id}`\n⭐ Points:'
        f' {points}\n🗣️ Language: {lang.upper()}\n📢 Status: Verified ✅',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Checked Profile')

  elif text in [
      t['btn_ref'],
      '🔗 Referral',
      '🔗 রেফারেল লিংক',
      '🔗 Реф. ссылка',
      '🔗 رابط الإحالة',
      '🔗 추천 링크',
      '🔗 推荐链接',
      '🔗 Tautan Rujukan',
      '🔗 Taklif Havolasi',
      '🔗 Реферал сілтеме',
      '🔗 Истиноди даъватӣ',
      '🔗 Dəvət Linki',
  ]:
    bot_info = bot.get_me()
    bot.send_message(
        message.chat.id,
        f'🔗 **Referral Link:**\n`https://t.me/{bot_info.username}?start={user_id}`\n\nShare'
        ' with friends to earn points!',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Requested Referral Link')

  elif text in [
      t['btn_lang'],
      '🗣️ Language',
      '🗣️ ভাষা পরিবর্তন',
      '🗣️ Язык',
      '🗣️ اللغة',
      '🗣️ 언어',
      '🗣️ 切换语言',
      '🗣️ Ubah Bahasa',
      '🗣️ Tilni Oʻzgartirish',
      '🗣️ Тілді өзгерту',
      '🗣️ Интихоби забон',
      '🗣️ Dili Dəyiş',
  ]:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('English 🇬🇧', callback_data='lang_en'),
        InlineKeyboardButton('Bengali 🇧🇩', callback_data='lang_bn'),
        InlineKeyboardButton('Russian 🇷🇺', callback_data='lang_ru'),
        InlineKeyboardButton('Arabic 🇸🇦', callback_data='lang_ar'),
        InlineKeyboardButton('Korean 🇰🇷', callback_data='lang_ko'),
        InlineKeyboardButton('Chinese 🇨🇳', callback_data='lang_zh'),
        InlineKeyboardButton('Indonesian 🇮🇩', callback_data='lang_id'),
        InlineKeyboardButton('Uzbek 🇺🇿', callback_data='lang_uz'),
        InlineKeyboardButton('Kazakh 🇰🇿', callback_data='lang_kk'),
        InlineKeyboardButton('Tajik 🇹🇯', callback_data='lang_tg'),
        InlineKeyboardButton('Azerbaijani 🇦🇿', callback_data='lang_az'),
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
  print('Multi-Language Super Bot is running live on Render...')
  bot.infinity_polling(skip_pending=True)
