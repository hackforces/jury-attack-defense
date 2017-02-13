import subprocess
import schedule
import time
import MySQLdb

STATUS_CODE = {
    'SUCCESS': 101,
    'CORRUPT': 102,
    'MUMBLE':  103,
    'DOWN':    104,
    'UNKNOWN': 110
}

BASE_PATH = "./checker"
HOSTNAME = "127.0.0.1"
#flag = "kek"
#CHECK_TIME = 10
#PUT_TIME = 120
#code = 110
#outs = "Internal error"

#start = time.time()

conn = MySQLdb.connect(user="root", password="keklol", host="localhost", db="ctf")

def check(hostname):
    code = 110
    #print("CHECK: {}".format(time.time() - start))
    outs = "Internal error"
    args = (BASE_PATH, "check", hostname)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    try:
        outs, errs = popen.communicate(timeout=2)
        code = popen.returncode
    except subprocess.TimeoutExpired as e:
        #print(e)
        code = 104
        outs = "Host unreachable"
        popen.kill()
    return outs, code

def put(hostname, flag):
    #print("PUT: {}".format(time.time() - start))
    code = 110
    outs = "Internal error"
    args = (BASE_PATH, "put", hostname, flag)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    try:
        outs, errs = popen.communicate(timeout=2)
        code = popen.returncode
    except subprocess.TimeoutExpired as e:
        #print(e)
        code = 104
        outs = "Host unreachable"
        popen.kill()
    return outs, code

def get(hostname, flag):
    code = 110
    outs = "Internal error"
    args = (BASE_PATH, "get", host, flag)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    try:
        outs, errs = popen.communicate(timeout=2)
        code = popen.returncode
    except subprocess.TimeoutExpired as e:
        #print(e)
        code = 104
        outs = "Host unreachable"
        popen.kill()
    return outs, code

schedule.every(0.133).minutes.do(check, HOSTNAME)
schedule.every(2).minutes.do(put, HOSTNAME, "KEK")

if __name__ == '__main__':
    while 1:
        schedule.run_pending()
        time.sleep(0.1)
