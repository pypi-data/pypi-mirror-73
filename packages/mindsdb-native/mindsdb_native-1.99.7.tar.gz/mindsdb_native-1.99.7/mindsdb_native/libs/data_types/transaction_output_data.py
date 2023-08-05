from mindsdb_native.libs.constants.mindsdb import *

from mindsdb_native.libs.data_types.mindsdb_logger import log
from mindsdb_native.libs.data_types.transaction_output_row import TransactionOutputRow


class TrainTransactionOutputData():
    def __init__(self):
        self.data_frame = None
        self.columns = None


class PredictTransactionOutputData():
    def __init__(self, transaction, data):
        self.data = data
        self.transaction = transaction
        self.input_confidence = None
        self.extra_insights = None

    def __iter__(self):
        for i, value in enumerate(self.data[self.transaction.lmd['columns'][0]]):
            yield TransactionOutputRow(self, i)

    def __getitem__(self, item):
        return TransactionOutputRow(self, item)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data[self.transaction.lmd['columns'][0]])
