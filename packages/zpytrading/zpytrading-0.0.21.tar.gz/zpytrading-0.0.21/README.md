# zpytrading

Python - Zinnion SDK

https://pypi.org/project/zpytrading/

`pip3 install --upgrade --force-reinstall --no-cache-dir zpytrading`

`sudo -H pip3 install zpytrading`

### Requirements

You need to download and export the path to `libztrading.so` https://github.com/Zinnion/zpytrading/wiki

### Example

```Python

import zpytrading
import json
import os
import sys


def init():
    zTrading = zpytrading.ZinnionAPI()
    streamingr_config = '{"subscriptions": [ "BINANCE_SPOT_BTC_USDT"], "channels": ["trade","indicator"], "comment": "lets do it" }'
    zTrading.add_streaming(streamingr_config)
    indicators_config = '{"indicators_config":[{"indicator_name":"decay","name":"","plot":true,"symbol_id":"BINANCE_SPOT_BTC_USDT","options":[9],"data_in_bar_type":["close"],"bar_type":"simple","timeframe":1,"max_bars":30}]}'
    zTrading.add_indicators(indicators_config)
    zTrading.start_streaming(handle_data)

def handle_data(self, data):
    print(data)

if __name__ == "__main__":
    init()


```

## Indicator Listing

```
104 total indicators

Overlay
   avgprice            Average Price
   bbands              Bollinger Bands
   dema                Double Exponential Moving Average
   ema                 Exponential Moving Average
   hma                 Hull Moving Average
   kama                Kaufman Adaptive Moving Average
   linreg              Linear Regression
   medprice            Median Price
   psar                Parabolic SAR
   sma                 Simple Moving Average
   tema                Triple Exponential Moving Average
   trima               Triangular Moving Average
   tsf                 Time Series Forecast
   typprice            Typical Price
   vidya               Variable Index Dynamic Average
   vwma                Volume Weighted Moving Average
   wcprice             Weighted Close Price
   wilders             Wilders Smoothing
   wma                 Weighted Moving Average
   zlema               Zero-Lag Exponential Moving Average

Indicator
   ad                  Accumulation/Distribution Line
   adosc               Accumulation/Distribution Oscillator
   adx                 Average Directional Movement Index
   adxr                Average Directional Movement Rating
   ao                  Awesome Oscillator
   apo                 Absolute Price Oscillator
   aroon               Aroon
   aroonosc            Aroon Oscillator
   atr                 Average True Range
   bop                 Balance of Power
   cci                 Commodity Channel Index
   cmo                 Chande Momentum Oscillator
   cvi                 Chaikins Volatility
   di                  Directional Indicator
   dm                  Directional Movement
   dpo                 Detrended Price Oscillator
   dx                  Directional Movement Index
   emv                 Ease of Movement
   fisher              Fisher Transform
   fosc                Forecast Oscillator
   kvo                 Klinger Volume Oscillator
   linregintercept     Linear Regression Intercept
   linregslope         Linear Regression Slope
   macd                Moving Average Convergence/Divergence
   marketfi            Market Facilitation Index
   mass                Mass Index
   mfi                 Money Flow Index
   mom                 Momentum
   msw                 Mesa Sine Wave
   natr                Normalized Average True Range
   nvi                 Negative Volume Index
   obv                 On Balance Volume
   ppo                 Percentage Price Oscillator
   pvi                 Positive Volume Index
   qstick              Qstick
   roc                 Rate of Change
   rocr                Rate of Change Ratio
   rsi                 Relative Strength Index
   stoch               Stochastic Oscillator
   stochrsi            Stochastic RSI
   tr                  True Range
   trix                Trix
   ultosc              Ultimate Oscillator
   vhf                 Vertical Horizontal Filter
   volatility          Annualized Historical Volatility
   vosc                Volume Oscillator
   wad                 Williams Accumulation/Distribution
   willr               Williams %R

Math
   crossany            Crossany
   crossover           Crossover
   decay               Linear Decay
   edecay              Exponential Decay
   lag                 Lag
   max                 Maximum In Period
   md                  Mean Deviation Over Period
   min                 Minimum In Period
   stddev              Standard Deviation Over Period
   stderr              Standard Error Over Period
   sum                 Sum Over Period
   var                 Variance Over Period

Simple
   abs                 Vector Absolute Value
   acos                Vector Arccosine
   add                 Vector Addition
   asin                Vector Arcsine
   atan                Vector Arctangent
   ceil                Vector Ceiling
   cos                 Vector Cosine
   cosh                Vector Hyperbolic Cosine
   div                 Vector Division
   exp                 Vector Exponential
   floor               Vector Floor
   ln                  Vector Natural Log
   log10               Vector Base-10 Log
   mul                 Vector Multiplication
   round               Vector Round
   sin                 Vector Sine
   sinh                Vector Hyperbolic Sine
   sqrt                Vector Square Root
   sub                 Vector Subtraction
   tan                 Vector Tangent
   tanh                Vector Hyperbolic Tangent
   todeg               Vector Degree Conversion
   torad               Vector Radian Conversion
   trunc               Vector Truncate
```
