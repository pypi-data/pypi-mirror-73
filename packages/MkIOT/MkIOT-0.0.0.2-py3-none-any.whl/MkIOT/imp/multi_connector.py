from . import iot_device
import threading



class multi_outbound_connector(object):

    def __init__(self, on_connected_global=None, on_disconnected_global=None):
        self.on_connected_global = on_connected_global
        self.on_disconnected_global = on_disconnected_global
        self.outbound_connections = {}

    
    def connect_to_outbound_server(self, HOST, PORT, on_connected=None, on_disconnected=None):
        def disconnect():
            if on_disconnected is not None:
                threading.Thread(target=on_disconnected, daemon=True).start()
            if self.on_disconnected_global is not None:
                threading.Thread(target=on_disconnected, daemon=True).start()

        def connect():
            if on_connected is not None:
                threading.Thread(target=on_connected, daemon=True).start()
            if self.on_connected_global is not None:
                threading.Thread(target=self.on_connected_global, daemon=True).start()

        self.outbound_connections[HOST + ":" + str(PORT)] = iot_device.IOT_Device(HOST, PORT, connect, on_disconnect=disconnect)

        return self.outbound_connections[HOST + ":" + str(PORT)]