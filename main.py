import flask
import json 

from fsm.msi_transient_fsm import MSI_Transient_FSM
from driver import Driver

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if flask.request.method == 'POST':
        message = 'Hello ' + flask.request.form['name-input'] + '!'
    return flask.render_template('index.html', message=message)

@app.route('/get_next_step', methods=['POST'])
def get_next_step():
   
    msiFSM = MSI_Transient_FSM(0, 0, "Invalid")
    msiFSM2 = MSI_Transient_FSM(1, 0, "Invalid")
    msiFSM3 = MSI_Transient_FSM(2, 0, "Invalid")

    processors = [msiFSM, msiFSM2, msiFSM3]
    driver = Driver(processors, 20)

    jsonBody = flask.request.json
    action = jsonBody['action']
    processorID = jsonBody['processor']

    driver.processMessage(action, processorID) 
    instructions = driver.getInstructions()

    return json.dumps(instructions, separators=(',', ':'))

if __name__ == '__main__':
    app.run()