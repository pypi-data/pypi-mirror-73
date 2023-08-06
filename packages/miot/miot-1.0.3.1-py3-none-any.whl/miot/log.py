# CENTRALISED LOGGING
# (c) Copyright Si Dunford, Jun 2020

LOG_NAME = "miot"
LOG_FILE = "miot.log"

LOG_LEVEL = logging.DEBUG   # USE THIS DURING DEVELOPMENT
#LOG_LEVEL = logging.INFO   # USE THIS AFTER PUBLICATION

import logging

log       = logging.getLogger( LOG_NAME )
handler   = logging.FileHandler( LOG_FILE )
formatter = logging.Formatter( '%(asctime)s %(levelname)s %(message)s' )

handler.setFormatter( formatter )
log.setLevel( LOG_LEVEL )        
log.addHandler( handler )

log.debug("========================================")
log.debug("Initialised MIoT logs")


    
    
