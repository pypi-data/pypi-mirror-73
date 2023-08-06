import heapq
#import logging
from datetime import datetime, timezone

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
#_logger = logging.getLogger(__name__)


class NBest(object):

    def __init__(self, size, minimize=False):
        self.items = {}
        self.item_list = []
        self.size = size
        self.item_hash = None
        self.floor = None
        self.minimize = minimize

    def set_item_hash(self, hashfn):
        self.item_hash = hashfn

    def insert(self, item, value):
        """
        Just do insertion sort.  Probably most efficient for nbest
        of small size.
        """
        coeff = +1
        if self.minimize:
            coeff = -1
        if self.floor is not None and coeff * value < self.floor:
            return False
        if self.item_hash is None:
            key = item
        else:
            key = self.item_hash(item)
#        _logger.info("Looking for %s" % key)
        inserted = False
        record = (key, item, value, datetime.now(timezone.utc))
        for i, entry in enumerate(self.item_list):
            if key == entry[0]:
                return False
            if coeff * value > coeff * entry[2]:
                self.item_list.insert(i, record)
                inserted = True
                break
        if len(self.item_list) < self.size and not inserted:
            self.item_list.append(record)
            inserted = True
        self.items[key] = record
        while len(self.item_list) > self.size:
            self.item_list.pop()
        if len(self.item_list) == self.size:
            self.floor = coeff * self.item_list[-1][2]
        return inserted

    def _item_value(self, item, include_scores=False, include_timestamps=False):
        key, thing, value, timestamp = item
        if include_scores:
            if include_timestamps:
                return (value, thing, timestamp)
            else:
                return (value, thing)
        elif include_timestamps:
            return (thing, timestamp)
        else:
            return thing

    def result(self, include_scores=False, include_timestamps=False):
        return [ self._item_value(item, include_scores, include_timestamps) 
                 for item in self.item_list ]

    def all_items(self, include_scores=False, include_timestamps=False):
        return [ self._item_value(item, include_scores, include_timestamps) 
                 for item in self.items.values() ]

        

    def __len__(self):
        return len(self.item_list)


class NBestOld(object):
    
    def __init__(self, size):
        self.heap = []
        self.items = {}
        self.size = size
        self.item_hash = None

    def set_item_hash(self, hashfn):
        self.item_hash = hashfn

    def insert(self, item, value):
        if len(self.heap) >= self.size and value < self.heap[0][0]:
            return
        if self.item_hash is None:
            heapq.heappush(self.heap, (value, item))
        else:
            # Don't insert an already stored value
            if self.item_hash(item) in self.items:
                return
            heapq.heappush(self.heap, (value, item))
            self.items[ self.item_hash(item) ] = (value, item)
        while len(self.heap) > self.size:
            hitem = heapq.heappop(self.heap)
            if self.item_hash is not None:
                del self.items[ self.item_hash(hitem[1]) ]
        # Need to repair
        if self.item_hash is not None and len(self.items) != len(self.heap):
            self.items = {}
            for value, item in self.heap:
                self.items[ self.item_hash(item) ] = (value, item)
                

    def result(self, include_scores=False):
        temp = []
        res = []
        temp[:] = self.heap
        while True:
            try:
                item = heapq.heappop(temp)
                if include_scores:
                    res.insert(0, item)
                else:
                    res.insert(0, item[1])
            except:
                break
        return res


    def __len__(self):
        return len(self.heap)

