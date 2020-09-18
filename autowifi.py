import platform
import subprocess
import time
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

def ping_check(host):
  param = '-n' if platform.system().lower()=='windows' else '-c'
  command = ['ping', param, '1', host]
  return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()==0

def main():
  print(banner)
  # Check if user connect to wifi
  print("[!]Checking connection...")
  while not ping_check(URL):
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
        flg = True
        continue
      if flg:
        print("[!]You are connected")
        flg = False
      time.sleep(check_time)
    except KeyboardInterrupt:
      print("[!]Stop the script!")
      break
    except e:
      print(e)
      break
  input("Press anykey to continue...")

if __name__ == '__main__':
  main()
