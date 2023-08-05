from threador_config import call_task
import datetime


class Executor:
    __slots__ = ('tasks',)

    def __init__(self, *args, tasks, **kwargs):
        self.tasks = tasks or []

    def run(self):
        _start = datetime.datetime.now()
        tasks = []

        for task_name, args, kwargs in self.tasks:
            args = args or ()
            kwargs = kwargs or {}
            tasks.append(call_task.delay(task_name, *args, **kwargs))

        while all([i.ready() for i in tasks]):
            pass

        result = tuple(i.get(timeout=0.0) for i in tasks)
        print(datetime.datetime.now() - _start)
        return result
