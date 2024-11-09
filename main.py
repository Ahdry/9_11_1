import random
import time
from threading import Thread
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Гость за столом, по умолчанию None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Ожидание от 3 до 10 секунд
        time.sleep(random.randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            # Пытаемся рассадить гостей
            seated = False
            for table in self.tables:
                if table.guest is None:  # Если стол свободен
                    table.guest = guest
                    guest.start()  # Запускаем поток гостя
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    seated = True
                    break

            if not seated:  # Если не нашли свободный стол
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                if table.guest is not None:  # Если за столом есть гость
                    if not table.guest.is_alive():  # Если гость закончил приём пищи
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол

                        # Если очередь не пуста, садим следующего гостя
                        if not self.queue.empty():
                            next_guest = self.queue.get()
                            table.guest = next_guest
                            next_guest.start()
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
            time.sleep(1)  # Небольшая задержка перед следующей проверкой


# Выполняемый код
# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()
