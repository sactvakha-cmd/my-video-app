import os
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__, template_folder=".") # ตั้งค่าให้หาไฟล์ html ในโฟลเดอร์เดียวกันได้เลยเพื่อความง่าย

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "กรุณาใส่ลิงก์", 400

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}", 500

if __name__ == '__main__':
    # ตั้งค่าให้รองรับการรันบนระบบ Cloud
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
