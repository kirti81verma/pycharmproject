from flask import Flask
app=Flask(__name__)
state=''
@app.before_request
def before_request():
    global state
    state+=' before request'
@app.teardown_request
def tear_request(excep):
    global state
    state+=' tear request'
@app.after_request
def after_request(resp):
    global state
    state+=' after request'

    return resp
@app.route('/')
def index():
    return 'hello'+state
if __name__=='__main__':
    app.run(debug=True)

