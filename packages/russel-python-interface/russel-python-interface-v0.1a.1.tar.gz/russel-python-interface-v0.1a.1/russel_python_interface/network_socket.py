import json
import socket
import struct
import time

timeout: int = 2


class Socket:
    sock: socket.socket = None
    running_receive: bool = True
    last_time: int = time.time()
    running: bool = True

    def __del__(self):
        self.running = False

    @staticmethod
    def create_ipc(ipc_socket_path: str) -> "Socket":
        this_socket: Socket = Socket()
        this_socket.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        this_socket.sock.connect(ipc_socket_path)
        # start_new_thread(this_socket.kill_thread, ())
        return this_socket

    @staticmethod
    def create_network(host: str, port: int) -> "Socket":
        this_socket: Socket = Socket()
        this_socket.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this_socket.sock.connect((host, port))
        # start_new_thread(this_socket.kill_thread, ())
        return this_socket

    @staticmethod
    def create_from_uri(uri: str) -> "Socket":
        this_socket: Socket = Socket()
        this_socket.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host: str = uri.split(":")[0]
        port: int = int(uri.split(":")[1])
        this_socket.sock.connect((host, port))
        return this_socket

    def close(self) -> None:
        self.send_string(json.dumps({"command": "close"}))
        self.sock.close()

    def send_byte(self, message: bytes) -> None:
        try:
            self.sock.sendall(self.__encode_uint32(len(message) + 4) + message)
        except:
            raise FileNotFoundError("IPC socket form daemon not found. Is the daemon running")

    def send_string(self, message: str) -> None:
        try:
            self.send_byte(message.encode())
        except socket.error as _:
            raise FileNotFoundError("IPC socket from daemon not found. Is the daemon running ?")

    def send_json(self, message: dict) -> None:
        try:
            self.send_byte(json.dumps(message).encode())
        except Exception as e:
            raise e

    def receive(self) -> json:
        data = bytearray()
        n: int = 4
        header_size: bool = False

        while len(data) < n:
            package = self.sock.recv(n - len(data))
            if not package:
                break
            else:
                if not header_size:
                    n: int = self.__decode_uint32(package[0:4]) - 4
                    header_size = True
                else:
                    data.extend(package)
        try:
            my_json = data.decode("ascii").replace("'", '"').replace("\x00", "")
            return json.loads(my_json)
        except Exception as e:
            return {}

    def kill_thread(self):
        while self.running:
            while self.running and time.time() - self.last_time > timeout:
                time.sleep(0.5)

            self.running_receive = False
            time.sleep(1)

    @staticmethod
    def __encode_uint32(num: int) -> bytes:
        return struct.pack("I", num)

    @staticmethod
    def __decode_uint32(num: bytes) -> int:
        try:
            return struct.unpack("I", num)[0]
        except Exception as e:
            return 0
