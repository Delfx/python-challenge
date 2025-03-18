from decimal import Decimal
import pdfplumber
import re
from python_challenge.dto.invoice import InvoiceDTO
from python_challenge.dto.measurement import Measurement
from python_challenge.dto.money import Money 
from python_challenge.dto.invoice_item import InvoiceItemDTO
from python_challenge.dto.delivery_record import DeliveryRecord
from python_challenge.dto.unit_price import UnitPrice
from datetime import datetime

class InvoiceParser:
    def parse_invoice(self, invoice_path: str) -> InvoiceDTO:
        result = InvoiceDTO()
        result.supplier = "cepsa"

        # Your implementation goes here
        # Open the PDF file using pdfplumber
        with pdfplumber.open(invoice_path) as pdf:
            page = pdf.pages[0]
            
            # Crop specific areas of the page where required data is located
            cropped_page_value = page.crop((0, 510, page.width, page.height - 270))
            cropped_page_product = page.crop((0, 360, page.width, page.height - 395))
            
            # Extract tables from the cropped sections
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
            
            # Extract text from cropped sections and split into lines
            table_value = cropped_page_value.extract_text_simple().split("\n")
            table_product = cropped_page_product.extract_text_simple().split("\n")
            
            # Extract required data from the tables
            date_str = table_date_no[0][0][0].split("\n")[1].strip()
            number = table_date_no[0][0][1].split("\n")[1].strip()
            due_str = table_all[0][4][0].split("\n")[-1].strip()
            number_primary_amount_match = re.findall(r"(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+))", table_all[0][9][1])[1].replace(".", "").replace(",", ".")
            currency_primary_amount_match = re.findall(r"\w+ \((\w+)\)", table_all[0][7][0])[0]
            global_from_airport = None

            # Assign the extracted data to the result object
            result.date = datetime.strptime(date_str, "%d.%m.%Y").date()
            result.number = number
            result.due_date = datetime.strptime(due_str, "%d.%m.%Y").date()
            result.primary_amount = Money(amount=number_primary_amount_match, currency=currency_primary_amount_match)
            result.items = []
            
            # Check if delivery_records is None and initialize it as an empty list if true
            if result.delivery_records is None:
                result.delivery_records = []
                
            # Iterate through the table_product list, processing two lines at a time
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
                
                # Save from_airport as a global variable
                global_from_airport = from_airport

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

                # Iterate through the table_value list
                if not result.aggregated_items:
                    result.aggregated_items = []
                    
                    # Iterate through the table_value list
                    for item in table_value:
                        parts = item.split()
                        
                        # Extract Description: Everything before the first numeric value
                        description_match = re.match(r"^(.*?)(?=\d)", item.strip())  # Get text before numbers
                        description = description_match.group(1).strip() if description_match else item
                        
                        # Extract Quantity and Unit
                        quantity_match = re.search(r"([\d.,]+)\s*([A-Z]+)", item)
                        if quantity_match:
                            quantity_str, unit = quantity_match.groups()
                            quantity_value = Decimal(quantity_str.replace(".", "").replace(",", "."))  # Convert to correct number
                        else:
                            continue  # Skip if quantity is not found

                        # Extract Unit Price and Currency
                        unit_price_match = re.search(r"([\d.,]+)\s*([A-Z]{3})/ ([A-Z]+)", item)
                        if unit_price_match:
                            unit_price_str, currency, unit_price_unit = unit_price_match.groups()
                            unit_price = Decimal(unit_price_str.replace(",", "."))
                        else:
                            currency_match = re.search(r"([A-Z]{3})$", item)  # If no unit price, just get the last currency
                            currency = currency_match.group(1) if currency_match else "EUR"
                            unit_price = None  # No unit price for items like "Hook up Fee"

                        # Extract Primary Amount
                        primary_amount_match = re.findall(r"([\d.,]+)\s*([A-Z]{3})", item)
                        if primary_amount_match:
                            primary_amount_str, primary_currency = primary_amount_match[-1]  # Last occurrence should be the total price
                            primary_amount = Decimal(primary_amount_str.replace(".", "").replace(",", "."))
                        else:
                            continue  # Skip if no price found

                        # Create InvoiceItemDTO object
                        invoice_item = InvoiceItemDTO(
                            base= global_from_airport, 
                            description=description,
                            quantity_priced=Measurement(value=quantity_value, unit=unit),
                            unit_price_dto=UnitPrice(amount=unit_price, currency=currency, unit=unit_price_unit) if unit_price else None,
                            primary_amount=Money(amount=primary_amount, currency=primary_currency)
                        )

                        # Append to result
                        result.aggregated_items.append(invoice_item)
                                            
            
        return result
