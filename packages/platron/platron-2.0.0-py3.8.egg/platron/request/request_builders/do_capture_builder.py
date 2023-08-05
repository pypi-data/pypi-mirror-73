from platron.request.request_builders.request_builder import RequestBuilder
from platron.sdk_exception import SdkException
from platron.request.data_objects.long_record import LongRecord

class DoCaptureBuilder(RequestBuilder):
    '''
    Do capture API request
    '''

    def __init__(self, payment):
        """
        Args:
            payment (string): platron payment id
        """
        self.pg_payment_id = payment
       
    def add_long_record(self, long_record):
        """Add lond record to capture
        Args:
            long_record (LongRecord): long record params
        """
        if type(long_record) != LongRecord:
            raise SdkException('Only long record object expected')
        
        long_record_params = long_record.get_params()
        for param_name in long_record_params.keys():
            setattr(self, param_name, long_record_params.get(param_name))
    
    def get_url(self):
        return self.PLATRON_URL + 'do_capture.php' 