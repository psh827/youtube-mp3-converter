from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os, io, uuid

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html>
<head><title>YouTube MP3</title></head>
<body>
    <h2>YouTube 링크를 MP3로 변환</h2>
    <form method="POST">
        <input type="text" name="url" size="50" placeholder="유튜브 링크를 입력하세요">
        <button type="submit">변환</button>
    </form>
    {% if download_link %}
        <p><a href="{{ download_link }}">MP3 다운로드</a></p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    if request.method == 'POST':
        url = request.form['url']
        filename = str(uuid.uuid4()) + '.mp3'
        buffer = io.BytesIO()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '-',  # 표준출력
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                # Render 서버에서는 파일 저장이 제한되므로 간단 다운로드 방식만 구현
        except Exception as e:
            return f"<h3>오류: {e}</h3>"

        download_link = f"/download/{filename}"

    return render_template_string(html, download_link=download_link)

@app.route('/download/<filename>')
def download(filename):
    # Render에서는 파일 저장 불가하므로 실제 다운로드는 따로 구현 필요
    return f"<h3>서버에서 직접 다운로드는 구현 생략됨</h3>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render가 PORT 환경변수로 포트 지정함
    app.run(host="0.0.0.0", port=port)
