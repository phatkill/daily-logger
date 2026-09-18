import http.server
import socketserver
import socket
import webbrowser
import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect, just finds the outbound interface IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def print_qr_code(url):
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        print("\n" + "="*50)
        print("  QUET MA QR NAY TREN DIEN THOAI DE MO APP:")
        print("="*50 + "\n")
        qr.print_ascii(invert=True)
    except Exception as e:
        pass

def run_server(port=8080):
    # Set cwd to daily-logger dir
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)

    ip = get_local_ip()
    local_url = f"http://localhost:{port}"
    lan_url = f"http://{ip}:{port}"

    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.manifest': 'text/cache-manifest',
        '.json': 'application/json',
    })

    # Try binding port
    while True:
        try:
            httpd = socketserver.TCPServer(("", port), Handler)
            break
        except OSError:
            port += 1
            local_url = f"http://localhost:{port}"
            lan_url = f"http://{ip}:{port}"

    print("\n" + "#"*60)
    print("  🚀 DAILY LOGGER - NHAT KY 1 CHAM DA KHOI CHAY!")
    print("#"*60)
    print(f"\n👉 Tren may tinh:  {local_url}")
    print(f"📱 Tren dien thoai: {lan_url}")
    print("\n(Dien thoai va may tinh can ket noi chung mang Wi-Fi)")

    print_qr_code(lan_url)

    print("\n💡 MEI DUNG:")
    print("1. Mo camera dien thoai quet ma QR hoac go link vao trinh duyet.")
    print("2. Chon 'Them vao Man hinh chinh' (Add to Home Screen) de dung nhu App Store/CH Play!")
    print("3. Nhan Ctrl + C de dung server.\n")

    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung server. Tam biet!")

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
