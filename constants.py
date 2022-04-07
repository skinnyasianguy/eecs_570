import sys

DEFAUT_VALUE = 100
NULL_VALUE = sys.maxsize

# Constants for ID
MEMORY_ID = -1
BUS_ID = -2

# Constants for Events
EVENT_GET_S = "GetS"
EVENT_GET_M = "GetM"
EVENT_DATA = "Data"
EVENT_UPDATE = "Update"
EVENT_PUT_M = "PutM"
EVENT_LOAD = "Load"
EVENT_STORE = "Store"
EVENT_EVICT = "Evict"

# Constants for Cache Controller States
STATE_I = "I"
STATE_IS_D = "IS_D"
STATE_IM_D = "IM_D"
STATE_S = "S"
STATE_SM_D = "SM_D"
STATE_M = "M"
STATE_IS_AD = "IS_AD"
STATE_IM_AD = "IM_AD"
STATE_IS_A = "IS_A"
STATE_IM_A = "IM_A"
STATE_SM_AD = "SM_AD"
STATE_SM_A = "SM_A"
STATE_MI_A = "MI_A"
STATE_II_A = "II_A"
STATE_E = "E"
STATE_EI_A = "EI_A"

# Constants for Memory Controller States
STATE_I_OR_S = "IorS"
STATE_I_OR_S_D = "IorS_D"
STATE_I_OR_S_A = "IorS_A"
STATE_M = "M"
