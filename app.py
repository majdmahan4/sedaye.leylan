from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def get_client_ip(request):
    """Get client IP address considering proxy headers"""
    # Check for X-Forwarded-For header first (used by Render, Cloudflare, etc.)
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def is_iranian_ip(ip):
    """Check if IP belongs to Iran using ipinfo.io API"""
    try:
        # Alternative API: http://ip-api.com/json/{ip}?fields=countryCode
        response = requests.get(
            f"https://ipinfo.io/{ip}/json?token=a659e8a8d75d01",
            timeout=3
        )
        data = response.json()
        country = data.get("country", "").upper()
        return country == "IR"
    except Exception as e:
        print(f"IP Check Error: {e}")
        return False  # Fail-safe: assume not Iranian if API fails

@app.route('/')
def home():
    ip = get_client_ip(request)
    print(f"Client IP: {ip}")  # Debug - view in Render logs
    
    if is_iranian_ip(ip):
        # Content for Iranian users
        content = """
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>تبلیغات ویژه</title>
            <style>
                body {
                    font-family: Tahoma, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    text-align: right;
                }
                .container {
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    max-width: 600px;
                    margin: auto;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                }
                h1 {
                    color: #e74c3c;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    text-decoration: none;
                    color: #fff;
                    background: #27ae60;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>به صفحه تبلیغات ویژه خوش آمدید</h1>
                 <p>
                    تا حالا فکر کرده‌اید که چه اسراری پشت پرده شهرداری و فرمانداری لیلان وجود دارد؟ شاید باور نکنید، اما شواهدی هست که نشان می‌دهد برخی مسئولان با بازی‌های ناعادلانه و تقلب‌های سیستماتیک سعی در فریب مردم دارند. من اطلاعاتی دارم که می‌تواند دیدگاه شما را نسبت به این موضوعات دگرگون کند. از تقلب‌های پنهانی تا فسادهای آشکار، همه چیز در اینجا برای شما فاش شده است.
                </p>
                <a href="https://example.com/ir">مشاهده جزئیات</a>
            </div>
        </body>
        </html>
        """
    else:
        # Content for non-Iranian users
        content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Restricted</title>
            <style>
                .popup {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .popup-content {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    text-align: center;
                    max-width: 400px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                }
            </style>
        </head>
        <body>
            <div class="popup">
                <div class="popup-content">
                    <h2>دسترسی محدود</h2>
                    <p>لطفاً فیلترشکن خود را غیرفعال کنید تا به محتوای ویژه دسترسی پیدا کنید.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    return render_template_string(content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
