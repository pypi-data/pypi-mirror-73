import time
from _thread import start_new_thread
from typing import List, Dict
from uuid import uuid4

import russel_python_interface.static_vars
from russel_python_interface.basic_routines import StandardRoutine, MatrixScalarProd, MatrixVectorMulti, MatrixSum
from russel_python_interface.benchmark import BenchmarkData
from russel_python_interface.network_socket import Socket
from russel_python_interface.routine import Routine
from russel_python_interface.task import Task
from russel_python_interface.task_sets import TaskSet, TaskSetTask


class Engine:
    unix_path: str = ""
    host: str = ""
    port: int = 0
    local: bool = True
    running: bool = False

    socket: Socket = None

    result_set: Dict[int, Task] = {}
    pending_unassigned_task: Dict[str, Task] = {}

    returned_requests: Dict[str, dict] = {}
    waiting_tokens: List[str] = []  # Messages with tokens that are not contained in this list will be deleted

    task_respond_func = None
    delete_from_set = None

    engine_id: str = ""

    benchmark: bool = False
    benchmark_data: BenchmarkData = None

    @staticmethod
    def create_connect_to_local(unix_path: str = "/etc/russel/russel.sock", benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.socket = Socket.create_ipc(unix_path)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    @staticmethod
    def create_connect_to_network(host: str = "127.0.0.1", port: int = 8321, benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.socket = Socket.create_network(host, port)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    @staticmethod
    def create_from_uri(uri: str, benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.socket = Socket.create_from_uri(uri)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    def upload_all_local_routines(self):
        self.upload_routine(MatrixScalarProd)
        self.upload_routine(MatrixSum)
        self.upload_routine(MatrixVectorMulti)

    def start(self):
        if not self.running:
            start_new_thread(self.receiving_loop, ())
            self.running = True

    def kill(self):
        self.running = False
        self.socket.close()

    def force_schedule(self):
        data: dict = {"id": russel_python_interface.static_vars.work_scheduler_id, "command": "api", "data": {}}
        data["data"]["command"] = "force_schedule"

        self.socket.send_json(data)

    def run_task(
            self, name: str, data: List[float], required_vars: List[int]
    ) -> str:  # TOOD: later than also numpy stuff
        task: Task = Task.create_from_file(name, data)
        task.required_vars = required_vars
        return self.run_prepared_task(task)

    def run_template_task(self, template: StandardRoutine, data: List[float]) -> str:
        task: Task = Task.create_from_template(template, data)
        task.required_vars = template.return_vars
        return self.run_prepared_task(task)

    def run_prepared_task(self, task: Task) -> str:
        data: dict = {
            "id": russel_python_interface.static_vars.work_scheduler_id,
            "command": "api",
            "data": task.serialize(self.engine_id),
            "token": str(uuid4()),
        }
        if type(task) is Task:
            data["data"]["command"] = "register_new_task"
        elif type(task) is TaskSetTask:
            data["data"]["command"] = "task_from_set"

        self.pending_unassigned_task[data["token"]] = task
        self.socket.send_json(data)

        return data["token"]

    def upload_routine(self, template: StandardRoutine):
        data: dict = {
            "command": "api",
            "id": russel_python_interface.static_vars.routine_manager_id,
            "data": Routine.create_from_template(template).serialize(),
            "token": str(uuid4()),
        }
        data["data"]["command"] = "save_and_add"

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track(data["token"], False)

        self.socket.send_json(data)

    def task_done(self, token: str) -> bool:
        return self.pending_unassigned_task[token].solved

    def resend_task(self, token: str) -> None:
        self.run_prepared_task(self.pending_unassigned_task[token])

    def make_request(self, data: dict, wait: bool = False) -> str:
        uuid: str = str(uuid4())
        data["token"] = uuid

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track(data["token"], False)

        self.socket.send_json(data)

        if wait:
            timeout: int = int(time.time())

            # Waits 10 Seconds than returns maybe throw a exception
            while uuid not in self.returned_requests.keys() and time.time() - timeout < 10:
                time.sleep(0.05)

        return uuid

    def get_task(self, token: str) -> Task:
        return self.pending_unassigned_task[token]

    def get_request(self, token: str) -> dict:
        if token in self.returned_requests:
            data: dict = self.returned_requests[token]
            del self.returned_requests[token]
            return data

    def receiving_loop(self):
        while self.running:
            message: dict = self.socket.receive()

            if message is None:
                continue

            if "token" in message.keys() and message["token"] in self.waiting_tokens:
                self.returned_requests[message["token"]] = message

                if self.benchmark:
                    self.benchmark_data.track(message["token"], False)

                self.waiting_tokens.remove(message["token"])

            if "command" in message and message["command"] == "task_return":
                task: Task = self.pending_unassigned_task[message["token"]]
                token: str = message["token"]

                del message["command"]
                del message["token"]
                for key in message.keys():  # Sets data so it can be accessed
                    task.encode_data(int(key), message[key])

                task.set_done()

                if self.benchmark:
                    self.benchmark_data.track(token, True)

                if self.task_respond_func is not None:
                    self.task_respond_func(token, task)
                if self.delete_from_set is not None:
                    if token in self.delete_from_set:
                        del self.delete_from_set[token]

            if "command" in message and message["command"] == "task_return_error":
                raise RuntimeError("Routine Failed")

    def set_task_handler(self, task_handler):
        self.task_respond_func = task_handler

    def register_task_set(self, task_set: TaskSet):
        token: str = str(uuid4())

        data: dict = {
            "id": russel_python_interface.static_vars.work_scheduler_id,
            "command": "api",
            "token": token,
            "data": task_set.serialize(),
        }

        data["data"]["command"] = "create_task_set"
        self.waiting_tokens.append(token)

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track(data["token"], False)

        self.socket.send_json(data)

        while token not in self.returned_requests.keys():
            print("Waiting for return id")
            time.sleep(0.05)
        print(self.returned_requests)
        return_data: dict = self.get_request(token)
        print(return_data)
        task_set.my_task_id[self.engine_id] = return_data["task_set_id"]
        task_set.usable = True

    def send_task_set_task(self, task: TaskSetTask) -> str:

        data: dict = {
            "id": russel_python_interface.static_vars.work_scheduler_id,
            "command": "api",
            "data": task.serialize(self.engine_id),
            "token": str(uuid4()),
        }
        data["data"]["command"] = "task_from_set"

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track(data["token"], False)

        self.pending_unassigned_task[data["token"]] = task
        self.socket.send_json(data)

        return data["token"]

    def delete_task_set(self, task_set: TaskSet):
        id: int = task_set.my_task_id[self.engine_id]
        data: dict = {
            "command": "api",
            "id": russel_python_interface.static_vars.work_scheduler_id,
            "data": {"command": "remove_task_set", "task_set_id": id},
        }

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)

        self.socket.send_json(data)

    def set_delete_from_set(self, set):
        self.delete_from_set = set
