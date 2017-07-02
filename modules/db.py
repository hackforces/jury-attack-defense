# import postgresql
# import psycopg2
# import time
# http://docs.sqlalchemy.org/en/latest/core/connections.html Fetch types
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
# import datetime
# ts = time.time()
# timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def attackType(attack_type):
    return ['ping', 'check', 'put', 'get'].index(attack_type)

class Database(object):
    # queries = {
    # 'getTeams': 'SELECT * FROM teams LIMIT 20',
    # 'getServices': 'SELECT * FROM services LIMIT 20',
    # }
    def __init__(self, connString):
        try:
            self.conn = create_engine(connString, poolclass=QueuePool, pool_size=20)
        except Exception as ex:
            print("Exception: {}".format(ex))

    def getTeams(self, limit=0):
        request = "SELECT * FROM teams LIMIT {}".format(limit)
        result = self.conn.execute(request).fetchall()
        return result
        # request = self.conn.prepare('SELECT * FROM teams LIMIT $1')
        # return self.conn.query(request)
    def getServices(self, limit=0):
        request = "SELECT * FROM services LIMIT {}".format(limit)
        result = self.conn.execute(request).fetchall()
        # cursor.close()
        return result
        # request = self.conn.prepare('SELECT * FROM services LIMIT $1')
        # return request(limit)
        # return self.conn.query(request)
    def saveAttack(self, info):
        request = "INSERT INTO logs(team_id, service_id, timestamp, type, code, message, flag) VALUES ({}, {}, '{}', {}, {}, '{}', '{}')".format(
            info[0], info[1], info[2], attackType(info[3]), info[4], info[5].decode("utf-8"), info[6]
        )
        result = self.conn.execute(request)
        return result
    def getTeamByIP(self, network):
        request = "SELECT id, name FROM teams WHERE network = '{}'".format(network)
        result = self.conn.execute(request).fetchone()
        # cursor.close()
        return result
    def findFlag(self, flag):
        request = "SELECT id, team_id, service_id, timestamp FROM logs WHERE flag = '{}'".format(flag)
        result = self.conn.execute(request).fetchone()
        return result

    def saveFlag(self, flag_id, team_id):
        request = "SELECT COUNT(flag_id) FROM flags_stolen WHERE flag_id = {}".format(flag_id)
        if self.conn.execute(request).scalar():
            return False

        request = "INSERT INTO flags_stolen (flag_id, team_id) VALUES ({}, {})".format(flag_id, team_id)
        result = self.conn.execute(request)
        return True

        # request = self.conn.prepare('INSERT INTO logs(team_id, service_id, timestamp, type, code, message) VALUES($1, $2, $3, $4, $5, $6)')
        # return request(team, service, timestamp, atype, code, message)
        # return self.conn.query(request)
    # def update(self):
    #     while len(q) > 0:
    #         request = self.conn.prepare('INSERT INTO logs(team_id, service_id, type, code, message) VALUES($1, $2, $3, $4, $5)')
    #         request(1, 2, 3, 4, 5)
    #         q.pop()

    def close(self):
        self.conn.close()
