import subprocess
import sys
import os
import pathlib
import urllib.request
import io
import json
import re
import shutil
from PIL import Image

def clone_final_perfect():
    url = "https://iskusstvo-zaboty-o-t-qqkkaff.gamma.site/"
    repo = "x2v0/andrey-massage-test"
    
    print("=== 1. Скачиваем HTML и парсим JSON ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # Извлекаем JSON
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not match:
        print("❌ JSON не найден!")
        sys.exit(1)
        
    json_data = json.loads(match.group(1))
    
    images = set()
    def extract_imgs(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'url' and isinstance(v, str) and 'cdn.gamma.app' in v: images.add(v)
                else: extract_imgs(v)
        elif isinstance(obj, list):
            for i in obj: extract_imgs(i)
            
    extract_imgs(json_data)

    print("=== 2. Скачиваем картинки с правильными именами ===")
    os.makedirs("assets/images", exist_ok=True)
    
    # Жесткая привязка хэшей Gamma к нашим именам
    mapping = {
        "2f59a233": "avatar.webp",
        "b1be837c": "cabinet.webp",
        "c3071931": "neck1.webp",
        "7d229ba2": "back.webp",
        "95b869a4": "legs.webp",
        "f038f01f": "diploma.webp",
        "d90988be": "certificate.webp",
        "f8613bea": "master.webp",
        "5a10b8fc": "gate.webp",
        "fe1def6f": "calf.webp",
        "b82082ec": "calf1.webp",
        "4c1910dd": "wall.webp"
    }
    
    source_dir = pathlib.Path.home() / "andrey-perfect" / "assets" / "images"

    for img_url in sorted(images):
        match = re.search(r"([a-f0-9]{8})", img_url)
        if not match:
            continue
        hash_val = match.group(1)
        new_name = mapping.get(hash_val)
        
        if not new_name:
            continue # Пропускаем неизвестные картинки

        target_path = f"assets/images/{new_name}"
        
        # Если картинка уже есть в боевой папке, просто копируем ее (быстро)
        if (source_dir / new_name).exists():
            shutil.copy(source_dir / new_name, target_path)
            print(f"  [+] Скопирована: {new_name}")
            continue

        # Иначе скачиваем и сжимаем
        try:
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req_img).read()
            img = Image.open(io.BytesIO(data))
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.thumbnail((800, 800), Image.Resampling.LANCZOS)
            img.save(target_path, "WEBP", quality=80)
            print(f"  [+] Скачана: {new_name}")
        except Exception as e:
            print(f"  [-] Ошибка {new_name}: {e}")

    print("=== 3. Генерируем красивый HTML ===")
    html_out = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Массажист Андрей | Ваш путь к здоровью</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #f4f9f9; --card: #ffffff; --text: #2d3748; --muted: #718096; --accent: #0fa37f; --border: #e2e8f0; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Inter", sans-serif; }
        body { background-color: var(--bg); color: var(--text); line-height: 1.6; padding-bottom: 40px; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px 15px; }
        .hero { text-align: center; padding: 40px 0 30px 0; }
        .avatar { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; margin-bottom: 20px; border: 4px solid #fff; box-shadow: 0 8px 24px rgba(15, 163, 127, 0.15); }
        h1 { font-size: 2rem; margin-bottom: 15px; font-weight: 700; color: #1a202c; }
        h2 { font-size: 1.8rem; margin-bottom: 5px; font-weight: 700; color: #1a202c; }
        .subtitle { font-size: 1.2rem; color: var(--muted); margin-bottom: 15px; }
        .phone { font-size: 1.1rem; margin-bottom: 25px; font-weight: 500; }
        .btn-group { display: flex; flex-direction: column; gap: 12px; margin: 0 auto 40px auto; }
        .btn { display: block; padding: 16px; background: var(--accent); color: white; text-decoration: none; border-radius: 12px; font-size: 1.1rem; font-weight: 600; text-align: center; box-shadow: 0 4px 15px rgba(15, 163, 127, 0.3); }
        .btn-outline { background: transparent; border: 2px solid var(--accent); color: var(--accent); box-shadow: none; }
        .section { background: var(--card); margin-bottom: 25px; padding: 30px 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04); border: 1px solid var(--border); }
        .section h3 { font-size: 1.3rem; margin-bottom: 20px; font-weight: 700; }
        .section p { margin-bottom: 15px; color: var(--muted); font-size: 1rem; }
        .section ul { list-style-type: none; padding-left: 0; margin-bottom: 20px; }
        .section ul li { margin-bottom: 15px; font-size: 1rem; color: var(--muted); position: relative; padding-left: 20px; }
        .section ul li::before { content: "•"; color: var(--accent); position: absolute; left: 0; font-size: 1.5rem; top: -4px; }
        .section ul li strong { color: var(--text); font-weight: 600; display: block; }
        .image-block { margin-bottom: 30px; text-align: center; }
        .image-block img { width: 100%; border-radius: 16px; display: block; margin-bottom: 12px; object-fit: cover; }
        .image-caption { font-size: 1.05rem; font-weight: 500; }
        .narrow-img { width: 85%; max-width: 400px; margin: 0 auto 25px auto; display: block; border-radius: 16px; }
        .accent-card { background: linear-gradient(135deg, #0fa37f, #0c8a6b); padding: 25px; border-radius: 16px; margin-bottom: 30px; text-align: center; }
        .accent-card img { width: 100%; border-radius: 12px; margin-bottom: 20px; display: block; }
        .accent-card p { color: white; font-size: 1.2rem; margin: 0; font-weight: 600; }
        .map-container { width: 100%; height: 300px; border-radius: 16px; overflow: hidden; margin-top: 20px; }
        .map-container iframe { width: 100%; height: 100%; border: none; }
        .footer { font-size: 0.85rem; color: var(--muted); text-align: center; padding: 20px 0; margin-top: 10px; }
        @media (min-width: 768px) {
            .container { max-width: 800px; }
            .hero .btn-group { flex-direction: row; justify-content: center; }
            .hero .btn-group .btn { padding: 16px 40px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>Ваш путь к здоровью</h1>
            <img src="assets/images/avatar.webp" alt="Андрей" class="avatar">
            <h2>Массажист Андрей.</h2>
            <p class="subtitle">Тело скажет вам спасибо.</p>
            <p class="phone">Тел./SMS: 89804874646</p>
            <div class="btn-group">
                <a href="https://t.me/Andrey_Looo" class="btn">Записаться в Telegram</a>
                <a href="https://max.ru/u/f9LHodD0cOK26pA79D_jKjFz6mb_iOC8FaNsI9dEB3l6uTNIQU7Qn5KM-xA" class="btn btn-outline">Написать в MAX</a>
            </div>
        </div>

        <div class="section">
            <h3>🧖 Классический массаж</h3>
            <p>⏳ Длительность: 60 минут<br>💰 Стоимость: 2 500 руб.</p>
            <p><em>Восстановления тонуса, снятия мышечного напряжения и глубокой релаксации.</em></p>
            <h3 style="margin-top: 30px;">✨ Зоны особого внимания:</h3>
            <ul>
                <li><strong>Шейный отдел</strong> — снимает зажимы, убирает чувство «тяжелой головы».</li>
                <li><strong>Грудной отдел</strong> — раскрывает плечи, помогает расправить спину.</li>
                <li><strong>Поясничный отдел</strong> — убирает усталость и глубоко расслабляет мышцы.</li>
            </ul>
        </div>

        <div class="section" style="text-align: center;">
            <h3 style="text-transform: uppercase;">КАБИНЕТ</h3>
        </div>
        <div class="image-block"><img class="narrow-img" src="assets/images/cabinet.webp" alt="Кабинет"></div>
        <div class="image-block">
            <img class="narrow-img" src="assets/images/legs.webp" alt="Грудной отдел">
            <div class="image-caption">Грудной отдел</div>
        </div>
        <div class="image-block">
            <img class="narrow-img" src="assets/images/neck1.webp" alt="Шейно-воротниковая зона">
            <div class="image-caption">Шейно-воротниковая зона</div>
        </div>
        <div class="image-block">
            <img class="narrow-img" src="assets/images/back.webp" alt="Поясничный отдел">
            <div class="image-caption">Поясничный отдел</div>
        </div>

        <div class="section" style="background: transparent; border: none; text-align: center; padding: 0;">
            <p style="color: var(--text); font-size: 1.1rem; font-weight: 500;">Проработаем икроножную, камбаловидную и переднюю большеберцовую мышцы.</p>
        </div>
        <div class="image-block"><img class="narrow-img" src="assets/images/calf.webp" alt="Массаж ног"></div>
        <div class="image-block"><img class="narrow-img" src="assets/images/calf1.webp" alt="Массаж ног"></div>

        <div class="section">
            <h3>🎓 Экспертность и доверие</h3>
            <div class="image-block">
                <img src="assets/images/certificate.webp" alt="Сертификат" class="narrow-img">
            </div>
            <div class="accent-card">
                <img src="assets/images/diploma.webp" alt="Диплом">
                <p>Опыт работы - более 4 лет.</p>
            </div>
        </div>

        <div class="section">
            <h3>📍 Адрес</h3>
            <p>Московская обл. Дмитровский г.о. пос. Овсянниково ул. Соловьиная роща д. 3</p>
            <p>Шлагбаум. Для открытия звоните по телефону 89804874646</p>
            <div class="map-container">
                <iframe src="https://yandex.ru/map-widget/v1/?text=Московская%20обл.%20Дмитровский%20г.о.%20пос.%20Овсянниково%20ул.%20Соловьиная%20роща%20д.%203&z=16"></iframe>
            </div>
        </div>

        <div class="section" style="background: transparent; border: none; text-align: center; padding: 0;">
            <p style="color: var(--text); font-size: 1.1rem; font-weight: 500;">Калитка для входа и въездные ворота для автомобиля.</p>
        </div>
        <div class="image-block"><img src="assets/images/gate.webp" alt="Ворота" class="narrow-img"></div>
        <div class="image-block"><img src="assets/images/wall.webp" alt="Забор" class="narrow-img"></div>

        <div class="footer">
            <p>Налоговый статус-самозанятый. ИНН 501000559757</p>
            <p>Услуги носят исключительно эстетический (бытовой) характер, направлены на уход за телом и релаксацию, и не являются медицинскими процедурами.</p>
        </div>
    </div>
</body>
</html>"""

    pathlib.Path("index.html").write_text(html_out, encoding="utf-8")
    pathlib.Path(".nojekyll").touch()

    print("=== 4. Деплой ===")
    subprocess.run(["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "Final Beautiful Clone (Mapped Images)"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "branch", "-M", "master"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "remove", "origin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{repo}.git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push", "-u", "origin", "master", "-f"], stdout=subprocess.DEVNULL)
    subprocess.run(["gh", "api", "-X", "POST", f"repos/{repo}/pages", "-f", "source[branch]=master", "-f", "source[path]=/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"\n✅ ГОТОВО! Сайт доступен: https://x2v0.github.io/andrey-massage-test/")

if __name__ == "__main__":
    clone_final_perfect()
    
