FROM python:3.11-slim

# Install system dependencies for PsychoPy (audio, video, OpenGL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libegl1-mesa \
    libgles2-mesa \
    libasound2 \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY experiments/ ./experiments/
COPY config/ ./config/
COPY data/ ./data/
COPY output/ ./output/

# Use virtual display for headless rendering
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=offscreen

COPY docker/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "-c", "import psychopy; print(f'PsychoPy {psychopy.__version__} ready')"]
