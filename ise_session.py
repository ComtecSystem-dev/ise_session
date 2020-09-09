import requests

def request_action(url, id, pwd):
    print("\t Request URL : %s" % (url))
    session = requests.Session()
    session.auth = (id, pwd)
    response = session.delete(url, verify=False)
    print("\t %s " % response.text)

input_ip = input("IP : ")
input_id = input("ID : ")
input_pwd = input("PWD : ")

while(True):
    print("1. Delete Session - Session ID")
    print("2. Delete Session - MAC")
    print("9. Delete Session - All")
    print("0. EXIT(0)")
    select_input = input("SELECT => ")
    if select_input == "0":
        break
    elif select_input == "1":
        input_val = input("Session ID => ")
        url = "https://%s/admin/API/mnt/Session/Delete/SessionID/%s" % (input_ip, input_val)
        request_action(url, input_id, input_pwd)
    elif select_input == "2":
        input_val = input("MAC => ")
        url = "https://%s/admin/API/mnt/Session/Delete/MACAddress/%s" % (input_ip, input_val)
        request_action(url, input_id, input_pwd)
    elif select_input == "9":
        input_val = ''
        url = "https://%s/admin/API/mnt/Session/Delete/All" % (input_ip)
        request_action(url, input_id, input_pwd)
    else:
        print("input error!!!")
        continue
    