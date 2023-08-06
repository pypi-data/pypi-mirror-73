"""Python connectivity for Itasca software.

This library implements a connection via sockets between Python and
the numerical modeling software from Itasca Consulting Group.

itascacg.com/software

FLAC, FLAC3D, PFC2D, PFC3D, UDEC & 3DEC"""

from __future__ import print_function
import json
import struct
import socket
import select
import time
import subprocess
import os
import numpy as np

class _ItascaFishSocketServer(object):
    """Low level details of the Itasca FISH socket communication"""
    def __init__(self, fish_socket_id=0):
        assert type(fish_socket_id) is int and 0 <= fish_socket_id < 6
        self.port = 3333 + fish_socket_id

    def start(self):
        """() -> None.
        Open the low level socket connection. Blocks but allows the Python thread
        scheduler to run.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", self.port))
        self.socket.listen(1)
        while True:
            connected, _, _ = select.select([self.socket], [], [], 0.0)
            if connected: break
            else: time.sleep(1e-8)
        self.conn, addr = self.socket.accept()
        print('socket connection established by', addr)

    def send_data(self, value):
        """(value: any) -> None.
        Send value to Itasca software. value must be int, float, length two list 
        of doubles, length three list of doubles or a string.
        """
        while True:
            _, write_ready, _ = select.select([], [self.conn], [], 0.0)
            if write_ready: break
            else: time.sleep(1e-8)

        if type(value) == int:
            self.conn.sendall(struct.pack("i", 1))
            self.conn.sendall(struct.pack("i", value))

        elif type(value) == float:
            self.conn.sendall(struct.pack("i", 2))
            self.conn.sendall(struct.pack("d", value))

        elif type(value) == list and len(value)==2:
            float_list = [float(x) for x in value]
            self.conn.sendall(struct.pack("i", 5))
            self.conn.sendall(struct.pack("dd", float_list[0], float_list[1]))

        elif type(value) == list and len(value)==3:
            float_list = [float(x) for x in value]
            self.conn.sendall(struct.pack("i", 6))
            self.conn.sendall(struct.pack("ddd", float_list[0],
                                          float_list[1], float_list[2]))
        elif type(value) == str:
            length = len(value)
            self.conn.sendall(struct.pack("ii", 3, length))
            buffer_length = 4*(1+(length-1)/4) # this may be the wrong buffer length?
            format_string = "%is" % buffer_length
            value += " "*int(buffer_length - length)
            self.conn.sendall(struct.pack(format_string, value.encode('utf-8')))
        else:
            raise Exception("unknown type in send_data")

    def wait_for_data(self):
        """() -> None.
        Block until data is available. This call allows the Python thread scheduler 
        to run.
        """
        while True:
            input_ready, _, _ = select.select([self.conn],[],[], 0.0)
            if input_ready: return
            else: time.sleep(1e-8)

    def read_type(self, type_string):
        """(type: str) -> any.
        This method should not be called directly. Use the read_data method.
        """
        byte_count = struct.calcsize(type_string)
        bytes_read = 0
        data = b''
        self.wait_for_data()
        while bytes_read < byte_count:
            data_in = self.conn.recv(byte_count - bytes_read)
            data += data_in
            bytes_read += len(data)
        assert len(data)==byte_count, "bad packet data"
        return data

    def read_data(self):
        """() -> any.
        Read the next item from the socket connection.
        """
        raw_data = self.read_type("i")
        type_code, = struct.unpack("i", raw_data)
        if type_code == 1:     # int
            raw_data = self.read_type("i")
            value, = struct.unpack("i", raw_data)
            return value

        elif type_code == 2:   # float
            raw_data = self.read_type("d")
            value, = struct.unpack("d", raw_data)
            return value

        elif type_code == 3:   # string
            length_data = self.read_type("i")
            length, = struct.unpack("i", length_data)
            buffer_length = length + ((4 * (1 + length // 4) - length) % 4)
            format_string = "%is" % buffer_length
            data = self.read_type(format_string)
            return data[:length].decode("utf-8")

        elif type_code == 5:   # V2
            raw_data = self.read_type("dd")
            value0, value1 = struct.unpack("dd", raw_data)
            return [value0, value1]

        elif type_code == 6:   # V3
            raw_data = self.read_type("ddd")
            value0, value1, value3 = struct.unpack("ddd", raw_data)
            return [value0, value1, value3]

        assert False, "Data read type error"

    def get_handshake(self):
        """() -> int.
        Read the handshake packet from the socket.
        """

        raw_data = self.read_type("i")
        value, = struct.unpack("i", raw_data)
        print("handshake got: ", value)
        return value

    def close(self):
        """() -> None.
        Close the active socket connection.
        """
        self.conn.close()


class _ItascaSoftwareConnection(object):
    """Base class for communicating via FISH sockets with an Itasca program. This
    class spawns a new instance of the Itasca software and initializes the socket
    communication.
    """

    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        self.executable_name = None
        self.server = _ItascaFishSocketServer(fish_socket_id)
        self.iteration = 0
        self.global_time = 0
        self.fishcode = 178278912

    def start(self, datafile_name):
        """(datafile_name: str) -> None.
        Launch Itasca software in a separate process, open the specified data file.
        The green execute button must be pressed in the Itasca software to start
        the calculation.
        """
        if os.access(datafile_name, os.R_OK):
            args = f'"{self.executable_name}" call {datafile_name}'
            self.process = subprocess.Popen(args)

        else:
            raise ValueError("The file {} is not readable".format(datafile_name))

    def connect(self):
        """() -> None.
        Connect to Itasca software, read fishcode to confirm connection. Call
        this function to establish the socket connection after calling the start
        method to launch the code.
        """
        assert self.process
        self.server.start()
        value = self.server.get_handshake()
        print("got handshake packet")
        assert value == self.fishcode
        print("connection OK")

    def send(self, data):
        """(data: any) -> None.
        Send an item to the Itasca code.
        """
        self.server.send_data(data)

    def receive(self):
        """() -> any.
        Read an item from the Itasca code.
        """
        return self.server.read_data()

    def end(self):
        """() -> None.
        Close the socket connection.
        """
        self.server.close()

    def shutdown(self):
        """()-> None.
        Shutdown running softwarecode.
        """
        self.process.kill()

class FLAC3D_Connection(_ItascaSoftwareConnection):
    """Launch and connect to FLAC3D."""
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\FLAC3D700\\exe64\\flac3d700_gui.exe"

class PFC3D_Connection(_ItascaSoftwareConnection):
    """Launch and connect to PFC3D."""
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\PFC600\\exe64\\pfc3d600_gui.exe"

class PFC2D_Connection(_ItascaSoftwareConnection):
    """Launch and connect to PFC2D."""
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\PFC600\\exe64\\pfc2d600_gui.exe"


class FLAC_Connection(_ItascaSoftwareConnection):
    """Launch and connect to FLAC. """
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\FLAC800\\exe64\\flac800_64.exe"

    def connect(self):
        """() -> None.
        Call this function to connect to FLAC once it has been started manually.
        """
        self.process=True
        _ItascaSoftwareConnection.connect(self)

class UDEC_Connection(_ItascaSoftwareConnection):
    """Launch and connect to UDEC. """
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\UDEC700\\Exe64\\udec700_gui.exe"

    def connect(self):
        """() -> None.
        Call this function to connect to UDEC once it has been started manually.
        """
        self.process=True
        _ItascaSoftwareConnection.connect(self)

class ThreeDEC_Connection(_ItascaSoftwareConnection):
    """Launch and connect to 3DEC."""
    def __init__(self, fish_socket_id=0):
        """(fish_socket_id=0: int) -> Instance. Constructor."""
        _ItascaSoftwareConnection.__init__(self, fish_socket_id)
        self.executable_name = "C:\\Program Files\\Itasca\\3DEC520\\exe64\\3dec_dp520_gui_64.exe"


class FishBinaryReader(object):
    """Read structured FISH binary files.
    Call the constructor with the structured FISH filename and call
    read() to read individual values. This class also supports
    iteration. Return values are converted to python types. Supports
    int, float, string, bool, v2 and v3.

    >>> fish_file = FishBinaryReader('my_fish_data.fish')
    >>> for val in fish_file:
    ...    print val
    42
    "this is a string"
    [1.0,2.0,3.0]
    """
    def __init__(self, filename):
        """(filename: str) -> FishBinaryReader object. """
        self.file = open(filename, "rb")
        fishcode = self._read_int()
        assert fishcode == 178278912, "invalid FISH binary file"

    def _read_int(self):
        data = self.file.read(struct.calcsize('i'))
        value, = struct.unpack("i", data)
        return value

    def _read_double(self):
        data = self.file.read(struct.calcsize('d'))
        value, = struct.unpack("d", data)
        return value

    def read(self):
        """() -> any.
        Read and return a value (converted to a Python type) from the .fish
        binary file.
        """
        type_code = self._read_int()

        if type_code == 1:  # int
            return self._read_int()

        if type_code == 8:  # bool
            value = self._read_int()
            return_value = True if value else False
            return return_value

        if type_code == 2:  # float
            return self._read_double()

        if type_code == 3:
            length = self._read_int()
            buffer_length = 4*(1+(length-1)/4) # this may be wrong
            format_string = "%is" % buffer_length
            data = self.file.read(struct.calcsize(format_string))
            return data[:length].decode("utf-8")

        if type_code == 5:  # v2
            return [self._read_double(), self._read_double()]

        if type_code == 6:  # v3
            return [self._read_double(), self._read_double(),
                    self._read_double()]

    def __iter__(self):
        self.file.seek(0)  # return to the begining of the file
        self._read_int()   # pop the magic number off
        return self

    def __next__(self):
        """() -> any.
        Get the next item from the FISH binary file.
        """
        try:
            return self.read()
        except:
            raise StopIteration

    next = __next__  # alias for Python 2 support.

    def aslist(self):
        """() -> [any].
        Return fish file contents as a Python list.
        """
        return [x for x in self]

    def asarray(self):
        """() -> numpy array.
        Return fish file contents as a numpy array. Types must be homogeneous.
        """
        return np.array(self.aslist())

class UDECFishBinaryReader(FishBinaryReader):
    "Special version of FishBinarReader for files generated by UDEC."
    def _read_int(self):
        data = self.file.read(struct.calcsize('i'))
        value, = struct.unpack("i", data)
        data = self.file.read(struct.calcsize('i')) # read the dummy data off
        return value

class FishBinaryWriter(object):
    """Write fish binary data. data can be any iterable (array, list, etc.).
    example: FishBinaryWriter("t.fis", [12.23, 1, 33.0203, 1234.4])
    """
    def __init__(self, filename, data):
        """(filename: str, data: iterable) -> FishBinaryWriter instance."""
        with open(filename, "wb") as f:
            self._write_int(f,178278912)
            for datum in data:
                if type(datum) is float:
                    self._write_int(f, 2)
                    self._write_double(f, datum)
                elif type(datum) is int:
                    self._write_int(f, 1)
                    self._write_int(f, datum)
                else:
                    raise TypeError(
                        "Currently unsupported type for Fish binary write ")

    def _write_int(self, f, datum):
        f.write(struct.pack("i", datum))

    def _write_double(self, f, datum):
        f.write(struct.pack("d", datum))

class UDECFishBinaryWriter(FishBinaryWriter):
    """Fish Binary writer for UDEC (which has 8 byte ints)"""
    def _write_int(self, f, datum):
        f.write(struct.pack("i", datum))
        f.write(struct.pack("i", 0))

######################################################################
# p2pLink below here
######################################################################

class _fileSocketAdapter(object):
    """This object is an adapter which allows np.save and np.load to write 
    directly to the socket. This object appears to be a file object but does
    reading and writing over a socket connection.
    """
    def __init__(self, s):
        """(s: _baseSocket) -> None.
        Constructor.
        """
        self.s=s
        self.first = True
        self.offset = 0

    def write(self, data):
        """(data: str) -> None.
        Write bytes to stream.
        """
        self.s._sendall(data)

    def read(self, byte_count):
        """(byte_count: int) -> str.
        Read bytes from stream.
        """
        bytes_read = 0
        data = b''
        # this is a hack because we have to support seek for np.load
        if self.offset:
            assert self.offset <= byte_count
            assert self.offset==6
            assert not self.first
            data += self.buff
            bytes_read += self.offset
            self.offset = 0

        while bytes_read < byte_count:
            self.s.wait_for_data()
            data_in = self.s.conn.recv(min(4096, byte_count-bytes_read))
            data = b"".join([data, data_in])
            bytes_read += len(data_in)

        # this is a hack because we have to support seek for np.load
        if self.first and byte_count==6:
            self.buff = data
            self.first = False
        return data

    def readline(self):
        """() -> str.
        Read a line from the stream."""
        data=''
        while True:
            self.s.wait_for_data()
            byte = self.s.conn.recv(1)
            if byte == '\n':
                return data
            else:
                data += byte
        return data

    def seek(self, a0, a1):
        """(offset: int, mode: int) -> None.
        This is a hack to support np.load and np.save talking over sockets.
        """
        assert a1 == 1
        assert a0 == -6
        assert len(self.buff)==6
        self.offset = 6

class _socketBase(object):
    code = 12345

    def _sendall(self, data):
        """(bytes: str) -> None.
        Low level socket send, do not call this function directly.
        """
        nbytes = len(data)
        sent = 0
        while sent < nbytes:
            self._wait_for_write()
            sent += self.conn.send(data[sent:])

    def _wait_for_write(self):
        """() -> None.
        Block until socket is write ready but let thread scheduler run.
        """
        while True:
            _, write_ready, _ = select.select([], [self.conn], [], 0.0)
            if write_ready: break
            else: time.sleep(1e-8)

    def send_data(self, value):
        """(value: any) -> None.
        Send value. value must be a number, a string or a NumPy array.
        """
        if type(value) == int:
            self._sendall(struct.pack("i", 1))
            self._sendall(struct.pack("i", value))

        elif type(value) == float:
            self._sendall(struct.pack("i", 2))
            self._sendall(struct.pack("d", value))

        elif type(value) == list and len(value)==2:
            float_list = [float(x) for x in value]
            self._sendall(struct.pack("i", 5))
            self._sendall(struct.pack("dd", float_list[0], float_list[1]))

        elif type(value) == list and len(value)==3:
            float_list = [float(x) for x in value]
            self._sendall(struct.pack("i", 6))
            self._sendall(struct.pack("ddd", float_list[0],
                                          float_list[1], float_list[2]))

        elif type(value) == str:
            length = len(value)
            self._sendall(struct.pack("ii", 3, length))
            buffer_length = 4*(1+(length-1)/4)
            format_string = "%is" % buffer_length
            value += " "*int(buffer_length - length)
            self._sendall(struct.pack(format_string, value.encode("utf-8")))

        elif type(value) == np.ndarray:
            self._sendall(struct.pack("i", 7))
            np.save(_fileSocketAdapter(self), value)

        elif type(value) == dict:
            length = len(value)
            data = json.dumps(value).encode("utf-8")
            self._sendall(struct.pack("ii", 8, len(data)))
            self._sendall(data)

        else:
            raise Exception("unknown type in send_data")

    def wait_for_data(self):
        """() -> None.
        Block until data is available. This call allows the Python thread
        scheduler to run.
        """
        while True:
            input_ready, _, _ = select.select([self.conn],[],[], 0.0)
            if input_ready: return
            else: time.sleep(1e-8)

    def read_type(self, type_string, array_bytes=None):
        """(type: str) -> any.
        This method should not be called directly. Use the read_data method.
        """
        if array_bytes is None:
            byte_count = struct.calcsize(type_string)

        else:
            byte_count = array_bytes

        bytes_read = 0
        data = b''
        while bytes_read < byte_count:
            self.wait_for_data()
            data_in = self.conn.recv(min(4096,byte_count - bytes_read))
            data = b"".join([data, data_in])
            bytes_read += len(data_in)
        assert len(data)==byte_count, "bad packet data"
        return data

    def read_data(self):
        """() -> any.
        Read the next item from the socket connection.
        """
        raw_data = self.read_type("i")
        type_code, = struct.unpack("i", raw_data)

        if type_code == 1:     # int
            raw_data = self.read_type("i")
            value, = struct.unpack("i", raw_data)
            return value

        elif type_code == 2:   # float
            raw_data = self.read_type("d")
            value, = struct.unpack("d", raw_data)
            return value

        elif type_code == 3:   # string
            length_data = self.read_type("i")
            length, = struct.unpack("i", length_data)
            buffer_length = (4*(1+(length-1)/4))
            format_string = "%is" % buffer_length
            data = self.read_type(format_string)
            return data[:length].decode("utf-8")

        elif type_code == 5:   # V2
            raw_data = self.read_type("dd")
            value0, value1 = struct.unpack("dd", raw_data)
            return [value0, value1]

        elif type_code == 6:   # V3
            raw_data = self.read_type("ddd")
            value0, value1, value3 = struct.unpack("ddd", raw_data)
            return [value0, value1, value3]

        elif type_code == 7:  # NumPy array:
            a = np.load(_fileSocketAdapter(self))
            return a

        elif type_code == 8: # python dict
            raw_data = self.read_type("i")
            length, = struct.unpack("i", raw_data)
            data = self.read_type(None, length)
            return json.loads(data)

        assert False, "Data read type error"

    def close(self):
        """() -> None.
        Close the active socket connection.
        """
        if hasattr(self, "conn"):
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()

        else:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, eType, eValue, eTrace):
        print("cleaning up socket")
        self.close()

class p2pLinkServer(_socketBase):
    """Python to Python socket link server. Send and receive numbers, strings
    and NumPy arrays between Python instances."""
    def __init__(self, port=5000):
        """(port=5000) -> None. Create a Python to Python socket server. Call
        the start() method to open the connection."""
        assert type(port) is int
        self.port = port

    def start(self):
        """() -> None. Open the socket connection. Blocks but allows the
        Python thread scheduler to run.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", self.port))
        self.socket.listen(1)

        while True:
            connected, _, _ = select.select([self.socket], [], [], 0.0)
            if connected:
                break

            else:
                time.sleep(1e-8)

        self.conn, addr = self.socket.accept()
        assert self.read_data() == _socketBase.code
        print("got code")

class p2pLinkClient(_socketBase):
    """Python to Python socket link client. Send and receive numbers, strings
    and NumPy arrays between Python instances."""
    def __init__(self,port=5000):
        """(port=5000) -> None. Create a Python to Python socket link client.
        Call the start() method to open the connection.""
        """
        assert type(port) is int
        self.port = port
    def connect(self, machine):
        """(machine: str) -> None. Connect to a Python to Python link server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((machine,self.port))
        self.conn = self.socket
        self.send_data(_socketBase.code)
        print("sent code")
