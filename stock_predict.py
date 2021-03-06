# -*- coding: utf-8 -*-
"""stock_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c2d3zI_G_-5SwNWf5uh9qzY3El9sH9P7
"""

#とりあえずモジュールのインストール
!pip install mpl_finance
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import ssl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_finance as mpf
import math
import time
import pickle
from datetime import datetime as dt

def get_datas(stock_number):
    df_list = []
    year = range(2018,2021) #2010〜2020年までの株価データを取得
    for y in year:
        try:
            print(str(y)+"年のデータを取得中")
            url = 'https://kabuoji3.com/stock/{}/{}/'.format(stock_number,y)
            ssl._create_default_https_context = ssl._create_unverified_context#SSLエラー防止
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})#検索エンジンをFireFoxにしてあげないと無理っぽい
            html = urllib.request.urlopen(req).read() 
            soup = BeautifulSoup(html, "html.parser")
            tag_tr = soup.find_all('tr')
            head = [h.text for h in tag_tr[0].find_all('th')]

            for i in range(1,len(tag_tr)):
                df_list.append([d.text for d in tag_tr[i].find_all('td')])
        except IndexError:
            print(str(y)+'のデータは存在しません')
    
    data=pd.DataFrame(np.array(df_list),columns=head)
    data = data.set_index('日付')#日付をインデックスにする
    print(head)
    return data

datas=get_datas(3041)
datas=pd.DataFrame(datas,dtype=float)#全データをfloat型に

datas

"""#グラフの絵画"""

fig = plt.figure(figsize=(22,30))
ax1=fig.add_subplot(8,1,1)#Figure.add_subplot(nrows, ncols, index),台紙を縦nrows分割・横ncols分割したうちのindex番目の位置に配置されたAxesが返される。
ax2=fig.add_subplot(8,1,2)#plt.subplots(nrows, ncols)もあるけど今回は一つづつ図を見やすくしたいので,,,,
ax3=fig.add_subplot(8,1,3)
ax4=fig.add_subplot(8,1,4)
ax5=fig.add_subplot(8,1,5)
ax6=fig.add_subplot(8,1,6)
ax7=fig.add_subplot(8,1,7)
ax8=fig.add_subplot(8,1,8)

#箱ひげ図
mpf.candlestick2_ohlc(ax1,
                      opens     = datas["始値"].values,
                      highs     = datas["高値"].values,
                      lows      = datas["安値"].values,
                      closes    = datas["終値"].values,
                      width     = 0.8,
                      colorup   = "g",
                      colordown = "r")
mpf.candlestick2_ohlc(ax3,
                      opens     = datas["始値"].values,
                      highs     = datas["高値"].values,
                      lows      = datas["安値"].values,
                      closes    = datas["終値"].values,
                      width     = 0.8,
                      colorup   = "g",
                      colordown = "r")
#日足5日平均(短期)
sma_short = datas['終値'].rolling(5).mean()
ax1.plot(sma_short, color='Blue', linewidth='1.0', label='moving average per 5 days')
ax2.plot(sma_short, color='Blue', linewidth='1.0', label='moving average per 5 days')
#日足25日平均(中期)
sma_middle=datas['終値'].rolling(25).mean()
ax1.plot(sma_middle, color='Green', linewidth='1.0', label='moving average per 25 days')
ax2.plot(sma_middle, color='Green', linewidth='1.0', label='moving average per 25 days')
#日足75日平均(長期)
sma_long=datas['終値'].rolling(75).mean()
ax1.plot(sma_long, color='Red', linewidth='1.0', label='moving average per 75 days')
ax2.plot(sma_long, color='Red', linewidth='1.0', label='moving average per 75 days')

ax1.legend(loc='upper left')#lower rightとかにできるよ
ax2.legend(loc='upper left')#lower rightとかにできるよ

#軸をうまいこと調整してくれる
ax1.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax1.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax2.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax2.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax3.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax3.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax4.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax4.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax5.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax5.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax6.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax6.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax7.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax7.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax8.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax8.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())

#ゴールデンクロス
for s,m,l,date in zip(sma_short,sma_middle,sma_long,datas.index.values):
  if(np.isnan(l)==False):
    if(int(s)-10<int(m)&int(m)<int(s)+10):
        ax2.scatter(date,m,marker='o',s=10,c="k")
    if(int(s)-10<int(l)&int(l)<int(s)+10):
        ax2.scatter(date,l,marker='o',s=10,c="k")
    if(int(m)-10<int(l)&int(l)<int(m)+10):
        ax2.scatter(date,m,marker='o',s=10,c="k")

#ボリンジャーバンド
bband_std=datas['終値'].rolling(25).std()
bband_upper_1 = sma_middle + bband_std
bband_lower_1= sma_middle - bband_std
bband_upper_2 = sma_middle + (bband_std * 2)
bband_lower_2= sma_middle - (bband_std * 2)
bband_upper_3 = sma_middle + (bband_std * 3)
bband_lower_3= sma_middle - (bband_std * 3)
ax3.plot(bband_upper_1, color='Blue', linewidth='1.0', label='γ')
ax3.plot(bband_lower_1, color='Blue', linewidth='1.0')
ax3.plot(bband_upper_2, color='Green', linewidth='1.0', label='2γ')
ax3.plot(bband_lower_2, color='Green', linewidth='1.0')
ax3.plot(bband_upper_3, color='Red', linewidth='1.0', label='3γ')
ax3.plot(bband_lower_3, color='Red', linewidth='1.0')
ax3.legend(loc='upper left')#lower rightとかにできるよ

#出来高
ax4.bar(datas.index.values,datas["出来高"].values,label="volume")
ax4.legend(loc='upper left')#lower rightとかにできるよ

#一目均衡表(三役好転を見極める)??
tenkan = (datas["高値"].rolling(window=9,min_periods=1).max()+datas["安値"].rolling(window=9).min())/2
tenkan=tenkan.iloc[26:]
base = (datas["高値"].rolling(window=26, min_periods=1).max()+datas["安値"].rolling(window=26).min())/2
base=base.iloc[26:]
senkou1 = ((tenkan+base)/2).iloc[26:]
senkou2 = ((datas["高値"].rolling(window=52).max()+datas["安値"].rolling(window=52, min_periods=1).min())/2).iloc[52:]
tikou=datas["終値"]
ax5.plot(tenkan[78:], color='Red', linewidth='1.0',label="Convergion")
ax5.plot(base[78:], color='Blue', linewidth='1.0',label="Base")
ax5.plot(tikou.values[130:], color='Green', linewidth='1.0',label="unprecedent")
ax5.fill_between(datas.index.values[104:],senkou1.values[26:-26], senkou2.values[26:-26], color="Magenta", alpha=0.2, label="cloud")
ax5.legend(loc='upper right')

#乖離率
divergence_short = ((datas["終値"]-sma_short)/sma_short)*100
ax6.plot(divergence_short, color='Blue', linewidth='1.0', label='divergence per 5 days')
divergence_middle = ((datas["終値"]-sma_middle)/sma_middle)*100
ax6.plot(divergence_middle, color='Green', linewidth='1.0', label='divergence per 25 days')
divergence_long = ((datas["終値"]-sma_long)/sma_long)*100
ax6.plot(divergence_long, color='Red', linewidth='1.0', label='divergence per 75 days')
ax6.legend(loc='upper right')

#RSI
diff = datas["終値"].diff()
diff = diff[1:]
up, down = diff.copy(), diff.copy()
up[up < 0] = 0
down[down > 0] = 0
up_sma_14 = up.rolling(window=14, center=False).mean()
down_sma_14 = down.abs().rolling(window=14, center=False).mean()
RS = up_sma_14 / down_sma_14
RSI = 100.0 - (100.0 / (1.0 + RS))
ax7.plot(RSI, color='Red', linewidth='1.0', label='RSI')
ax7.legend(loc='upper left')

#MACD
macd_ema12= datas['終値'].ewm(span=12).mean()
macd_ema26 = datas['終値'].ewm(span=26).mean()
macd = macd_ema12 - macd_ema26
macd_signal = macd.ewm(span=9).mean()
ax8.plot(macd, color='Blue', linewidth='1.0', label='macd')
ax8.plot(macd_signal, color='Red', linewidth='1.0', label='macd_signal')
ax8.legend(loc='upper left')

plt.show()# グラフの描画

"""#データをまとめる"""

#データをまとめる
ai_data=pd.DataFrame(datas["終値"].values,columns=["close"],index=datas.index.values)
#単純移動平均線追加
ai_data["sma_short"]=sma_short
ai_data["sma_middle"]=sma_middle
ai_data["sma_long"]=sma_long
#ボリンジャーバンド追加
ai_data["bband_upper_1"]=bband_upper_1
ai_data["bband_upper_2"]=bband_upper_2
ai_data["bband_upper_3"]=bband_upper_3
ai_data["bband_lower_1"]=bband_lower_1
ai_data["bband_lower_2"]=bband_lower_2
ai_data["bband_lower_3"]=bband_lower_3
#出来高追加
ai_data["Volume"]=datas["出来高"]
#乖離率
ai_data["divergence_short"]=divergence_short
ai_data["divergence_middle"]=divergence_middle
ai_data["divergence_long"]=divergence_long
#RSI
ai_data["RSI"]=RSI
#MACD
ai_data["macd"]=macd
ai_data["macd_signal"]=macd_signal
#NaNデータの部分を削除
ai_data=ai_data[74:]
#valuesだけとる
ai_data_values=ai_data.values

len(ai_data)

"""#LSTM"""

#単純移動平均線からの予測
#データ正規化
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
ai_data_values = scaler.fit_transform(ai_data_values)

#データ整形
#とりあえず一ヶ月でみていくか
n_rnn=400
n_sample=len(ai_data_values)-n_rnn
x=np.zeros((n_sample,n_rnn,17))
t=np.zeros((n_sample, n_rnn,17))

for i in range(0,n_sample):
  for j in range(0,n_rnn):
    x[i][j]=ai_data_values[i+j][:]
    t[i][j]=ai_data_values[i+1+j][:]

#モデル構築
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM,GRU

#初期値
batch_size=100
n_in=17
n_mid=10
n_out=17
epochs=100

#LSTM
model_lstm=Sequential()
model_lstm.add(LSTM(n_mid,input_shape=(n_rnn,n_in),return_sequences=True))
model_lstm.add(Dense(n_out,activation="linear"))
model_lstm.compile(loss="mean_squared_error", optimizer="sgd")
print(model_lstm.summary())

history_lstm = model_lstm.fit(x, t, epochs=epochs, batch_size=batch_size, verbose=0)

#Lossの可視化
loss_lstm = history_lstm.history['loss']
plt.plot(np.arange(len(loss_lstm)), loss_lstm, label="LSTM")
plt.legend()
plt.show()

#予測結果格納
predicted_lstm=x[0]
predicted_lstm=predicted_lstm.reshape(1,n_rnn,17)
y_lstm=np.zeros((n_sample*n_rnn,17))
for i in range(0,n_sample):
  for j in range(0,n_rnn):
    y_lstm[i*n_rnn+j]=predicted_lstm[0][j]

  predicted_lstm=model_lstm.predict(predicted_lstm)

#説明変数の予測結果
y_lstm=scaler.inverse_transform(y_lstm)

#予測結果をdataFrameに
predict_price_lstm=pd.DataFrame(y_lstm,columns=ai_data.columns)

predict_price_lstm

#結果株価の比較
fig = plt.figure(figsize=(25,10))
ax=fig.add_subplot(1,1,1)
#軸をうまいこと調整してくれる
ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
#元データの表示
ax.plot(ai_data["close"], color='Red', linewidth='1.0', label='real stock')
ax.plot(predict_price_lstm["close"][:len(ai_data)], color='Blue', linewidth='1.0', label='predict stock')
ax.legend(loc='upper left')
plt.show()

"""#RRL(にっしー)"""

from tqdm import tqdm
import datetime as dt
import math
import time
from datetime import datetime
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import keras
from keras.models import Sequential  
from keras.layers.core import Activation  
from keras.layers import Input, Dense, LSTM ,GRU 
from keras.models import Model
from keras.callbacks import CSVLogger
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

# データセットを作る
# 上が学習用、下がテスト用
n_train = 200*2
n_test = 100
# インデックスの入れ物を作る
train_index, test_index = [],[]
# 学習データとテストデータのインデックスの取得
for i in range(0,len(ai_data)-int(n_train/n_test)*n_test,n_test):
    train_index.append(ai_data.index[i:i+n_train])
    test_index.append(ai_data.index[i+n_train:(i+n_test)+n_train])

# ポジションの入れ物
Dt = np.zeros(n_train)
# 報酬関数の入れ物
Rt = np.zeros(n_train)
# 評価関数の定義
Ut = Rt.cumsum()

# テスト用の入れ物
ut = np.zeros((len(test_index),n_test))
dt = np.zeros(n_test)
rt = np.zeros(n_test)

# 繰り返し回数
epoch = 25
# 学習率
l=0.85
lr = 0.1

c = 0
# 価格変動の作成：ztの部分
dd=ai_data.copy()
dd1 = dd.close.copy()
dd2 = dd1.diff().fillna(0)

# 使用する学習データの数
# あまり大きい数にしてしまうと、ものすごく時間がかかるので注意。
span = 4
# 学習をスタートする期間の指定 ※0以上になるように！
# ここでは、最新のデータからspanの値分前の時点から学習をスタートする
nn = len(test_index)-span

# 学習部分
for j in tqdm(range(nn,nn+span)):
    print('\n\n',j+1-nn,'回目')
   # 重みとバイアスの初期化
    W = np.zeros(len(ai_data.columns))
    b = 0
    u = 0
   # 勾配の入れ物
    dW = np.zeros(len(W))
    db = np.zeros(1)
    du = np.zeros(1)
    dRt = np.zeros((n_train,2,len(ai_data.columns)))
    dDt = np.zeros((n_train,len(ai_data.columns)))
    dDt_b = np.zeros(n_train)
    dDt_u = np.zeros(n_train)
   # 価格変動の取得：ztの部分
    train_dd = dd2[train_index[j]]
   # 学習のスタート
    for k in tqdm(range(epoch)):
        for i,t in tqdm(enumerate(train_index[j])):
            a = np.array(ai_data.loc[t])
           # ポジションと報酬の計算
            if i == 0:
                x = np.dot(W,a) + b
                Dt[i] = np.tanh(x)
                Dw,Db,Du = 0,0,0
            else:
                x = np.dot(W,a)+b+u*Dt[i-1]
                Dt[i] = np.tanh(x)
                Rt[i] = (train_dd[i]*Dt[i-1]-c*abs(Dt[i]-Dt[i-1]))
               # 評価関数の計算
                Ut[:i+1] = Rt[:i+1].cumsum()
               # 重み更新
                dDt[i] = a/np.cosh(x)**2 + u*dDt[i-1]/np.cosh(x)**2
                dDt_b[i] = 1/np.cosh(x)**2+u*dDt_b[i-1]/np.cosh(x)**2
                dDt_u[i] = Dt[i-1]/np.cosh(x)**2+u*dDt_b[i-1]/np.cosh(x)**2
                dRt[i][0] = -c*np.sign(Dt[i]-Dt[i-1])
                dRt[i][1] = train_dd[i] + c*np.sign(Dt[i]-Dt[i-1])
                dW = dRt[i][0]*dDt[i] + dRt[i][1]*dDt[i-1]
                db = -c*np.sign(Dt[i]-Dt[i-1])*dDt_b[i] + (train_dd[i] + c*np.sign(Dt[i]-Dt[i-1]))*dDt_b[i-1]
                du = -c*np.sign(Dt[i]-Dt[i-1])*dDt_u[i] + (train_dd[i] + c*np.sign(Dt[i]-Dt[i-1]))*dDt_u[i-1]
               # 普通の重み更新
                Dw += dW
                Db += db
                Du += du
        W += lr*Dw
        b += lr*Db
        u += lr*Du
       # コード実行時に、学習した結果による評価関数の収益の結果を出力してます。
        print(Ut[-1])
   # テストデータによる予測結果の計算
   # 価格変動の取得：ztの部分
    test_dd = dd2[test_index[j]]
    for i,t in tqdm(enumerate(test_index[j])):
        a = np.array(ai_data.loc[t])
        if i == 0:
            x = np.dot(W,a) + b + u*dt[-1]
           # この時、δの値が0.6を上回ればロング、-0.6を下回ればショートをとります。
            dt[i] = (np.tanh(x)>0.75).astype(float) - (np.tanh(x)<-0.75).astype(float)
           # 報酬関数の計算
            rt[i] = test_dd[i]*dt[-1] - c*abs(dt[i]-dt[-1])
        else:
            x = np.dot(W,a)+b+u*dt[i-1]
           # この時、δの値が0.6を上回ればロング、-0.6を下回ればショートをとります。
            dt[i] = (np.tanh(x)>0.75).astype(float) - (np.tanh(x)<-0.75).astype(float)
           # 報酬関数の計算
            rt[i] = test_dd[i]*dt[i-1]-c*abs(dt[i]-dt[i-1])
   # 評価関数の計算
    ut[j] = rt.copy()
   # ポジションログも保存しておきます。
    dt_log.append(dt.copy())

"""#RRL(ブログ)"""

class TradingRRL(object):
    def __init__(self, T=300, M=150, init_t=500, mu=100, sigma=0, rho=1.0, n_epoch=10):
        self.T = T#シャープレシオの期間
        self.M = M#過去M個の価格変動
        self.init_t = init_t#現在時刻のインデックス
        self.mu = mu#売買可能数
        self.sigma = sigma#最小売買単位にかける手数料手数料無いのになんか不本意だけど0だと消えるので計算式再度導出やなぁ...
        self.rho = rho#学習率
        self.all_t = None
        self.all_p = None
        self.t = None
        self.p = None
        self.r = None
        self.x = np.zeros([T, M+2])#入力
        self.F = np.zeros(T+1)#アクション[-1,1]
        self.R = np.zeros(T)#時刻Tの報酬
        self.w = np.ones(M+2)#重み
        self.w_opt = np.ones(M+2)#重み最適解
        self.epoch_S = np.empty(0)#学習回数毎のシャープレシオを記録
        self.n_epoch = n_epoch#学習回数
        self.progress_period = 1#1回ごとに学習結果を表示する
        self.q_threshold = 0.7
        self.all_t = ai_data.index.values[::-1]#時系列データ
        self.all_p = ai_data.close.values[::-1]#終値データ

    def quant(self, f):
        fc = f.copy()
        fc[np.where(np.abs(fc) < self.q_threshold)] = 0
        return np.sign(fc)

    def set_t_p_r(self):#現在(インデックス0)から過去を入れてる
        self.t = self.all_t[self.init_t:self.init_t+self.T+self.M+1]
        self.p = self.all_p[self.init_t:self.init_t+self.T+self.M+1]
        self.r = -np.diff(self.p)

    def set_x_F(self):#xとFの計算
        for i in range(self.T-1, -1 ,-1):
            self.x[i] = np.zeros(self.M+2)
            self.x[i][0] = 1.0
            self.x[i][self.M+2-1] = self.F[i+1]
            for j in range(1, self.M+2-1, 1):
                self.x[i][j] = self.r[i+j-1]
            self.F[i] = np.tanh(np.dot(self.w, self.x[i]))

    def calc_R(self):
        self.R = self.mu * (self.F[1:] * self.r[:self.T] - self.sigma * np.abs(-np.diff(self.F)))

    def calc_sumR(self):
        self.sumR  = np.cumsum(self.R[::-1])[::-1]
        self.sumR2  = np.cumsum((self.R**2)[::-1])[::-1]

    def calc_dSdw(self):#dS,dWの計算
        self.set_x_F()
        self.calc_R()
        self.calc_sumR()
        self.A      =  self.sumR[0] / self.T
        self.B      =  self.sumR2[0] / self.T
        self.S      =  self.A / np.sqrt(self.B - self.A**2)
        self.dSdA   =  self.S * (1 + self.S**2) / self.A
        self.dSdB   = -self.S**3 / 2 / self.A**2
        self.dAdR   =  1.0 / self.T
        self.dBdR   =  2.0 / self.T * self.R
        self.dRdF   = -self.mu * self.sigma * np.sign(-np.diff(self.F))
        self.dRdFp  =  self.mu * self.r[:self.T] + self.mu * self.sigma * np.sign(-np.diff(self.F))
        self.dFdw   = np.zeros(self.M+2)
        self.dFpdw  = np.zeros(self.M+2)
        self.dSdw   = np.zeros(self.M+2)
        for i in range(self.T-1, -1 ,-1):
            if i != self.T-1:
                self.dFpdw = self.dFdw.copy()
            self.dFdw  = (1 - self.F[i]**2) * (self.x[i] + self.w[self.M+2-1] * self.dFpdw)
            self.dSdw += (self.dSdA * self.dAdR + self.dSdB * self.dBdR[i]) * (self.dRdF[i] * self.dFdw + self.dRdFp[i] * self.dFpdw)

    def update_w(self):
        self.w += self.rho * self.dSdw
    def fit(self):
        
        pre_epoch_times = len(self.epoch_S)

        self.calc_dSdw()
        print("Epoch loop start. Initial sharp's ratio is " + str(self.S) + ".")#シャープレシオ初期値出力
        self.S_opt = self.S
        
        tic = time.clock()#学習時間の計測スタート
        for e_index in range(self.n_epoch):#エポック回学習
            self.calc_dSdw()
            if self.S > self.S_opt:#シャープレシオは大きいほどよいので,学習過程で一番良かったやつを持ってくる
                self.S_opt = self.S
                self.w_opt = self.w.copy()
            self.epoch_S = np.append(self.epoch_S, self.S)
            self.update_w()
            if e_index % self.progress_period  == self.progress_period-1:
                toc = time.clock()
                print("Epoch: " + str(e_index + pre_epoch_times + 1) + "/" + str(self.n_epoch + pre_epoch_times) +". Shape's ratio: " + str(self.S) + ". Elapsed time: " + str(toc-tic) + " sec.")
        toc = time.clock()
        print("Epoch: " + str(e_index + pre_epoch_times + 1) + "/" + str(self.n_epoch + pre_epoch_times) +". Shape's ratio: " + str(self.S) + ". Elapsed time: " + str(toc-tic) + " sec.")
        self.w = self.w_opt.copy()
        self.calc_dSdw()
        print("Epoch loop end. Optimized sharp's ratio is " + str(self.S_opt) + ".")

    def save_weight(self):
        pd.DataFrame(self.w).to_csv("w.csv", header=False, index=False)
        pd.DataFrame(self.epoch_S).to_csv("epoch_S.csv", header=False, index=False)
        
    def load_weight(self):
        tmp = pd.read_csv("w.csv", header=None)
        self.w = tmp.T.values[0]

T=1000
M=200
init_t=1000
mu=100
sigma=0
rho=0.9
n_epoch=30
# RRL agent with initial weight.
ini_rrl = TradingRRL(T, M, init_t, mu, sigma, rho, n_epoch)
ini_rrl.set_t_p_r()
ini_rrl.calc_dSdw()
# RRL agent for training 
rrl = TradingRRL(T, M, init_t, mu, sigma, rho, n_epoch)
rrl.all_t = ini_rrl.all_t
rrl.all_p = ini_rrl.all_p
rrl.set_t_p_r()
rrl.fit()

# Plot results.
# Training for initial term T.
plt.plot(range(len(rrl.epoch_S)),rrl.epoch_S)
plt.title("Sharp's ratio optimization")
plt.xlabel("Epoch times")
plt.ylabel("Sharp's ratio")
plt.grid(True)
# plt.savefig("sharp's ratio optimization.png", dpi=300)
plt.close

fig, ax = plt.subplots(nrows=3, figsize=(15, 10))
t = np.linspace(1, rrl.T, rrl.T)[::-1]
ax[0].plot(t, rrl.p[:rrl.T])#現在からシャープレシオ期間の終値を出力
ax[0].set_xlabel("time")
ax[0].set_ylabel("close")
ax[0].grid(True)

#はじめのシャープレシオにおけるF(売りか買いか)と学習後のシャープレシオにおけるFの比較
ax[1].plot(t, ini_rrl.F[:rrl.T], color="blue", label="With initial weights")
ax[1].plot(t, rrl.F[:rrl.T], color="red", label="With optimized weights")
ax[1].set_xlabel("time")
ax[1].set_ylabel("F")
ax[1].legend(loc="upper left")
ax[1].grid(True)

#はじめのシャープレシオにおけるR(利益)と学習後のシャープレシオにおけるRの比較
ax[2].plot(t, ini_rrl.sumR, color="blue", label="With initial weights")
ax[2].plot(t, rrl.sumR, color="red", label="With optimized weights")
ax[2].set_xlabel("time")
ax[2].set_ylabel("Sum of reward[yen]")
ax[2].legend(loc="upper left")
ax[2].grid(True)
# plt.savefig("rrl_train.png", dpi=300)
plt.show()# グラフの描画

# Prediction for next term T with optimized weight.
# RRL agent with initial weight.
ini_rrl_f = TradingRRL(T, M, init_t-T, mu, sigma, rho, n_epoch)
ini_rrl_f.all_t = ini_rrl.all_t
ini_rrl_f.all_p = ini_rrl.all_p
ini_rrl_f.set_t_p_r()
ini_rrl_f.calc_dSdw()
# RRL agent with optimized weight.
rrl_f = TradingRRL(T, M, init_t-T, mu, sigma, rho, n_epoch)
rrl_f.all_t = ini_rrl.all_t
rrl_f.all_p = ini_rrl.all_p
rrl_f.set_t_p_r()
rrl_f.w = rrl.w
rrl_f.calc_dSdw()

fig, ax = plt.subplots(nrows=3, figsize=(15, 10))
t_f = np.linspace(rrl.T+1, rrl.T+rrl.T, rrl.T)[::-1]
ax[0].plot(t_f, rrl_f.p[:rrl_f.T])
ax[0].set_xlabel("time")
ax[0].set_ylabel("close")
ax[0].grid(True)

ax[1].plot(t_f, ini_rrl_f.F[:rrl_f.T], color="blue", label="With initial weights")
ax[1].plot(t_f, rrl_f.F[:rrl_f.T], color="red", label="With optimized weights")
ax[1].set_xlabel("time")
ax[1].set_ylabel("F")
ax[1].legend(loc="lower right")
ax[1].grid(True)

ax[2].plot(t_f, ini_rrl_f.sumR, color="blue", label="With initial weights")
ax[2].plot(t_f, rrl_f.sumR, color="red", label="With optimized weights")
ax[2].set_xlabel("time")
ax[2].set_ylabel("Sum of reward[yen]")
ax[2].legend(loc="lower right")
ax[2].grid(True)
# plt.savefig("rrl_prediction.png", dpi=300)
plt.show()