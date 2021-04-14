#Mehrdad Yazdanibiouki
#Eluvio coding challenge- Option 3-

###########################################################
# ********** Setup Parameters*********
#
# Set to a valid file name (e.g. items_lookup_input.txt) to read from file. Or set to empty
# to read batches (comma seperated IDs) from the command line
INPUT_FILE_NAME = ""

MAX_CONCURRENT_REQUESTS = 5
# I used local host for testing purposes
BASE_ITEM_INFO_URL = 'https://eluv.io/items/'
# BASE_ITEM_INFO_URL = 'http://localhost:3000/items?id='
ITEM_INFO_HEADERS = {'Authorization': 'Y1JGMmR2RFpRc211MzdXR2dLNk1UY0w3WGpI'}
############################################################

from item_fetcher import ItemFetcherUtil


def main():
    itemFetcher = ItemFetcherUtil()
    itemFetcher.initialize(MAX_CONCURRENT_REQUESTS, BASE_ITEM_INFO_URL, ITEM_INFO_HEADERS)

    if INPUT_FILE_NAME != "":
        batches = []
        with open(INPUT_FILE_NAME) as inputFile:
            batches = inputFile.read().splitlines()
        for batch in batches:
            itemIds = batch.split(',')
            itemInfos = itemFetcher.lookupItems(itemIds)
            for i in itemIds:
                assert i in itemInfos.keys()
                print("Item info for item ID " + i + ": " + itemInfos[i])
            print("============================================")
    else:
        while True:
            itemIdsStr = input("Please enter item Ids to look up (comma separated): ")
            if itemIdsStr == '':
                break
            itemIds = itemIdsStr.split(',')

            itemInfos = itemFetcher.lookupItems(itemIds)

            for i in itemIds:
                assert i in itemInfos.keys()
                print("Item info for item ID " + i + ": " + itemInfos[i])


if __name__ == '__main__':
    main()
