import threading
import asyncio
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler


class Waiter():
    def __init__(self, event_loop, timeout_msec = -1):
        self._timeout_msec = timeout_msec
        self._event = Subject()
        self._wait_exit = False
        self.result_ob = None
        self._event_loop = event_loop
        self._timer = None

        self.scheduler = AsyncIOScheduler(loop=event_loop)
        self.done = asyncio.Future()


    def set_timeout(self, timeout_msec):
        self._timeout_msec = timeout_msec

    def _timeout_callback(self):

        self._event.on_next('timeout')

    async def wait(self):
        if self._timeout_msec > 0:
            self._timer = threading.Timer(self._timeout_msec/1000, self._timeout_callback)
            self._timer.start()

        self._wait_exit = False

        def cb_next(data):
            if self._timer:
                self._timer.cancel()

            self._wait_exit = True
            self.done.set_result(data)

        def cb_completed():

            self.done.set_result('done')

        #self._event.subscribe(on_next=cb_next, on_completed=cb_completed, scheduler=self.scheduler)
        self._event.subscribe(on_next=cb_next, scheduler=self.scheduler)
        result = await self.done


        return result

    def end(self, msg):
        self._event.on_next(msg or 'success')
        self._event.on_completed()
        #self.result_ob.dispose()

    def set_next(self, msg):
        self._event.on_next(msg)


    def cancel(self):
        #TODO
        pass