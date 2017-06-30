
import os

# Load exploits to files from DataBase
def loadExpolits(exploits):
    # print(exploits)
    exploits_dir = 'exploits'
    if not os.path.exists(exploits_dir):
        os.makedirs(exploits_dir)
    for e in exploits:
        exploit_dir = os.path.join(exploits_dir, strFmt(e['name']))
        if not os.path.exists(exploit_dir):
            os.makedirs(exploit_dir)
        with open(os.path.join(exploit_dir, "exploit"), "w+") as fh:
            fh.write(e['exploit'])
        os.chmod(os.path.join(exploit_dir, "exploit"), 0o777)

# Save exploit files to Databases
# def saveExpolits(exploits):

# # Listener for success attack
# def success_attack(event):
#     global DB
#     # print(event.retval)
#     if len(event.retval) == 5:
#         DB.saveAttack(1, 2, str(time.time()), 1, event.retval[0], event.retval[1].decode("utf-8"))
    # print(event.retval)
def attackType(attack_type):
    return ['ping', 'check', 'put', 'get'].index(attack_type)
    # if(attack_type is 'check'):
    #     return 1
    # elif(attack_type is 'put'):
    #     return 2
    # elif(attack_type is 'get'):
    #     return 3
    # elif(attack_type is 'ping'):
    #     return 0
def strFmt(st):
    return st.replace(" ", "_").lower()
    
def testExploit(e):
    exploits_dir = 'exploits'
    if not os.path.exists(exploits_dir):
        os.makedirs(exploits_dir)
    exploit_dir = os.path.join(exploits_dir, 'test')
    if not os.path.exists(exploit_dir):
        os.makedirs(exploit_dir)
    with open(os.path.join(exploit_dir, e['name']), "w+") as fh:
        fh.write(e['exploit'])
        os.chmod(os.path.join(exploit_dir, e['name']), 0o777)
