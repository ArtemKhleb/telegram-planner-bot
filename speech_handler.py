import os
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ContextTypes
from db import add_task

async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    voice_path_ogg = "voice.ogg"
    voice_path_wav = "voice.wav"
    await file.download_to_drive(voice_path_ogg)

    sound = AudioSegment.from_ogg(voice_path_ogg)
    sound.export(voice_path_wav, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_path_wav) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            result = add_task(text)
            await update.message.reply_text(f"📝 Задача по голосу добавлена: {result}")
        except sr.UnknownValueError:
            await update.message.reply_text("❌ Не удалось распознать голосовое сообщение.")
        except sr.RequestError:
            await update.message.reply_text("⚠️ Ошибка при соединении с сервисом распознавания.")

    os.remove(voice_path_ogg)
    os.remove(voice_path_wav)