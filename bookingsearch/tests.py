from django.test import TestCase

# Create your tests here.

from . import availability


class AvailabilityTests(TestCase):

    def test_find_element_by_key_in_dictionary(self):

        testdata = [
            {'roomtype': 1, 'occupied': 1},
            {'roomtype': 2, 'occupied': 1},
            {'roomtype': 3, 'occupied': 3},
            {'roomtype': 4, 'occupied': 1}]

        self.assertEqual(availability.find_occupied(1, testdata), 1)
        self.assertEqual(availability.find_occupied(2, testdata), 1)
        self.assertEqual(availability.find_occupied(3, testdata), 3)
        self.assertEqual(availability.find_occupied(4, testdata), 1)
        self.assertEqual(availability.find_occupied(5, testdata), 0)


    def test_serialize_booking_data(self):

        testdata = {
            'arrival': '2021-10-01',
            'departure': '2021-10-09',
            'guests': 1,
            'roomtype_id': 1,
            'room_number': 1,
            'price': 317.58
        }

        self.assertEqual(availability.serialize_booking_data(testdata),
            "arrival:2021-10-01;departure:2021-10-09;guests:1;roomtype_id:1;room_number:1;price:317.58")


    def test_generate_booking_reference(self):

        booking_reference = availability.generate_booking_reference()
        self.assertTrue(type(booking_reference) is str)
        self.assertTrue(len(booking_reference) == 10)
