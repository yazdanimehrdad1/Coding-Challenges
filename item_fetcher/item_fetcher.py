from threading import Thread
from queue import Queue
import requests


class RequestWorker(Thread):
    # A RequestWorker creates a thread that pulls requests off the given request queue and processes them
    def __init__(self, requestQueue, responseQueue):
        Thread.__init__(self)
        self.daemon = True
        self.requestQueue = requestQueue
        self.responseQueue = responseQueue

    def run(self):
        # The thraed blocks until there is a request in the queue for it to process.
        # Then it makes the HTTP request and puts the response into the resposne queue
        # and tells the queue that the processign of that request is completed
        while True:
            reqId, reqUrl, reqHeaders = self.requestQueue.get()
            try:
                response = requests.get(reqUrl, headers=reqHeaders)
                self.responseQueue.put((reqId, response.text))
            finally:
                self.requestQueue.task_done()


class ItemFetcherUtil:

    def __init__(self):
        self.itemCache = {}
        self.requestQueue = Queue()
        self.responseQueue = Queue()
        self.baseUrl = ""
        self.headers = {}
        self.running = False

    def initialize(self, maxConcurrentReqs, baseUrl, headers):
        self.baseUrl = baseUrl
        self.headers = headers

        # Create the worker threads and get them running. They'll all just block
        # waiting for requests to be placed in the request queue
        for i in range(maxConcurrentReqs):
            w = RequestWorker(self.requestQueue, self.responseQueue)
            w.start()

        # the request fetcher is running and ready to take requests
        self.running = True

    def lookupItems(self, itemIds):
        # This method will block until all the item infos are available and will then
        # return a dictionary of the item infos.
        # An asynchronous version might be desired if we don't want the calling client to block.
        # In that case a callback would be provided by the client and it would get notified when
        # the results are ready. We may also desire to get the response for each item as soon as
        # it's available, in which case a callback for each item would need to be supplied.

        if self.running == False:
            print("Error: ItemFetcherUtil has not been initialized.")
            return None

        for i in itemIds:
            # For any items not in the cache, add a request to the request queue
            if i not in self.itemCache:
                # Not in cache, so add a placeholder to the cache to avoid generating duplicate requests
                # in case there are duplicate IDs in the batch. Then add a request to the request queue
                self.itemCache[i] = ""
                fetchUrl = self.baseUrl + str(i)
                self.requestQueue.put((i, fetchUrl, self.headers))

        # Call join to ensure that all requests in the queue have been processed. Then add all the
        # responses to the cache
        self.requestQueue.join()

        while not self.responseQueue.empty():
            itemId, itemInfo = self.responseQueue.get()
            self.itemCache[itemId] = itemInfo

        # Now the data for all the requested item IDs must be in the cache. Just return a dictionary
        # of the items
        itemInfos = {}
        for i in itemIds:
            assert i in self.itemCache.keys()
            itemInfos[i] = self.itemCache[i]

        return itemInfos
