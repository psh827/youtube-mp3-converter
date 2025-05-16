import yt_dlp

def download_as_mp3(youtube_url):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # 저장 파일 이름: 영상 제목.mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # 192kbps
        }],
        'noplaylist': True,
        'quiet': False,  # 다운로드 진행상황 표시
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([youtube_url])

if __name__ == "__main__":
    url = input("유튜브 링크를 입력하세요: ").strip()
    try:
        download_as_mp3(url)
        print("MP3 변환이 완료되었습니다!")
    except Exception as e:
        print(f"오류 발생: {e}")
