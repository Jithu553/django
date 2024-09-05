from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceTests(APITestCase):
    def setUp(self):
        self.invoice_url = '/api/invoices/'
        self.invoice = Invoice.objects.create(date='2024-09-05', customer_name='Test Customer')
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Test Detail',
            quantity=2,
            unit_price=10.00
        )

    def test_create_invoice(self):
        data = {
            'date': '2024-09-05',
            'customer_name': 'New Customer',
            'details': [
                {
                    'description': 'New Detail',
                    'quantity': 5,
                    'unit_price': 15.00
                }
            ]
        }
        response = self.client.post(self.invoice_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_update_invoice(self):
        data = {
            'date': '2024-09-06',
            'customer_name': 'Updated Customer',
            'details': [
                {
                    'id': self.invoice_detail.id,
                    'description': 'Updated Detail',
                    'quantity': 3,
                    'unit_price': 12.00
                }
            ]
        }
        response = self.client.put(f'{self.invoice_url}{self.invoice.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.invoice_detail.refresh_from_db()
        self.assertEqual(self.invoice.customer_name, 'Updated Customer')
        self.assertEqual(self.invoice_detail.description, 'Updated Detail')
        self.assertEqual(self.invoice_detail.quantity, 3)

    def test_delete_invoice(self):
        response = self.client.delete(f'{self.invoice_url}{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
