from  queue import Queue
from time import sleep
import threading
from random import randint

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        sleep(randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.q = Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = None
            for table in self.tables:

                if table.guest is None:
                    free_table = table

            if free_table:
                free_table.guest = guest
                guest.start()
                print(f'{guest.name} сел(-а) за стол номер {free_table.number}')

            else:
                self.q.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.q.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

                        if not self.q.empty():
                            next_guest = self.q.get()
                            table.guest = next_guest
                            next_guest.start()
                            print(f'{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


tables1 = [Table(number) for number in range(1, 6)]

guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

guests1 = [Guest(name) for name in guests_names]

cafe = Cafe(*tables1)

cafe.guest_arrival(*guests1)

cafe.discuss_guests()


