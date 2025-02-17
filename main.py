# pylint: disable=protected-access, line-too-long
"""Program that manages Hotels, Customers and Reservations."""

import json
import os


class Hotel:
    """Class for managing Hotels information"""
    FILE_NAME = "hotels.txt"

    @staticmethod
    def _load_hotels():
        if not os.path.exists(Hotel.FILE_NAME):
            return {}
        try:
            with open(Hotel.FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Corrupted hotel data file.")
            return {}

    @staticmethod
    def _load_customers():
        customer_file = "customers.txt"
        if not os.path.exists(customer_file):
            return {}
        try:
            with open(customer_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Corrupted customer data file.")
            return {}

    @staticmethod
    def _save_hotels(hotels):
        with open(Hotel.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(hotels, file, indent=4)

    @classmethod
    def create(cls, hotel_id, name, location, rooms):
        """Allows user to create a new hotel instance"""
        hotels = cls._load_hotels()
        if hotel_id in hotels:
            print(f"Error: Hotel ID {hotel_id} already exists.")
            return
        hotels[hotel_id] = {"name": name, "location": location, "rooms": rooms, "reservations": []}  # noqa: E501
        cls._save_hotels(hotels)

    @classmethod
    def delete(cls, hotel_id):
        """Allows user to delete a hotel instance"""
        hotels = cls._load_hotels()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        del hotels[hotel_id]
        cls._save_hotels(hotels)

    @classmethod
    def display(cls, hotel_id):
        """Displays information for a given hotel"""
        hotels = cls._load_hotels()
        return hotels.get(hotel_id, "Hotel not found.")

    @classmethod
    def modify(cls, hotel_id, name=None, location=None, rooms=None):
        """Allows modification of any hotel value"""
        hotels = cls._load_hotels()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        if name:
            hotels[hotel_id]["name"] = name
        if location:
            hotels[hotel_id]["location"] = location
        if rooms:
            hotels[hotel_id]["rooms"] = rooms
        cls._save_hotels(hotels)

    @classmethod
    def reserve_room(cls, hotel_id, customer_id):
        """Allows user to reserve a room for any given hotel"""
        hotels = cls._load_hotels()
        customers = cls._load_customers()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        if customer_id not in customers:
            print(f"Error: Customer ID {customer_id} is not listed in the system.")  # noqa: E501
            return
        if customer_id in hotels[hotel_id]["reservations"]:
            print(f"Error: Customer ID {customer_id} already has a reservation at this hotel.")  # noqa: E501
            return
        if hotels[hotel_id]["rooms"] <= len(hotels[hotel_id]["reservations"]):
            print("Error: No available rooms.")
            return
        hotels[hotel_id]["reservations"].append(customer_id)
        cls._save_hotels(hotels)

    @classmethod
    def cancel_reservation(cls, hotel_id, customer_id):
        """Allows user to cancel an established reservation"""
        hotels = cls._load_hotels()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        if customer_id not in hotels[hotel_id]["reservations"]:
            print(f"Error: Reservation for Customer ID {customer_id} not found.")  # noqa: E501
            return
        hotels[hotel_id]["reservations"].remove(customer_id)
        cls._save_hotels(hotels)


class Customer:
    """Class for managing Customers information"""
    FILE_NAME = "customers.txt"

    @staticmethod
    def _load_customers():
        if not os.path.exists(Customer.FILE_NAME):
            return {}
        try:
            with open(Customer.FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: Corrupted customer data file.")
            return {}

    @staticmethod
    def _save_customers(customers):
        with open(Customer.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(customers, file, indent=4)

    @classmethod
    def create(cls, customer_id, name, contact):
        """Allows user to create a new customer"""
        customers = cls._load_customers()
        if customer_id in customers:
            print(f"Error: Customer ID {customer_id} already exists.")
            return
        customers[customer_id] = {"name": name, "contact": contact}
        cls._save_customers(customers)

    @classmethod
    def delete(cls, customer_id):
        """Allows user to delete a valid customer"""
        customers = cls._load_customers()
        if customer_id not in customers:
            print(f"Error: Customer ID {customer_id} does not exist.")
            return
        del customers[customer_id]
        cls._save_customers(customers)

    @classmethod
    def display(cls, customer_id):
        """Displays information for a given customer"""
        customers = cls._load_customers()
        return customers.get(customer_id, "Customer not found.")

    @classmethod
    def modify(cls, customer_id, name=None, contact=None):
        """Allows user to modify any value of a given customer"""
        customers = cls._load_customers()
        if customer_id not in customers:
            print(f"Error: Customer ID {customer_id} does not exist.")
            return
        if name:
            customers[customer_id]["name"] = name
        if contact:
            customers[customer_id]["contact"] = contact
        cls._save_customers(customers)


class Reservation:
    """Class for managing reservations"""
    @classmethod
    def create(cls, customer_id, hotel_id):
        """Allows user to create a new reservation"""
        hotels = Hotel._load_hotels()
        customers = Customer._load_customers()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        if customer_id not in customers:
            print(f"Error: Customer ID {customer_id} does not exist.")
            return
        hotels[hotel_id]["reservations"].append(customer_id)
        Hotel._save_hotels(hotels)

    @classmethod
    def cancel(cls, customer_id, hotel_id):
        """Allows user to cancel a given reservation"""
        hotels = Hotel._load_hotels()
        if hotel_id not in hotels:
            print(f"Error: Hotel ID {hotel_id} does not exist.")
            return
        if customer_id not in hotels[hotel_id]["reservations"]:
            print(f"Error: Reservation for Customer ID {customer_id} not found.")  # noqa: E501
            return
        hotels[hotel_id]["reservations"].remove(customer_id)
        Hotel._save_hotels(hotels)
