import os
import json

# فولدر ملفات الـ JSON
JSON_FOLDER = "downloaded"   # غيّره لو فولدر مختلف


def process_json_files():
    # نلف على كل الملفات في الفولدر
    for filename in os.listdir(JSON_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(JSON_FOLDER, filename)

            # نقرأ البيانات
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # لو الـ URL فاضي
            if not data.get("telegram_url"):
                print(f"\n[!] Missing URL in: {filename}")

                # نطلب من المستخدم URL جديد
                new_url = input("Enter URL: ").strip()

                # نحفظه
                data["telegram_url"] = new_url

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print(f"[✔] Updated: {filename}")
            else:
                print(f"[OK] {filename} already has a URL.")


if __name__ == "__main__":
    print("[+] Starting URL fixer...")
    process_json_files()
    print("\n[✔] Done!")
