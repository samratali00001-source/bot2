import os
import sqlite3
import threading
import urllib.parse
from datetime import datetime
import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import requests
from flask import Flask

# --- RENDER WEB SERVER WRAPPER ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot is running live on Render!'


def run_web():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# --- CONFIGURATION ---
TOKEN = '8944416320:AAEpQrzPWGmBfnzeoSerHq4WmJRXU1-UMog'  # Put your Telegram Bot Token here
bot = telebot.TeleBot(TOKEN)

# Put your 3 Telegram channel usernames here
CHANNELS = ['@DarkBugBountyHunter', '@pythonJavalanguage', '@fullstackwebdeveloperx']

# Put your Private Admin Group/Chat ID here (must be negative like -100xxxxxxxxxx)
ADMIN_GROUP_ID = -1003850262852

# --- MULTI-LANGUAGE DICTIONARY ---
TRANSLATIONS = {
    'en': {
        'btn_qr': '📷 QR Code Generator',
        'btn_lang': '🗣️ Change Language',
        'btn_math': '🧮 Math Solver',
        'btn_image': '🎨 Image Generator',
        'btn_ref': '🔗 Referral Link',
        'btn_profile': '📊 My Profile',
        'welcome': (
            '🎉 Welcome! Your subscription is verified. Choose an option from'
            ' the menu below:'
        ),
        'sub_warning': (
            '⚠️ To use this bot, you must join our 3 channels first!'
        ),
        'qr_prompt': (
            '📷 Send the text or URL you want to convert into a QR Code:'
        ),
        'math_prompt': (
            '🧮 Send your mathematical expression to solve (e.g., 25 + 5 * 4):'
        ),
        'image_prompt': '🎨 Describe the image you want to generate in English:',
        'lang_prompt': '🗣️ Choose your preferred language:',
        'profile_text': (
            '📊 **Your Profile:**\n\n🆔 User ID:'
            ' `{user_id}`\n⭐ Points: {points}\n🗣️ Language:'
            ' {lang}\n📢 Status: Verified ✅'
        ),
    },
    'bn': {
        'btn_qr': '📷 কিউআর কোড জেনারেটর',
        'btn_lang': '🗣️ ভাষা পরিবর্তন',
        'btn_math': '🧮 ম্যাথ সলভার',
        'btn_image': '🎨 ইমেজ জেনারেটর',
        'btn_ref': '🔗 রেফারেল লিংক',
        'btn_profile': '📊 আমার প্রোফাইল',
        'welcome': (
            '🎉 স্বাগতম! আপনার সাবস্ক্রিপশন ভেরিফাইড। নিচের মেনু থেকে অপশন'
            ' বেছে নিন:'
        ),
        'sub_warning': (
            '⚠️ বট ব্যবহার করতে হলে প্রথমে ৩টি চ্যানেলে জয়েন করতে হবে!'
        ),
        'qr_prompt': '📷 যে লেখা বা লিংক কিউআর কোড বানাতে চান তা পাঠান:',
        'math_prompt': '🧮 আপনার ম্যাথ সমীকরণটি পাঠান (যেমন: 25 + 5 * 4):',
        'image_prompt': '🎨 আপনি কেমন ছবি তৈরি করতে চান তা ইংরেজিতে বর্ণনা করুন:',
        'lang_prompt': '🗣️ আপনার পছন্দের ভাষা সিলেক্ট করুন:',
        'profile_text': (
            '📊 **আপনার প্রোফাইল:**\n\n🆔 ইউজার আইডি:'
            ' `{user_id}`\n⭐ পয়েন্ট: {points}\n🗣️ ভাষা: {lang}\n📢 স্ট্যাটাস: ভেরিফাইড'
            ' ✅'
        ),
    },
    'ru': {
        'btn_qr': '📷 Генератор QR',
        'btn_lang': '🗣️ Изменить язык',
        'btn_math': '🧮 Решатель математики',
        'btn_image': '🎨 Генератор картинок',
        'btn_ref': '🔗 Реф. ссылка',
        'btn_profile': '📊 Мой профиль',
        'welcome': (
            '🎉 Добро пожаловать! Подписка подтверждена. Выберите опцию ниже:'
        ),
        'sub_warning': '⚠️ Сначала подпишитесь на 3 канала!',
        'qr_prompt': '📷 Отправьте текст или ссылку для создания QR-кода:',
        'math_prompt': '🧮 Отправьте математическое выражение (например: 25 + 5 * 4):',
        'image_prompt': '🎨 Опишите картинку на английском:',
        'lang_prompt': '🗣️ Выберите язык:',
        'profile_text': (
            '📊 **Ваш профиль:**\n\n🆔 ID:'
            ' `{user_id}`\n⭐ Очки: {points}\n🗣️ Язык: {lang}\n📢 Статус:'
            ' Проверено ✅'
        ),
    },
    'ar': {
        'btn_qr': '📷 منشئ QR',
        'btn_lang': '🗣️ تغيير اللغة',
        'btn_math': '🧮 حل الرياضيات',
        'btn_image': '🎨 منشئ الصور',
        'btn_ref': '🔗 رابط الإحالة',
        'btn_profile': '📊 ملفي الشخصي',
        'welcome': '🎉 أهلاً بك! تم التحقق من اشتراكك. اختر من القائمة أدناه:',
        'sub_warning': '⚠️ يجب الانضمام إلى القنوات الـ 3 أولاً!',
        'qr_prompt': '📷 أرسل النص أو الرابط لإنشاء رمز الاستجابة السريعة:',
        'math_prompt': '🧮 أرسل التعبير الرياضي (مثال: 25 + 5 * 4):',
        'image_prompt': '🎨 صف الصورة باللغة الإنجليزية:',
        'lang_prompt': '🗣️ اختر لغتك:',
        'profile_text': (
            '📊 **ملفك الشخصي:**\n\n🆔 المعرف:'
            ' `{user_id}`\n⭐ النقاط: {points}\n🗣️ اللغة:'
            ' {lang}\n📢 الحالة: متحقق ✅'
        ),
    },
    'ko': {
        'btn_qr': '📷 QR 코드 생성',
        'btn_lang': '🗣️ 언어 변경',
        'btn_math': '🧮 수학 풀이기',
        'btn_image': '🎨 이미지 생성기',
        'btn_ref': '🔗 추천 링크',
        'btn_profile': '📊 내 프로필',
        'welcome': '🎉 환영합니다! 구독이 확인되었습니다. 아래 메뉴를 선택하세요:',
        'sub_warning': '⚠️ 먼저 3개의 채널에 가입해야 합니다!',
        'qr_prompt': '📷 QR 코드로 변환할 텍스트나 URL을 보내주세요:',
        'math_prompt': '🧮 수식을 보내주세요 (예: 25 + 5 * 4):',
        'image_prompt': '🎨 생성할 이미지를 영어로 설명해주세요:',
        'lang_prompt': '🗣️ 언어를 선택하세요:',
        'profile_text': (
            '📊 **프로필:**\n\n🆔 ID:'
            ' `{user_id}`\n⭐ 포인트: {points}\n🗣️ 언어: {lang}\n📢 상태: 인증됨 ✅'
        ),
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
        joined_date TEXT
    )
""")
conn.commit()


# --- EXACT LOG FORMAT FUNCTION ---
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
    desc = f'🤖 All-in-One Smart Telegram Bot!\n👥 Total Users: {total} (This Month: +{monthly})\n👇 Tap Start below.'
    bot.set_my_description(desc)
  except Exception as e:
    print('Description update error:', e)


def check_subscriptions(user_id):
  for channel in CHANNELS:
    try:
      member = bot.get_chat_member(channel, user_id)
      if member.status not in ['creator', 'administrator', 'member']:
        return False
    except Exception as e:
      print(f'Error checking channel {channel}: {e}')
      return False
  return True


def main_menu_keyboard(lang):
  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
  markup = ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(KeyboardButton(t['btn_qr']), KeyboardButton(t['btn_lang']))
  markup.add(KeyboardButton(t['btn_math']), KeyboardButton(t['btn_image']))
  markup.add(KeyboardButton(t['btn_ref']), KeyboardButton(t['btn_profile']))
  return markup


def get_action_from_text(text):
  for lang, t in TRANSLATIONS.items():
    if text == t['btn_qr']:
      return 'QR'
    if text == t['btn_lang']:
      return 'LANG'
    if text == t['btn_math']:
      return 'MATH'
    if text == t['btn_image']:
      return 'IMAGE'
    if text == t['btn_ref']:
      return 'REF'
    if text == t['btn_profile']:
      return 'PROFILE'
  return None


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


@bot.message_handler(commands=['start'])
def start_command(message):
  user_id = message.from_user.id
  args = message.text.split()

  referred_by = None
  if len(args) > 1:
    try:
      ref_id = int(args[1])
      if ref_id != user_id:
        referred_by = ref_id
    except ValueError:
      pass

  cursor.execute(
      'SELECT user_id, language FROM users WHERE user_id = ?', (user_id,)
  )
  user_data = cursor.fetchone()

  if not user_data:
    joined_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'INSERT INTO users (user_id, referred_by, language, state, joined_date)'
        ' VALUES (?, ?, \'en\', \'IDLE\', ?)',
        (user_id, referred_by, joined_date),
    )
    conn.commit()
    update_bot_description()

    log_user_action(message, 'Started the bot / New User Registered')

    if referred_by:
      cursor.execute(
          'UPDATE users SET points = points + 1 WHERE user_id = ?',
          (referred_by,),
      )
      conn.commit()
      log_user_action(message, f'Joined via referral link of ID: {referred_by}')

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


@bot.callback_query_handler(func=lambda call: call.data == 'check_join')
def callback_check_join(call):
  user_id = call.from_user.id
  cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
  row = cursor.fetchone()
  lang = row[0] if row else 'en'

  if check_subscriptions(user_id):
    bot.answer_callback_query(call.id, '✅ Verified successfully!')
    try:
      bot.edit_message_text(
          '🎉 Thank you! You can now use the bot.',
          call.message.chat.id,
          call.message.message_id,
      )
    except Exception:
      pass
    bot.send_message(
        call.message.chat.id, 'Main Menu:', reply_markup=main_menu_keyboard(lang)
    )
    log_user_action(call.message, 'Successfully verified channel subscriptions')
  else:
    bot.answer_callback_query(
        call.id, '❌ You have not joined all channels yet!', show_alert=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_language(call):
  user_id = call.from_user.id
  lang = call.data.split('_')[1]
  cursor.execute(
      'UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id)
  )
  conn.commit()

  bot.answer_callback_query(call.id, 'Language updated!')
  try:
    bot.edit_message_text(
        '✅ Language updated successfully.',
        call.message.chat.id,
        call.message.message_id,
    )
  except Exception:
    pass
  bot.send_message(
      call.message.chat.id, 'Main Menu:', reply_markup=main_menu_keyboard(lang)
  )
  log_user_action(call.message, f'Changed language to: {lang.upper()}')


@bot.message_handler(func=lambda message: True)
def handle_text(message):
  user_id = message.from_user.id

  if not check_subscriptions(user_id):
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    lang = row[0] if row else 'en'
    t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    bot.send_message(
        message.chat.id, t['sub_warning'], reply_markup=subscription_keyboard()
    )
    return

  text = message.text

  cursor.execute(
      'SELECT state, language FROM users WHERE user_id = ?', (user_id,)
  )
  row = cursor.fetchone()
  state = row[0] if row else 'IDLE'
  lang = row[1] if row else 'en'
  t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])

  action = get_action_from_text(text)

  if action == 'QR':
    cursor.execute(
        "UPDATE users SET state = 'WAITING_QR' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, t['qr_prompt'])
    log_user_action(message, 'Opened QR Code Generator')

  elif action == 'LANG':
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('English 🇬🇧', callback_data='lang_en'),
        InlineKeyboardButton('Bengali 🇧🇩', callback_data='lang_bn'),
        InlineKeyboardButton('Russian 🇷🇺', callback_data='lang_ru'),
        InlineKeyboardButton('Arabic 🇸🇦', callback_data='lang_ar'),
        InlineKeyboardButton('Korean 🇰🇷', callback_data='lang_ko'),
    )
    bot.send_message(message.chat.id, t['lang_prompt'], reply_markup=markup)
    log_user_action(message, 'Opened Language Settings Menu')

  elif action == 'MATH':
    cursor.execute(
        "UPDATE users SET state = 'WAITING_MATH' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, t['math_prompt'])
    log_user_action(message, 'Opened Math Solver')

  elif action == 'IMAGE':
    cursor.execute(
        "UPDATE users SET state = 'WAITING_IMAGE' WHERE user_id = ?", (user_id,)
    )
    conn.commit()
    bot.send_message(message.chat.id, t['image_prompt'])
    log_user_action(message, 'Opened Text to Image Generator')

  elif action == 'REF':
    bot_info = bot.get_me()
    ref_link = f'https://t.me/{bot_info.username}?start={user_id}'
    bot.send_message(
        message.chat.id,
        f'🔗 **Referral Link:**\n`{ref_link}`\n\nShare with friends to earn'
        ' points!',
        parse_mode='Markdown',
    )
    log_user_action(message, 'Requested Referral Link')

  elif action == 'PROFILE':
    cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    p_row = cursor.fetchone()
    points = p_row[0] if p_row else 0
    profile_msg = t['profile_text'].format(
        user_id=user_id, points=points, lang=lang.upper()
    )
    bot.send_message(message.chat.id, profile_msg, parse_mode='Markdown')
    log_user_action(message, 'Checked Profile')

  else:
    if state == 'WAITING_QR':
      qr_text = text.strip()
      try:
        encoded_text = urllib.parse.quote(qr_text)
        qr_url = (
            'https://api.qrserver.com/v1/create-qr-code/?size=250x250&data='
            f'{encoded_text}'
        )
        bot.send_photo(
            message.chat.id, qr_url, caption='✨ QR Code generated!'
        )
        log_user_action(message, f'QR Code Generated for text: {qr_text}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to generate QR code.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_MATH':
      expression = text.strip()
      try:
        allowed_chars = set('0123456789+-*/(). ')
        if all(char in allowed_chars for char in expression):
          result = eval(expression)
          bot.send_message(
              message.chat.id,
              f'🧮 **Result:** `{expression} = {result}`',
              parse_mode='Markdown',
          )
          log_user_action(message, f'Math Solved: {expression} = {result}')
        else:
          bot.send_message(
              message.chat.id, '❌ Invalid characters in expression!'
          )
      except Exception:
        bot.send_message(message.chat.id, '❌ Invalid math expression!')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    elif state == 'WAITING_IMAGE':
      prompt = text.strip()
      bot.send_message(message.chat.id, '🎨 Generating image...')
      try:
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f'https://image.pollinations.ai/prompt/{encoded_prompt}'
        bot.send_photo(message.chat.id, image_url, caption=f'✨ Prompt: {prompt}')
        log_user_action(message, f'Text to Image Prompt: {prompt}')
      except Exception:
        bot.send_message(message.chat.id, '❌ Failed to generate image.')
      cursor.execute(
          "UPDATE users SET state = 'IDLE' WHERE user_id = ?", (user_id,)
      )
      conn.commit()

    else:
      bot.send_message(
          message.chat.id, t['welcome'], reply_markup=main_menu_keyboard(lang)
      )


# RUN BOT WITH FLASK THREAD FOR RENDER
if __name__ == '__main__':
  t = threading.Thread(target=run_web)
  t.daemon = True
  t.start()

  print('Bot is running successfully on Render with custom activity logs...')
  bot.infinity_polling(skip_pending=True)
