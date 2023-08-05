from .base import BaseMeter, ZeroMeasurementsError
from .aggregators.batch import Average

class ExactMatch(BaseMeter):
    INVALID_BATCH_DIMENSION_MESSAGE = ('Expected both tensors have at less two '
                                       'dimension and same shape')
    INVALID_INPUT_TYPE_MESSAGE = 'Expected types (Tensor, LongTensor) as inputs'

    def __init__(self, aggregator=None):
        """ Constructor

        Arguments:
            size_average (bool): Average of batch size
        """
        self.aggregator = aggregator

        if self.aggregator is None:
            self.aggregator = Average()

        self.reset()

    def reset(self):
        self.result = self.aggregator.init()

    def _get_result(self, a, b):
        b = len(a)
        return a.view(b, -1) == b.view(b, -1)

    def measure(self, a, b):
        self.result = self.aggregator.combine(self.result,
                                              self._get_result(a, b))
