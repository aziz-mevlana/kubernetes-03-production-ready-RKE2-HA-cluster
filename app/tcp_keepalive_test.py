#!/usr/bin/env python3
"""
Long-lived TCP connection test (10+ dakika).
Istio Gateway (31400) uzerinden socket uygulamasina bağlanir,
idle-timeout'a dusmemek icin periyodik PING atar, yanitlari loglar.
Baglanti koparsa script exit code 1 verir.

Kullanim:
    python3 tcp_keepalive_test.py <host> <port> [duration_seconds]
"""
import socket
import sys
import time
import datetime

HOST = sys.argv[1] if len(sys.argv) > 1 else "10.53.0.207"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 31400
DURATION = int(sys.argv[3]) if len(sys.argv) > 3 else 600  # 10 dakika
PING_INTERVAL = 25  # saniye (server idle timeout 60sn, 25sn guvenli)


def log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(20)
    log(f"Baglaniyor: {HOST}:{PORT}")
    sock.connect((HOST, PORT))
    log("TCP baglantisi kuruldu (Istio Gateway uzerinden)")

    sock.settimeout(PING_INTERVAL + 10)
    start = time.time()
    counter = 0

    try:
        while time.time() - start < DURATION:
            counter += 1
            sock.sendall(b"PING\n")
            data = sock.recv(1024)
            if b"PONG" not in data:
                log(f"HATA: beklenmeyen yanit: {data!r}")
                return 1
            elapsed = int(time.time() - start)
            log(f"[{counter}] PONG alindi - baglanti acik ({elapsed}s/ {DURATION}s)")
            time.sleep(PING_INTERVAL)
        log("TEST BASARILI: baglanti kesintisiz acik kaldi.")
        return 0
    except (socket.timeout, ConnectionResetError, BrokenPipeError, OSError) as e:
        log(f"FAIL: baglanti koptu ({e})")
        return 1
    finally:
        sock.close()


if __name__ == "__main__":
    sys.exit(main())