from platron.request.request_builders.request_builder import RequestBuilder
from platron.sdk_exception import SdkException
from platron.request.data_objects.item import Item

class ReceiptBuilder(RequestBuilder):
    '''
    Receipt builder API requests
    '''

    receipt_items = []

    def __init__(self, operation_type, payment_id = None, order_id = None):
        """
        Payment id or order id must be nut null
        Args:
            operation_type (string): operation type payment|refund|moneyback
            payment_id (string): platron payment id
            order_id (string): merchant order id
        """
        if payment_id == None and order_id == None:
            raise SdkException('payment id or order id must be nut null')

        if self.__get_operstion_types().get(operation_type) == None:
            raise SdkException('Wrong vat. Use from constants')
                
        self.pg_operation_type = operation_type
        if payment_id != None:
            self.pg_payment_id = payment_id
        if order_id != None:
            self.pg_order_id = order_id
        
    def get_url(self):
        return self.PLATRON_URL + 'receipt.php'

    def add_item(self, item):
        """Add item to receipt
        Args:
            item (Item): 1 item in receipt
        """
        if not isinstance(item, Item):
            raise SdkException('Only item object expected')

        self.receipt_items.append(item.get_params())

    def add_customer(self, name, inn):
        """Add customer to receipt
        Args:
            name (string): customer name
            inn (string): customer inn
        """
        self.pg_customer_name = name
        self.pg_customer_inn = inn
        return self

    def add_additional_payment(self, amount, type):
        """Add customer to receipt
        Args:
            amount (string): additional payment amount
            type (string): additional payment type
        """
        if self.__get_additional_payment_types().get(operation_type) == None:
            raise SdkException('Wrong additional payment type. Use from constants')

        self.pg_additional_payment_amount = amount
        self.pg_additional_payment_type = type
        return self
    
    def __get_operstion_types(self):
        return {'payment': True, 'refund' : True, 'moneyback' : True}

    def __get_additional_payment_types(self):
        return {'prepayment': True, 'credit' : True}
    
    def item_function(self, parent):
        ''' Как будут называться элементы, не имеющие названия - receipt_items '''
        return 'pg_items'
    
    def after_xml_created(self, xml):
        return xml.replace('<receipt_items>', '').replace('</receipt_items>', '')