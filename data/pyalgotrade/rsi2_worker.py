#!/usr/bin/python
from pyalgotrade.optimizer import worker
import rsi2

# The if __name__ == '__main__' part is necessary if running on Windows.
if __name__ == '__main__':
    worker.run(rsi2.RSI2, "192.168.1.10", 5000, workerName="localworker")
<<<<<<< HEAD
=======

>>>>>>> 8af68b313b7f2adfb8f05e8597d906cc4c0877b3
