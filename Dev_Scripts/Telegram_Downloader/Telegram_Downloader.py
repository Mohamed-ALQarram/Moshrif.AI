from telethon import TelegramClient
import asyncio
import os
import json
import re

# --- Telegram API ---
# API ID + API HASH
api_id = 000000 #write your id
api_hash = "your-API"

# قناة النصوص
SOURCE_CHANNEL = "https://t.me/moshrif_knowledge"

# القناة اللي هندور فيها على الفيديوهات فقط
ALLOWED_CHANNELS = ["moshrif_youtube"]

# فولدر الإخراج
OUTPUT_FOLDER = "downloaded"


# --- Normalization ---
def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower()

    # إزالة الامتدادات
    text = re.sub(r"\.(txt|mp4|pdf|mkv|mov|avi|mp3|m4a|ogg)$", "", text)

    # توحيد الهمزات
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")

    # إزالة الرموز
    text = re.sub(r"[_\-\.;,]", " ", text)

    # إزالة المسافات الزيادة
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --- استخراج لينك رسالة تليجرام ---
async def extract_link_from_msg(msg):
    chat = await msg.get_chat()
    username = getattr(chat, "username", None)

    if username:  # قناة عامة
        return f"https://t.me/{username}/{msg.id}"

    # قناة خاصة
    if hasattr(msg.peer_id, "channel_id"):
        return f"https://t.me/c/{msg.peer_id.channel_id}/{msg.id}"

    return ""


# --- البحث الأساسي (Global-like search) ---
async def global_search(query: str):
    query_norm = normalize(query)

    async for msg in client.iter_messages(None, search=query_norm, limit=50):

        # معرفة أصل الرسالة
        chat = await msg.get_chat()
        username = getattr(chat, "username", None)

        # لو الرسالة مش من القناة المطلوبة → تجاهل
        if not username or username not in ALLOWED_CHANNELS:
            continue

        # لو الرسالة بدون file → مالهاش لازمة
        if not msg.file:
            continue

        mime = getattr(msg.file, "mime_type", "")

        # -------------------------------
        #   أولوية 1 → VIDEO
        # -------------------------------
        if mime.startswith("video"):

            # تطابق مع نص الرسالة
            text = msg.message or ""
            if query_norm in normalize(text):
                url = await extract_link_from_msg(msg)
                file_no_ext = msg.file.name.rsplit(".", 1)[0]
                return url, file_no_ext

            # تطابق مع اسم الملف
            if msg.file.name and query_norm in normalize(msg.file.name):
                url = await extract_link_from_msg(msg)
                file_no_ext = msg.file.name.rsplit(".", 1)[0]
                return url, file_no_ext

        # -------------------------------
        #   أولوية 2 → AUDIO
        # -------------------------------
        if mime.startswith("audio"):

            text = msg.message or ""
            if query_norm in normalize(text):
                url = await extract_link_from_msg(msg)
                file_no_ext = msg.file.name.rsplit(".", 1)[0]
                return url, file_no_ext

            if msg.file.name and query_norm in normalize(msg.file.name):
                url = await extract_link_from_msg(msg)
                file_no_ext = msg.file.name.rsplit(".", 1)[0]
                return url, file_no_ext

    # لو مفيش فيديو ولا صوت مطابق
    return "", ""


# --- العملية الأساسية ---
async def main():

    await client.start()
    print("[+] Logged in successfully")

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # نلف على ملفات TXT
    async for msg in client.iter_messages(SOURCE_CHANNEL):

        if msg.file and msg.file.name.endswith(".txt"):

            filename = msg.file.name
            print(f"\n[+] Processing {filename}")

            # تحميل ملف txt
            file_path = await msg.download_media(OUTPUT_FOLDER + "/")
            print(f"[+] Downloaded: {file_path}")

            # قراءة محتوى txt
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            name_no_ext = filename.rsplit(".", 1)[0]

            print(f"[~] Searching for media using: {name_no_ext}")
            url, clean_name = await global_search(name_no_ext)

            if url:
                print(f"[+] Media Found: {url}")
            else:
                print("[!] No media found (URL empty)")

            # JSON
            json_data = {
                "filename": clean_name if clean_name else name_no_ext,
                "telegram_url": url,
                "content": content
            }

            json_path = os.path.join(OUTPUT_FOLDER, name_no_ext + ".json")

            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(json_data, jf, ensure_ascii=False, indent=4)

            print(f"[✔] Saved JSON: {json_path}")

            # حذف txt الأصلي
            os.remove(file_path)


client = TelegramClient("session", api_id, api_hash)
asyncio.run(main())
