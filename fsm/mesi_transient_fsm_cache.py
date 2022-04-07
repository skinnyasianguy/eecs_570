import constants

<<<<<<< HEAD
class MSI_Transient_FSM_Cache:
=======
class MESI_Transient_FSM_Cache:
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54
    def __init__(self, id, value, state):
        self.value = value
        self.state = state
        self.id = id

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

<<<<<<< HEAD
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
                print("Processor ", self.id, " is transitioning from I to IS_D")
                self.state = constants.STATE_IS_D
=======
    def updateState(self, message, buffer, bus):  
        event = message["action"]

        if self.state == constants.STATE_I:
            if event == constants.EVENT_LOAD:
                self.state = constants.STATE_IS_AD
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54

                instruction = {
                    "action" : constants.EVENT_GET_S,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)
<<<<<<< HEAD
                
            elif event == constants.EVENT_STORE:
                print("Processor ", self.id, " is transitioning from I to IM_D")
                self.state = constants.STATE_IM_D
=======

            elif event == constants.EVENT_STORE:
                self.state = constants.STATE_IM_AD
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54

                instruction = {
                    "action" : constants.EVENT_GET_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

<<<<<<< HEAD
        elif self.state == constants.STATE_IS_D:
            if event == constants.EVENT_DATA:
                print("Processor ", self.id, " is transitioning from IS_D to S")

                self.value = message["value"]
                self.state = constants.STATE_S
                self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_IM_D:
            if event == constants.EVENT_DATA:
                print("Processor ", self.id, " is transitioning from IM_D to M")

                self.value = message["value"]
                self.state = constants.STATE_M
                self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_S:
            if event == constants.EVENT_STORE:
                print("Processor ", self.id, " is transitioning from S to SM_D")
                self.state = constants.STATE_SM_D
=======
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
                    self.state == constants.STATE_E
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
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_S:
            if event == constants.EVENT_STORE:
                self.state = constants.STATE_SM_AD
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54

                instruction = {
                    "action" : constants.EVENT_GET_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID
                }
<<<<<<< HEAD
                buffer.append(instruction)
                bus.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_EVICT or event == constants.EVENT_GET_M:
                print("Processor ", self.id, " is transitioning from S to I")
=======
                bus.append(instruction)
                buffer.append(instruction)
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_EVICT:
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54
                self.state = constants.STATE_I
                self.value = constants.NULL_VALUE
                self.recordUpdate(self.value, buffer)

<<<<<<< HEAD
        elif self.state == constants.STATE_SM_D:
            if event == constants.EVENT_DATA:
                print("Processor ", self.id, " is transitioning from S to M")
                self.state = constants.STATE_M
                self.value = message["value"]
                self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_M:
            if event == constants.EVENT_EVICT:
                print("Processor ", self.id, " is transitioning from M to I")
=======
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
                    self.value = message["value"]
                    self.recordUpdate(self.value, buffer)

        elif self.state == constants.STATE_E:
            if event == constants.EVENT_STORE:
                self.state = constants.STATE_M
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_EVICT:
                self.state = constants.STATE_EI_A
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54

                instruction = {
                    "action" : constants.EVENT_PUT_M,
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "value" : self.value
                }
                buffer.append(instruction)
                bus.append(instruction)
<<<<<<< HEAD

                self.state = constants.STATE_S
                self.value = constants.NULL_VALUE
                self.recordUpdate(self.value, buffer)

            elif event == constants.EVENT_GET_S:
                print("Processor ", self.id, " is transitioning from M to S")

                instruction = {
                    "action" : constants.EVENT_DATA,
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "value" : self.value
                }
                buffer.append(instruction)
                bus.append(instruction)

                self.state = constants.STATE_S
                self.recordUpdate(None, buffer)

            elif event == constants.EVENT_GET_M:
                print("Processor ", self.id, " is transitioning from M to I")

                instruction = {
                    "action" : constants.EVENT_DATA,
=======
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


        elif self.state == constants.STATE_M:
            if event == constants.EVENT_EVICT:
                self.state = constants.STATE_MI_A

                instruction = {
                    "action" : constants.EVENT_PUT_M,
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54
                    "src" : self.id,
                    "dst" : constants.BUS_ID,
                    "value" : self.value
                }
                buffer.append(instruction)
                bus.append(instruction)
<<<<<<< HEAD

                self.state = constants.STATE_I
                self.value = constants.NULL_VALUE
                self.recordUpdate(self.value, buffer)










                

       
   
=======
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
                    

                
                



            


       
>>>>>>> 4453385003fb45c6c20c68724efa9e161fe99a54
