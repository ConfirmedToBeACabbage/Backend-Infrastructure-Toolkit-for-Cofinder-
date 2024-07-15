from flask import Flask
from TMManage import TransactionManager

# Flask setup
app = Flask(__name__)

#-API Gateway Routes-#

# Testing for instantiation
@app.route("/testinit")
def testinit():
    print('1')
    response = tm.route_req('testinit', [])
    return str(response) + 'wtf'

#-Transaction Manager Routes-#

# Return the Transaction Manager log
@app.route("/tm/log")
def return_log(): 
    return tm.ret_log()

#-PostgreSQL Routes-#

# Begin a connection
@app.route("/pg/conn/<dbname>/<user>/<password>/<host>/<port>")
def pg_conn(dbname, user, password, host, port):
    tm.route_req('pg/conn', [dbname, user, password, host, port])
    return 'Paceholder'

# Check for the uptime
@app.route("/pg/chk/<user>")
def pg_chk(user):
    tm.route_req('pg/chk', [user])
    return 'Paceholder'

# Send a query
@app.route("/pg/query/<query>/<user>")
def pg_query(query, user):
    result = tm.route_req('pg/query/', [query, user])
    return str(result)

#-Cron Jobs-#
@app.route("/admin/job/<password>/<job_action>/<job_py_name>/<time>")
def admin_cron_job(password, job_action, job_py_name, time):
    if(str(password).strip() == 'placeholder'):
        tm.route_req('/admin/job/' + str(job_action).strip() + '/' + str(job_py_name).strip() + '/' + str(time).strip())

    return 0 

@app.route("/admin/job/<password>/log")
def admin_cron_log(password):
    if(str(password).strip() == 'placeholder'):
        tm.route_req('/admin/job/log')

    return 0 

# Main entrance
if __name__ == "__main__":
    print("Running")

    # Testing #
    #tm.route_req('pg/conn', ['postgres', 'writeonlyusr', 'testing2', 'localhost', '5432'])
    #print(tm.ret_log())

    tm = TransactionManager()
    
    app.run(host='0.0.0.0', debug=True, threaded=True)


