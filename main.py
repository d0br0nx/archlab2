from dataclasses import dataclass, field
from typing import List
import json
import unittest
from unittest.mock import Mock


# Абстрактний клас Item
@dataclass
class Item:
    ID: int
    weight: float
    count: int
    containerID: int
    items: List['Item'] = field(default_factory=list)

    def getTotalWeight(self) -> float:
        """
        Розраховує загальну вагу вантажу, включаючи внутрішні елементи (рекурсивно).
        """
        total_weight = self.weight * self.count
        for item in self.items:
            total_weight += item.getTotalWeight()
        return total_weight


# Конкретні класи Item, використовуючи патерн фабрики
class Small(Item):
    pass

class Heavy(Item):
    pass

class Refrigerated(Item):
    pass

class Liquid(Item):
    pass


# Абстрактний клас Ship
@dataclass
class IShip:
    fuel: int

    def sail(self, destination_port):
        """
        Абстрактний метод відправлення корабля в пункт призначення.
        """
        pass


# Конкретні класи Ship, використовуючи патерн будівельника
@dataclass
class LightWeightShip(IShip):
    name: str
    weight_capacity: int
    fuel_capacity: int
    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        """
        Додає вантаж до корабля.
        """
        self.items.append(item)

    def sail(self, destination_port):
        """
        Реалізація методу відправлення корабля для легкого корабля.
        """
        print(f"{self.name} is sailing to {destination_port.name}")


@dataclass
class MediumShip(IShip):
    name: str
    weight_capacity: int
    fuel_capacity: int
    refrigerator_placeholder: bool
    water_container_placeholder: bool
    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        """
        Додає вантаж до корабля.
        """
        self.items.append(item)

    def sail(self, destination_port):
        """
        Реалізація методу відправлення корабля для середнього корабля.
        """
        print(f"{self.name} is sailing to {destination_port.name}")


@dataclass
class HeavyShip(IShip):
    name: str
    weight_capacity: int
    fuel_capacity: int
    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        """
        Додає вантаж до корабля.
        """
        self.items.append(item)

    def sail(self, destination_port):
        """
        Реалізація методу відправлення корабля для важкого корабля.
        """
        print(f"{self.name} is sailing to {destination_port.name}")


# Простий клас Port
@dataclass
class Port:
    name: str
    coordinates: str
    containers: List[Item] = field(default_factory=list)

    def load_ship(self, ship):
        """
        Завантажує вантаж з корабля в порт.
        """
        for item in ship.items:
            self.containers.append(item)
        ship.items = []

    def unload_ship(self, ship):
        """
        Вивантажує вантаж з порту на корабель.
        """
        for item in self.containers:
            ship.add_item(item)
        self.containers = []


# Клас системи управління портом
class PortManagementSystem:
    def __init__(self):
        self.ports = []
        self.ships = []

    def add_port(self, port: Port):
        """
        Додає порт до системи.
        """
        self.ports.append(port)

    def add_ship(self, ship: IShip):
        """
        Додає корабель до системи.
        """
        self.ships.append(ship)

    def simulate_ship_movement(self, ship, source_port, destination_port):
        """
        Симулює переміщення корабля від одного порту до іншого.
        """
        print(f"Moving {ship.name} from {source_port.name} to {destination_port.name}")
        source_port.unload_ship(ship)
        ship.sail(destination_port)
        destination_port.load_ship(ship)

    def process_operations(self, operations):
        """
        Обробляє послідовність операцій з вхідного файлу.
        """
        for operation in operations:
            self.execute_operation(operation)

    def execute_operation(self, operation):
        """
        Виконує окрему операцію в системі.
        """
        parts = operation.split()
        if parts[0] == "LOAD":
            ship_name = parts[1]
            source_port_name = parts[3]
            destination_port_name = parts[5]

            ship = next((s for s in self.ships if s.name == ship_name), None)
            source_port = next((p for p in self.ports if p.name == source_port_name), None)
            destination_port = next((p for p in self.ports if p.name == destination_port_name), None)

            if ship and source_port and destination_port:
                self.simulate_ship_movement(ship, source_port, destination_port)
            else:
                print(f"Error: Invalid ship, source port, or destination port in operation: {operation}")

# Тести
class TestPortManagementSystem(unittest.TestCase):
    def test_process_operations(self):
        system = PortManagementSystem()

        port_a = Port(name="PortA", coordinates="A123")
        port_b = Port(name="PortB", coordinates="B456")

        system.add_port(port_a)
        system.add_port(port_b)

        ship = LightWeightShip(name="Ship1", fuel=100, weight_capacity=50, fuel_capacity=200)
        system.add_ship(ship)

        input_operations = [
            "LOAD Ship1 FROM PortA TO PortB",
            "UNLOAD Ship1 TO PortB FROM Ship1",
            # Додайте інші операції за необхідності
        ]

        system.process_operations(input_operations)

        self.assertEqual(len(port_a.containers), 0)
        self.assertEqual(len(port_b.containers), 0)  # оскільки вивантажуємо на корабель, а не на порт
        self.assertEqual(len(ship.items), 0)


if __name__ == '__main__':
    unittest.main()
