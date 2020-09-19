import platform
import time
import socket
from requests import Session
from bs4 import BeautifulSoup as bs

URL = "http://172.16.0.1:8002/index.php?zone=iuh"
form = {
  "auth_user": "dhcn",  #default
  "auth_pass": "dhcn",  #default
  "auth_voucher": "",   #admin disable
  "redirurl": "",
  "accept": "Đăng nhập"
}
check_time = 3          #seconds
banner = """\
#############################################
#             AUTOWIFI BY FOX               #
#############################################
"""

def check_host(host, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(5)
  try:
    s.connect((host, port))
    return True
  except (socket.timeout, OSError):
    return False
  except Exception as e:
    print("check_host error:", str(e))
    input()
    return False

def main():
  print(banner)
  # Check if user connect to wifi
  print("[!]Checking connection...")
  while not check_host("172.16.0.1", 8002):
    print("[!]Please connect to wifi DHCN!")
    input("Press any key to continue...\n")

  flg = True
  t = Session()

  # Verify loop
  while True:
    try:
      r = t.post(URL, data=form)
      soup = bs(r.content, 'lxml')
      r = soup.find("div", {"id": "error-message"})
      if r:
        print("[?]You has disconnected, reason:", r)
        flg = False
        continue
      if flg:
        print("[!]You are connected")
        flg = False
      time.sleep(check_time)
    except KeyboardInterrupt:
      print("[!]Stop the script!")
      break
    except Exception as e:
      flg = True
      print("main_loop error:", e)
      input("Press anykey to continue...")
  input("Press anykey to continue...")

if __name__ == '__main__':
  main()
