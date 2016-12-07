#!/usr/bin/python
from pyalgotrade.optimizer import worker
import vwap_strategy

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    worker.run(vwap_strategy.VWAPMomentum,"192.168.1.10", 5001, workerName="localworker")

