import constants

class MSI_Split_FSM_Memory:
    def __init__(self, value, state):
        self.value = value
        self.state = state
        self.id = constants.MEMORY_ID
        self.owner = None
        self.requestQueue = []

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def getQueue(self):
        return self.requestQueue

    def recordUpdate(self, value, buffer):
        instruction = {
            "action" : "Update",
            "target" : self.id,
            "value" : value,
            "state" : self.state
        }
        buffer.append(instruction)

    def reset(self):
        self.state = constants.STATE_I_OR_S
        self.value = constants.DEFAUT_VALUE
        self.requestQueue = []

    def updateState(self, message, buffer, bus):  
        event = message["action"]
        msg_processed = True

        if self.state == constants.STATE_I_OR_S:
            if event == constants.EVENT_GET_S:
                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : {message["src"]},
                    "src" : self.id, 
                    "dst" : constants.BUS_ID
                }
                buffer.append(instruction)
                bus.append(instruction)

            elif event == constants.EVENT_GET_M:
                self.state = constants.STATE_M
                self.owner = message["src"]

                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : {message["src"]},
                    "src" : self.id, 
                    "dst" : constants.BUS_ID
                }
                buffer.append(instruction)
                bus.append(instruction)
        
        elif self.state == constants.STATE_M:
            if event == constants.EVENT_GET_S:
                self.owner = None 
                self.state = constants.STATE_I_OR_S_D

            elif event == constants.EVENT_GET_M:
                self.owner = message["src"]

            elif event == constants.EVENT_PUT_M:
                if message["src"] == self.owner:
                    self.owner = None 
                    self.state = constants.STATE_I_OR_S_D

            elif event == constants.EVENT_DATA:
                if self.id in message["target"]:
                    self.value = message["value"]
                    self.state = constants.STATE_I_OR_S_A
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_I_OR_S_D:
            if event == constants.EVENT_DATA:
                if self.id in message["target"]:
                    self.value = message["value"]
                    self.state = constants.STATE_I_OR_S
                    self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_GET_S or event == constants.EVENT_GET_M or event == constants.EVENT_PUT_M:
                if not message.get("reprocessing", True):
                    self.requestQueue.append(message)
                msg_processed = False

                instruction = {
                    "action" : constants.EVENT_STALL,
                    "target" : self.id
                }
                buffer.append(instruction)

        elif self.state == constants.STATE_I_OR_S_A:
            if event == constants.EVENT_GET_S:
                self.owner = None 
                self.state = constants.STATE_I_OR_S

            elif event == constants.EVENT_PUT_M:
                if message["src"] == self.owner:
                    self.owner = None 
                    self.state = constants.STATE_I_OR_S

        return msg_processed





   