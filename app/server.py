import asyncio
import logging

# Loglama ayarları
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peername = writer.get_extra_info('peername')
    logging.info(f"Yeni TCP bağlantısı kuruldu: {peername}")
    
    try:
        while True:
            # İstemciden veri veya ping bekle (Örn: 60 saniye boyunca veri gelmezse zaman aşımı)
            data = await asyncio.wait_for(reader.read(1024), timeout=60.0)
            if not data:
                logging.info(f"İstemci bağlantıyı sonlandırdı: {peername}")
                break
            
            message = data.decode().strip()
            logging.info(f"Alınan mesaj ({peername}): {message}")
            
            if message.upper() == "PING":
                writer.write(b"PONG\n")
                await writer.drain()
            elif message.upper() == "EXIT":
                writer.write(b"Gule gule!\n")
                await writer.drain()
                break
            else:
                response = f"ECHO: {message}\n"
                writer.write(response.encode())
                await writer.drain()
                
    except asyncio.TimeoutError:
        logging.warning(f"Zaman aşımı (Idle Timeout): {peername} uzun süre sessiz kaldı, bağlantı düşürülüyor.")
    except Exception as e:
        logging.error(f"Bağlantı hatası ({peername}): {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        logging.info(f"Bağlantı kapatıldı ve kaynaklar serbest bırakıldı: {peername}")

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    addr = server.sockets[0].getsockname()
    logging.info(f"TCP Socket Sunucusu aktif ve dinleniyor: {addr}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Sunucu manuel olarak durduruldu.")
