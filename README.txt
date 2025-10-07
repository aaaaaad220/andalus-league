
مشروع: Andalusian Champions League

ملف مضغوط يحتوي على تطبيق Flask بسيط لعرض:
- الصفحة الرئيسية
- جدول المباريات
- التشكيلة
- جدول الترتيب
- لوحة تحكم مع تسجيل دخول (يتطلب إدخال MAC يدوياً)

كيفية التشغيل:
1. ثبت بايثون (3.8+).
2. ثبّت Flask:
   pip install Flask
3. فك الضغط وتشغيل:
   cd andalusian_champions_league
   python app.py
4. افتح المتصفح: http://127.0.0.1:5000

بيانات الدخول التجريبية موجودة في users.json:
- username: admin
- password: admin123
- mac: 00:11:22:33:44:55

ملاحظة: للوصول للوحة التحكم، استخدم الصفحة /dashboard وأدخل اليوزر والباسورد والـ MAC.

