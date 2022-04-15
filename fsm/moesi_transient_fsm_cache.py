import constants

class MOESI_Transient_FSM_Cache:
	def __init__(self, id, value, state):
		self.value = value
		self.state = state
		self.id = id
		self.protocol = "MOESI"
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

		elif (self.state == constants.STATE_S or self.state == constants.STATE_M or
			self.state == constants.STATE_O or self.state == constants.STATE_E):

			buffer.append({
				"processor" : self.id,
				"actions" : [constants.EVENT_LOAD, constants.EVENT_STORE, constants.EVENT_EVICT]
			})

	def unhandledEvent(self, event):
		assert f"Unhandled event {event} in state {self.state}"

	def unhandledState(self):
		assert f"Unhandled state {self.state}"

	def updateState(self, message, buffer, bus):  
		event = message["action"]

		###########
		# Invalid #
		###########
		if self.state == constants.STATE_I:
			if event == constants.EVENT_LOAD:
				self.state = constants.STATE_IS_AD

				instruction = {
					"action" : constants.EVENT_GET_S,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
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
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
				}
				bus.append(instruction)
				buffer.append(instruction)
				self.recordUpdate(None, buffer)

			else:
				self.unhandledEvent(event)
		#####################
		# Invalid to Shared #
		#####################
		elif self.state == constants.STATE_IS_AD:
			if event == constants.EVENT_GET_S:
				if message["src"] == self.id:
					self.state = constants.STATE_IS_D
					self.recordUpdate(None, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		elif self.state == constants.STATE_IS_D:
			if event == constants.EVENT_DATA:
				if message["target"] == self.id:
					if message["exclusive"] == 1:
						self.state = constants.STATE_E
					else:
						self.state = constants.STATE_S
					self.value = message["value"]
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		#######################
		# Invalid to Modified #
		#######################
		elif self.state == constants.STATE_IM_AD:
			if event == constants.EVENT_GET_M:
				if message["src"] == self.id:
					self.state = constants.STATE_IM_D
					self.recordUpdate(None, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		elif self.state == constants.STATE_IM_D:
			if event == constants.EVENT_DATA:
				if message["target"] == self.id:
					self.state = constants.STATE_M
					self.value = self.lastWrite
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		##########
		# Shared #
		##########
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
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
				}
				bus.append(instruction)
				buffer.append(instruction)
				self.recordUpdate(None, buffer)
			elif event == constants.EVENT_EVICT:
				instruction = {
					"action" : constants.EVENT_PUT_S,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
				}
				bus.append(instruction)
				buffer.append(instruction)
				self.state = constants.STATE_I
				self.value = constants.NULL_VALUE
				self.recordUpdate(self.value, buffer)
			elif event == constants.EVENT_GET_S:
				assert message["src"] != self.id
			elif event == constants.EVENT_GET_M:
				if message["src"] != self.id:
					self.state = constants.STATE_I
					self.value = constants.NULL_VALUE
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			elif event == constants.EVENT_PUT_M:
				assert message["src"] != self.id
			elif event == constants.EVENT_DATA:
				assert message["target"] != self.id
			else:
				self.unhandledEvent(event)
		######################
		# Shared to Modified #
		######################
		elif self.state == constants.STATE_SM_AD:
			if event == constants.EVENT_GET_M:
				if message["src"] == self.id:
					self.state = constants.STATE_SM_D
					self.recordUpdate(None, buffer)
				else:
					self.state = constants.STATE_IM_AD
					self.recordUpdate(None, buffer)
			else:
				self.unhandledEvent(event)
		
		elif self.state == constants.STATE_SM_D:
			if event == constants.EVENT_DATA:
				if message["target"] == self.id:
					self.state = constants.STATE_M
					self.value = self.lastWrite
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		############
		# Modified #
		############
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

			elif event == constants.EVENT_EVICT:
				self.state = constants.STATE_MI_A

				instruction = {
					"action" : constants.EVENT_PUT_M,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"value" : self.value,
					"target" : constants.MEMORY_ID
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.recordUpdate(None, buffer)
			
			elif event == constants.EVENT_GET_S:
				if message["src"] != self.id:
					instruction = {
						"action" : constants.EVENT_DATA,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"value" : self.value,
						"target" : message["src"],
						"exclusive" : 0
					}
					buffer.append(instruction)
					bus.append(instruction)

					instruction = {
						"action" : constants.EVENT_NO_DATA,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"target" : constants.MEMORY_ID
					}
					buffer.append(instruction)
					bus.append(instruction)

					self.state = constants.STATE_O
					self.recordUpdate(None, buffer)
				else:
					assert False

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
				else:
					assert False
			else:
				self.unhandledEvent(event)

		#######################
		# Modified to Invalid #
		#######################
		elif self.state == constants.STATE_MI_A:
			if event == constants.EVENT_PUT_M:
				if message["src"] == self.id:
					instruction = {
						"action" : constants.EVENT_DATA,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"value" : self.value,
						"target" : constants.MEMORY_ID
					}
					buffer.append(instruction)
					bus.append(instruction)

					self.state = constants.STATE_I
					self.value = constants.NULL_VALUE
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		#############
		# Exclusive #
		#############
		elif self.state == constants.STATE_E:
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
				self.state = constants.STATE_M
				self.value = message["value"]

				buffer.append(instruction)
				self.recordUpdate(self.value, buffer)

			elif event == constants.EVENT_EVICT:
				self.state = constants.STATE_EI_A

				instruction = {
					"action" : constants.EVENT_PUT_M,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"value" : self.value,
					"target" : constants.MEMORY_ID
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
					instruction = {
						"action" : constants.EVENT_NO_DATA_E,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"value" : self.value,
						"exclusive" : 0,
						"target" : constants.MEMORY_ID
					}
					buffer.append(instruction)
					bus.append(instruction)
					self.recordUpdate(None, buffer)
				else:
					assert False
			elif event == constants.EVENT_GET_M:
				if message["src"] != self.id:
					self.state = constants.STATE_I

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
					self.value = constants.NULL_VALUE
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		########################
		# Exclusive to Invalid #
		########################
		elif self.state == constants.STATE_EI_A:
			if event == constants.EVENT_PUT_M:
				assert message["src"] == self.id
				instruction = {
					"action" : constants.EVENT_NO_DATA_E,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.value = constants.NULL_VALUE
				self.state = constants.STATE_I
				self.recordUpdate(self.value, buffer)
		#########
		# Owned #
		#########
		elif self.state == constants.STATE_O:
			if event == constants.EVENT_LOAD:
				instruction = {
					"action" : constants.EVENT_HIT,
					"target" : self.id
				}
				buffer.append(instruction)
			elif event == constants.EVENT_STORE:
				self.state = constants.STATE_OM_A
				self.lastWrite = message["value"]

				instruction = {
					"action" : constants.EVENT_GET_M,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"target" : constants.MEMORY_ID
				}
				bus.append(instruction)
				buffer.append(instruction)
				self.value = self.lastWrite
				self.recordUpdate(self.lastWrite, buffer)
			elif event == constants.EVENT_EVICT:
				self.state = constants.STATE_OI_A

				instruction = {
					"action" : constants.EVENT_PUT_M,
					"src" : self.id,
					"dst" : constants.BUS_ID,
					"value" : self.value,
					"target" : constants.MEMORY_ID
				}
				buffer.append(instruction)
				bus.append(instruction)
				self.recordUpdate(None, buffer)
			elif event == constants.EVENT_GET_S:
				if message["src"] != self.id:
					instruction = {
						"action" : constants.EVENT_DATA,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"value" : self.value,
						"target" : message["src"],
						"exclusive" : 0
					}
					buffer.append(instruction)
					bus.append(instruction)

					self.recordUpdate(None, buffer)
				else:
					assert False
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
				else:
					assert False
			elif event == constants.EVENT_DATA:
				assert message["target"] != self.id
			else:
				self.unhandledEvent(event)

		#####################
		# Owned to Modified #
		#####################
		elif self.state == constants.STATE_OM_A:
			if event == constants.EVENT_GET_M:
				if message["src"] == self.id:
					self.state = constants.STATE_M
					self.recordUpdate(None, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)

		####################
		# Owned to Invalid #
		####################
		elif self.state == constants.STATE_OI_A:
			if event == constants.EVENT_PUT_M:
				if message["src"] == self.id:
					instruction = {
						"action" : constants.EVENT_DATA,
						"src" : self.id,
						"dst" : constants.BUS_ID,
						"value" : self.value,
						"target" : constants.MEMORY_ID
					}
					buffer.append(instruction)
					bus.append(instruction)

					self.state = constants.STATE_I
					self.value = constants.NULL_VALUE
					self.recordUpdate(self.value, buffer)
				else:
					assert False
			else:
				self.unhandledEvent(event)
		else:
			self.unhandledState()
