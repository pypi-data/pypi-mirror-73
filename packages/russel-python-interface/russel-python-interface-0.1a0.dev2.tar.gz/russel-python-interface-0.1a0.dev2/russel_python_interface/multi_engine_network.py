import copy
import time
from typing import List, Dict

from russel_python_interface.engine import Engine
from russel_python_interface.task_sets import TaskSetTask, TaskSet


class MultiEngineNetwork:
    engines: Dict[float, Engine] = {}
    persistent: List[Engine] = []

    @staticmethod
    def create(endpoints: List[List[str]]) -> "MultiEngineNetwork":
        network: MultiEngineNetwork = MultiEngineNetwork()

        for endpoint in endpoints:
            if endpoint[1] == "IPC":
                e: Engine = Engine.create_connect_to_local(endpoint[0])
                e.start()
                e.upload_all_local_routines()
                network.engines[time.time()] = e
                network.persistent.append(e)
            elif endpoint[1] == "PUB":
                e: Engine = Engine.create_from_uri(endpoint[0])
                e.start()
                e.upload_all_local_routines()
                network.engines[time.time()] = e
                network.persistent.append(e)

        return network

    def schedule_task_from_task_set(self, task: TaskSetTask) -> (str, int):

        last_update: float = min(self.engines.keys())
        e: Engine = self.engines[last_update]
        token: str = e.send_task_set_task(task)

        current_time: float = time.time()
        del self.engines[last_update]
        self.engines[current_time] = e
        return token, list(self.persistent).index(e)

    def send_task_set(self, task_set: TaskSet):
        for k in self.engines:
            self.engines[k].register_task_set(task_set)

    def solve_task_batch(self, tasks: List[TaskSetTask]):
        expecting_task: Dict[str, int] = {}

        for k in self.engines:
            self.engines[k].set_delete_from_set(expecting_task)

        for task in tasks:
            token, index = self.schedule_task_from_task_set(task)
            print(index, token)
            expecting_task[token] = index

        for k in self.engines:
            self.engines[k].force_schedule()

        while len(expecting_task) > 0:

            temp_tokens = copy.deepcopy(expecting_task)

            for task_token in temp_tokens:
                if task_token in expecting_task:
                    self.persistent[expecting_task[task_token]].resend_task(task_token)

            for k in self.engines:
                self.engines[k].force_schedule()

            time.sleep(0.2)

    def delete_task_set(self, task_set: TaskSet):

        for k in self.engines:
            e = self.engines[k]
            e.delete_task_set(task_set)
