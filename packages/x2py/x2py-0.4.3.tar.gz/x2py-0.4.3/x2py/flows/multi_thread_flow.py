# Copyright (c) 2017, 2018 Jae-jun Kang
# See the file LICENSE for details.

from threading import Thread

from x2py.builtin_events import *
from x2py.event import EventProxy
from x2py.flow import Flow
from x2py.flows.event_based_flow import EventBasedFlow
from x2py.util.trace import Trace

class MultiThreadFlow(EventBasedFlow):
    def __init__(self, name=None, num_threads=2):
        super(MultiThreadFlow, self).__init__(name)
        self.threads = []
        self.num_threads = num_threads

    def start(self):
        with self._lock:
            if len(self.threads) != 0:
                return

            self._setup()
            self.cases.setup_with(self)

            for i in range(self.num_threads):
                thread = Thread(target=self)
                thread.setName("{} {}".format(self.name, i + 1))
                thread.start()
                self.threads.append(thread)

            self.queue.enqueue(FlowStart())

    def stop(self):
        with self._lock:
            if len(self.threads) == 0:
                return

            self.queue.close(FlowStop())

            for thread in self.threads:
                thread.join()
            del self.threads[:]

            self.cases.teardown_with(self)
            self._teardown()

    def __call__(self):
        Flow.thread_local.current = self
        Flow.thread_local.event_proxy = EventProxy()
        Flow.thread_local.handler_chain = []

        while True:
            event = self.queue.dequeue()
            if event is None:
                break
            self.dispatch(event)

        Flow.thread_local.handler_chain = None
        Flow.thread_local.event_proxy = None
        Flow.thread_local.current = None

