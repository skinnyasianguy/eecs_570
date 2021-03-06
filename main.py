import flask
import json 
import constants

from fsm.msi_transient_fsm_cache import MSI_Transient_FSM_Cache
from fsm.msi_transient_fsm_memory import MSI_Transient_FSM_Memory
from fsm.msi_split_fsm_cache import MSI_Split_FSM_Cache
from fsm.msi_split_fsm_memory import MSI_Split_FSM_Memory
from fsm.mesi_transient_fsm_cache import MESI_Transient_FSM_Cache
from fsm.mesi_transient_fsm_memory import MESI_Transient_FSM_Memory
from fsm.mosi_transient_fsm_cache import MOSI_Transient_FSM_Cache
from fsm.mosi_transient_fsm_memory import MOSI_Transient_FSM_Memory
from fsm.moesi_transient_fsm_cache import MOESI_Transient_FSM_Cache
from fsm.moesi_transient_fsm_memory import MOESI_Transient_FSM_Memory

from driver import Driver
from flask_cors import CORS
from flask import request

app = flask.Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

msiFSM = MSI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
msiFSM2 = MSI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
msiFSM3 = MSI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)

processors = [msiFSM, msiFSM2, msiFSM3]
memory = MSI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I_OR_S)
driver = Driver(processors, memory)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if flask.request.method == 'POST':
        message = 'Hello ' + flask.request.form['name-input'] + '!'
    return flask.render_template('index.html', message=message)

@app.route('/execute_processor_action', methods=['POST'])
def execute_processor_action():
    jsonBody = flask.request.json

    driver.processProcessorAction(jsonBody) 
    buffer = driver.getBuffer()
    result = json.dumps(buffer, default=set_default)

    driver.clearBuffer()
    return result

@app.route('/execute_bus_event', methods=['POST'])
def execute_bus_event():
    jsonBody = flask.request.json
    driver.processBusEvent(jsonBody.get("busIndex", 0))

    buffer = driver.getBuffer()
    result = json.dumps(buffer, default=set_default)

    driver.clearBuffer()
    return result

@app.route('/execute_queue_event', methods=['POST'])
def execute_queue_event():
    jsonBody = flask.request.json
    driver.processQueueEvent(jsonBody.get("processor", 0))

    buffer = driver.getBuffer()
    result = json.dumps(buffer, default=set_default)

    driver.clearBuffer()
    return result

@app.route('/get_bus_events', methods=['GET'])
def get_bus_event():
    result = json.dumps(driver.getBus(), default=set_default)
    return result

@app.route('/get_queue_events', methods=['GET'])
def get_queue_events():
    result = json.dumps(driver.getQueues(), default=set_default)
    return result

@app.route('/clear_machine', methods=['GET'])
def clear_machine():
    driver.reset()

    return "Cleared"

@app.route('/get_valid_instructions', methods=['GET'])
def get_valid_instructions():
    driver.loadValidActions()
    result = json.dumps(driver.getBuffer(), default=set_default)

    driver.clearBuffer()
    return result

@app.route('/get_initial_state', methods=['GET'])
def get_initial_state():

    protocol = request.args.get('protocol')
    type = request.args.get('type')
    initDriver(protocol, type)

    driver.setInitialState()
    buffer = driver.getBuffer()

    result = json.dumps(buffer, default=set_default)
    driver.clearBuffer()
    return result

def initDriver(protocol, type):
    global msiFSM
    global msiFSM2
    global msiFSM3

    global memory 
    global processors
    global driver

    if protocol == "MSI":
        if type == "baseline":
            msiFSM = MSI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
            msiFSM2 = MSI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
            msiFSM3 = MSI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)
            memory = MSI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I_OR_S)
        
        elif type == "split":
            msiFSM = MSI_Split_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
            msiFSM2 = MSI_Split_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
            msiFSM3 = MSI_Split_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)
            memory = MSI_Split_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I_OR_S)

    elif protocol == "MESI":
        msiFSM = MESI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
        msiFSM2 = MESI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
        msiFSM3 = MESI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)
        memory = MESI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I)

    elif protocol == "MOSI":
        msiFSM = MOSI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
        msiFSM2 = MOSI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
        msiFSM3 = MOSI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)
        memory = MOSI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I_OR_S)

    elif protocol == "MOESI":
    	msiFSM = MOESI_Transient_FSM_Cache(0, constants.NULL_VALUE, constants.STATE_I)
    	msiFSM2 = MOESI_Transient_FSM_Cache(1, constants.NULL_VALUE, constants.STATE_I)
    	msiFSM3 = MOESI_Transient_FSM_Cache(2, constants.NULL_VALUE, constants.STATE_I)
    	memory = MOESI_Transient_FSM_Memory(constants.DEFAUT_VALUE, constants.STATE_I)

    processors = [msiFSM, msiFSM2, msiFSM3]
    driver = Driver(processors, memory)

if __name__ == '__main__':
    app.run()