class Data:
    """ Класс для описания пакета данных. """

    def __init__(self, data: str, ip: int):
        self.data = data
        self.ip = ip

    def __repr__(self):
        return f"Data('{self.data}', {self.ip})"


class Server:
    """ Класс для описания сервера в сети. """
    _ip_counter = 1

    def __init__(self):
        """
        Инициализация объектов

        ip - уникальный IP
        buffer - список входящих пакетов
        router - ссылка на роутер
        """
        self.ip = Server._ip_counter
        Server._ip_counter += 1
        self.buffer = []
        self.router = None

    def send_data(self, data: Data):
        """ Отправка пакета данных через роутер. """
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        """ Возвращает принятые пакеты и очищает буфер. """
        received_data = self.buffer[:]
        self.buffer.clear()
        return received_data

    def get_ip(self):
        """ Возвращает IP-адрес сервера """
        return self.ip


class Router:
    """
    Класс для описания роутера

    servers - словарь подключенных серверов {ip: server}
    buffer - очередь пакетов
    """

    def __init__(self):
        self.servers = {}
        self.buffer = []

    def link(self, server: Server):
        """ Подключение сервера к роутеру. """
        self.servers[server.get_ip()] = server
        server.router = self

    def unlink(self, server: Server):
        """ Отключение сервера от роутера. """
        self.servers.pop(server.get_ip(), None)
        server.router = None

    def send_data(self):
        """ Отправка пакетов по назначению """
        for packet in self.buffer:
            if packet.ip in self.servers:
                self.servers[packet.ip].buffer.append(packet)
        self.buffer.clear()


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("hello", sv_to.get_ip()))
sv_from2.send_data(Data("hello", sv_to.get_ip()))
sv_to.send_data(Data("hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()
