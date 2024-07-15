from flask import Flask
from flask import request

app = Flask(__name__)

# API Gateway #
@app.route("/testinit")
def testinit():
    return "Hello, this is working as intended; This is the main server flask NGINX should be reverse proxying to. Test 2"

@app.route('/m/req_table/<table>', methods = ['GET', 'POST', 'DELETE'])
def req_table(table):

    # Get
    if request.method == 'GET':
        return ""
    
    # Post
    if request.method == 'POST':
        return ""
    
    else:
        return "Error 405"
    
if __name__ == "__main__":
    print("Running")
    app.run(host='0.0.0.0', debug=True)