import flask
import json 
import constants

from fsm.msi_transient_fsm_cache import MSI_Transient_FSM_Cache
from fsm.msi_transient_fsm_memory import MSI_Transient_FSM_Memory
from driver import Driver
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

msiFSM = MSI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
msiFSM2 = MSI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
msiFSM3 = MSI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)

processors = [msiFSM, msiFSM2, msiFSM3]
memory = MSI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I_OR_S)
driver = Driver(processors, memory)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if flask.request.method == 'POST':
        message = 'Hello ' + flask.request.form['name-input'] + '!'
    return flask.render_template('index.html', message=message)

@app.route('/execute_processor_action', methods=['POST'])
def execute_processor_action():
    jsonBody = flask.request.json

    driver.processMessage(jsonBody) 
    instructions = driver.getInstructions()
    result = json.dumps(instructions)

    driver.clearInstructions()
    return result

@app.route('/execute_bus_event', methods=['POST'])
def execute_bus_event():
    driver.processBusEvent()
    instructions = driver.getInstructions()
    result = json.dumps(instructions)

    driver.clearInstructions()
    return result

@app.route('/get_bus_events', methods=['GET'])
def get_bus_event():
    result = json.dumps(driver.getBus())
    return result

@app.route('/clear_machine', methods=['GET'])
def clear_machine():
    driver.reset()

    return "Cleared"

@app.route('/get_valid_instructions', methods=['GET'])
def get_valid_instructions():
    driver.loadValidActions()
    result = json.dumps(driver.getInstructions())

    driver.clearInstructions()
    return result

# TODO : Need to fix this when we add more protocols
@app.route('/get_initial_state', methods=['GET'])
def get_initial_state():
    driver.setInitialState()
    instructions = driver.getInstructions()

    result = json.dumps(instructions)
    driver.clearInstructions()
    return result

if __name__ == '__main__':
    app.run()