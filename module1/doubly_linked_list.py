class ObjList:
    def __init__(self, data: str):
        """
        Создание нового узла списка.

        data - свойство с данными
        next - ссылка на следующий узел
        prev - ссылка на предыдущий узел
        """
        self.__data = data
        self.__next = None
        self.__prev = None

    def set_next(self, obj):
        """ Установка ссылки на следующий объект. """
        self.__next = obj

    def get_next(self):
        """ Возвращает следующий объект. """
        return self.__next

    def set_prev(self, obj):
        """ Установка ссылки на предыдущий объект. """
        self.__prev = obj

    def get_prev(self):
        """ Возвращает предыдущий объект. """
        return self.__prev

    def set_data(self, data: str):
        """ Устанавливает данные в узел. """
        self.__data = data

    def get_data(self):
        """ Возвращает данные из узла. """
        return self.__data


class LinkedList:
    def __init__(self):
        """
        Создает пустой список.

        head - ссылка на первый элемент списка
        tail - ссылка на последний элемент списка
        """
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList):
        """ Добавление объекта в конец списка. """
        if self.tail is None:
            self.head = self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

    def remove_obj(self, obj: ObjList):
        """ Удаление объекта из списка. """
        if obj is None or self.head is None:
            return

        if obj == self.head and obj == self.tail:
            self.head = self.tail = None

        elif obj == self.head:
            self.head = obj.get_next()
            if self.head:
                self.head.set_prev(None)

        elif obj == self.tail:
            self.tail = obj.get_prev()
            if self.tail:
                self.tail.set_next(None)

        else:
            prev_obj = obj.get_prev()
            next_obj = obj.get_next()
            prev_obj.set_next(next_obj)
            next_obj.set_prev(prev_obj)

        del obj  # удаление объекта из памяти

    def get_data(self):
        """ Возвращает список данных всех узлов. """
        result = []
        current = self.head

        while current:
            result.append(current.get_data())
            current = current.get_next()
        return result
