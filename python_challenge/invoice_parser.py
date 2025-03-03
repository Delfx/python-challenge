from python_challenge.dto.invoice import InvoiceDTO

class InvoiceParser:
    def parse_invoice(self, invoice_path: str) -> InvoiceDTO:
        result = InvoiceDTO()
        result.supplier = 'cepsa'

        # Your implementation goes here

        return result
