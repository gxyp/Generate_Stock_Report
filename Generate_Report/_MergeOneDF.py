#!/usr/bin/python
# coding: utf-8 

import pandas as pd
import numpy as np
import _G3TF163 as gtf

def _YearMap(x):
	return x[:4]

def get3DF(stockNum):
	g3tf = gtf.G3TF163()
	g3tf.get3Table(stockNum)

	df = pd.read_csv(g3tf.getAssetsFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfA = df.T

	df = pd.read_csv(g3tf.getProfitsFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfP = df.T
	dfAll = dfA.join(dfP, lsuffix='_A', rsuffix='_P')
         
	df = pd.read_csv(g3tf.getMoneyFile(stockNum),encoding ='gb18030')
	df.set_index([' 报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfM = df.T
	dfAll = dfAll.join(dfM, lsuffix='_A', rsuffix='_M')

	df = pd.read_csv(g3tf.getZycwzbFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfZycwzb = df.T
	dfAll = dfAll.join(dfZycwzb, lsuffix='_A', rsuffix='_zycwzb')

	df = pd.read_csv(g3tf.getYynlFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfYynl = df.T
	dfAll = dfAll.join(dfYynl, lsuffix='_A', rsuffix='_Yynl')

	df = pd.read_csv(g3tf.getCznlFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfCznl = df.T
	dfAll = dfAll.join(dfCznl, lsuffix='_A', rsuffix='_Cznl')

	df = pd.read_csv(g3tf.getYlnlFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfYlnl = df.T
	dfAll = dfAll.join(dfYlnl, lsuffix='_A', rsuffix='_Ylnl')

	df = pd.read_csv(g3tf.getChnlFile(stockNum),encoding ='gb18030')
	df.set_index(['报告日期'],drop=True,append=False,inplace=True,verify_integrity=False)
	dfChnl = df.T
	dfAll = dfAll.join(dfChnl, lsuffix='_A', rsuffix='_Chnl')


	dfAll = dfAll.apply(pd.to_numeric, errors='coerce').fillna(0, downcast='infer')
	dfAll.rename(index = _YearMap,inplace = True)	
	return dfAll


def getRecentTrade(IsSH,stockNum):
	g3tf = gtf.G3TF163()
	g3tf.getLsjysjTable(IsSH,stockNum)
	df = pd.read_csv(g3tf.getLsjysjFile(stockNum),encoding ='gb18030')
	df['股票代码'] = df['股票代码'].apply(lambda x:x[-6:])
	df['总市值(亿)'] = df['总市值'] / 1E+8 
	df['流通市值(亿)'] = df['流通市值'] / 1E+8 
	df.drop(columns=['总市值','流通市值'],inplace=True)
	return df

def _SeasonMap(x):
	SS = x[5] + x[6]
	if SS == '12':
		ChangeS = 'Q4'
	elif SS == '09':
		ChangeS = 'Q3'
	elif SS == '06':
		ChangeS = 'Q2'
	elif SS == '03':
		ChangeS = 'Q1'
	else :
		ChangeS = 'xx'
	#return x[:4] + ChangeS 
	return x[2:4] + ChangeS 

def getSeasonDF(stockNum):
	g3tf = gtf.G3TF163()
	g3tf.getSeasonTable(stockNum)
	df = pd.read_csv(g3tf.getSeasonFile(stockNum),encoding='gb18030')
	df.rename(columns={'报告日期':'Quarterly_Report'},inplace=True)
	df.set_index(['Quarterly_Report'],drop=True,append=False,inplace=True,verify_integrity=False)
	df.rename(columns = _SeasonMap,inplace = True)	
	return df.iloc[:,0:10]     # 季节数据取最近10个

if __name__ == '__main__':
#	get3DF("600519").columns.to_series().to_csv('column_list.txt')
	print(get3DF("600519").head())
#	print(get3DF("600519").loc[0,'货币资金(万元)'])
#	print(getSeasonDF("600519").head())
	#print(getRecentTrade('0',"600519").to_markdown(index=False))

