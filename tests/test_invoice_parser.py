import unittest
import json
from python_challenge.invoice_parser import InvoiceParser

class TestInvoiceParser(unittest.TestCase):
    def test_parse_invoice(self):
        result = InvoiceParser().parse_invoice('tests/fixtures/test_invoice.pdf')

        with open('tests/fixtures/expected_output.json', 'r') as f:
            expected_output = f.read()

        assert json.dumps(result.to_dict(), indent=4) == expected_output


if __name__ == "__main__":
    unittest.main()
