class Driver:
    def __init__(self, processors, memoryValue):
        self.processors = processors
        self.hasValues = [False, False, False]
        self.instructions = []
        self.memoryValue = memoryValue

    # TODO : Make it better lmao
    def setInitialState(self):

        for i in range (len(self.processors)):
            temp = {
                "processor" : i,
                "value" : 0,
                "register" : "A",
                "state" : "Invalid"
            }

            self.instructions.append(temp)

        temp = {
            "processor" : -1,
            "value" : 20,
            "register" : "A",
        }

        self.instructions.append(temp)

    def getValidActions(self):
        for i in range (len(self.processors)):
            processorState = self.processors[i].getState()

            if processorState == "Invalid":
                self.instructions.append({
                    "processor" : i,
                    "actions" : ["Load", "Store"]
                })

            elif processorState == "Shared":
                self.instructions.append({
                    "processor" : i,
                    "actions" : ["Load", "Store", "Evict"]
                })

    def getInstructions(self):
        return self.instructions

    def clearInstructions(self):
        self.instructions = []

    def reset(self):
        for i in range (len(self.processors)):
            self.processors[i].setState("Invalid")
            self.processors[i].setValue(0)

    def doesMemoryHaveData(self, excludeIndex):
        retval = -1

        for i in range(len(self.hasValues)):
            if self.hasValues[i] and i != excludeIndex:
                return i

        return retval

    def processMessage(self, action, processorID, newValue):
        if action == "GET_S":
            self.processors[processorID].updateState(action, self.instructions)

            # Processor was either Shared or Modified so nothing happens
            if (len(self.instructions) == 0):
                return

            index = self.doesMemoryHaveData(-1)

            # Memory has the data
            if index == -1:
                instruction = {
                    "action": "BusReply",
                    "src": -1,
                    "dst": -2
                }

                self.instructions.append(instruction)
                
            # One of the processors has the data
            else:
                self.processors[index].updateState("BusRd", self.instructions)
                if self.processors[index].getState() == "Modified":
                    self.memoryValue = self.processors[index].getValue()
                    instruction = {
                        "action": "Update",
                        "target": -1,
                        "value": self.memoryValue,
                        "state": "hi"
                    }
                    self.instructions.append(instruction)

            updatedValue = self.memoryValue if index == -1 else self.processors[index].getValue()

            instruction = {
                "action": "Update",
                "target": processorID,
                "value": updatedValue,
                "state": "Shared"
            }
            self.instructions.append(instruction)
            
            self.processors[processorID].setValue(updatedValue)
            self.hasValues[processorID] = True

        elif action == "GET_M":
            self.processors[processorID].updateState(action, self.instructions)

            # Processor was Modified so nothing happens
            if (len(self.instructions) == 0):
                return

            busInstruction = self.instructions[0]['action']
            index = self.doesMemoryHaveData(processorID)

            for i in range(len(self.processors)):
                if i == processorID:
                    continue

                self.processors[i].updateState(busInstruction, self.instructions)
                self.hasValues[i] = False

            if busInstruction == "BusRdX":
                if index == -1:
                    instruction = {
                        "action": "BusReply",
                        "src": -1,
                        "dst":-2
                    }

                    self.instructions.append(instruction)

                else: 
                    instruction = {
                        "action": "BusReply",
                        "src": index,
                        "dst": -2
                    }
                    self.instructions.append(instruction)

            instruction = {
                "action": "Update",
                "target": processorID,
                "value": newValue,
                "state": "Modified"
            }
            self.instructions.append(instruction)

            self.processors[processorID].setValue(newValue)
            self.hasValues[processorID] = True

        elif action == "EVICT":
            originalState = self.processors[processorID].getState()
            originalValue = self.processors[processorID].getValue()

            self.processors[processorID].updateState(action, self.instructions)

            if originalState == 'Modified':
                self.memoryValue = originalValue

                instruction = {
                    "action": "Update",
                    "target": -1,
                    "value": 0,
                    "state": "Invalid"
                }
                self.instructions.append(instruction)

            
            
                

