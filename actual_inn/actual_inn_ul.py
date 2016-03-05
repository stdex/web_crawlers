import pymysql.cursors

class Database:

    host = 'localhost'
    #port = 3306
    user = 'root'
    password = ''
    db = 'inn_ul'
    cursorclass = pymysql.cursors.DictCursor
    charset = 'utf8mb4'

    def __init__(self):
        self.connection = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.db,
            cursorclass = self.cursorclass,
            charset = self.charset
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except pymysql.InternalError as e:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

def cl_inn(sInn):
    nA11 = 0
    nA12 = 0
    aW =[None] * 10
    sCtrlNum = ""
    aW[0] = 31
    aW[1] = 29
    aW[2] = 23
    aW[3] = 19
    aW[4] = 17
    aW[5] = 13
    aW[6] = 7
    aW[7] = 5
    aW[8] = 3
    for i in range(0,9):
        nA11 += int(sInn[i:i+1]) * aW[i]
    nA11 = 11 - nA11 % 11
    nA11 = 0 if nA11 > 9 else nA11
    nA11 = str(nA11)
    if sInn[9:9+1] == nA11: 
        return True
    else:
        return False


if __name__ == "__main__":
    db = Database()
    for inx in range(2300000000,2399999999):
        if cl_inn(str(inx)):
            inn_table = 'actual_inn_ul'
            inn_dict = {'inn': str(inx)}
            inn_columns = "(`"+"`,`".join(inn_dict.keys())+"`)"
            inn_placeholders = "('"+"','".join(map(str,inn_dict.values()))+"')"
            inn_query = "REPLACE INTO %s %s VALUES %s" % (inn_table, inn_columns, inn_placeholders)
            try:
                db.insert(inn_query)
            except:
                print(inn_query)

#2311014546
#2313017430
#sInn = "2311014546"
#for i in range(0,9):
#    print(sInn[i:i+1])
#print(cl_inn(sInn))
