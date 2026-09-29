import os
import re
import time
from google import genai
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key, http_options={'timeout': 120000})

prompt = """اكتب خبراً رياضياً موجزاً بالعربية عن كرة القدم الجزائرية.
يجب أن يكون:
- عنوان جذاب في سطر
- نص الخبر في سطرين أو ثلاثة
- بدون رموز ماركداون (** أو ##)"""

def generate_news():
    """يجرب عدة نماذج حتى ينجح"""
    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
    ]
    
    for model in models:
        for attempt in range(2):
            try:
                print(f"🔄 محاولة: {model} (#{attempt+1})")
                chat = client.chats.create(model=model)
                response = chat.send_message(prompt)
                if response.text and len(response.text.strip()) > 20:
                    print(f"✅ نجح مع: {model}")
                    return response.text.strip()
            except Exception as e:
                err = str(e)[:150]
                print(f"⚠️ {model} فشل: {err}")
                time.sleep(5)
    
    return None


# 1) توليد الخبر
news_text = generate_news()

if not news_text:
    news_text = "شهدت الساحة الرياضية الجزائرية تطورات جديدة، تابعونا لكل الأخبار الحصرية."
    print("⚠️ استخدام النص الاحتياطي")
else:
    print("✅ تم توليد الخبر بنجاح")


# 2) تنظيف قسم الأخبار في index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# التاريخ الحالي بالعربي
today = datetime.now().strftime("%d/%m/%Y")

# قالب الخبر الجديد
news_block = f'''    <div class="news-auto-card" id="auto-news">
      <span class="news-auto-date">📅 {today}</span>
      <h3>📰 خبر اليوم</h3>
      <p>{news_text}</p>
    </div>'''

# استبدال القسم القديم (بين <div class="news-auto-card"...> و </div> الأخير)
pattern = r'<div class="news-auto-card" id="auto-news">.*?</div>'
html = re.sub(pattern, news_block, html, count=1, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم تحديث index.html بنجاح")
