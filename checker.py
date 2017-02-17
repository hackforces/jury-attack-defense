import subprocess
import threading
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

conn = MySQLdb.connect(user="root", password="keklol1488", host="localhost", db="ctf")

def mysql_query(self, query, args=(), one=True, is_destructive=False):
    assert(isinstance(query, str))
    assert(isinstance(args, tuple))
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        if is_destructive:
            db.commit()
        if one:
            return cursor.fetchone()
        else:
            return cursor.fetchall()
    finally:
        cursor.close()

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
    exit(0)
    print("{}: {}".format(hostname, code))
    #return outs, code

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


def putall():
    hosts = []
    for i in range(2, 254):
        t = threading.Thread(target=put, args=["192.168.100." + str(i), "KEK"])
        t.start()
        hosts.append(t)
    for i in hosts:
        i.join()
    return 0

def checkall():
    hosts = []
    for i in range(2, 254):
        t = threading.Thread(target=put, args=["192.168.100." + str(i), "KEK"])
        t.start()
        hosts.append(t)
    for i in hosts:
        i.join()
    return 0

# def getall():
#     hosts=""
#     print("KEK")
#     return 0
#
# schedule.every(0.133).minutes.do(check, HOSTNAME)
# schedule.every(3).minutes.do(put, HOSTNAME, "KEK")

#schedule.every(0.133).minutes.do(check, HOSTNAME)
schedule.every(0.1).minutes.do(putall)

if __name__ == '__main__':
    while 1:
        schedule.run_pending()
        time.sleep(0.01)
