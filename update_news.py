import os
import google.generativeai as genai

# قراءة المفتاح من إعدادات GitHub
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# إعداد الذكاء الاصطناعي (موديل حديث ومتوافق)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# الطلب من الذكاء الاصطناعي كتابة خبر رياضي جزائري
prompt = """
اكتب خبراً رياضياً حقيقياً ومحدثاً عن الكرة الجزائرية (المنتخب الوطني أو الدوري الجزائري) باللغة العربية.
يجب أن يكون الخبر قصيراً (من 2 إلى 3 أسطر).
اكتبه بأسلوب صحفي.
"""

try:
    response = model.generate_content(prompt)
    news_text = response.text.strip()
    print("✅ تم توليد الخبر بنجاح:")
    print(news_text)
except Exception as e:
    print(f"❌ خطأ في توليد الخبر: {e}")
    news_text = "شهدت الساحة الرياضية الجزائرية تطورات جديدة، تابعونا لكل الأخبار الحصرية."

# قراءة ملف الموقع الحالي
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# تجهيز كود HTML للخبر الجديد
new_news_html = f'''
<div class="news-item">
    <h3>📰 خبر جديد</h3>
    <p>{news_text}</p>
</div>
'''

# إضافة الخبر الجديد قبل إغلاق قسم الأخبار
if '<div class="news-container">' in html:
    html = html.replace(
        '<div class="news-container">',
        '<div class="news-container">' + new_news_html,
        1
    )
    print("✅ تمت إضافة الخبر إلى index.html بنجاح!")
else:
    print("⚠️ لم يتم العثور على news-container في index.html")

# حفظ الملف المعدل
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
