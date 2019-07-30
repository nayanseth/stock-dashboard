import requests
from requests.auth import HTTPBasicAuth
import urllib3
import json
import configparser
from datetime import datetime
import pytz


def executeRestApi(url, apiHeader):
	
	print ("\nREST API: {}\n".format(url))

	requestOperation = requests.get(url, headers=apiHeader, verify=False)
	return json.loads(requestOperation.content)

def writeForexData(fromCurrency, toCurrency, input):

	''' Alpha Vantage API Parser
	if "Realtime Currency Exchange Rate" in input:
		forexData = input["Realtime Currency Exchange Rate"]
		forexFile.write(forexData["1. From_Currency Code"] + " ({}),".format(forexData["2. From_Currency Name"]))
		forexFile.write(forexData["3. To_Currency Code"] + " ({}),".format(forexData["4. To_Currency Name"]))
		forexFile.write(forexData["5. Exchange Rate"] + ",")
		forexFile.write(forexData["6. Last Refreshed"] + ",")
		forexFile.write(forexData["7. Time Zone"] + ",")
		forexFile.write(forexData["8. Bid Price"] + ",")
		forexFile.write(forexData["9. Ask Price"] + "\n")
	'''

	if input["chart"]["error"] is not None:
		print ("Could not retrieve the forex exchange rate")
	else:
		forexMetaData = input["chart"]["result"][0]["meta"]
		exchangeTimeZone = forexMetaData["exchangeTimezoneName"]
		timestamp = input["chart"]["result"][0]["timestamp"][0]
		exchangeTime = datetime.fromtimestamp(timestamp, pytz.timezone(exchangeTimeZone))
		indicators = input["chart"]["result"][0]["indicators"]
		
		forexFile.write(fromCurrency + ",")
		forexFile.write(toCurrency + ",")
		forexFile.write(str(indicators["quote"][0]["close"][0]) + ",")
		forexFile.write(str(indicators["quote"][0]["open"][0]) + ",")
		forexFile.write(str(indicators["quote"][0]["high"][0]) + ",")
		forexFile.write(str(indicators["quote"][0]["low"][0]) + ",")
		forexFile.write(str(indicators["adjclose"][0]["adjclose"][0]) + ",")
		forexFile.write(exchangeTime.strftime("%d/%B/%Y") + ",")
		forexFile.write(exchangeTime.strftime("%H:%M:%S") + ",")
		forexFile.write(exchangeTimeZone + ",")
		forexFile.write(forexMetaData["exchangeName"] + "\n")
		
def writeCryptoCurrencyData(input, market):
	for cryptoData in input:
		cryptoCurrencyFile.write(cryptoData["price_date"] + ",")
		cryptoCurrencyFile.write(cryptoData["currency"] + ",")
		cryptoCurrencyFile.write(market + ",")
		cryptoCurrencyFile.write(cryptoData["price"] + ",")
		cryptoCurrencyFile.write(cryptoData["high"] + ",")
		cryptoCurrencyFile.write(cryptoData["circulating_supply"] + ",")
		cryptoCurrencyFile.write(cryptoData["market_cap"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["price_change"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["price_change_pct"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["volume"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["volume_change"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["volume_change_pct"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["market_cap_change"] + ",")
		cryptoCurrencyFile.write(cryptoData["1d"]["market_cap_change_pct"] + "\n")

def writeStockData(input):

	''' Alpha Vantage API Parser
	if "Error Message" in input:
		print "Error retrieving data for the Stock {}".format(stockSymbol)
	else:
		apiMetadata = input["Meta Data"]
		dailyTimeSeries = input["Time Series (Daily)"]
		for timestamp in dailyTimeSeries:
			stocksFile.write(timestamp + ",")
			if ":" in stockSymbol:
				stockMetadata = stockstockSymbol.split(":")
				market = stockMetadata[0]
				symbol = stockMetadata[1]
				stocksFile.write(symbol + ",")
				stocksFile.write(market + ",")
			else:
				stocksFile.write(stockSymbol + ",")
				stocksFile.write("NASDAQ" + ",")
			stocksFile.write(dailyTimeSeries[timestamp]["1. open"] + ",")
			stocksFile.write(dailyTimeSeries[timestamp]["2. high"] + ",")
			stocksFile.write(dailyTimeSeries[timestamp]["3. low"] + ",")
			stocksFile.write(dailyTimeSeries[timestamp]["4. close"] + ",")
			stocksFile.write(dailyTimeSeries[timestamp]["5. volume"] + ",")
			stocksFile.write(apiMetadata["3. Last Refreshed"] + ",")
			stocksFile.write(apiMetadata["5. Time Zone"] + "\n")
			break
	'''

	if input["quoteSummary"]["error"] is not None:
		print ("Could not retrieve the forex exchange rate")
	else:
		stockStatistics = input["quoteSummary"]["result"][0]["summaryDetail"]
		stockMetadata = input["quoteSummary"]["result"][0]["price"]
		stocksFile.write(stockMetadata["symbol"] + ",")
		stocksFile.write(stockMetadata["longName"] + ",")
		stocksFile.write(stockMetadata["exchangeName"] + ",")
		if stockStatistics["regularMarketPreviousClose"]:
			stocksFile.write(str(stockStatistics["regularMarketPreviousClose"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["regularMarketOpen"]:
			stocksFile.write(str(stockStatistics["regularMarketOpen"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["regularMarketDayHigh"]:
			stocksFile.write(str(stockStatistics["regularMarketDayHigh"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["regularMarketDayLow"]:
			stocksFile.write(str(stockStatistics["regularMarketDayLow"]["raw"]))
		stocksFile.write(",")
		if stockMetadata["regularMarketPrice"]:
			stocksFile.write(str(stockMetadata["regularMarketPrice"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["dividendRate"]:
			stocksFile.write(stockStatistics["dividendRate"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["dividendYield"]:
			stocksFile.write(stockStatistics["dividendYield"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["exDividendDate"]:
			stocksFile.write(stockStatistics["exDividendDate"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["payoutRatio"]:
			stocksFile.write(stockStatistics["payoutRatio"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["fiveYearAvgDividendYield"]:
			stocksFile.write(stockStatistics["fiveYearAvgDividendYield"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["beta"]:
			stocksFile.write(stockStatistics["beta"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["trailingPE"]:
			stocksFile.write(stockStatistics["trailingPE"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["forwardPE"]:
			stocksFile.write(stockStatistics["forwardPE"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["regularMarketVolume"]:
			stocksFile.write(stockStatistics["regularMarketVolume"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["averageVolume10days"]:
			stocksFile.write(stockStatistics["averageVolume10days"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["bid"]:
			stocksFile.write(str(stockStatistics["bid"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["ask"]:
			stocksFile.write(str(stockStatistics["ask"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["bidSize"]:
			stocksFile.write(str(stockStatistics["bidSize"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["askSize"]:
			stocksFile.write(str(stockStatistics["askSize"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["marketCap"]:
			stocksFile.write(stockStatistics["marketCap"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["fiftyTwoWeekLow"]:
			stocksFile.write(str(stockStatistics["fiftyTwoWeekLow"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["fiftyTwoWeekHigh"]:
			stocksFile.write(str(stockStatistics["fiftyTwoWeekHigh"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["fiftyDayAverage"]:
			stocksFile.write(str(stockStatistics["fiftyDayAverage"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["twoHundredDayAverage"]:
			stocksFile.write(str(stockStatistics["twoHundredDayAverage"]["raw"]))
		stocksFile.write(",")
		if stockStatistics["priceToSalesTrailing12Months"]:
			stocksFile.write(stockStatistics["priceToSalesTrailing12Months"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["trailingAnnualDividendRate"]:
			stocksFile.write(stockStatistics["trailingAnnualDividendRate"]["fmt"])
		stocksFile.write(",")
		if stockStatistics["trailingAnnualDividendYield"]:
			stocksFile.write(stockStatistics["trailingAnnualDividendYield"]["fmt"])
		stocksFile.write(",")
		
		stocksFile.write(stockMetadata["currency"])
		#stocksFile.write(",")
		#if stockStatistics["trailingAnnualDividendRate"]:
		#	stocksFile.write(stockStatistics["trailingAnnualDividendRate"]["fmt"])
		stocksFile.write("\n")

def getForexData():
	forexFile.write("From Currency, To Currency, Close, Open, High, Low, Adjusted Close, Date, Last Refreshed, Time Zone, Exchange Name\n")
	
	fromCurrencyList = preferences.get("FOREX","fromCurrencyList").strip().split(",")
	toCurrencyList = preferences.get("FOREX","toCurrencyList").strip().split(",")
	
	for fromCurrency in fromCurrencyList:
		for toCurrency in toCurrencyList:
			apiUrl = forexApi.format(fromCurrency, toCurrency)
			writeForexData(fromCurrency, toCurrency, executeRestApi(apiUrl,apiHeader))

def getCryptoCurrencyData():
	cryptoCurrencyFile.write("Date, From Currency, To Currency, Price, High, Circulating Supply, Market Cap, Price Change, Price Change %, Volume, Volume Change, Volume Change %, Market Cap Change, Market Cap Change %\n")

	marketList = preferences.get("CRYPTOCURRENCY","marketList").strip().split(",")
	cryptoCurrencies = preferences.get("CRYPTOCURRENCY","cryptoCurrencyList").strip()

	for market in marketList:
		apiUrl = cryptoCurrencyApi.format(cryptoCurrencies, market)
		writeCryptoCurrencyData(executeRestApi(apiUrl, apiHeader), market)


def getStocksData():
	stocksFile.write("Stock Symbol, Long Name, Exchange, Regular Market Previous Close, Regular Market Open, Regular Market High, Regular Market Low, Regular Market Price, Dividend Rate, Dividend Yield, Ex Dividend Date, Payout Ratio, 5 Yr Avg Dividend Yield, Beta, Trailing PE, Forward PE, Regular Market Volume, Avg Volume 10 Days, Bid, Ask, Bid Size, Ask Size, Market Cap, 52 Wk Low, 52 Wk High, 50 Day Avg, 200 Day Avg, Price to Sales Trailing 12 Months, Trailing Annual Dividend Rate, Trailing Annual Dividend Yield, Currency,  Time Zone\n")
	stocksList = preferences.get("STOCKS","stocksList").strip().split(",")
	
	for stock in stocksList:
		apiUrl = stocksApi.format(stock)
		writeStockData(executeRestApi(apiUrl,apiHeader))


if __name__ == "__main__":

	preferences = configparser.ConfigParser()

	preferences.read("preferences.ini")
	
	# Ignore Warnings

	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

	# ALPHA VANTAGE API KEY

	apiKey = preferences.get("ALPHAVANTAGE","apiKey").strip()
	nomicsApiKey = preferences.get("NOMICS", "apiKey").strip()

	# Alpha Vantage APIs

	alphaVantageForexApi = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=" + apiKey
	alphaVantageCryptoCurrencyApi = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={}&market={}&apikey=" + apiKey
	alphaVantageStocksApi = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=" + apiKey

	# Yahoo Finance APIs

	#forexApi = "https://query1.finance.yahoo.com/v8/finance/chart/{}{}=X"
	forexApi = "https://query1.finance.yahoo.com/v8/finance/chart/{}{}=X?includePrePost=false&interval=1d&range=1d"
	cryptoCurrencyApi = "https://api.nomics.com/v1/currencies/ticker?ids={}&interval=1d&convert={}&key=" + nomicsApiKey
	stocksApi = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?modules=price%2CsummaryDetail"


	# Common API Header Parameters

	apiHeader = {"Content-Type": "application/json"}

	forexFile = open("forex.csv", "w")
	stocksFile = open("stocks.csv", "w")


	getForexData()
	forexFile.close()
	getStocksData()
	stocksFile.close()
	if nomicsApiKey != "null" and nomicsApiKey != "":
		cryptoCurrencyFile = open("crypto.csv", "w")
		getCryptoCurrencyData()
		cryptoCurrencyFile.close()
	