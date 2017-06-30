import subprocess
from os import path,system
import random, string
from time import time

CHECKER = {
    'FLAG_PREFIX' : 'CTF',
    'FLAG_LENGTH' : 30
}
class Zond:
    def attack(spath, attack_type, team, service):
        """
        Primary function for Zond class. Open subprocess with formatted exploit-script and wait for it up to 6 secs.
        -----------
            INPUT:
                Script path - string
                Attack Type - string enum(ping, check, put, get)
                Team - object Team
                Service - object Service
                Flag - string

            OUTPUT:
                Return CODE - integer enum(101, 102, 103, 104, 110)
                Message - string
                Attack Type - string enum(ping, check, put, get)
                Team ID - integer
                Service ID - integer
                Flag - string
        ----------
        """
        ttime = str(time())
        flag = CHECKER['FLAG_PREFIX'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(CHECKER['FLAG_LENGTH'])) + '='

        command = "{} {} {} {}".format(
            path.join(spath, "exploits", service['name'].replace(" ", "_").lower(), "exploit"),
            attack_type,
            team['network'],
            flag
        )
        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate(timeout=6)
            # print(output)
            # print("{}:{} - {}".format(t, s, p.returncode))
            # print (output)
            return team['id'], service['id'], ttime, attack_type, p.returncode, output, flag
        except subprocess.TimeoutExpired as ex:
            return team['id'], service['id'], ttime, attack_type, 104, "Timed out", flag
        except Exception as ex:
            return team['id'], service['id'], ttime, attack_type, 110, "Internal error", flag


    def ping(hostname):
        try:
            response = os.system("ping -c 1 -W 2 " + hostname + " > /dev/null 2>&1") # -t 3 нужно ли?
            print(response)
            if response == 0:
                print("ok")
                return(101)
            print("Host unreachable")
            return(104)
        except:
            print("Host unreachable")
            return(104)
