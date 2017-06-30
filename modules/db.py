import postgresql
# import time
# import datetime
# ts = time.time()
# timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

class Database(object):
    # queries = {
    # 'getTeams': 'SELECT * FROM teams LIMIT 20',
    # 'getServices': 'SELECT * FROM services LIMIT 20',
    # }
    def __init__(self, connString):
        try:
            self.conn = postgresql.open(connString)
        except Exception as ex:
            print("Exception: {}".format(ex))

    def getTeams(self, limit=0):
        request = self.conn.prepare('SELECT * FROM teams LIMIT $1')
        return request(limit)
        # return 3
        # return self.conn.query(request)
    def getServices(self, limit=0):
        request = self.conn.prepare('SELECT * FROM services LIMIT $1')

        return request(limit)
        # return self.conn.query(request)
    def saveAttack(self, team, service, timestamp, atype=1, code=110, message='Internal error'):
        request = self.conn.prepare('INSERT INTO logs(team_id, service_id, type, code, message) VALUES($1, $2, $3, $4, $5)')
        return request(team, service, atype, code, message)
        # return self.conn.query(request)
    def close(self):
        self.conn.close()
