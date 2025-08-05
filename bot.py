from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os
from youtubesearchpython import VideosSearch

AUDD_API_TOKEN= "4343bcb8509693d30c70a106f4099519"
TELEGRAM_BOT_TOKEN= "7795235602:AAEqchim5sZgbzUv17kGymFBoJqd7cInCE4"

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await voice.get_file()
    file_path = f"{voice.file_id}.ogg"
    await file.download_to_drive(file_path)

    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'api_token': AUDD_API_TOKEN,
            'return': 'apple_music,spotify',
        }
        response = requests.post('https://api.audd.io/', data=data, files=files)

    os.remove(file_path)
    result = response.json()

    if result['status'] == 'success' and result['result']:
        title = result['result']['title']
        artist = result['result']['artist']
        query = f"{artist} {title}"

        videos_search = VideosSearch(query, limit=1)
        yt_result = videos_search.result()['result'][0]
        yt_link = yt_result['link']

        await update.message.reply_text(f"آهنگ پیدا شد 🎵:\n{query}\nلینک یوتیوب: {yt_link}")
    else:
        await update.message.reply_text("متأسفم، نتونستم آهنگ رو تشخیص بدم 😔")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Bot is running...")
    app.run_polling()
