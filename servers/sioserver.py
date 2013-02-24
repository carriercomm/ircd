import functools
import tornado
import tornadio2
from server import Server


class Connection(tornadio2.conn.SocketConnection):
    def __init__(self, server, *kargs, **kwargs):
        super(Connection, self).__init__(*kargs, **kwargs)
        self.server = server

    def on_open(self, info):
        self.tag = '%s-%x' % (info.ip, id(self))
        self.server.user_connect(self.tag, info.ip)

    def on_message(self, message):
        self.server.user_message(self.tag, message)

    def on_close(self):
        self.server.user_disconnect(self.tag)


class SioServer(object):
    @tornado.gen.engine
    def __init__(self, config):
        self.server = Server('sio')

        conn_maker = functools.partial(Connection, self.server)
        router = tornadio2.TornadioRouter(conn_maker)

        app = tornado.web.Application(
            router.urls,
            flash_policy_file=config.flash_policy_file,
            flash_policy_port=config.flash_policy_port,
            socket_io_port=config.socketio_port)

        tornadio2.SocketServer(app, auto_start=False)
