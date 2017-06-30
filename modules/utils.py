
import os

def saveExpolits(exploits):
    # print(exploits)
    exploits_dir = 'exploits'
    if not os.path.exists(exploits_dir):
        os.makedirs(exploits_dir)
    for e in exploits:
        exploit_dir = os.path.join(exploits_dir, e['name'].replace(" ", "_").lower())
        if not os.path.exists(exploit_dir):
            os.makedirs(exploit_dir)
        with open(os.path.join(exploit_dir, "exploit"), "w+") as fh:
            fh.write(e['exploit'])
        os.chmod(os.path.join(exploit_dir, "exploit"), 0o777)
