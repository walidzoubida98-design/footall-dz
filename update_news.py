import os
import time
from google import genai

# قراءة المفتاح من إعدادات GitHub
api_key = os.environ.get("GEMINI_API_KEY")

# إعداد الكائن الاستدعائي (النسخة الحديثة)
client = genai.Client(api_key=api_key)

# النص المطلوب من النموذج
prompt = """
اكتب ملخصاً يومياً موجزاً عن آخر الأخبار الوطنية أو الدولية. 
يجب أن يكون النص ما بين سطرين إلى ثلاثة أسطر.
"""

def generate_with_retry(prompt, max_retries=5, wait=30):
    """توليد النص مع إعادة المحاولة عند فشل 503"""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                print(f"⚠️ محاولة {attempt+1}/{max_retries} فشلت، انتظار {wait} ثانية...")
                time.sleep(wait)
                wait = wait * 2  # 30 → 60 → 120 ...
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
        print("⚠️ لم يتم توليد النص، سيتم استخدام نص افتراضي")
        news_text = "تابعوا آخر الأخبار الوطنية والدولية من مصادرنا الموثوقة."

except Exception as e:
    print(f"❌ خطأ في توليد النص: {e}")
    news_text = "تابعوا آخر الأخبار الوطنية والدولية من مصادرنا الموثوقة."


# قراءة ملف الأخبار الحالي
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# قسم الخبر الجديد HTML
new_news_html = f"""
<div class="news-item">
    <h3>📰 خبر اليوم</h3>
    <p>{news_text}</p>
</div>
"""

# إضافة الخبر الجديد إلى index.html
# ملاحظة: عدّلي هذا الجزء حسب مكان الإضافة في ملفك
html = html.replace("<!-- NEWS_PLACEHOLDER -->", new_news_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم إضافة النص إلى index.html")
