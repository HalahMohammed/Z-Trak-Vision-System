# modbus_interface.py
from modbus_worker_non_threads import ModbusWorkerSync
from config import *

class ModbusInterface:
    def __init__(self):
        self.worker = ModbusWorkerSync(
            host=MODBUS_HOST,
            read_address=MODBUS_READ_ADDRESS,
            write_address=MODBUS_WRITE_ADDRESS,
            read_count=MODBUS_READ_COUNT,
            write_count=MODBUS_WRITE_COUNT,
            mode="register"
        )
        self.connected = False
    
    def connect(self):
        """Establish connection to Modbus device"""
        try:
            self.worker.connect()
            self.connected = True
            print("Modbus connection established")
        except Exception as e:
            print(f"Modbus connection failed: {e}")
    
    def write_register(self, write_address, write_count, write_value):
        """Write to Modbus register"""
        if not self.connected:
            raise ConnectionError("Modbus not connected")
        
        self.worker.mode = "register"
        self.worker.write_addr = write_address
        self.worker.write_count = write_count
        return self.worker.write(write_value)
    
    def read_register(self, read_address, read_count):
        """Read from Modbus register"""
        if not self.connected:
            raise ConnectionError("Modbus not connected")
        
        self.worker.mode = "register"
        self.worker.read_addr = read_address
        self.worker.read_count = read_count
        return self.worker.read()
    
    def read_coil(self, read_coil, read_count):
        """Read from Modbus coil"""
        if not self.connected:
            raise ConnectionError("Modbus not connected")
        
        self.worker.mode = "coil"
        self.worker.read_addr = read_coil
        self.worker.read_count = read_count
        return self.worker.read()
