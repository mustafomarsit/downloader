import aiogram
import os
import dotenv
import asyncio
import yt_dlp
import random
import re

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

dotenv.load_dotenv()

bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# URL tekshirish funksiyasi
def is_valid_url(url: str):
    return re.match(
        r"https?://(www\.)?(youtube\.com|youtu\.be|tiktok\.com|instagram\.com)/[^\s]+",
        url,
    ) is not None

@dp.message(Command("start"))
async def start_command(message: types.Message):
    username = message.from_user.username or message.from_user.full_name
    await message.answer(
        f"👋 Salom, @{username}!\n\n"
        "Men siz uchun YouTube, Instagram va TikTok videolarini yuklab beruvchi botman!\n\n"
        "📥 Linkni yuboring va men sizga videoni yuboraman. 😊"
    )

#help komandasi
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "ℹ️ Foydalanish bo‘yicha yordam:\n\n"
        "1. /start — bot haqida qisqacha ma'lumot\n"
        "2. /help — yordam oynasi\n"
        "3. Link yuboring (YouTube, TikTok, Instagram) — men sizga video yuboraman.\n\n"
        "❗ Iltimos, faqat jamoat (public) videolarni yuboring."
    )



# Linkni qabul qilib, video yuklab beruvchi funksiya
@dp.message()
async def message_handler(message: types.Message):
    url = message.text.strip()

    if is_valid_url(url):
        filename = str(random.randint(1, 100))
        opts = {"format": "best", "outtmpl": f"{filename}.%(ext)s"}

        await message.answer("⏳ Video yuklanmoqda, biroz kuting...")

        try:
            video_info = yt_dlp.YoutubeDL(opts).extract_info(url, download=True)
            video = types.FSInputFile(f"{filename}.mp4")
            await message.answer_video(video, caption=f"📹 {video_info['title']}")
        except Exception as e:
            await message.answer("❌ Video yuklab olinmadi. Xatolik yuz berdi.")
            print(e)
        finally:
            if os.path.exists(f"{filename}.mp4"):
                os.remove(f"{filename}.mp4")
    else:
        await message.answer("🚫 Bu URL noto‘g‘ri ko‘rinadi. Iltimos, to‘g‘ri link yuboring.")

# Bot ishga tushganda chiqariladigan funksiya
def on_start():
    print("✅ Bot ishga tushdi!")

# Asosiy ishga tushirish funksiyasi
async def main():
    dp.startup.register(on_start)
    await dp.start_polling(bot)

# Botni ishga tushirish
asyncio.run(main())
