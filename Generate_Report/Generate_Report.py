#!/usr/bin/python
# coding: utf-8


import sys
import numpy as np
import pandas as pd
import datetime
import configparser
import os
import base64
import matplotlib.pyplot as plt

import _MergeOneDF as M1DF

Print2File= True

#plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "stock.ini")
tmpfold = os.path.join(curpath, "tmp")

if not os.path.exists(tmpfold):
    os.mkdir(tmpfold)

conf = configparser.ConfigParser()
conf.read(cfgpath, encoding="utf-8")
sections = conf.sections()

stockNum = conf.get('default','stock_code')    
IsSH = conf.get('default','IsSH')    
countYear = int(conf.get('default','defaultCount'))

today = datetime.date.today().strftime('%Y-%m-%d')      

dfTrade = M1DF.getRecentTrade(IsSH,stockNum)
dfSeason = M1DF.getSeasonDF(stockNum)

a = dfTrade.loc[0,'名称']

def _ParseDataFrame(df):
    #111111111111111
    df['股东权益(亿)'] = df['所有者权益(或股东权益)合计(万元)'] / 1E+4
    df['资产周转率(%)'] = df['营业总收入(万元)'] / df['资产总计(万元)']* 100
    df['利润率(%)'] = df['净利润(万元)_A'] / df['营业总收入(万元)'] * 100
    df['财务杠杆(%)'] = ( 100 / df['股东权益比率(%)'] ) * 100 

    #22222222222222
    df['营业收入(亿)'] = df['营业收入(万元)'] / 1E+4 
    df['归母净利润(亿)'] = df['归属于母公司所有者的净利润(万元)'] / 1E+4 
    df['净利润(亿)'] = df['净利润(万元)_A'] / 1E+4 

    #33333333333333333
    df['负债合计(亿)'] = df['负债合计(万元)'] / 1E+4
    df['资产合计(亿)'] = df['资产总计(万元)'] / 1E+4
    #有息负债 = 短期借款 + 应付利息 + 一年内到期的非流动负债 + 长期借款 + 应付债券 + 长期应付款
    df['有息负债(万)'] =  df['短期借款(万元)'] + df['应付利息(万元)']
    df['有息负债(万)'] =  df['有息负债(万)'] + df['一年内到期的非流动负债(万元)']
    df['有息负债(万)'] =  df['有息负债(万)'] + df['长期借款(万元)']
    df['有息负债(万)'] =  df['有息负债(万)'] + df['应付债券(万元)']
    df['有息负债(万)'] =  df['有息负债(万)'] + df['长期应付款(万元)']
    df['有息负债(亿)'] =  df['有息负债(万)'] / 1E+4
    #货币资金 = 现金 + 银行理财产品（有可能在其他流动资产科目也有可能在交易性金融资产科目）
    df['准货币资金(万)'] = df['货币资金(万元)'] + df['交易性金融资产(万元)']
    df['准货币资金(万)'] = df['准货币资金(万)'] + df['其他流动资产(万元)']
    df['准货币资金(亿)'] =  df['准货币资金(万)'] / 1E+4
    df['财务费用(亿)'] =  df['财务费用(万元)'] / 1E+4

    #4444444444444444444
    df['应付预收(万)'] = df['应付票据(万元)'] + df['应付账款(万元)'] + df['预收账款(万元)']
    df['应付预收(亿)'] = df['应付预收(万)'] / 1E+4

    df['应收预付(万)'] = df['应收票据(万元)'] + df['应收账款(万元)'] + df['预付款项(万元)']
    df['应收预付(亿)'] = df['应收预付(万)'] / 1E+4

    df['应收款比总收入(%)'] = df['应收账款(万元)'] / df['营业总收入(万元)'] * 100
    df['应收款比总资产(%)'] = df['应收账款(万元)'] / df['资产总计(万元)'] * 100
    df['库存比总资产(%)'] = df['存货(万元)'] / df['资产总计(万元)'] * 100

    #555555555
    df['准固定资产(万)'] = df['固定资产(万元)'] + df['在建工程(万元)'] + df['工程物资(万元)']
    df['准固定资产(亿)'] = df['准固定资产(万)'] / 1E+4

    df['准固定资产占比(%)'] = df['准固定资产(万)'] / df['资产总计(万元)'] * 100

    #666666666
    df['营业利润(亿)'] = df['营业利润(万元)_A'] / 1E+4
    df['税前利润生产资产占比(%)'] = df['营业利润(亿)'] / df['准固定资产(亿)'] * 100

    #888888
    df['交易性金融资产(亿)'] = df['交易性金融资产(万元)'] / 1E+4
    df['买入返售金融资产(亿)'] = df['买入返售金融资产(万元)'] / 1E+4
    df['可供出售金融资产(亿)'] = df['可供出售金融资产(万元)'] / 1E+4
    df['其他流动资产(亿)'] = df['其他流动资产(万元)'] / 1E+4
    df['持有至到期投资(亿)'] = df['持有至到期投资(万元)'] / 1E+4
    df['投资性房地产(亿)'] = df['投资性房地产(万元)'] / 1E+4
    df['长期股权投资(亿)'] = df['长期股权投资(万元)'] / 1E+4

    #999999
    df['毛利润(万)'] = df['营业收入(万元)'] - df['营业成本(万元)']
    df['毛利润率(%)'] = df['毛利润(万)'] / df['营业收入(万元)'] * 100
    #这里要去看看书
    df['老唐营业利润(万)'] = df['营业利润(万元)_A'] - df['公允价值变动收益(万元)'] - df['投资收益(万元)_A']
    df['销售占毛利润(%)'] = df['销售费用(万元)'] / df['毛利润(万)'] * 100
    df['管理占毛利润(%)'] = df['管理费用(万元)'] / df['毛利润(万)'] * 100
    df['财务占毛利润(%)'] = df['财务费用(万元)'] / df['毛利润(万)'] * 100
    df['老唐营业利润率(%)'] = df['老唐营业利润(万)'] / df['营业收入(万元)'] * 100
    df['收到现金比收入(%)'] = df[' 销售商品、提供劳务收到的现金(万元)'] / df['营业收入(万元)'] * 100
    df['经营余额比利润(%)'] = df[' 经营活动产生的现金流量净额(万元)'] / df['净利润(万元)_A'] * 100

    #10  10  10  10  10
    df['经营活动现金流净值(亿)'] = df[' 经营活动产生的现金流量净额(万元)'] / 1E+4
    df['构建资产支付的现金(亿)'] = df[' 购建固定资产、无形资产和其他长期资产所支付的现金(万元)'] / 1E+4
    df['投资活动现金流净值(亿)'] = df[' 投资活动产生的现金流量净额(万元)'] / 1E+4
    df['筹措活动现金流净值(亿)'] = df[' 筹资活动产生的现金流量净额(万元)'] / 1E+4

    #11  11  11  11  11
    df['分红金额(亿)'] = (df[' 分配股利、利润或偿付利息所支付的现金(万元)'] - df[' 其中：子公司支付给少数股东的股利、利润(万元)']) / 1E+4
    #df['分红占归母净利润比(%)'] = df['分红金额(亿)'] / df['归母净利润(亿)'] * 100

if Print2File == True :
    fname = a + '(' + stockNum + ')--' + today + '.md'
    f = open(fname,"w")
    __console__= sys.stdout
    sys.stdout = f

print("# 股票分析")
print('## 前言')
print('>采用markdown的方式输出本文，方便做注释和校对，然后生成pdf，半年，一年，甚至两三年后可以回看这些判断是否正确。\n')
print('>对于打算买入的一只股票来讲，请牢记巴老先生的"四只脚"投资标准,①我们能够了解。②良好的经济前景。③德才兼备的管理人。④吸引人的价格。')
print('>下面所做的基本面分析仅仅是用来排除的，当计划买入的时候，请再次考虑上面的四个条件是否满足')
print('\n')

print('## 近期数据 %s    ---  %s' %(a, stockNum))
print (dfTrade.to_markdown(index=False,floatfmt=".2f"))

print('### 公司简介')
print('\n')
print('\n')

dfFdata = M1DF.get3DF(stockNum)
countYear = dfFdata.shape[0] if countYear > dfFdata.shape[0] else countYear
currentYear = int(dfFdata.index.to_series()[0][:4]) + 1
_ParseDataFrame(dfFdata)
# 输出公司描述信息。
print('## 企业财报分析')
print('----')

print('1. ROE')
print('> 如果只能选择一个指标的话，ROE就是巴老的选择。 我们尽量选取持续ROE>15%的优秀公司。')
print('> 同时展开杜邦分析，看利润来自哪里:  利润率，资产周转率，财务杠杆？')
print('> 高分红也容易维持高的ROE, 这时要看净资产的增长速度')
print('\n')

dfshow = dfFdata[['净资产收益率加权(%)','利润率(%)','资产周转率(%)','财务杠杆(%)','股东权益(亿)','净资产增长率(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#----------------------------------------------------------------------------------

print('2. 企业经营分析')
print('> 主要看销售额和净利润是否在稳步增长\n')

dfshow = dfFdata[['营业收入(亿)','主营业务收入增长率(%)','归母净利润(亿)','净利润增长率(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('3. 资产负债表分析')
print('> 通过总资产粗略判断公司的整体实力及扩张能力')
print('> 建议: 准货币资金 - 有息负债总额 > 0')
print('> 通过资产负债率分析公司债务风险，基于公司有息负债，现金情况和财务费用来分析公司偿还能力，以及造假可能')
print('> 想想存贷双高的康美，')
print('\n')

dfshow = dfFdata[['负债合计(亿)','资产合计(亿)','有息负债(亿)','准货币资金(亿)','财务费用(亿)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('4. 通过比较“应付预收”和“应收预付”来分析公司的行业地位')
print('> 应付预收（应付票据+应付账款+预收款项） - 应收预付（应收票据+应收账款+预付款项）＞0')
print('> “应收账款”/“营业收入”占比，趋势')
print('> “应收账款”/“资产合计”占比，趋势. 占比大于20%的要去查年报')
print('> “库存”/“资产合计”占比，趋势. 占比大于20%的要去查年报')
print('> 1年期的应收账款/应收账款总额至少要＞70%，这个目前没有代码接口，需要自行查年报 \n')

dfshow = dfFdata[['应付预收(亿)','应收预付(亿)','应收款比总收入(%)','应收款比总资产(%)','库存比总资产(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('5. 通过准固定资产分析公司的资产类型')
print('> 准固定资产（固定资产+在建工程+工程物资）与总资产的比率＞40% 一般为重资产行业')
print('> 对于重资产行业，要看行业趋势，对于行业高增长阶段，价格又足够低，是可以考虑的 \n')

dfshow = dfFdata[['准固定资产(亿)','资产合计(亿)','准固定资产占比(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('6. 按照老唐新手财page173算轻重')
print('> 生产资产 = （固定资产+在建工程+工程物资） ------  无形资产里面土地资产没有接口，所以没有计算')
print('> "当年税前利润总额 / 生产资产" 和社会平均资本回报率(银行贷款的两倍 12%) 的关系 \n')

dfshow = dfFdata[['营业利润(亿)','准固定资产(亿)','税前利润生产资产占比(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('7. 通过流动比和速动比看公司短期偿债能力')
print('> 流动比率=流动资产合计/流动负债合计 建议> 2')
print('> 流动比率=速动资产合计(流动资产 - 库存)/流动负债合计 建议 > 1\n')

dfshow = dfFdata[['流动比率(%)','速动比率(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('8. 通过投资类资产分析公司对主业的专注程度')
print('> 对于主业非投资类公司，显然这项越少越好\n')

dfshow = dfFdata[['交易性金融资产(亿)','买入返售金融资产(亿)','其他流动资产(亿)','可供出售金融资产(亿)', \
                  '持有至到期投资(亿)','投资性房地产(亿)','长期股权投资(亿)','资产合计(亿)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('9. 通过毛利率，费用占比看公司，行业的位置和管理能力')
print('> 我们希望选取毛利率高的公司。>40% ')
print('> 我们希望选取三费低的公司。这才能体现出优秀的管理能力 ')
print('> page 226 财务费率为负不计入， 三费占毛利润 < 30% 为**优秀的企业**。 如果 >70%， **通常而言，关注价值不大**')
print('> page 228 面对营业利润率数据，投资者不仅要看数字大小，更要对比历史变化。营业利润率上升了，要看主要是因为售价提升，成本下降，还是费用控制得力')
print('> 对于能收上来钱的公司才是好公司，所以后两项最好都能够 >100% ')
print('\n')

dfshow = dfFdata[['毛利润率(%)','销售占毛利润(%)','管理占毛利润(%)','财务占毛利润(%)', \
                  '老唐营业利润率(%)','收到现金比收入(%)','经营余额比利润(%)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------

print('10. 通过经营现金流的净值和投资支付的现金看企业的近似自由现金流')
print('> 三个活动现金流净值表')
print('> +--  挣钱， 扩张，分红。 奶牛型， 关注可持续性')
print('> ++-  挣钱， 股利 or 卖家当，分红。 老母鸡型， 低PE高股息率')
print('> +-+  挣钱， 扩张，筹钱。 蛮牛型，关注项目前景，资金是否足够支持')
print('> 其他的就不要考虑了，惹不起躲的起！')
print('\n')

dfshow = dfFdata[['归母净利润(亿)','经营活动现金流净值(亿)','构建资产支付的现金(亿)','投资活动现金流净值(亿)','筹措活动现金流净值(亿)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')
#---------------------------------------------------------------------------------------
print('11. 分红数据, 是从下一年的筹措数据里面抓出来的，所以会错一年???')
#dfshow = dfFdata[['归母净利润(亿)','分红金额(亿)','分红占归母净利润比(%)']].T
dfshow = dfFdata[['归母净利润(亿)','分红金额(亿)']].T
print (dfshow.iloc[:,0:countYear].sort_index(axis=1).to_markdown(floatfmt=".2f"))
print('评论：\n')
print('---')


print('12. 应Mr. He要求，增加季度数据')
dfSeasonM = dfSeason.loc[['主营业务收入(万元)','主营业务利润(万元)','净利润(万元)'],:].T
dfSeasonM = dfSeasonM.apply(pd.to_numeric, errors='coerce').fillna(0, downcast='infer')

dfSeasonShow = dfSeasonM[['主营业务收入(万元)','主营业务利润(万元)','净利润(万元)']].sort_index(axis=0)
dfSeasonShow.rename(columns={'主营业务收入(万元)':'M_operating_revenue(M)','主营业务利润(万元)':'M_operating_profit(M)',\
		'净利润(万元)':'net_profit(M)'},inplace = True)
dfSeasonShow = dfSeasonShow / 100
ax = dfSeasonShow.plot.bar(rot=0,figsize=(10,4))
#ax.legend(bbox_to_anchor=(1.0, 1.0))

#plt.figure(figsize=(6.4,4.8))
#plt.figure().set_size_inches(6, 4, forward=True)
plt.savefig("./tmp/test.png")
#plt.show()

ftmp = open('./tmp/test.png','rb')
ls_fSeason_64_encode = base64.b64encode(ftmp.read())
#ls_fSeason_64_encode = base64.encodestring(ftmp.read())
ftmp.close()

ls_fSeason = str(ls_fSeason_64_encode)
ls_fSeason = ls_fSeason.replace("\\n","")
ls_fSeason = ls_fSeason.replace("b'","")
ls_fSeason = ls_fSeason.replace("'","")

dfSeasonM['主营业务利润率(%)'] = dfSeasonM['主营业务利润(万元)'] / dfSeasonM['主营业务收入(万元)'] * 100
dfSeasonM['净利率(%)'] = dfSeasonM['净利润(万元)'] / dfSeasonM['主营业务收入(万元)'] * 100
print(dfSeasonM.T.sort_index(axis=1).to_markdown(floatfmt=".0f"))

#   print('![Quarterly_report][Quarterly_report]')
print('![Quarterly_report](data:image/png;base64,' + ls_fSeason + ')')
#print(ls_fSeason)
#print(')')

print('评论：\n')
print('---')

#   print('[Quarterly_report]:data:image/png;base64,' + ls_fSeason) 

#print(ls_fSeason)

#---------------------------------------------------------------------------------------


if Print2File == True :
    sys.stdout= __console__
    f.close()
