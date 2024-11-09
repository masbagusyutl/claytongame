import requests
import time
import random
from colorama import Fore, Style, init

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
        self.base_url = "https://tonclayton.fun/api/cc82f330-6a6d-4deb-a15b-6a332a67ffa7"
        self.retries = 5

    def make_request(self, endpoint, method='post', data=None, init_data=""):
        url = f"{self.base_url}{endpoint}"
        headers = {**self.headers, "Init-Data": init_data}

        for attempt in range(self.retries):
            try:
                response = requests.request(method, url, json=data, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
            except requests.RequestException as e:
                if attempt < self.retries - 1:
                    print(Fore.RED + f"Kesalahan API, mencoba ulang ({attempt + 1}): {str(e)}")
                    time.sleep(5)
                else:
                    return {"success": False, "error": str(e)}

    def login(self, init_data):
        response = self.make_request("/user/authorization", "post", {}, init_data)
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
        response = self.make_request("/user/daily-claim", "post", {}, init_data)
        if response['success']:
            if response['data'].get("message") == "daily reward claimed successfully":
                print(Fore.GREEN + "Berhasil klaim hadiah harian.")
            else:
                print(Fore.RED + f"Gagal klaim hadiah harian: {response['error']}")
        else:
            print(Fore.RED + f"Gagal klaim hadiah harian: {response['error']}")
            if "details" in response:
                print(Fore.RED + f"Detail kesalahan: {response['details']}")

    def get_partner_tasks(self, init_data):
        response = self.make_request("/tasks/partner-tasks", "get", {}, init_data)
        if response['success']:
            self.process_tasks(response['data'], "partner", init_data)
        else:
            print(Fore.RED + f"Gagal memuat tugas partner: {response['error']}")

    def get_daily_tasks(self, init_data):
        response = self.make_request("/tasks/daily-tasks", "get", {}, init_data)
        if response['success']:
            self.process_tasks(response['data'], "daily", init_data)
        else:
            print(Fore.RED + f"Gagal memuat tugas harian: {response['error']}")


    def get_other_tasks(self, init_data):
        response = self.make_request("/tasks/default-tasks", "get", {}, init_data)
        if response['success']:
            self.process_tasks(response['data'], "other", init_data)
        else:
            print(Fore.RED + f"Gagal memuat tugas lainnya: {response['error']}")


    def process_tasks(self, tasks, task_type, init_data):
        for task in tasks:
            if not task.get("is_completed") and not task.get("is_claimed"):
                task_id = task.get("task_id")
                print(Fore.YELLOW + f"Mengerjakan tugas {task_type}: {task['task']['title']}")
                if self.complete_task(task_id, init_data):
                    self.claim_task_reward(task_id, init_data)
            else:
                print(Fore.YELLOW + f"Tugas {task_type} {task['task']['title']} sudah selesai atau sudah diklaim.")

    def complete_task(self, task_id, init_data):
        response = self.make_request("/tasks/complete", "post", {"task_id": task_id}, init_data)
        if response['success']:
            print(Fore.GREEN + f"Tugas {task_id} selesai.")
            return True
        else:
            print(Fore.RED + f"Gagal menyelesaikan tugas {task_id}: {response['error']}")
            return False

    def claim_task_reward(self, task_id, init_data):
        response = self.make_request("/tasks/claim", "post", {"task_id": task_id}, init_data)
        if response['success']:
            reward = response['data'].get("reward_tokens", 0)
            print(Fore.GREEN + f"Klaim hadiah tugas {task_id}: Mendapat {reward} CL")
        else:
            print(Fore.RED + f"Gagal klaim hadiah tugas {task_id}: {response['error']}")

    def play_2048(self, init_data):
        print(Fore.YELLOW + "Memulai permainan 2048")
        start_game_result = self.make_request("/game/start", "post", {}, init_data)
        
        if start_game_result["success"] and "session_id" in start_game_result["data"]:
            session_id = start_game_result["data"]["session_id"]
            print(Fore.GREEN + f"Permainan 2048 dimulai")
            milestones = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
            
            for milestone in milestones:
                time.sleep(5)
                save_game_result = self.make_request(
                    "/game/save-tile", 
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
                "/game/over", 
                "post", 
                {"session_id": session_id, "multiplier": 1, "maxTile": milestones[-1]}, 
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
        start_game_result = self.make_request("/stack/st-game", "post", {}, init_data)
        
        if start_game_result["success"] and "session_id" in start_game_result["data"]:
            session_id = start_game_result["data"]["session_id"]
            print(Fore.GREEN + f"Permainan Stack dimulai")
            scores = [10, 20, 30, 40, 50, 60, 70, 80, 90]
            
            for score in scores:
                time.sleep(random.uniform(5, 10))
                update_result = self.make_request(
                    "/stack/update-game", 
                    "post", 
                    {"session_id": session_id, "score": score}, 
                    init_data
                )
                if update_result["success"]:
                    print(Fore.GREEN + f"Stack berhasil diperbarui dengan Skor : {score}")
                else:
                    print(Fore.RED + f"Gagal memperbarui skor {score}: {update_result['error']}")
                    break
            
            end_game_result = self.make_request(
                "/stack/en-game", 
                "post", 
                {"session_id": session_id, "score": scores[-1], "multiplier": 1}, 
                init_data
            )
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

            # Perbarui game terakhir dengan pilihan baru
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
