import os
import re
import google.generativeai as genai

# قراءة المفتاح من إعدادات GitHub
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# إعداد الذكاء الاصطناعي
model = genai.GenerativeModel('gemini-pro')

# الطلب من الذكاء الاصطناعي كتابة خبر رياضي جزائري
prompt = """
اكتب خبراً رياضياً حقيقياً ومحدثاً عن الكرة الجزائرية (المنتخب الوطني أو الدوري الجزائري) باللغة العربية.
يجب أن يكون الخبر قصيراً (من 2 إلى 3 أسطر).
اكتبه بأسلوب صحفي.
"""

response = model.generate_content(prompt)
news_text = response.text.strip()

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
# ملاحظة: نبحث عن وسم <div class="news-container"> أو ما يشابهه
if '<div class="news-container">' in html:
    html = html.replace('<div class="news-container">', '<div class="news-container">' + new_news_html)
    print("✅ تمت إضافة الخبر بنجاح!")
else:
    print("⚠️ لم يتم العثور على قسم الأخبار في الصفحة. يرجى إضافة <div class='news-container'></div> في ملف index.html")

# حفظ الملف المعدل
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
