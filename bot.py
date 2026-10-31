import os
import subprocess
import telebot

# Bot tokeni birbaşa təyin olundu
TOKEN = '9242918763:AAH_zMpEmcXUvOkM_hTiwfhaqFzP8HM1Ir8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salam! Mən video emal edən botam. Videonu göndər, onu 1080p, 90fps və rəng korreksiyası ilə emal edib sənə qaytarım.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    input_path = "input.mp4"
    output_path = "output.mp4"

    with open(input_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "⏳ Video qəbul edildi, emal olunur (1080p, 90fps)...")

    # FFmpeg əmri: 1080p, 90fps və rəng korreksiyası filtrləri
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', 'scale=1080:-2,fps=90,eq=contrast=1.1:brightness=0.03:saturation=1.2,unsharp=5:5:0.8:3:3:0.4',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'copy', output_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        with open(output_path, 'video/mp4') as vid:
            bot.send_video(message.chat.id, vid, caption="✅ Hazırdır: 1080p, 90fps")
    except Exception as e:
        bot.reply_to(message, f"❌ Xəta baş verdi: {e}")
    finally:
        # Faylları təmizləyirik
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    bot.infinity_polling()
