from time import sleep

# Абстрактное состояние,
class OrderState:
    def process_order(self, order):
        pass


# Конкретные состояния
class ProcessingState(OrderState):
    def process_order(self, order):
        print("Заказ в обработке")
        order.ready_for_delivery += 30
        return ShippedState()


class ShippedState(OrderState):
    def process_order(self, order):
        print("Заказ отправлен")
        order.ready_for_delivery += 30
        return DeliveredState()


class DeliveredState(OrderState):
    def process_order(self, order):
        print("Заказ доставлен")
        order.ready_for_delivery += 40
        return OrderOver()


class OrderOver(OrderState):
    def process_order(self, order):
        return None


# Класс заказа, в основной функции которого process, вызывается функция process_order из текущего объекта состояния
# текущий объект состояния производит некоторые действия, в том числе, изменяет значение self.ready_for_delivery и
# возвращает либо объект следующего состояния, либо None, что означает окончание обработки заказа
class Order:
    def __init__(self):
        self._state = ProcessingState()
        self.ready_for_delivery = 0

    def process(self):
        new_state = self._state.process_order(self)
        if new_state:
            if self.ready_for_delivery > 0:
                print(f"Процент выполнения заказа: {self.ready_for_delivery}%")
            self._state = new_state


# Пример использования
order = Order()
order.process()  # Заказ в обработке
sleep(1)
order.process()  # Заказ отправлен
sleep(1)
order.process()  # Заказ доставлен
