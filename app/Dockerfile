# Resmi hafif Python imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksiz dosyaları engellemek ve python çıktısını doğrudan konsola yansıtmak için
ENV PYTHONUNBUFFERED=1

# Kodları çalışma dizinine kopyala
COPY server.py .

# Uygulamanın dinleyeceği portu belirt
EXPOSE 8080

# Sunucuyu başlat
CMD ["python", "server.py"]
