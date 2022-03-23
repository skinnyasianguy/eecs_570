import flask

# A simple Flask App which takes
# a user's name as input and responds
# with "Hello {name}!"

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if flask.request.method == 'POST':
        message = 'Hello ' + flask.request.form['name-input'] + '!'
    return flask.render_template('index.html', message=message)

@app.route('/hello')
def hello_world():
   return "hello world"

if __name__ == '__main__':
    app.run()