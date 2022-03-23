class MSI_Transient_FSM:
    def __init__(self, id, value, state):
        self.value = value
        self.state = state
        self.id = id

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def updateState(self, action, instructions):        
        if self.state == "Invalid":
            if action == "GET_S":
                print("Processor ", self.id, " is transitioning from Invalid to Shared")

                instruction = {
                    "action": "BusRead",
                    "src": self.id,
                    "dst": -2
                }

                instructions.append(instruction)
                self.state = "Shared"

            elif action == "GET_M":
                print("Processor ", self.id, " is transitioning from Invalid to Modified")
                self.state = "Modified"

            else:
                print("Action not supported") 

   