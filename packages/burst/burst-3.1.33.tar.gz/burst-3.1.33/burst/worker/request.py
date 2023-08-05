from ..share.task import Task
from ..share import constants
from ..share.log import logger


class Request(object):
    """
    请求
    """

    # 业务层需要访问的对象，消息内容
    box = None

    # connection
    conn = None
    # 封装的task，外面不需要理解
    task = None
    is_valid = False
    blueprint = None
    route_rule = None
    # 是否中断处理，即不调用view_func，主要用在before_request中
    interrupted = False
    # 中断后要写入的数据
    interrupt_data = None

    def __init__(self, conn, task):
        self.conn = conn
        self.task = task
        # 赋值
        self.is_valid = self._parse_raw_data()

    def _parse_raw_data(self):
        if not self.task.body:
            return True

        self.box = self.app.box_class()

        if self.box.unpack(self.task.body) > 0:
            self._parse_route_rule()
            return True
        else:
            logger.error('unpack fail. request: %s', self)
            return False

    def _parse_route_rule(self):
        if self.cmd is None:
            return

        route_rule = self.app.get_route_rule(self.cmd)
        if route_rule:
            # 在app层，直接返回
            self.route_rule = route_rule
            return

        for bp in self.app.blueprints:
            route_rule = bp.get_route_rule(self.cmd)
            if route_rule:
                self.blueprint = bp
                self.route_rule = route_rule
                break

    @property
    def worker(self):
        return self.conn.worker

    @property
    def app(self):
        return self.worker.app

    @property
    def client_ip(self):
        """
        客户端连接IP，外面不需要了解task
        :return:
        """
        return self.task.client_ip

    @property
    def cmd(self):
        try:
            return self.box.cmd
        except:
            return None

    @property
    def view_func(self):
        return self.route_rule['view_func'] if self.route_rule else None

    @property
    def endpoint(self):
        if not self.route_rule:
            return None

        bp_endpoint = self.route_rule['endpoint']

        return '.'.join([self.blueprint.name, bp_endpoint] if self.blueprint else [bp_endpoint])

    def make_rsp(self, data):
        """
        生成要写回的数据。业务层代码不要调用
        如果处理函数没有return数据的话，data可能为None，此时相当于直接进行ask_for_task
        :param data: dict/box/str
        :return:
        """
        if isinstance(data, self.app.box_class):
            data = data.pack()
        elif isinstance(data, dict):
            data = self.box.map(data).pack()

        task = Task(dict(
            cmd=constants.CMD_WORKER_TASK_DONE,
            body=data or '',
        ))

        return task.pack()

    def interrupt(self, data=None):
        """
        中断处理
        不能在这里直接write数据，是因为write之后就会告知proxy申请task，而业务层很可能误调用多次
        :param data: 要响应的数据，不传即不响应。多次调用，以最后一次为准。
        :return:
        """
        self.interrupted = True
        self.interrupt_data = data

    def __repr__(self):
        return '<%s cmd: %r, endpoint: %s, task: %r, worker: %s>' % (
            type(self).__name__, self.cmd, self.endpoint, self.task, self.worker
        )
