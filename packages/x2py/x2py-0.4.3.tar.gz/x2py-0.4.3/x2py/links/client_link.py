# Copyright (c) 2017, 2018 Jae-jun Kang
# See the file LICENSE for details.

from x2py.links.session_based_link import SessionBasedLink

class ClientLink(SessionBasedLink):
    """Common base class for single-session client links."""

    def __init__(self, name):
        super(ClientLink, self).__init__(name)
        self.session = None  # current link session

    def cleanup(self):
        if self.session is None:
            return
        self.session.close()
        self.sesison = None
        super(ClientLink, self).cleanup()

    def send(self, event):
        if self.session is not None:
            self.session.send(event)

    def _on_connect(self, result, context):
        super(ClientLink, self)._on_connect(result, context)
        if result:
            context.polarity = True
            self.session = context

    def _on_disconnect(self, handle, context):
        super(ClientLink, self)._on_disconnect(handle, context)
        self.session = None
