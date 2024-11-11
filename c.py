import requests
import time
from colorama import Fore, Style, init
from datetime import datetime, timedelta
import re
import random

# Initialize Colorama
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
    API_ENDPOINTS = {
        "LOGIN": "user/authorization",
        "DAILY_CLAIM": "user/daily-claim",
        "PARTNER_TASKS": "tasks/partner-tasks",
        "DAILY_TASKS": "tasks/daily-tasks",
        "DEFAULT_TASKS": "tasks/default-tasks",
        "TASK_COMPLETE": "tasks/complete",
        "TASK_CLAIM": "tasks/claim",
        "GAME_START": "game/start",
        "GAME_SAVE_TILE": "game/save-tile",
        "GAME_OVER": "game/over",
        "STACK_START": "stack/st-game",
        "STACK_UPDATE": "stack/update-game",
        "STACK_END": "stack/en-game",
    }

    GAME_CONFIG = {
        "TILE_SEQUENCE": [4, 8, 16, 32, 64, 128, 256, 512, 1024],
        "RETRY_ATTEMPTS": 5,
        "RETRY_DELAY": 5,
    }

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        self.base_url = "https://tonclayton.fun"
        self.api_base_id = None

    def fetch_api_base_id(self):
        try:
            print(Fore.CYAN + "Mengambil API Base ID dari halaman utama...")
            response = requests.get(self.base_url)
            response.raise_for_status()

            match = re.search(r'/assets/index-([^"]+)\.js', response.text)
            if match:
                js_file = match.group(0).split('/')[-1]
                js_response = requests.get(f"{self.base_url}/assets/{js_file}")
                js_response.raise_for_status()

                id_match = re.search(r'_ge="([^"]+)"', js_response.text)
                if id_match:
                    self.api_base_id = id_match.group(1)
                    print(Fore.GREEN + f"API Base ID berhasil diambil")
                else:
                    raise ValueError("Pola API Base ID tidak ditemukan.")
            else:
                raise ValueError("Tidak dapat menemukan file JavaScript utama.")
        except requests.RequestException as e:
            print(Fore.RED + f"Gagal mengambil API Base ID: {str(e)}")

    def make_request(self, endpoint_key, method='post', data=None, init_data=""):
        if not self.api_base_id:
            self.fetch_api_base_id()
            if not self.api_base_id:
                print(Fore.RED + "API Base ID belum diinisialisasi. Tidak dapat membuat permintaan.")
                return {"success": False, "error": "API Base ID tidak diinisialisasi."}

        url = f"{self.base_url}/api/{self.api_base_id}/{self.API_ENDPOINTS[endpoint_key]}"
        headers = {**self.headers, "Init-Data": init_data}

        for attempt in range(self.GAME_CONFIG["RETRY_ATTEMPTS"]):
            try:
                response = requests.request(method, url, json=data, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
            except requests.RequestException as e:
                if attempt < self.GAME_CONFIG["RETRY_ATTEMPTS"] - 1:
                    print(Fore.RED + f"Kesalahan API, mencoba ulang ({attempt + 1}): {str(e)}")
                    time.sleep(self.GAME_CONFIG["RETRY_DELAY"])
                else:
                    return {"success": False, "error": str(e)}

    def login(self, init_data):
        response = self.make_request("LOGIN", "post", {}, init_data)
        if response['success']:
            user_data = response['data']['user']
            print(Fore.YELLOW + f"Akun: {user_data['username']}")
            print(Fore.YELLOW + f"Level: {user_data['level']}")
            print(Fore.YELLOW + f"Token: {user_data['tokens']}")
            print(Fore.YELLOW + f"Kesempatan Harian: {user_data['daily_attempts']}")
            return response
        else:
            print(Fore.RED + f"Gagal login: {response['error']}")
            return None

    def claim_daily_reward(self, init_data):
        response = self.make_request("DAILY_CLAIM", "post", {}, init_data)
        if response['success']:
            print(Fore.GREEN + "Berhasil klaim hadiah harian.")
        else:
            print(Fore.RED + f"Gagal klaim hadiah harian: {response['error']}")

    def get_partner_tasks(self, init_data):
        print(Fore.CYAN + "Mengambil tugas mitra...")
        return self.make_request("PARTNER_TASKS", "get", {}, init_data)

    def get_daily_tasks(self, init_data):
        print(Fore.CYAN + "Mengambil tugas harian...")
        return self.make_request("DAILY_TASKS", "get", {}, init_data)

    def get_other_tasks(self, init_data):
        print(Fore.CYAN + "Mengambil tugas lainnya...")
        return self.make_request("DEFAULT_TASKS", "get", {}, init_data)

    def process_tasks(self, task_getter, task_type, init_data):
        print(Fore.CYAN + f"Mengolah tugas {task_type}...")
        response = task_getter(init_data)
        if not response["success"]:
            print(Fore.RED + f"Gagal mengambil tugas {task_type}: {response['error']}")
            return

        tasks = response["data"]
        if not isinstance(tasks, list) or not tasks:
            print(Fore.YELLOW + f"Tidak ada tugas {task_type} yang tersedia.")
            return

        for task in tasks:
            if not task.get("is_completed") and not task.get("is_claimed"):
                task_id = task["task_id"]
                print(Fore.YELLOW + f"Mengerjakan tugas {task_type}: {task['task']['title']}")
                if self.complete_task(task_id, init_data):
                    self.claim_task_reward(task_id, init_data)
            else:
                print(Fore.YELLOW + f"Tugas {task_type} {task['task']['title']} sudah selesai atau sudah diklaim.")

    def complete_task(self, task_id, init_data):
        response = self.make_request("TASK_COMPLETE", "post", {"task_id": task_id}, init_data)
        if response["success"]:
            print(Fore.GREEN + f"Tugas {task_id} selesai.")
            return True
        else:
            print(Fore.RED + f"Gagal menyelesaikan tugas {task_id}: {response['error']}")
            return False

    def claim_task_reward(self, task_id, init_data):
        response = self.make_request("TASK_CLAIM", "post", {"task_id": task_id}, init_data)
        if response["success"]:
            reward = response["data"].get("reward_tokens", 0)
            print(Fore.GREEN + f"Klaim hadiah tugas {task_id}: Mendapat {reward} CL")
        else:
            print(Fore.RED + f"Gagal klaim hadiah tugas {task_id}: {response['error']}")

    def play_2048(self, init_data):
        print(Fore.YELLOW + "Memulai permainan 2048")
        start_game_result = self.make_request("GAME_START", "post", {}, init_data)
        
        if start_game_result["success"] and "session_id" in start_game_result["data"]:
            session_id = start_game_result["data"]["session_id"]
            print(Fore.GREEN + f"Permainan 2048 dimulai")
            for milestone in self.GAME_CONFIG["TILE_SEQUENCE"]:
                time.sleep(5)
                save_game_result = self.make_request(
                    "GAME_SAVE_TILE", 
                    "post", 
                    {"session_id": session_id, "maxTile": milestone}, 
                    init_data
                )
                if save_game_result["success"]:
                    print(Fore.GREEN + f"Berhasil mencapai tile {milestone}")
                else:
                    print(Fore.RED + f"Gagal simpan tile {milestone}: {save_game_result['error']}")
                    break
            
            end_game_result = self.make_request(
                "GAME_OVER", 
                "post", 
                {"session_id": session_id, "multiplier": 1, "maxTile": self.GAME_CONFIG["TILE_SEQUENCE"][-1]}, 
                init_data
            )
            if end_game_result["success"]:
                reward = end_game_result["data"]
                print(Fore.GREEN + f"Permainan 2048 selesai | Mendapatkan {reward['earn']} CL | {reward['xp_earned']} XP")
            else:
                print(Fore.RED + f"Kesalahan saat mengakhiri permainan 2048 | {end_game_result['error']}")
        else:
            print(Fore.RED + "Gagal memulai permainan 2048")

    def play_stack(self, init_data):
        print(Fore.YELLOW + "Memulai permainan Stack")
        start_game_result = self.make_request("STACK_START", "post", {}, init_data)
        
        if start_game_result["success"] and "session_id" in start_game_result["data"]:
            session_id = start_game_result["data"]["session_id"]
            print(Fore.GREEN + f"Permainan Stack dimulai")
            scores = [10, 20, 30, 40, 50, 60, 70, 80, 90]
            
            for score in scores:
                time.sleep(random.uniform(5, 10))
                update_result = self.make_request("STACK_UPDATE", "post", {"session_id": session_id, "score": score}, init_data)
                if update_result["success"]:
                    print(Fore.GREEN + f"Stack berhasil diperbarui dengan Skor : {score}")
                else:
                    print(Fore.RED + f"Gagal memperbarui skor {score}: {update_result['error']}")
                    break
            
            end_game_result = self.make_request("STACK_END", "post", {"session_id": session_id, "score": scores[-1], "multiplier": 1}, init_data)
            if end_game_result["success"]:
                reward = end_game_result["data"]
                print(Fore.GREEN + f"Permainan Stack selesai | Mendapatkan {reward['earn']} CL | {reward['xp_earned']} XP")
            else:
                print(Fore.RED + f"Kesalahan saat mengakhiri permainan Stack: {end_game_result['error']}")
        else:
            print(Fore.RED + "Gagal memulai permainan Stack")

    def play_random_game(self, init_data, daily_attempts):
        game_attempts = 0
        last_game = None

        while game_attempts < daily_attempts:
            # Select random game type
            game_choice = random.choice(['2048', 'stack'])
            while game_choice == last_game and daily_attempts > 1:
                game_choice = random.choice(['2048', 'stack'])

            # Update last game with new choice
            last_game = game_choice
            
            # Increment attempt count
            game_attempts += 1
            print(Fore.CYAN + f"Memulai game ke-{game_attempts} dari {daily_attempts} | Game: {game_choice.capitalize()}")
            
            # Play selected game
            if game_choice == '2048':
                self.play_2048(init_data)
            else:
                self.play_stack(init_data)
                
            time.sleep(5)  # Delay between games to mimic real user interaction

    def main(self):
        print_welcome_message()
        try:
            with open("data.txt", "r") as file:
                data = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "File 'data.txt' tidak ditemukan.")
            return

        print(Fore.CYAN + f"Total akun yang diproses: {len(data)}")
        for i, init_data in enumerate(data):
            print(Fore.YELLOW + f"Memproses akun ke-{i + 1} dari {len(data)}...")
            
            # Login and fetch daily attempts
            user_data = self.login(init_data)
            if user_data:
                daily_attempts = user_data['data']['user']['daily_attempts']
                print(Fore.YELLOW + f"Kesempatan Harian Tersisa: {daily_attempts}")
                self.claim_daily_reward(init_data)
                self.get_partner_tasks(init_data)
                self.get_daily_tasks(init_data)
                self.get_other_tasks(init_data)
                
                # Start games until daily attempts are exhausted
                self.play_random_game(init_data, daily_attempts)
            time.sleep(5)  # Delay between processing accounts

        self.start_countdown()

    def start_countdown(self):
        end_time = datetime.now() + timedelta(days=1)
        while datetime.now() < end_time:
            remaining = end_time - datetime.now()
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"\rWaktu tersisa hingga restart: {hours:02}:{minutes:02}:{seconds:02}", end="")
            time.sleep(1)
        
        print("\nMemulai ulang proses setelah 1 hari.")
        self.main()

if __name__ == "__main__":
    client = Clayton()
    client.main()
