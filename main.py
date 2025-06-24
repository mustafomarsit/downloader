import aiogram
import os
import dotenv
import asyncio
import yt_dlp
import random

dotenv.load_dotenv()

bot = aiogram.Bot(os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher()


def is_valid_url(url: str):
    if url.startswith("https://youtube.com/"):
        return True
    else:
        return False


@dp.message()
async def start_handler(message: aiogram.types.Message):
    url = message.text

    if is_valid_url(url):
        filename = random.randint(1, 100)
        opts = {"format": "best", "outtmpl": f"{filename}.%(ext)s"}

        await message.answer("video is downloading, please wait a moment...")

        video_info = yt_dlp.YoutubeDL(opts).extract_info(url, download=True)

        video = aiogram.types.FSInputFile(f"{filename}.mp4")
        await message.answer_video(video, caption=video_info["title"])

        os.remove(f"{filename}.mp4")
    else:
        await message.answer(f"{url} is not valid url.")


def on_start():
    print("bot has been started...")


async def main():
    dp.startup.register(on_start)
    await dp.start_polling(bot)


asyncio.run(main())