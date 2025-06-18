Mana siz so‘ragan **README.md** fayliga qisqa **loyiha tavsifi** va **clone qilib ishlatish bo‘yicha markdown ko‘rsatmalar** qo‘shilgan professional shakli:

---

### 📄 `README.md`

````markdown
# 🧰 JobFinder – Django asosidagi ish topish platformasi

JobFinder — bu Django framework asosida qurilgan ochiq manbali web ilova bo‘lib, ish beruvchilar va ish izlovchilarni bog‘lashga xizmat qiladi. Foydalanuvchilar profil yaratib, ish e’lonlarini ko‘rishlari va ishga ariza yuborishlari mumkin.

---

## 🔥 Xususiyatlar

- 👤 Foydalanuvchi autentifikatsiyasi (ro‘yxatdan o‘tish, login)
- 💼 Ish e’lonlarini qo‘shish va ko‘rish
- 📄 HTML shablonlar yordamida frontend
- 🔒 Maxfiy sozlamalar `.env` orqali boshqariladi

---

## 🚀 Loyihani ishga tushirish

Quyidagi buyruqlar orqali loyihani yuklab olib ishga tushiring:

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/your-username/jobfinder.git
cd jobfinder
````

### 2. Virtual environment yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Talablarni o‘rnatish

```bash
pip install -r requirements.txt
```

### 4. `.env` faylini yaratish

`.env` faylni asosiy papkaga quyidagi formatda qo‘shing:

```
SECRET_KEY=django-insecure-XXXXXX
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Migratsiyalar va serverni ishga tushirish

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

👉 Web ilova manzili: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Superuser yaratish (admin panel uchun)

```bash
python manage.py createsuperuser
```

Admin panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 📂 Loyihaning qisqacha tuzilishi

```
jobfinder/
├── accounts/        # Foydalanuvchilar bilan bog‘liq app
├── jobs/            # Ish e’lonlari app
├── templates/       # HTML fayllar
├── static/          # Statik fayllar (CSS, JS)
├── media/           # Yuklangan fayllar
├── .env             # Maxfiy sozlamalar
├── manage.py        # Django boshqaruv fayli
└── requirements.txt # Kutubxonalar ro‘yxati
```

---

## 🤝 Litsenziya

Ushbu loyiha MIT litsenziyasi asosida tarqatiladi — istalgan maqsadda foydalanishingiz mumkin.

---

## 👤 Muallif

Samandar Khamrayev — 2025
GitHub: [https://github.com/samandar-hamrayev/](https://github.com/samandar-hamrayev/)

```

