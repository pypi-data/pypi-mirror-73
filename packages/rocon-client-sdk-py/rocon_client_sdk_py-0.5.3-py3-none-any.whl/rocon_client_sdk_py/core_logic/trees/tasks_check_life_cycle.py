import py_trees
import asyncio
from overrides import overrides
from .task import Task, AsyncTask
from rocon_client_sdk_py.const import *
from rocon_client_sdk_py.utils.util import *


class TaskCheckLifeCycle(AsyncTask):
    def __init__(self, name="checkLifeCycle"):
        super(TaskCheckLifeCycle, self).__init__(name)
        self.count = 0

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

    async def _do_work(self):

        self.count += 1
        print("Count of Behavior Tree's full cycle : {}".format(self.count))
        show_memory_usage(uuid=self.context.worker.uuid)

        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status


    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)
