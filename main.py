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

@app.route('/get_next_step', methods=['POST'])
def get_next_step():
   print(flask.request.json)
   return flask.request.json

if __name__ == '__main__':
    app.run()