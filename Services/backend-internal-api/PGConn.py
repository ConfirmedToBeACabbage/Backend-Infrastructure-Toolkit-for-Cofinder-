import psycopg2


# Connection utility class to our postgres server
class PCopg2Connect():

    # Pre developed queries 
    # Samples here (Developed further pseudocode for now)
    test1 = "SELECT * FROM TEST1;"
    test2 = "INSERT INTO TEST1(id, NAME) VALUES (2, 'test2');"

    # Current transaction
    curr_trans = ''

    # Current connection 
    __conn = 0
    __conn_cursor = 0

    # Instantiation of psycog
    __pscog = psycopg2

    # Private "technically", not meant to be called on 
    __dbname    = ''
    __user      = ''
    __password  = ''
    __host      = ''
    __port      = ''

    # Nothing on instantiation
    def __init__(self):
        pass


    # Connection 
    def connect(self, dbname, user, password, host, port):

        if(self.__pscog != 0):
            try:
                self.__conn = self.__pscog.connect(dbname=dbname, 
                                                   user=user, 
                                                   password=password, 
                                                   host=host, 
                                                   port=port) 
            except Exception as e:
                return str(e)
            
        # If successful
        if(self.__conn.status == 1):
            
            # Set all variables 
            self.__dbname  = dbname
            self.__user = user
            self.__password = password
            self.__host = host
            self.__port = port

            # Set the cursor 
            self.__conn_cursor = self.__conn.cursor()

        # Else clear the connection
        else: 
            self.__conn = 0

        return self.__conn.status 

    # Execution of a query (Baseline, other methods do filtering for the query)
    def query_exec(self, query):

        # Checking 
        check = [0, 0]
        check = self.__uptime_check__()

        for item in check:

            # Something wrong with the connection  
            if(item == 0):
                return 0

        # Run query (Parameterized checks)
        self.__conn_cursor.execute(query)

        return self.__conn_cursor.fetchall()

    # Builds a query which then should be executed via query_exec
    def query_builder(self, query):

        result = ''

        if(query == 'test1'):
            result = self.query_exec(self.test1)
        elif(query == 'test2'):
            result = self.query_exec(self.test2)

        return result

    # Uptime check
    def __uptime_check__(self):
        
        # Check if we even have a connection
        if(self.__conn != 0):
            return [self.__conn.status, self.__conn.closed]
        # Otherwise just return 0 0 
        else:
            return [0, 0]


## Testing locally
# Test 1 
#conn = psycopg2.connect(dbname="postgres", user="writeonlyusr", password="testing2", host='localhost', port='5432') 

#print("Is the status up? (1)" + str(conn.status))
#print("Is the connection closed? (1)" + str(conn.closed))
#print(conn.info.server_version)
#print()

#cursorA = conn.cursor()
#cursorA.execute("INSERT INTO TEST1(id, NAME) VALUES (2, 'test2');")
#print(cursorA.fetchall())

# Im stupid you need to commit lmao 
#conn.commit()

# Test 2
#conn = psycopg2.connect(dbname="postgres", user="readonlyusr", password="testing1", host='localhost', port='5432') 

#print("Is the status up? (1)" + str(conn.status))
#print("Is the connection closed? (1)" + str(conn.closed))
#print(conn.info.server_version)
#print()

#cursorB = conn.cursor()
#cursorB.execute("SELECT * FROM TEST1;")
#print(cursorB.fetchall())