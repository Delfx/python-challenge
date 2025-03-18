from decimal import Decimal
import pdfplumber
import re
from python_challenge.dto.invoice import InvoiceDTO
from python_challenge.dto.measurement import Measurement
from python_challenge.dto.money import Money 
from python_challenge.dto.invoice_item import InvoiceItemDTO
from python_challenge.dto.delivery_record import DeliveryRecord
from datetime import datetime



class InvoiceParser:
    def parse_invoice(self, invoice_path: str) -> InvoiceDTO:
        result = InvoiceDTO()
        result.supplier = "cepsa"

        # Your implementation goes here
        with pdfplumber.open(invoice_path) as pdf:
            page = pdf.pages[0]
            cropped_page_value = page.crop((0, 510, page.width, page.height - 270))
            cropped_page_product = page.crop((0, 360, page.width, page.height - 395))

            table_date_no = page.extract_tables()
            table_all = page.extract_tables(
                table_settings={
                    "explicit_vertical_lines": [
                        45,
                        560, 
                    ],
                    "snap_tolerance": 3
                }
            )
            
            # im = cropped_page_product.to_image()
            # im.show()
            
            table_value = cropped_page_value.extract_text_simple().split("\n")
            table_product = cropped_page_product.extract_text_simple().split("\n")
            
            print(table_product)
            
                        
            date_str = table_date_no[0][0][0].split("\n")[1].strip()
            number = table_date_no[0][0][1].split("\n")[1].strip()
            due_str = table_all[0][4][0].split("\n")[-1].strip()
            number_primary_amount_match = re.findall(r"(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+))", table_all[0][9][1])[1].replace(".", "").replace(",", ".")
            currency_primary_amount_match = re.findall(r"\w+ \((\w+)\)", table_all[0][7][0])[0]
            
            # match

            result.date = datetime.strptime(date_str, "%d.%m.%Y").date()
            result.number = number
            result.due_date = datetime.strptime(due_str, "%d.%m.%Y").date()
            result.primary_amount = Money(amount=number_primary_amount_match, currency=currency_primary_amount_match)
            result.items = []

                        

            if result.delivery_records is None:
                result.delivery_records = []

            for i in range(0, len(table_product) - 1, 2):  # Process two lines at a time
                product_line = table_product[i].strip()
                details_line = table_product[i + 1].strip()

                # Extract Product Name
                product_name = product_line.replace("Product:", "").strip()

                # Extract Details
                details_parts = details_line.split()
                delivery_date = datetime.strptime(details_parts[0], "%d.%m.%Y").date()
                receipt_no = details_parts[1]
                aircraft_reg = details_parts[2]
                flight_no = details_parts[3]
                from_airport = details_parts[4]
                to_airport = details_parts[5]
                quantity_value = Decimal(details_parts[6].replace(".", "").replace(",", "."))
                quantity_unit = "L"  # Assuming liters as unit

                # Create a DeliveryRecord object
                delivery_record = DeliveryRecord(
                    id=receipt_no,
                    base=from_airport,  # Base is not available in the extracted data
                    date=delivery_date,
                    flight_number=flight_no,
                    aircraft_registration=aircraft_reg,
                    quantity=Measurement(value=quantity_value, unit=quantity_unit),
                    product=product_name
                )

                # Append to result
                result.delivery_records.append(delivery_record)

            
            
           
            
           
        return result
