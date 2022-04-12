import constants

class MSI_Split_FSM_Cache:
    def __init__(self, id, value, state):
        self.value = value
        self.state = state
        self.id = id
        self.protocol = "MSI_SPLIT"

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def recordUpdate(self, value, buffer):
        instruction = {
            "action" : "Update",
            "target" : self.id,
            "value" : value,
            "state" : self.state
        }
        buffer.append(instruction)

    def getProtocol(self):
        return self.protocol

    def loadValidActions(self, buffer):
        if self.state == constants.STATE_I:
            buffer.append({
                "processor" : self.id,
                "actions" : [constants.EVENT_LOAD, constants.EVENT_STORE]
            })

        elif self.state == constants.STATE_S or self.state == constants.STATE_M:
            buffer.append({
                "processor" : self.id,
                "actions" : [constants.EVENT_LOAD, constants.EVENT_STORE, constants.EVENT_EVICT]
            })

    def updateState(self, message, buffer, bus):  
        event = message["action"]

        if self.state == constants.STATE_I:
            if event == constants.EVENT_LOAD:
                self.state = constants.STATE_IS_AD

                instruction = {
                    "action" : constants.EVENT_GET_S,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_STORE:
                self.state = constants.STATE_IM_AD

                instruction = {
                    "action" : constants.EVENT_GET_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_IS_AD:
            if event == constants.EVENT_GET_S or event == constants.EVENT_GET_M:
                # Make sure it is an Own GetS or GetM
                if message["src"] == self.id:
                    self.state = constants.STATE_IS_D
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id: 
                    self.state = constants.STATE_IS_A
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IS_D: 
            if event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id: 
                    self.state = constants.STATE_S
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IS_A:
            if event == constants.EVENT_GET_S or event == constants.EVENT_GET_M:
                # Make sure it is an Own GetS or GetM
                if message["src"] == self.id:
                    self.state = constants.STATE_S 
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_IM_AD:
            if event == constants.EVENT_GET_M:
                # Make sure it is an Own GetM
                if message["src"] == self.id:
                    self.state = constants.STATE_IM_D
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id: 
                    self.state = constants.STATE_IM_A
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IM_D:
            if event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id:  
                    self.state = constants.STATE_M
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IM_A:
            if event == constants.EVENT_GET_M:
                # Make sure it is an Own GetM
                if message["src"] == self.id:
                    self.state == constants.STATE_M
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_S:
            if event == constants.EVENT_LOAD:
                instruction = {
                    "action" : constants.EVENT_HIT,
                    "target" : self.id
                }
                buffer.append(instruction)

            elif event == constants.EVENT_STORE:
                self.state = constants.STATE_SM_AD

                instruction = {
                    "action" : constants.EVENT_GET_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_EVICT:
                self.state = constants.STATE_I
                self.value = constants.NULL_VALUE
                self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_GET_M:
                # Make sure it is an Other GetM
                if message["src"] != self.id:
                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_SM_AD:
            if event == constants.EVENT_GET_M:
                # Make sure it is an Own GetM
                if message["src"] == self.id:
                    self.state = constants.STATE_SM_D
                    self.recordUpdate(None, buffer)

                else:
                    self.state = constants.STATE_IM_AD
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id: 
                    self.state = constants.STATE_SM_A
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_SM_D:
            if event == constants.EVENT_DATA:
                # Make sure Data message is meant for this processor 
                if message["target"] == self.id: 
                    self.state = constants.STATE_M
                    self.value = message["src"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_SM_A:
            if event == constants.EVENT_GET_M:
                # Make sure it is an Own GetM
                if message["src"] == self.id:
                    self.state = constants.STATE_M
                    self.recordUpdate(None, buffer)

                else:
                    self.state = constants.STATE_IM_A
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_M:
            if event == constants.EVENT_LOAD or event == constants.EVENT_STORE:
                instruction = {
                    "action" : constants.EVENT_HIT,
                    "target" : self.id
                }
                buffer.append(instruction)

            elif event == constants.EVENT_EVICT:
                self.state = constants.STATE_MI_A

                instruction = {
                    "action" : constants.EVENT_PUT_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_S:
                if message["src"] != self.id:
                    self.state = constants.STATE_S

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "value" : self.value,
                        "target" : message["src"],
                        "src" : self.id, 
                        "dst" : constants.BUS_ID
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_M:
                if message["src"] != self.id:
                    self.state = constants.STATE_I

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "value" : self.value,
                        "target" : message["src"],
                        "src" : self.id, 
                        "dst" : constants.BUS_ID
                    }
                    buffer.append(instruction)
                    bus.append(instruction)

                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_MI_A:
            if event == constants.EVENT_PUT_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_I

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "value" : self.value,
                        "target" : message["src"],
                        "src" : self.id, 
                        "dst" : constants.BUS_ID
                    }
                    buffer.append(instruction)
                    bus.append(instruction)

                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_GET_S:
                if message["src"] != self.id:
                    self.state = constants.STATE_I

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "value" : self.value,
                        "target" : message["src"],
                        "src" : self.id, 
                        "dst" : constants.BUS_ID
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_M:
                if message["src"] != self.id:
                    self.state = constants.STATE_II_A

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "value" : self.value,
                        "target" : message["src"],
                        "src" : self.id, 
                        "dst" : constants.BUS_ID
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_II_A:
            if event == constants.EVENT_PUT_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_I 
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)
       







                

       
   