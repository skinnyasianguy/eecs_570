import constants

class MESI_Transient_FSM_Memory:
    def __init__(self, value, state):
        self.value = value
        self.state = state
        self.id = constants.MEMORY_ID

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

    def updateState(self, message, buffer, bus):  
        event = message["action"]

        if self.state == constants.STATE_I:
            if event == constants.EVENT_GET_S or event == constants.EVENT_GET_M:
                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : message["src"],
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "exclusive" : 1
                }
                buffer.append(instruction)
                bus.append(instruction)

                self.state = constants.STATE_E_OR_M

            elif event == constants.EVENT_PUT_M:
                self.state = constants.STATE_I_D

        elif self.state == constants.STATE_S:
            if event ==  constants.EVENT_GET_S:
                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : message["src"],
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "exclusive" : 0
                }
                buffer.append(instruction)
                bus.append(instruction)
            
            elif event ==  constants.EVENT_GET_M:
                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : message["src"],
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "exclusive" : 0
                }
                buffer.append(instruction)
                bus.append(instruction)
                self.state = constants.STATE_E_OR_M

            elif event == constants.EVENT_PUT_M:
                self.state = constants.STATE_S_D

        elif self.state == constants.STATE_E_OR_M:
            if event == constants.EVENT_GET_S:
                self.state = constants.STATE_S_D
            elif event == constants.EVENT_PUT_M:
                self.state = constants.STATE_E_OR_M_D
                
        elif self.state == constants.STATE_I_D:
            if event == constants.EVENT_DATA:
                self.state = constants.STATE_I
                self.value = message["value"]
                self.recordUpdate(self.value, buffer)
            elif event == constants.EVENT_NO_DATA or event == constants.EVENT_NO_DATA_E:
                self.state = constants.STATE_I

        elif self.state == constants.STATE_S_D:
            if event == constants.EVENT_DATA:
                self.state = constants.STATE_S
                self.value = message["value"]
                self.recordUpdate(self.value, buffer)
            elif event == constants.EVENT_NO_DATA or event == constants.EVENT_NO_DATA_E:
                self.state = constants.STATE_S

        elif self.state == constants.STATE_E_OR_M_D:
            if event == constants.EVENT_DATA:
                self.state = constants.STATE_I
                self.value = message["value"]
                self.recordUpdate(self.value, buffer)
            elif event == constants.EVENT_NO_DATA:
                self.state = constants.STATE_E_OR_M
            elif event == constants.EVENT_NO_DATA_E:
                self.state = constants.STATE_I



                

            








        ##### MSI #########
        if self.state == constants.STATE_I_OR_S:
            if event == constants.EVENT_GET_S:
                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : message["src"],
                    "src" : self.id, 
                    "dst" : constants.BUS_ID
                }

                buffer.append(instruction)
                bus.append(instruction)
            
            elif event == constants.EVENT_GET_M:
                self.state = constants.STATE_M

                instruction = {
                    "action" : constants.EVENT_DATA,
                    "value" : self.value,
                    "target" : message["src"],
                    "src" : self.id, 
                    "dst" : constants.BUS_ID
                }
                buffer.append(instruction)
                bus.append(instruction)

        elif self.state == constants.STATE_I_OR_S_D:
            if event == constants.EVENT_DATA:
                self.value = message["value"] # Update memory value
                self.state = constants.STATE_I_OR_S
                self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_M:
            if event == constants.EVENT_GET_S:
                self.state = constants.STATE_I_OR_S_D

            elif event == constants.EVENT_PUT_M:
                self.state = constants.STATE_I_OR_S
                self.value = message["value"] # Update memory value
                self.recordUpdate(self.value, buffer)
                





   