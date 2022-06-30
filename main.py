from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self.items = {}
        self.capacity = 100

    def add(self, name, count):
        if name in self.items.keys():
            self.items[name] += count
        else:
            self.items[name] = count
        self.capacity -= count

    def remove(self, name, count):
        if self.items[name] - count > 0:
            self.items[name] -= count
        else:
            del self.items[name]


    @property
    def get_free_space(self):
        return self.capacity

    @property
    def get_items(self):
        return self.items

    @property
    def get_unique_items_count(self):
        return len(self.items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self.capacity = 20


class Request:
    def __init__(self, user_input):
        self.user_input = self._split_user_input(user_input)
        self.from_ = self.user_input[4]
        self.to = self.user_input[6]
        self.amount = int(self.user_input[1])
        self.product = self.user_input[2]

    @staticmethod
    def _split_user_input(user_input):
        return user_input.split(' ')

    def __repr__(self):
        return f'Доставить {self.amount} {self.product} из {self.from_} в {self.to}'


def main():
    while True:
        user_input = input("Введите запрос: ")

        if user_input == 'stop':
            print('Поработаем в следующий раз')
            break

        request = Request(user_input)

        from_ = store if request.from_ == 'склад' else shop
        to = store if request.to == 'склад' else shop

        if request.product in from_.items:
            print(f'Товар {request.product} находится на {request.from_}')
        else:
            print(f'Товара {request.product} нет в наличии')
            continue

        if from_.items[request.product] >= request.amount:
            print(f'Нужное количество есть на {request.from_}')
        else:
            print(f'Нет такого количества {request.product} на {request.from_}. '
                  f'На складе хранится {from_.items[request.product]} ед. товара')
            continue

        if to.get_free_space >= request.amount:
            print(f'В {request.to} достаточно места')
        else:
            print(f'В {request.to} недостаточно места. ')
            continue

        if request.to == 'магазин' and to.get_unique_items_count == 5 and request.product not in to.items:
            print('В магазин переполнен уникальными товарами')
            continue
        from_.remove(request.product, request.amount)
        print(f'Курьер забрал {request.amount} {request.product} со {request.from_}')
        print(f'Курьер везет {request.amount} {request.product} со {request.from_} в {request.to}')

        to.add(request.product, request.amount)
        print(f'Курьер доставил {request.amount} {request.product} в {request.to}')

        print('=' * 50)
        print(f'На складе хранятся:')
        for name, count in store.items.items():
            print(f'{name} {count}')
        print(f'Свободного места {from_.get_free_space - sum(from_.items.values())}')

        print('=' * 50)
        print(f'В магазине хранятся:')
        for name, count in shop.items.items():
            print(f'{name} {count}')
        print(f'Свободного места {to.get_free_space}')


if __name__ == '__main__':
    store = Store()
    shop = Shop()

    store_items = {
        'печеньки': 10,
        "молоко": 8,
        "чай": 12,
        "сок": 9
    }

    store.items = store_items

    main()

