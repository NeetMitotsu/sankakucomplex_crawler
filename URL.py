from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/user", methods=['POST'])
def show_user_profile():
    error = None
    searchword = request.args.get('segment')
    print(searchword)
    keyword = request.form['segment']
    response = make_response(keyword)
    response.headers['X-Something'] = 'A value'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
