import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pymysql
from pyecharts.charts import Kline, Line
from pyecharts import options as opts
from datetime import timedelta

def createPredict(symbol):
    db_connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="kline_database"
    )

    # 创建 cursor 对象
    cursor = db_connection.cursor()

    # 从数据库中提取数据
    symbols = [symbol]
    dataframes = []

    for symbol in symbols:
        query = f"SELECT date, open, high, low, close, volume FROM kline_data WHERE symbol = '{symbol}'"
        cursor.execute(query)
        data = cursor.fetchall()
        data = pd.DataFrame(data, columns=["date", "open", "high", "low", "close", "volume"])
        data.set_index("date", inplace=True)
        dataframes.append(data)

    # 关闭 cursor 和数据库连接
    cursor.close()
    db_connection.close()

    # 数据预处理和特征工程
    data = pd.concat(dataframes, axis=0)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data[['open', 'high', 'low', 'close', 'volume']])

    # 定义时间窗口大小
    window_size = 10

    # 创建时间窗口数据
    X = []
    y = []

    for i in range(len(scaled_data) - window_size):
        X.append(scaled_data[i:i + window_size])
        y.append(scaled_data[i + window_size][3]) # 使用收盘价作为目标

    X = np.array(X)
    y = np.array(y)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 构建 RNN 模型
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(units=64, activation='relu', input_shape=(window_size, 5)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    # 使用模型进行预测
    # 首先获取最后 window_size 天的数据作为输入
    last_window = scaled_data[-window_size:]
    last_window = np.expand_dims(last_window, axis=0)

    predicted_prices = []
    for _ in range(20):  # 预测未来 20 个交易日
        predicted_price = model.predict(last_window)[0][0]

        # 更新输入窗口
        new_row = np.zeros((1, 5))
        new_row[0, 3] = predicted_price  # 假设我们只预测了收盘价，将其放在正确的位置
        new_window = np.append(last_window[0, 1:, :], new_row, axis=0)
        last_window = np.expand_dims(new_window, axis=0)

        # 将预测价格添加到列表中
        predicted_prices.append(predicted_price)

    # 还原预测价格的原始尺度
    predicted_prices = np.array(predicted_prices).reshape(-1, 1)
    predicted_prices = scaler.inverse_transform(np.hstack((predicted_prices, np.zeros((predicted_prices.shape[0], 4)))))[:, 0]

    # 生成未来日期
    last_date = pd.to_datetime(data.index[0])
    predicted_dates = pd.date_range(start=last_date + timedelta(days=1), periods=20, freq='B')

    # 创建预测数据的 DataFrame
    predicted_data = pd.DataFrame(predicted_prices, index=predicted_dates, columns=["predicted_close"])


    # 使用 pyecharts 绘制预测的 K 线图（这里只展示收盘价）
    # 使用 pyecharts 绘制预测的 K 线图（这里只展示收盘价）
    kline = Line()
    kline.add_xaxis(predicted_dates.strftime('%Y-%m-%d').tolist())

    # 因为只预测了收盘价，其他的 OHLC 数据我们暂时用收盘价代替
    ohlc = predicted_data['predicted_close'].round(2).tolist()
    kline.add_yaxis("Predicted Data", ohlc)

    # 设置图表选项
    kline.set_global_opts(
        title_opts=opts.TitleOpts(title="Predicted Stock Price K-Line"),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(is_scale=True),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
    )

    kline.width = "2000px"  # 调整图表宽度
    kline.height = "990px"

    # 渲染图表到 HTML 文件
    kline.render("./src/assets/html/predicted_stock_price.html")
