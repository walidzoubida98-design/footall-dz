import os
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
    http_options={'timeout': 60000}
)

prompt = """
اكتب ملخصاً يومياً موجزاً عن آخر الأخبار الوطنية أو الدولية. 
يجب أن يكون النص ما بين سطرين إلى ثلاثة أسطر.
"""

def generate_with_retry(prompt, max_retries=3, wait=10):
    for attempt in range(max_retries):
        try:
            chat = client.chats.create(model="gemini-3.8-flash")
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                print(f"⚠️ محاولة {attempt+1}/{max_retries} فشلت، انتظار {wait}s...")
                time.sleep(wait)
                wait *= 2
            else:
                raise e
    return None


try:
    news_text = generate_with_retry(prompt)
    if news_text:
        news_text = news_text.strip()
        print("✅ تم توليد النص بنجاح")
        print(news_text)
    else:
        news_text = "تابعوا آخر الأخبار الوطنية والدولية من مصادرنا الموثوقة."
except Exception as e:
    print(f"❌ خطأ: {e}")
    news_text = "تابعوا آخر الأخبار الوطنية والدولية من مصادرنا الموثوقة."


with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_news_html = f"""
<div class="news-section" style="padding: 30px 20px; max-width: 1200px; margin: 0 auto;">
    <h3 style="color: #006233; margin-bottom: 15px;">📰 خبر اليوم</h3>
    <p style="line-height: 1.8; color: #222;">{news_text}</p>
</div>
"""

html = html.replace("</body>", new_news_html + "\n</body>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم إضافة الخبر إلى index.html")
