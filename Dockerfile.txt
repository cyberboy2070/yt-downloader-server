FROM python:3.11-slim

# Installiere FFmpeg, Node.js und npm (wichtig für yt-dlp JS-Challenges)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 10000

CMD ["python", "server.py"]
