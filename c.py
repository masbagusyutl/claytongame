import requests
import time
import random
from colorama import Fore, Style, init
from datetime import datetime

# Inisialisasi Colorama
init(autoreset=True)

def print_welcome_message():
    print(Fore.WHITE + r"""
_  _ _   _ ____ ____ _    ____ _ ____ ___  ____ ____ ___ 
|\ |  \_/  |__| |__/ |    |__| | |__/ |  \ |__/ |  | |__]
| \|   |   |  | |  \ |    |  | | |  \ |__/ |  \ |__| |         
          """)
    print(Fore.GREEN + Style.BRIGHT + "Nyari Airdrop Clayton Game")
    print(Fore.YELLOW + Style.BRIGHT + "Telegram: https://t.me/nyariairdrop")


class Clayton:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://tonclayton.fun",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        self.base_url = "https://tonclayton.fun/api"

    def login(self, init_data):
        response = self.make_request("/user/authorization", "post", {}, init_data)
        
        if response['success']:
            user_data = response['data']['user']
            
            print(Fore.YELLOW + f"Akun: {user_data['username']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Level: {user_data['level']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Token: {user_data['tokens']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Penyimpanan: {user_data['storage']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Bisa Klaim: {user_data['can_claim']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Kesempatan Harian: {user_data['daily_attempts']}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"XP Saat Ini: {user_data['current_xp']}" + Style.RESET_ALL)
            
            return response
        else:
            print(Fore.RED + f"Gagal dapat info akun: {response['error']}")
            return None

    def make_request(self, endpoint, method='post', data=None, init_data=""):
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        headers = {**self.headers, "Init-Data": init_data}

        try:
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def countdown(self, seconds):
        for i in range(seconds, -1, -1):
            hours, rem = divmod(i, 3600)
            minutes, secs = divmod(rem, 60)
            print(f"Menunggu {hours:02}:{minutes:02}:{secs:02} untuk memulai kembali.", end='\r')
            time.sleep(1)
        print("")


    def handle_all_tasks(self, init_data):
        task_types = ["default", "partner", "daily", "super"]
        for task_type in task_types:
            self.handle_tasks(task_type, init_data)
    
    def handle_tasks(self, task_type, init_data):
        print(Fore.YELLOW + f"Mengecek tugas {task_type}")
        tasks_result = self.get_task_list(task_type, init_data)
        
        if tasks_result["success"]:
            uncompleted_tasks = [task for task in tasks_result["data"] if not task['is_completed'] and not task['is_claimed']]
            for task in uncompleted_tasks:
                print(Fore.GREEN + f"Mengerjakan tugas {task_type} | {task['task']['title']}")
                complete_result = self.complete_task(init_data, task['task_id'])
                
                if complete_result["success"]:
                    reward_result = self.claim_task_reward(init_data, task['task_id'])
                    if reward_result["success"]:
                        print(Fore.GREEN + f"Berhasil menyelesaikan tugas {task_type} | {task['task']['title']} | Mendapatkan {reward_result['data']['reward_tokens']} CL")
                    else:
                        print(Fore.RED + f"Gagal klaim hadiah untuk tugas {task_type} | {task['task']['title']} | {reward_result['error']}")
                else:
                    print(Fore.RED + f"Gagal menyelesaikan tugas {task_type} | {task['task']['title']} | {complete_result['error']}")
        else:
            print(Fore.RED + f"Tidak dapat mendapatkan daftar tugas {task_type} | {tasks_result['error']}")

    def get_task_list(self, task_type, init_data):
        return self.make_request(f"/tasks/{task_type}-tasks", "get", {}, init_data)

    def complete_task(self, init_data, task_id):
        return self.make_request("/tasks/complete", "post", {"task_id": task_id}, init_data)

    def claim_task_reward(self, init_data, task_id):
        return self.make_request("/tasks/claim", "post", {"task_id": task_id}, init_data)

    def play_2048(self, init_data):
        print(Fore.YELLOW + "Memulai permainan 2048")
        start_game_result = self.make_request("/game/start", "post", {}, init_data)
        
        if start_game_result["success"] and start_game_result["data"]["message"] == "Game started successfully":
            print(Fore.GREEN + "Permainan 2048 dimulai dengan sukses")
            milestones = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
            end_time = time.time() + 150  # durasi 150 detik
            
            for milestone in milestones:
                if time.time() >= end_time:
                    break
                time.sleep(5)  # Jeda 5 detik untuk simulasi
                save_game_result = self.make_request("/game/save-tile", "post", {"maxTile": milestone}, init_data)
                if save_game_result["success"]:
                    print(Fore.GREEN + f"Berhasil mencapai tile {milestone}")
                    
            end_game_result = self.make_request("/game/over", "post", {"multiplier": 1}, init_data)
            if end_game_result["success"]:
                reward = end_game_result["data"]
                print(Fore.GREEN + f"Permainan 2048 selesai | Mendapatkan {reward['earn']} CL | {reward['xp_earned']} XP")
            else:
                print(Fore.RED + f"Kesalahan saat mengakhiri permainan 2048 | {end_game_result['error']}")
        else:
            print(Fore.RED + "Gagal memulai permainan 2048")


    def play_stack(self, init_data):
        print(Fore.YELLOW + "Memulai permainan Stack")
        start_game_result = self.make_request("/stack/st-game", "post", {}, init_data)
        
        if start_game_result["success"]:
            print(Fore.GREEN + "Permainan Stack dimulai dengan sukses")
            end_time = time.time() + 120  # durasi 120 detik
            scores = [10, 20, 30, 40, 50, 60, 70, 80, 90]
            current_score_index = 0
            
            while time.time() < end_time and current_score_index < len(scores):
                score = scores[current_score_index]
                update_result = self.make_request("/stack/update-game", "post", {"score": score}, init_data)
                if update_result["success"]:
                    print(Fore.GREEN + f"Update skor Stack: {score}")
                    current_score_index += 1
                else:
                    print(Fore.RED + f"Gagal update skor Stack: {update_result['error']}")
                time.sleep(random.uniform(5, 15))
            
            final_score = scores[current_score_index - 1] if current_score_index > 0 else 90
            end_game_result = self.make_request("/stack/en-game", "post", {"score": final_score, "multiplier": 1}, init_data)
            if end_game_result["success"]:
                reward = end_game_result["data"]
                print(Fore.GREEN + f"Permainan Stack selesai | Mendapatkan {reward['earn']} CL | {reward['xp_earned']} XP")
            else:
                print(Fore.RED + f"Kesalahan saat mengakhiri permainan Stack: {end_game_result['error']}")
        else:
            print(Fore.RED + "Gagal memulai permainan Stack")

    def play_random_game(self, init_data):
        games = [self.play_2048, self.play_stack]
        chosen_game = random.choice(games)
        chosen_game(init_data)

    def get_daily_attempts(self, init_data):
        login_result = self.login(init_data)
        if login_result and login_result['success']:
            return login_result['data']['user']['daily_attempts']
        return 0

    def main(self):
        print_welcome_message()  # Call the welcome message at the start
        print(Fore.CYAN + "Memulai proses utama...")
        
        try:
            with open("data.txt", "r") as file:
                data = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "File 'data.txt' tidak ditemukan.")
            return

        total_accounts = len(data)
        print(Fore.CYAN + f"Total akun yang ditemukan: {total_accounts}")

        for i, init_data in enumerate(data):
            print(Fore.YELLOW + f"Memproses akun ke-{i + 1} dari {total_accounts}...")
            
            self.login(init_data)
            self.handle_all_tasks(init_data)
            
            daily_attempts = self.get_daily_attempts(init_data)
            print(Fore.CYAN + f"Kesempatan bermain game awal: {daily_attempts}")
            
            while daily_attempts > 0:
                print(Fore.CYAN + f"Kesempatan bermain game tersisa: {daily_attempts}")
                self.play_random_game(init_data)
                daily_attempts = self.get_daily_attempts(init_data)
                time.sleep(5)  # Jeda 5 detik antara permainan
            
            print(Fore.CYAN + "Semua kesempatan bermain game telah digunakan.")
            print(Fore.CYAN + f"Menunggu 5 detik sebelum melanjutkan ke akun berikutnya...")
            time.sleep(5)

        print(Fore.CYAN + "Semua akun telah diproses. Menunggu 24 jam sebelum memulai ulang.")
        self.countdown(24 * 60 * 60)  # 24 jam = 24 * 60 * 60 detik

        # Setelah hitung mundur selesai, mulai ulang dari awal
        self.main()

# Jalankan kode utama
if __name__ == "__main__":
    client = Clayton()
    client.main()
