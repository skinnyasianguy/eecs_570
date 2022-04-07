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
EVENT_NO_DATA = "NoData"
EVENT_NO_DATA_E = "NoDataE"

# Constants for Cache Controller States
STATE_I = "I"
STATE_IS_D = "IS_D"
STATE_IM_D = "IM_D"
STATE_S = "S"
STATE_SM_D = "SM_D"
STATE_M = "M"


# Constants for Memory Controller States
STATE_I_OR_S = "IorS"
STATE_I_OR_S_D = "IorS_D"
STATE_M = "M"
STATE_E_OR_M = "EorM"
STATE_I_D = "I_D"
STATE_S_D = "S_D"
STATE_E_OR_M_D = "EorM_D"
STATE_E_OR_M = "EorM"