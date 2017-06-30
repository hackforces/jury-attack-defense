import subprocess
from os import path

class Zond:
    STATUS_CODE = {
        'SUCCESS':  101,
        'CORRUPT':  102,
        'MUMBLE':   103,
        'DOWN':     104,
        'INTERNAL': 110
    }

    def attack(spath, atype, hostname, service_name, flag):
        command = "{} {} {} {}".format(path.join(spath, "exploits", service_name.replace(" ", "_").lower(), "exploit"), atype, hostname, flag)
        try:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate(timeout=3)
            # print(output)
            # print("{}:{} - {}".format(t, s, p.returncode))
            # print (output)
            return p.returncode, output
        except subprocess.TimeoutExpired as ex:
            return 104, "Timed out"
        except Exception as ex:
            return 110, "Internal error"
