class MSI_Transient_FSM:
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

    def updateState(self, action, instructions):        
        if self.state == "Invalid":
            if action == "GET_S":
                print("Processor ", self.id, " is transitioning from Invalid to Shared")

                instruction = {
                    "action": "BusRd",
                    "src": self.id,
                    "dst": -2
                }

                instructions.append(instruction)
                self.state = "Shared"

            elif action == "GET_M":
                print("Processor ", self.id, " is transitioning from Invalid to Modified")

                instruction = {
                    "action": "BusRdX",
                    "src": self.id,
                    "dst": -2
                }

                instructions.append(instruction)
                self.state = "Modified"

        elif self.state == "Shared":
            if action == "BusRd":
                instruction = {
                    "action": "BusReply",
                    "src": self.id,
                    "dst": -2,
                    "value": self.value
                }

                instructions.append(instruction)

            elif action == "BusRdX" or action == "BusInv":
                print("Processor ", self.id, " is transitioning from Shared to Invalid")

                instruction = {
                    "action": "Update",
                    "target": self.id,
                    "value": 0,
                    "state": "Invalid"
                }
                instructions.append(instruction)

                self.value = 0 
                self.state = "Invalid"               

            elif action == "GET_M":
                print("Processor ", self.id, " is transitioning from Shared to Modified")

                instruction = {
                    "action": "BusInv",
                    "src": self.id,
                    "dst": -2
                }

                instructions.append(instruction)
                self.state = "Modified"

            elif action == "Evict":
                instruction = {
                    "action": "Update",
                    "target": self.id,
                    "value": 0, # TODO: change invalid value from 0 to Null
                    "state": "Invalid"
                }
                self.instructions.append(instruction)

        elif self.state == "Modified":
            if action == "BusRd":
                instruction = {
                    "action": "BusReply",
                    "src": self.id,
                    "dst": -2,
                    "value": self.value
                }
                instructions.append(instruction)

                instruction = {
                    "action": "Update",
                    "target": self.id,
                    "value": self.value,
                    "state": "Shared"
                }
                instructions.append(instruction)

                print("Processor ", self.id, " is transitioning from Modified to Shared")
                self.state = "Shared"

            elif action == "BusRdX":
                print("Processor ", self.id, " is transitioning from Modified to Invalid")
                self.value = 0

                instruction = {
                    "action": "BusReply",
                    "src": self.id,
                    "dst": -2
                }
                instructions.append(instruction)

                instruction = {
                    "action": "Update",
                    "target": self.id,
                    "value": 0,
                    "state": "Invalid"
                }
                instructions.append(instruction)

            elif action == "Evict":
                self.value = 0

                instruction = {
                    "action": "BusWB",
                    "src": self.id,
                    "dst": -2
                } 

                self.instructions.append(instruction)

                instruction = {
                    "action": "Update",
                    "target": self.id,
                    "value": 0, # TODO: change invalid value from 0 to Null
                    "state": "Invalid"
                }
                self.instructions.append(instruction)






   