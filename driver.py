import json

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

            # Memory has data
            if index == -1:
                instruction = {
                    "action": "BusReply",
                    "src": -1,
                    "dst": processorID,
                    "value": self.memoryValue
                }

                self.processors[processorID].setValue(self.memoryValue)
                self.instructions.append(instruction)

            else:
                instruction = {
                    "action": "BusReply",
                    "src": index,
                    "dst": processorID,
                    "value": self.processors[processorID].getValue()
                }

                self.processors[processorID].setValue(self.processors[processorID].getValue())
                self.instructions.append(instruction)


        #self.clearInstructions()

    
