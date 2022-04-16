import constants

class Driver:
    def __init__(self, processors, memory):
        self.processors = processors
        self.memory = memory

        # Buffer for return values to be sent back to the front end
        self.buffer = []

        # Representation of what is on the bus
        self.bus = []

    def setInitialState(self):
        self.reset() # Clear everything back to default first

        for i in range (len(self.processors)):
            instruction = {
                "processor" : i,
                "value" : self.processors[i].getValue(),
                "state" : self.processors[i].getState(),
                "protocol" : self.processors[i].getProtocol()
            }

            self.buffer.append(instruction)

        instruction = {
            "processor" : constants.MEMORY_ID,
            "value" : self.memory.getValue()
        }

        self.buffer.append(instruction)

    # Load all possible actions into the buffer
    def loadValidActions(self):
        for i in range (len(self.processors)):
            self.processors[i].loadValidActions(self.buffer)

    def getQueues(self):
        retval = []

        for i in range (len(self.processors)):
           retval.append(self.processors[i].getQueue())

        retval.append(self.memory.getQueue())
        return retval

    def getBuffer(self):
        return self.buffer

    def clearBuffer(self):
        self.buffer = []

    def getBus(self):
        return self.bus

    def clearBus(self):
        self.bus = []

    def reset(self):
        for i in range (len(self.processors)):
            self.processors[i].reset()

        self.memory.reset()
        self.clearBus()
        self.clearBuffer()

    def processProcessorAction(self, message):
        processorID = message["processor"]
        self.processors[processorID].updateState(message, self.buffer, self.bus)

    def processQueueEvent(self, processorID):
        if processorID == constants.MEMORY_ID:
            # Empty queue so don't do anything
            if len(self.memory.getQueue()) == 0:
                return

            message = self.memory.getQueue()[0]
            msg_processed = self.memory.updateState(message, self.buffer, self.bus)

            # Event was succesfully processed and did not stall so remove from queue
            if msg_processed:
                self.memory.getQueue().pop(0)

        else:
            # Empty queue so don't do anything
            if len(self.processors[processorID].getQueue()) == 0:
                return

            message = self.processors[processorID].getQueue()[0]
            msg_processed = self.processors[processorID].updateState(message, self.buffer, self.bus)

            # Event was succesfully processed and did not stall so remove from queue
            if msg_processed:
                self.processors[processorID].getQueue().pop(0)

    def processBusEvent(self, busIndex):
        # Empty bus so don't do anything
        if len(self.bus) == 0:
            return

        message = self.bus[busIndex] 
        for i in range(len(self.processors)):
            self.processors[i].updateState(message, self.buffer, self.bus)

        self.memory.updateState(message, self.buffer, self.bus)

        self.bus.pop(busIndex) # Finished processing bus message so remove from bus
            
            
                

