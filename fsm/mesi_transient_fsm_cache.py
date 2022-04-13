import constants

class MESI_Transient_FSM_Cache:
    def __init__(self, id, value, state):
        self.value = value
        self.state = state
        self.id = id
        self.protocol = "MESI"
        self.lastWrite = constants.NULL_VALUE

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def getProtocol(self):
        return self.protocol

    def recordUpdate(self, value, buffer):
        instruction = {
            "action" : "Update",
            "target" : self.id,
            "value" : value,
            "state" : self.state
        }
        buffer.append(instruction)

    def loadValidActions(self, buffer):
        if self.state == constants.STATE_I:
            buffer.append({
                "processor" : self.id,
                "actions" : [constants.EVENT_LOAD, constants.EVENT_STORE]
            })

        elif self.state == constants.STATE_S or self.state == constants.STATE_M or self.state == constants.STATE_E:
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
                self.lastWrite = message["value"]

                instruction = {
                    "action" : constants.EVENT_GET_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_IS_AD:
            if event == constants.EVENT_GET_S:
                if message["src"] == self.id:
                    self.state = constants.STATE_IS_D
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_IS_D:
            if event == constants.EVENT_DATA:
                if message["target"] == self.id and message["exclusive"] == 0:
                    self.state = constants.STATE_S
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

                elif message["target"] == self.id and message["exclusive"] == 1:
                    self.state = constants.STATE_E
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IM_AD:
            if event == constants.EVENT_GET_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_IM_D
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_IM_D:
            if event == constants.EVENT_DATA:
                if message["target"] == self.id:
                    self.state = constants.STATE_M
                    self.value = self.lastWrite
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_S:
            if event == constants.EVENT_LOAD:
                instruction = {
                    "action" : constants.EVENT_HIT,
                    "target" : self.id
                }
                buffer.append(instruction)

            elif event == constants.EVENT_STORE:
                self.state = constants.STATE_SM_AD
                self.lastWrite = message["value"]

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
                if message["src"] != self.id:
                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_SM_AD:
            if event == constants.EVENT_GET_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_SM_D
                    self.recordUpdate(None, buffer)

                else:
                    self.state = constants.STATE_IM_AD
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_SM_D:
            if event == constants.EVENT_DATA:
                if message["target"] == self.id:
                    self.state = constants.STATE_M
                    self.value = self.lastWrite
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_E:
            if event == constants.EVENT_STORE:
                self.state = constants.STATE_M
                self.value = message["value"]
                self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_EVICT:
                self.state = constants.STATE_EI_A

                instruction = {
                    "action" : constants.EVENT_PUT_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "value" : self.value
                }
                buffer.append(instruction)
                bus.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_S:
                if message["src"] != self.id:
                    self.state = constants.STATE_S

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "exclusive" : 0,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_M:
                if message["src"] != self.id:
                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)

                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_M:
            if event == constants.EVENT_LOAD:
                instruction = {
                    "action" : constants.EVENT_HIT,
                    "target" : self.id
                }
                buffer.append(instruction)

            elif event == constants.EVENT_STORE:
                instruction = {
                    "action" : constants.EVENT_HIT,
                    "target" : self.id
                }
                buffer.append(instruction)

                self.value = message["value"]
                self.recordUpdate(self.value, buffer)

            if event == constants.EVENT_EVICT:
                self.state = constants.STATE_MI_A

                instruction = {
                    "action" : constants.EVENT_PUT_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "value" : self.value
                }
                buffer.append(instruction)
                bus.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_S:
                if message["src"] != self.id:
                    self.state = constants.STATE_S

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_M:
                if message["src"] != self.id:
                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)

                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_MI_A:
            if event == constants.EVENT_PUT_M:
                if message["src"] == self.id:
                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : constants.NULL_VALUE
                    }
                    buffer.append(instruction)
                    bus.append(instruction)

                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE
                    self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_GET_S or constants.EVENT_GET_M:
                if message["src"] != self.id:
                    self.state = constants.STATE_II_A

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_EI_A:
            if event == constants.EVENT_PUT_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE

                    instruction = {
                        "action" : constants.EVENT_NO_DATA_E,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : constants.NULL_VALUE,
                        "target" : constants.NULL_VALUE
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_S or constants.EVENT_GET_M:
                if message["src"] != self.id:
                    self.state = constants.STATE_II_A

                    instruction = {
                        "action" : constants.EVENT_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : self.value,
                        "target" : message["src"]
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)

        elif self.state == constants.STATE_II_A:
            if event == constants.EVENT_PUT_M:
                if message["src"] == self.id:
                    self.state = constants.STATE_I
                    self.value = constants.NULL_VALUE

                    instruction = {
                        "action" : constants.EVENT_NO_DATA,
                        "src" : self.id,
                        "dst" : constants.BUS_ID,
                        "value" : constants.NULL_VALUE,
                        "target" : constants.NULL_VALUE
                    }
                    buffer.append(instruction)
                    bus.append(instruction)
                    self.recordUpdate(None, buffer)