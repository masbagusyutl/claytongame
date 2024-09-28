import time
import requests
import json
from datetime import datetime, timedelta, timezone
from termcolor import colored

def format_time(dt_str):
    # Ubah string ISO 8601 menjadi datetime dengan format yang mudah dibaca
    # Tangani kasus di mana string waktu memiliki nanodetik terlalu panjang
    if '.' in dt_str:
        dt_str = dt_str.split('.')[0] + 'Z'
    
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def login(account_data):
    login_url = "https://tonclayton.fun/api/user/login"
    headers = {
        "Content-Type": "application/json",
        "Init-Data": account_data,
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "2",
        "Origin": "https://tonclayton.fun",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://tonclayton.fun/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    payload = {}
    response = requests.post(login_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def claim_farming(headers):
    claim_url = "https://tonclayton.fun/api/user/claim"
    payload = {}
    response = requests.post(claim_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(colored("Farming berhasil.", 'green'))
    else:
        print(colored("Gagal melakukan farming.", 'red'))

def start_farming(headers):
    start_farming_url = "https://tonclayton.fun/api/user/start"
    payload = {}
    response = requests.post(start_farming_url, headers=headers, json=payload)
    if response.status_code == 200:
        start_time = response.json().get('start_time')
        if start_time:
            start_time = format_time(start_time)
            print(colored(f"Farming dimulai pada: {start_time}", 'green'))
        else:
            print(colored("Kunci 'start_time' tidak ditemukan dalam respons.", 'yellow'))
    else:
        print(colored("Gagal memulai farming.", 'red'))

def start_game(headers):
    start_game_url = "https://tonclayton.fun/api/game/start-game"
    payload = {}
    response = requests.post(start_game_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(colored("Game dimulai.", 'green'))
    else:
        print(colored("Gagal memulai game.", 'red'))

def save_tile(headers, max_tile):
    save_tile_url = "https://tonclayton.fun/api/game/save-tile-game"
    payload = {"maxTile": max_tile}
    response = requests.post(save_tile_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(colored(f"MaxTile: {max_tile} - {response.json()['message']}", 'green'))

def end_game(headers):
    over_game_url = "https://tonclayton.fun/api/game/over-game"
    payload = {}
    response = requests.post(over_game_url, headers=headers, json=payload)
    if response.status_code == 200:
        print(colored(f"Game selesai, Earn: {response.json()['earn']}", 'green'))

# Baca data dari file data.txt
with open('data.txt', 'r') as file:
    accounts = file.readlines()

# Total akun
total_accounts = len(accounts)


# Proses setiap akun
for idx, account in enumerate(accounts):
    # Tampilkan informasi proses
    print(colored(f"Memproses akun {idx + 1} dari {total_accounts}", 'yellow'))
    
    # Ambil data Init-Data untuk akun ini
    account_data = account.strip()
    
    # Lakukan login
    login_data = login(account_data)
    
    if login_data:
        headers = {
            "Content-Type": "application/json",
            "Init-Data": account_data,
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
            "Cache-Control": "no-cache",
            "Content-Length": "2",
            "Origin": "https://tonclayton.fun",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://tonclayton.fun/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        username = login_data['user']['username']
        level = login_data['user']['level']
        tokens = login_data['user']['tokens']
        storage = login_data['user']['storage']
        can_claim = login_data['user']['can_claim']
        daily_attempts = login_data['user']['daily_attempts']
        start_time = login_data['user']['start_time']
        current_xp = login_data['user']['current_xp']
        
        # Ubah format waktu mulai
        start_time_formatted = format_time(start_time)
        
        # Tampilkan informasi akun dalam format rapi
        print(colored(f"Akun: {username}", 'yellow'))
        print(colored(f"Level: {level}", 'yellow'))
        print(colored(f"Tokens: {tokens}", 'yellow'))
        print(colored(f"Storage: {storage}", 'yellow'))
        print(colored(f"Can Claim: {can_claim}", 'yellow'))
        print(colored(f"Daily Attempts: {daily_attempts}", 'yellow'))
        print(colored(f"Start Time: {start_time_formatted}", 'yellow'))
        print(colored(f"Current XP: {current_xp}", 'yellow'))
        
        # Lakukan tugas farming jika bisa claim
        if can_claim:
            claim_farming(headers)
            start_farming(headers)  # Memulai farming setelah claim farming
        
        # Mulai permainan sesuai dengan daily_attempts
        for attempt in range(daily_attempts):
            print(colored(f"Memulai game ke-{attempt + 1}", 'yellow'))
            start_game(headers)
            
            # Simulasi permainan selama 1 menit tanpa pengulangan max_tile
            game_duration = timedelta(minutes=1)
            end_time = datetime.now() + game_duration
            max_tile = 8  # Mulai dengan 4
            used_tiles = set()
            
            while datetime.now() < end_time:
                if max_tile not in used_tiles:
                    save_tile(headers, max_tile)
                    used_tiles.add(max_tile)
                
                # Gandakan nilai maxTile
                max_tile *= 2
                
                # Batasi maxTile hingga 2048
                if max_tile > 2048:
                    max_tile = 8
            
            end_game(headers)  # Selesaikan game
        
        # Istirahat sejenak sebelum akun berikutnya
        time.sleep(5)
    else:
        print(colored("Login gagal, melewati akun ini.", 'red'))

# Setelah semua akun diproses, lakukan hitung mundur selama 6 jam
countdown_time = timedelta(hours=6)
end_time = datetime.now() + countdown_time


print(colored("Menunggu 6 jam sebelum reset:", 'yellow'))
while datetime.now() < end_time:
    time_diff = end_time - datetime.now()
    print(colored(f"Waktu reset dalam: {time_diff}", 'yellow'), end='\r')
    time.sleep(1)

print(colored("\nWaktu reset tercapai, memulai ulang...", 'green'))

# Restart kode setelah hitung mundur selesai
exec(open(__file__).read())
