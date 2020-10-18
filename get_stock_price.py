from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib
import ssl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_finance as mpf

def get_datas(stock_number):
    df_list = []
    year = [2019,2020] #2015〜2020年までの株価データを取得
    for y in year:
        try:
            print(str(y)+"年のデータを取得中")
            url = 'https://kabuoji3.com/stock/{}/{}/'.format(stock_number,y)
            ssl._create_default_https_context = ssl._create_unverified_context#SSLエラー防止
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read() 
            soup = BeautifulSoup(html, "html.parser")
            tag_tr = soup.find_all('tr')
            head = [h.text for h in tag_tr[0].find_all('th')]

            for i in range(1,len(tag_tr)):
                df_list.append([d.text for d in tag_tr[i].find_all('td')])
        except IndexError:
            print(str(y)+'のデータは存在しません')
    
    data=pd.DataFrame(np.array(df_list),columns=head)
    data["日付"]=[s.replace("-","") for s in data["日付"]]
    data = data.set_index('日付')#日付をインデックスにする
    return data

datas=get_datas(3048)

print(datas)
# x_data=datas.index
# x_data_min=datetime.strptime(x_data[0],'%Y-%m-%d')
# x_data_max=datetime.strptime(x_data[-1],'%Y-%m-%d')
# fig = plt.figure(figsize=(15,6))
# ax = plt.subplot(1,1,1)
# plt.xlim([x_data_min,x_data_max])
# fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')# x軸の整形 



# # ロウソクチャートをプロット
# mpf.candlestick2_ohlc(ax,
#                       opens     = datas["始値"].values,
#                       highs     = datas["高値"].values,
#                       lows      = datas["安値"].values,
#                       closes    = datas["終値"].values,
#                       width     = 0.8,
#                       colorup   = "g",
#                       colordown = "r")
# #移動平均線のプロット
# sma = datas['始値'].rolling(5).mean()#日足5日平均
# ax.plot(sma, color='Blue', linewidth='1.0', label='短期移動平均線(5日毎)')

# ax.grid() #グリッド表示

# plt.show()# グラフの描画