from __future__ import division
from datetime import datetime, timedelta
class TimeStamp:

    def totimestamp(self,dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        # return td.total_seconds()
        return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 
    def todate(self,timestamp):
        d = datetime.fromtimestamp(timestamp)
        return d