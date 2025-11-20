from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__) # Düzeltildi: __name__

# DATABASE_URL'i ortam değişkeninden alıyoruz. 
# Render'da "Environment Variables" kısmına DATABASE_URL eklemelisin.
DATABASE_URL = os.getenv("DATABASE_URL")

# HTML ŞABLONU
HTML = """
<!doctype html>
<html>
<head>
    <title>Buluttan Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; } /* Düzeltildi: text-align, padding */
        h1 { color:#333; }
        form { margin: 20px auto; }
        input { padding: 10px; font-size: 16px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        ul { list-style: none; padding: 0; } /* Düzeltildi: Süslü parantez {} */
        li { background: white; margin: 5px auto; padding: 8px; border-radius: 5px; max-width: 300px; }
    </style>
</head>
<body>
    <h1>☁️ Buluttan Selam!</h1>
    <p> Adını Yaz, selamını bırak👇</p>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını Yaz" required>
        <button type="submit">Gönder</button> </form>
    <h3>Ziyaretçiler:</h3>
    <ul>
        {% for ad in isimler %}
             <li>{{ ad }}</li>
        {% endfor %} </ul>
</body>    
</html>
"""

def connect_db():
    # Eğer DATABASE_URL yoksa hata vermemesi için kontrol eklenebilir ama Render'da bu zorunlu.
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = connect_db()
    cur = conn.cursor()
    
    # Tablo oluşturma
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    # POST isteği geldiyse (Form gönderildiyse)
    if request.method == "POST":
        isim = request.form.get("isim")
        if isim:
            # Düzeltildi: SQL syntax hatası giderildi (parantezler ve VALUES yeri)
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()
    
    # Verileri çekme (Her durumda çalışmalı, girinti düzeltildi)
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()
    
    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__": # Düzeltildi: __name__ ve __main__
    app.run(host="0.0.0.0", port=5000)
