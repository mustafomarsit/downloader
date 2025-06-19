import aiogram
import os
import aiogram.filters
import dotenv
import asyncio
import yt_dlp
import random

dotenv.load_dotenv()

bot = aiogram.Bot(os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher()


@dp.message()
async def start_handler(message: aiogram.types.Message):
   url = message.text 
   filename = random.randint(1,100)
   opts = {"format" : "best" , "outtmpl" : f"{filename}.%(ext)s"}

   yt_dlp.YoutubeDL(opts).download(url)

   video = aiogram.types.FSInputFile(f"{filename}.mp4")

   await message.answer_video(video)

   os.remove(f"{filename}.mp4")

def on_start():
    print("bot has been started...")

async def main():
    dp.startup.register(on_start)
    await dp.start_polling(bot)

asyncio.run(main())

