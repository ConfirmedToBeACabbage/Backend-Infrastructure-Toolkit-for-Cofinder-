from CRONJob import CronJob # We just want CronJob to be exposed
import secrets, datetime, PGConn

# Manage transactions
class TransactionManager():

    # Log 
    __curr_log = {}
    __curr_index = 0

    # Params
    __curr_transactions = {}
    __curr_objects = {'': []}

    # Current token
    __curr_token = ''

    # Current Cron Manager
    __cron_jobs = ''

    def __init__(self):

        # Setup a token
        self.__curr_token = secrets.token_hex(nbytes=16)

        # Setup cron job class
        self.__cron_jobs = CronJob()
    
    # Association With Transaction
    def tran_create(self, clarify_tk):

        self.__curr_token = secrets.token_hex(nbytes=16)

        chk = True

        # Check for duplicate
        while(chk):

            # Create hash
            hash_c = hash(str(self.__curr_token))

            if(hash_c not in self.__curr_transactions):
                break

        # Current transaction should be added
        self.__curr_transactions[str(hash_c)] = clarify_tk

        # Return a hash association
        return hash_c

    # This is the route request, this handles requests to the actual utility framework.
    # This is almost like a security layer between user and the framework, even though this is only an internal api. 
    # This SPECIFICALLY handles the surface level requests, for example instantiations
    def route_req(self, route, params):

        print('2')

        # Split the route
        split_route = route.split('/')

        # Create transaction
        hash_c = self.tran_create(str(split_route[0]))

        # Check the route, these generally mimic the flask routes, but for the manager to send off to the framework.
        # This may seem redundant, however having a "middle" area where I can manage and check all the transactions is good for development purposes. 

        print('3')

        # Test init
        if(split_route[0] == 'testinit'):
            print("This is the way")
            self.log('RAN: ' + str(hash_c) + '|TESTINIT|')
            return 'Working as intended, transaction manager online'

        # CRON JOB
        if(split_route[0] == 'admin' and split_route[1] == 'job' and split_route[2] != 'log'):
            job_action = split_route[2]
            job_py_name = split_route[3]
            time = split_route[4]

            result_job = ''

            # Start a job
            if(str(job_action).split() == 'start'):
                result_job = self.__cron_jobs.start_job(job_py_name) 
            
            # Stop a job
            elif(str(job_action).split() == 'stop'):
                result_job = self.__cron_jobs.stop_job(job_py_name) 
            
            # Add a job
            elif(str(job_action).split() == 'add'):
                result_job = self.__cron_jobs.add_job(job_py_name, 'python', time)
            
            # Remove a job
            elif(str(job_action).split() == 'remove'):
                result_job = self.__cron_jobs.remove_job(job_py_name)

            # Log the job
            self.log(result_job)

        if(split_route[0] == 'admin' and split_route[1] == 'job' and split_route[2] == 'log'):
            result_job = ''

            result_job = self.__cron_jobs.get_job_names()

            self.log(result_job)

        # PG CONN
        if(split_route[0] == 'pg' and split_route[1] == 'conn'):
            connection = 0

            other_param = params[1]

            # User can have multiple transactions "instances" running at the same time
            self.__curr_objects[str(hash_c)] = [PGConn.PCopg2Connect(), str(other_param)] 

            # Connection
            conn = self.__curr_objects[str(hash_c)][0]

            # Connect only if a connection already doesn't exist for said user to this database
            for item, value in self.__curr_objects.items():
                
                #DEBUG
                #self.log('DEBUG: ' + str(item) + '|DEBUG CONNECTION VALUE|' + 'DEBUG: ' + str(value))
                #self.log('DEBUG: ' + str(item) + '|DEBUG CONNECTION HASHC|' + 'DEBUG: ' + str(hash_c))
                #self.log('DEBUG: ' + str(item) + '|DEBUG CONNECTION CURRENT TRANS|' + 'DEBUG: ' + str(self.__curr_transactions))
                #self.log('DEBUG: ' + str(item) + '|DEBUG CONNECTION IF IN|' + 'DEBUG: ' + str(item in self.__curr_transactions))
                #self.log('DEBUG: ' + str(item) + '|DEBUG CONNECTION ITEM|' + 'DEBUG: ' + str(item))
                #self.log('DEBUG: ' +  str(params[1]))
                #self.log('DEBUG: ' +  str(value))
                #DEBUG END 

                if(item in self.__curr_transactions and self.__curr_transactions[item][0] == 'pg' and str(params[1]) != value[1]):
                    connection = conn.connect(params[0], params[1], params[2], params[3], params[4])
                    break 

            # Close the transaction and log it if failure 
            if(connection == 0):
                self.log('FAILED: ' + str(hash_c) + '|PGCONNECTION|' + 'ERROR: ' + str(connection))
                return 'FAILED: ' + str(hash_c) + '|PGCONNECTION|' + 'ERROR: ' + str(connection)
            else: 
                self.log('RAN: ' + str(hash_c) + '|PGCONNECTION|')
                return 'RAN: ' + str(hash_c) + '|PGCONNECTION|'

        # PG CHK
        if(split_route[0] == 'pg' and split_route[1] == 'chk'):
            
            all_connections = []

            # O(N) because a user could have an active transaction association
            for item, value in self.__curr_objects.items():

                # Check if it's part of pg
                if(str(split_route[2]) in value and self.__curr_transactions[str(hash_c)] == 'pg'):
                    all_connections.append(str(hash_c) + 'Uptime: ' + value.__uptime_check__() + '\n\n')

            # Log 
            self.log('RAN: ' + str(hash_c) + ': ')
            self.__curr_transactions[hash_c] = 0 # Close transaction

            return '\n'.join(all_connections)

        # PG QUERY 
        if(split_route[0] == 'pg' and split_route[1] == 'query'):

            result = ''

            for item, value in self.__curr_objects.items():
                if(item in self.__curr_transactions and self.__curr_transactions[item] == 'pg' and value[1] == params[1]):
                    conn = self.__curr_objects[item][0]
                    result = conn.query_builder('test1')
                    break

            self.log('RAN: ' + str(hash_c) + '|PGQUERY|' + 'RESULT: ' + str(result))
            return result

        # Unhandled at the moment

    # Add to the log
    def log(self, log):
        self.__curr_index += 1
        self.__curr_log[self.__curr_index] = str(datetime.datetime.now()) + ' :: ' + str(log)

    # Return the log in the console
    def ret_log(self):

        str_ret = ''

        for item, value in self.__curr_log.items():
            str_ret += str(item) + ': ' + str(value) + '<br>'

        return str_ret 


tm = TransactionManager()