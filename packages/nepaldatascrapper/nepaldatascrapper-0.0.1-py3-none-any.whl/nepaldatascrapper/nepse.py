import requests

class NEPSE:
    def __init__(self):
        self.sources = ["http://www.nepalipaisa.com/Modules/GraphModule/webservices/MarketWatchService.asmx/GetTodaySharePrices"]

    def getData(self,symbol="",from_date="",to_date="",offset=1,limit=50):
        postData = {"fromdate":from_date,"toDate":to_date,"stockSymbol":symbol,"offset":offset,"limit":limit}
        response = requests.post(self.sources[0],json=postData)
        return response.json()["d"]

    def getShareInfo(self,symbol,info,from_date="",to_date="",offset=1,limit=50):
        return self.getData(symbol,from_date,to_date,offset,limit)[info]

    def getSharePrice(self,symbol,from_date="",to_date="",offset=1,limit=50):
        return [item["ClosingPrice"] for item in self.getData(symbol,from_date,to_date,offset,limit)]

    def getTodaysPrice(self):
        return self.getData()

    def getDividend(self):
        pass


if __name__ == "__main__":
    nepse = NEPSE()
    print(nepse.getSharePrice("BPCL",limit=1))

