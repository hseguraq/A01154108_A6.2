# pylint: disable=import-error, wrong-import-position
"""Program that performs several unit tests for main.py"""

import unittest
import sys
import os

# Adjusting path to import main.py from two levels up
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # noqa: E501
from main import Hotel, Customer, Reservation  # noqa: E402


class TestHotelSystem(unittest.TestCase):
    """Set of unit tests to evaluate operation of main.py"""
    def setUp(self):
        """Sets up a clean test environment by resetting hotel and customer files."""  # noqa: E501
        with open("hotels.txt", "w", encoding="utf-8") as f:
            f.write("{}")
        with open("customers.txt", "w", encoding="utf-8") as f:
            f.write("{}")

    def test_create_hotel(self):
        """Tests if a hotel can be created successfully."""
        Hotel.create("H1", "Grand Hotel", "NY", 100)
        self.assertEqual(Hotel.display("H1")["name"], "Grand Hotel")

    def test_create_customer(self):
        """Tests if a customer can be created successfully."""
        Customer.create("C1", "John Doe", "1234567890")
        self.assertEqual(Customer.display("C1")["name"], "John Doe")

    def test_hreserve_room(self):
        """Tests if a hotel room can be reserved by a customer."""
        Hotel.create("H2", "Declaracion Hotel", "NY", 2)
        Customer.create("C2", "Jane De", "1234567890")
        Hotel.reserve_room("H2", "C2")
        self.assertIn("C2", Hotel.display("H2")["reservations"])

    def test_reserve_room(self):
        """Tests if a reservation can be made and properly recorded."""
        Hotel.create("H1", "Grand Hotel", "NY", 2)
        Customer.create("C1", "John Doe", "1234567890")
        Reservation.create("C1", "H1")
        self.assertIn("C1", Hotel.display("H1")["reservations"])

    def test_hcancel_reservation(self):
        """Tests if a hotel room reservation can be canceled."""
        Hotel.create("H1", "Grand Hotel", "NY", 2)
        Customer.create("C1", "John Doe", "1234567890")
        Hotel.reserve_room("H1", "C1")
        Hotel.cancel_reservation("H1", "C1")
        self.assertNotIn("C1", Hotel.display("H1")["reservations"])

    def test_cancel_reservation(self):
        """Tests if a reservation can be canceled successfully."""
        Hotel.create("H1", "Grand Hotel", "NY", 2)
        Customer.create("C1", "John Doe", "1234567890")
        Reservation.create("C1", "H1")
        Reservation.cancel("C1", "H1")
        self.assertNotIn("C1", Hotel.display("H1")["reservations"])

    def test_no_available_rooms(self):
        """Tests if a reservation fails when no rooms are available."""
        Hotel.create("H1", "Grand Hotel", "NY", 1)
        Customer.create("C1", "John Doe", "1234567890")
        Customer.create("C2", "Jane Doe", "0987654321")
        Reservation.create("C1", "H1")
        self.assertNotIn("C2", Hotel.display("H1")["reservations"])

    def test_delete_hotel(self):
        """Tests if a hotel can be deleted successfully."""
        Hotel.create("H1", "Grand Hotel", "NY", 100)
        Hotel.delete("H1")
        self.assertEqual(Hotel.display("H1"), "Hotel not found.")

    def test_modify_hotel(self):
        """Tests if a hotel's information can be modified successfully."""
        Hotel.create("H1", "Grand Hotel", "NY", 100)
        Hotel.modify("H1", name="Grann Hotel II")
        self.assertEqual(Hotel.display("H1")["name"], "Grann Hotel II")

    def test_delete_customer(self):
        """Tests if a customer can be deleted successfully."""
        Customer.create("C1", "John Doe", "1234567890")
        Customer.delete("C1")
        self.assertEqual(Customer.display("C1"), "Customer not found.")

    def test_modify_customer(self):
        """Tests if a customer's contact information can be modified."""
        Customer.create("C1", "John Doe", "1234567890")
        Customer.modify("C1", contact="1112223333")
        self.assertEqual(Customer.display("C1")["contact"], "1112223333")

    def test_display_customer(self):
        """Tests if a customer's details can be retrieved successfully."""
        Customer.create("C1", "John Doe", "1234567890")
        self.assertEqual(Customer.display("C1")["name"], "John Doe")


if __name__ == "__main__":
    unittest.main()
