from flask import Flask , request , make_response, redirect,render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)


all = ['Buy cofee ','Send request','Send product']

@app.route('/')
def index():
    user_id = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_id',user_id)
    return response

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html' , error=error)

@app.errorhandler(500)
def internarErrorServer(error):
    return render_template('500.html' , error=error)    

@app.route('/hello')
def hello():
    user_id = request.cookies.get('user_id')
    
    context={
        "user_ip" : user_id,
        "all" : all
    }

    return render_template('hello.html',**context)

@app.route("/500")
def error_500():
    raise Exception('500 Internal server error test')
# return 'hello wolrd flask {} - {}'.format(user_id,user_name)

# if __name__ == '__name__':
#     app.run(port=5000)