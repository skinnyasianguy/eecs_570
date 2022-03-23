import flask
import json 

from fsm.msi_transient_fsm import MSI_Transient_FSM
from driver import Driver
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

msiFSM = MSI_Transient_FSM(0, 0, "Invalid")
msiFSM2 = MSI_Transient_FSM(1, 0, "Invalid")
msiFSM3 = MSI_Transient_FSM(2, 0, "Invalid")

processors = [msiFSM, msiFSM2, msiFSM3]
driver = Driver(processors, 20)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if flask.request.method == 'POST':
        message = 'Hello ' + flask.request.form['name-input'] + '!'
    return flask.render_template('index.html', message=message)

@app.route('/get_next_step', methods=['POST'])
def get_next_step():
    jsonBody = flask.request.json
    action = jsonBody['action']
    processorID = jsonBody['processor']

    driver.processMessage(action, processorID) 
    instructions = driver.getInstructions()
    result = json.dumps(instructions)

    driver.clearInstructions()
    return result

@app.route('/clear_machine', methods=['GET'])
def clear_machine():
    driver.reset()

    return "Cleared"

@app.route('/get_valid_instructions', methods=['GET'])
def get_valid_instructions():
    driver.getValidInstructions()
    result = json.dumps(driver.getInstructions())

    driver.clearInstructions()
    return result

@app.route('/get_initial_state', methods=['GET'])
def get_initial_state():
    driver.setInitialState()
    instructions = driver.getInstructions()

    result = json.dumps(instructions)
    driver.clearInstructions()
    return result

if __name__ == '__main__':
    app.run()