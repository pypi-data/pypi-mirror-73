from platron.request.data_objects.data_object import DataObject
from platron.sdk_exception import SdkException

class Item(DataObject):
    '''
    Item for receipt
    '''

    def __init__(self, label, price, quantity):
        """
        Args:
            label (string): product label
            price (string): price of 1 product
            quantity (string): count of product
        """
        self.pg_label = label
        self.pg_price = price
        self.pg_quantity = quantity
        
    def add_vat(self, vat):
        """
        If not seted vat = non used
        Args:
            vat (string): product vat 0|10|18|110|118
        """
        if self.__get_vat_variables().get(vat) == None:
            raise SdkException('Wrong vat. Use from constants')
            
        self.pg_vat = vat
        return self
    
    def add_amount(self, amount):
        """
        If price * quantity != amount looks like discount
        Args:
            vat (string): product vat from constant
        """
        self.pg_amount = amount
        return self

    def add_type(self, type):
        """
        Args:
            type (string): product type default = product
        """
        if self.__get_type_variables().get(type) == None:
            raise SdkException('Wrong type. Use from constants')

        self.pg_type = type
        return self

    def add_payment_type(self, type):
        """
        Args:
            type (string): payment type default = full payment
        """
        if self.__get_payment_type_variables().get(type) == None:
            raise SdkException('Wrong payment type. Use from constants')

        self.pg_payment_type = type
        return self

    def add_nomenclature_code(self, code):
        """
        Args:
            code (string): nomenclature product code in hex format
        """
        self.pg_nomenclature_code = code
        return self

    def add_agent(self, type, name, inn, phone):
        """
        Args:
            type (string): agent type
            name (string): agent name
            inn (string): agent inn
            phone (string): agent phone
        """
        if self.__get_agent_type_variables().get(type) == None:
            raise SdkException('Wrong agent type. Use from constants')

        self.pg_agent_type = type
        self.pg_agent_name = name
        self.pg_agent_inn = inn
        self.pg_agent_phone = phone
        return self

    def __get_vat_variables(self):
        return {'0' : True,'10' : True,'18' : True,'110' : True,'118' : True}

    def __get_type_variables(self):
        return {
            'product' : True,
            'product_excise' : True,
            'work' : True,
            'service' : True,
            'gambling_bet' : True,
            'gambling_win': True,
            'lottery_bet': True,
            'lottery_win': True,
            'rid': True,
            'payment': True,
            'commission': True,
            'composite': True,
            'other': True
        }

    def __get_payment_type_variables(self):
        return {
            'full_payment' : True,
            'pre_payment_full' : True,
            'pre_payment_part' : True,
            'advance' : True,
            'credit_part' : True,
            'credit_pay': True,
            'credit': True
        }

    def __get_agent_type_variables(self):
        return {
            'commissionaire': True,
            'bank_payment_agent': True,
            'bank_payment_subagent': True,
            'payment_agent': True,
            'payment_subagent': True,
            'agent': True,
            'solicitor': True
        }
        