#!/usr/bin/python
# coding: utf-8

import requests
import datetime

class G3TF163:

	url163head = "http://quotes.money.163.com/service/"
	url163tail = ".html"
	url163tailyear = ".html?type=year"
	url163yynltailyear = url163tailyear + "&part=yynl"
	url163cznltailyear = url163tailyear + "&part=cznl"
	url163ylnltailyear = url163tailyear + "&part=ylnl"
	url163chnltailyear = url163tailyear + "&part=chnl"

	localpathhead = "./tmp/"
	localpathtail = ".csv"

	def _getPath(self,tabletype,stockNum,urlhead,urltail):
		stockName = tabletype + stockNum
		path = urlhead + stockName + urltail
		return path
	
	def _getAssetsTable(self,stockNum):
		StockUrl = self._getPath("zcfzb_",stockNum,self.url163head,self.url163tailyear)
		localfile = self.getAssetsFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)
	
	def _getProfitsTable(self,stockNum):
		StockUrl = self._getPath("lrb_",stockNum,self.url163head,self.url163tailyear)
		localfile = self.getProfitsFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)
	
	def _getMoneyTable(self,stockNum):
		StockUrl = self._getPath("xjllb_",stockNum,self.url163head,self.url163tailyear)
		localfile = self.getMoneyFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	def _getZycwzbTable(self,stockNum):
		StockUrl = self._getPath("zycwzb_",stockNum,self.url163head,self.url163tailyear)
		localfile = self.getZycwzbFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)


	def _getYynlTable(self,stockNum):
		StockUrl = self._getPath("zycwzb_",stockNum,self.url163head,self.url163yynltailyear)
		localfile = self.getYynlFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	def _getCznlTable(self,stockNum):
		StockUrl = self._getPath("zycwzb_",stockNum,self.url163head,self.url163cznltailyear)
		localfile = self.getCznlFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	def _getYlnlTable(self,stockNum):
		StockUrl = self._getPath("zycwzb_",stockNum,self.url163head,self.url163ylnltailyear)
		localfile = self.getYlnlFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	def _getChnlTable(self,stockNum):
		StockUrl = self._getPath("zycwzb_",stockNum,self.url163head,self.url163chnltailyear)
		localfile = self.getChnlFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	def getLsjysjTable(self,IsSH,stockNum):
		today = datetime.date.today()
		todaym5 = today - datetime.timedelta(days=5) 	
		ftoday = today.strftime("%Y%m%d")
		ftodaym5 = todaym5.strftime("%Y%m%d")

		StockUrl  = "http://quotes.money.163.com/service/chddata.html?code="
		StockUrl = StockUrl + IsSH + stockNum
		StockUrl = StockUrl + "&start=" + ftodaym5
		StockUrl = StockUrl + "&end=" + ftoday
		StockUrl = StockUrl + "&fields=TCLOSE;HIGH;LOW;TOPEN;TCAP;MCAP" 

		localfile = self.getLsjysjFile(stockNum)
		r = requests.get(StockUrl) 
		with open(localfile, "wb") as code:
	        	code.write(r.content)

	
	def get3Table(self,stockNum):
		self._getAssetsTable(stockNum) 
		self._getProfitsTable(stockNum) 
		self._getMoneyTable(stockNum) 
		self._getZycwzbTable(stockNum) 
		self._getYynlTable(stockNum)
		self._getCznlTable(stockNum)
		self._getYlnlTable(stockNum)
		self._getChnlTable(stockNum)

	def getAssetsFile(self,stockNum):
		return self._getPath("assets_",stockNum,self.localpathhead,self.localpathtail)
	
	def getProfitsFile(self,stockNum):
		return self._getPath("profits_",stockNum,self.localpathhead,self.localpathtail)
	
	def getMoneyFile(self,stockNum):
		return self._getPath("money_",stockNum,self.localpathhead,self.localpathtail)
	
	def getZycwzbFile(self,stockNum):
		return self._getPath("zycwzb_",stockNum,self.localpathhead,self.localpathtail)

	def getYynlFile(self,stockNum):     # 盈利能力
		return self._getPath("yynl_",stockNum,self.localpathhead,self.localpathtail)
	
	def getCznlFile(self,stockNum):    # 成长能力 
		return self._getPath("cznl_",stockNum,self.localpathhead,self.localpathtail)

	def getYlnlFile(self,stockNum):    # 盈利能力
		return self._getPath("ylnl_",stockNum,self.localpathhead,self.localpathtail)

	def getChnlFile(self,stockNum):    # 偿还能力
		return self._getPath("chnl_",stockNum,self.localpathhead,self.localpathtail)

	def getLsjysjFile(self,stockNum):    # 历史交易数据
		return self._getPath("lsjysj_",stockNum,self.localpathhead,self.localpathtail)

if __name__ == '__main__':
#	print(G3TF163().getAssetsFile("600519"))
#	G3TF163().getLsjysjTable('0',"600519")
	stockNum = '600519'
	StockUrl =G3TF163()._getZycwzbTable(stockNum)

