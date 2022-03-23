class Driver:
    def __init__(self, processors, memoryValue):
        self.processors = processors
        self.hasValues = [False, False, False]
        self.instructions = []
        self.memoryValue = memoryValue

    def getInstructions(self):
        return self.instructions

    def clearInstructions(self):
        self.instructions = []

    def doesMemoryHaveData(self):
        retval = -1

        for i in range(len(self.hasValues)):
            if self.hasValues[i]:
                return i

        return retval

    def processMessage(self, action, processorID):
        if action == "GET_S":
            self.processors[processorID].updateState(action, self.instructions)

            index = self.doesMemoryHaveData()

            # Memory has the data
            if index == -1:
                instruction = {
                    "action": "BusReply",
                    "src": -1,
                    "dst": -2,
                    "value": self.memoryValue
                }

                self.processors[processorID].setValue(self.memoryValue)
                self.instructions.append(instruction)

            # One of the processors has the data
            else:
                instruction = {
                    "action": "BusReply",
                    "src": index,
                    "dst": -2,
                    "value": self.processors[index].getValue()
                }

                self.processors[processorID].setValue(self.processors[index].getValue())
                self.instructions.append(instruction)


            self.hasValues[processorID] = True

    
