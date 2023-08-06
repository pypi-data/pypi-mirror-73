# Modular Internet of Things, Core functionality
#
# FILE:     mqtt.py
# AUTHOR:   (c) Copyright Si.Dunford, 2019
# VERSION:  19.03.26.1751
# DATE:     26 March 2019
# STATE:    BETA
# LICENSE:  MIT License
#
# CHANGE LOG:
# 15 MAR 2019  0.0.1  Initial build
# 25 MAR 2019  0.1.1  Revised event handlers
# 26 MAR 2019  0.1.2  Bug fixes / Removed some debug output
#              0.1.3  Added config.getfloat(), config.set() and config.write()
# 27 MAR 2019  0.2.1  New version control, move from sandbox to miot
# 05 JUL 2020  0.3.1  Revision 3

# THIRD PARTY MODULES
import paho.mqtt.client as paho_mqtt


# Default connect method
def mqtt_connect( client, userdata, flags, rc ):
    print "Connected"
    if rc==0:    # Connected successfully
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        print "Listening on", userdata.topic
        client.subscribe( userdata.topic )
    else:
        print("Connection refused: Result code "+str(rc))
        if rc==1:
            print "  Incorrect protocol version"
        elif rc==2:
            print "  Invalid client identifier"
        elif rc==3:
            print "  Server unavailable"
        elif rc==4:
            print "  Bad username or password"
        elif rc==5:
            print "  Not authorised"
        else:
            print "Result code",rc



# WRAPPER FOR PAHO MQTT
class MQTT:

    def __init__( self, config ):
        self.broker = config.get( 'MQTT','broker','127.0.0.1' )
        self.port = config.getint( 'MQTT','port',1883 )
        self.username = config.get( 'MQTT','username','' )
        self.password = config.get( 'MQTT','password','' )
        self.clientid = '' # Use random client ID
        self.topic = "miot"
        self.on_connect = mqtt_connect
        self.on_disconnect = None
        self.on_message = None
        self.on_publish = None
        self.on_subscribe = None

    def forever( self, topic='', message_handler=None ):
        # Process arguments
        if not topic=='':
            self.topic = topic
        if not message_handler==None:
            self.on_message=message_handler

        # Create MQTT object with optional authentication
        self.mqtt = paho_mqtt.Client( self.clientid )
        if not self.username=='':
            print 'Using Authentication...'
            self.mqtt.username_pw_set(username=self.username,password=self.password)

        # Set userdata to self
        self.mqtt.user_data_set(self)

        # Assign event handlers
        if not self.on_connect==None:
            self.mqtt.on_connect=self.on_connect
        if not self.on_disconnect==None:
            self.mqtt.on_disconnect=self.on_disconnect
        if not self.on_message==None:
            self.mqtt.on_message=self.on_message
        if not self.on_publish==None:
            self.mqtt.on_publish=self.on_publish
        if not self.on_subscribe==None:
            self.mqtt.on_subscribe=self.on_subscribe

        # Connect to MQTT broker
        self.mqtt.connect( self.broker, self.port )
        self.mqtt.loop_forever()


# CONFIG FILE
CONFIGFILE = 'config.ini'
#os.path.join( 'etc','opt','miot','config.ini' )
config = Config( CONFIGFILE )

# MQTT
mqtt = MQTT( config )


