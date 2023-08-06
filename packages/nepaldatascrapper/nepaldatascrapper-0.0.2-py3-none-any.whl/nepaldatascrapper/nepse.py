import requests
from enum import Enum


class NEPSE:

    class Issue(Enum):
        AUCTION = 1
        IPO = 2 
        FPO = 3 
        Right = 4
        Mutual = 5
        Debenture = 6 

    def __init__(self):
        pass

    def getData(self,symbol="",from_date="",to_date="",offset=1,limit=50):
        url  = "http://www.nepalipaisa.com/Modules/GraphModule/webservices/MarketWatchService.asmx/GetTodaySharePrices"
        postData = {"fromdate":from_date,"toDate":to_date,"stockSymbol":symbol,"offset":offset,"limit":limit}
        response = requests.post(url,json=postData)
        return response.json()["d"]

    def getShareInfo(self,symbol,info,from_date="",to_date="",offset=1,limit=50):
        return self.getData(symbol,from_date,to_date,offset,limit)[info]

    def getSharePrice(self,symbol,from_date="",to_date="",offset=1,limit=50):
        return [item["ClosingPrice"] for item in self.getData(symbol,from_date,to_date,offset,limit)]

    def getTodaysPrice(self):
        return self.getData()

    def getDividend(self, fiscalYear, symbol=None, sectorName="", offset=1, limit=50, sortBy="Company"):
        url = "http://www.nepalipaisa.com/Modules/CompanyProfile//Webservices/CompanyService.asmx/GetAllDividendData"
        postData = {"offset":offset, "limit":limit, "FiscalYear":fiscalYear, "SortBy":sortBy, "companyCode":symbol, "sectorName":sectorName}
        response = requests.post(url, json=postData)
        return response.json()["d"]

    def getInvestment(self,categoryID=Issue.IPO, symbol="", offset=1, limit=10):
        url = "http://www.nepalipaisa.com/Modules/Investment/webservices/InvestmentService.asmx/GetAllInvestmentInfobyCategoryID"
        postData = {"offset":offset,"limit":limit,"categoryID":categoryID.value,"portalID":"1","cultureCode":"en-US","StockSymbol":symbol}
        response = requests.post(url, json=postData)
        return response.json()["d"]



