import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pyecharts.charts import Kline, Line, Bar, Grid
from pyecharts import options as opts

# 数据库连接参数
engine = create_engine('mysql+pymysql://root:123456@localhost/kline_database')

# 获取K线数据
def get_kline_data(symbol):
    #with pymysql.connect(**db_config) as conn:
    query = f"SELECT date, open, high, low, close,volume FROM kline_data WHERE Symbol = '{symbol}' ORDER BY date"
    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    return df


# 计算MACD
def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    df['EMA12'] = df['close'].ewm(span=short_period, adjust=False).mean().fillna(0)
    df['EMA26'] = df['close'].ewm(span=long_period, adjust=False).mean().fillna(0)
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean().fillna(0)
    return df['MACD'], df['Signal_Line']

# 计算KDJ
def calculate_kdj(df, n=9, m1=3, m2=3):
    low_list = df['low'].rolling(window=n, min_periods=1).min().fillna(0)
    high_list = df['high'].rolling(window=n, min_periods=1).max().fillna(0)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['K'] = rsv.ewm(alpha=1 / m1).mean().fillna(0)
    df['D'] = df['K'].ewm(alpha=1 / m2).mean().fillna(0)
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df['K'].fillna(0), df['D'].fillna(0), df['J'].fillna(0)

#绘制K线图和指标
def plot_kline_with_indicators(symbol):
    df = get_kline_data(symbol)
    ohlc = df[['open', 'close', 'low', 'high', 'volume']].values.tolist()
    dates = df['date'].apply(lambda x: x.strftime('%Y-%m-%d')).tolist()

    # 创建K线图
    kline = Kline()
    kline.add_xaxis(dates)
    kline.add_yaxis("K-Line", ohlc)

    kline.set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(is_scale=True),
        title_opts=opts.TitleOpts(title=f"{symbol} K-Line"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        datazoom_opts=[opts.DataZoomOpts()],
    )


    # 创建MACD柱状图
    macd, signal = calculate_macd(df)
    MACD_line = Line()
    MACD_line.add_xaxis(dates)
    MACD_line.add_yaxis("MACD", macd.tolist(), label_opts=opts.LabelOpts(is_show=False))
    MACD_line.add_yaxis("Signal Line", signal.tolist(), label_opts=opts.LabelOpts(is_show=False))

    # 创建KDJ线图
    kdj_line = Line()
    kdj_line.add_xaxis(dates)
    k, d, j = calculate_kdj(df)
    kdj_line.add_yaxis("K", k.tolist(), label_opts=opts.LabelOpts(is_show=False))
    kdj_line.add_yaxis("D", d.tolist(), label_opts=opts.LabelOpts(is_show=False))
    kdj_line.add_yaxis("J", j.tolist(), label_opts=opts.LabelOpts(is_show=False))

    #绘制成交量
    volumes = df['volume'].tolist()
    bar = Bar()
    bar.add_xaxis(dates)
    bar.add_yaxis("Volume", volumes, label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        legend_opts=opts.LegendOpts(pos_bottom="0%"),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(is_scale=True),
        title_opts=opts.TitleOpts(title="Volume")
    )

    # 创建Grid对象
    grid_chart1 = Grid(init_opts=opts.InitOpts(width="1024px", height="768px"))
    grid_chart2 = Grid(init_opts=opts.InitOpts(width="1024px", height="768px"))
    grid_chart3 = Grid(init_opts=opts.InitOpts(width="1024px", height="768px"))
    grid_chart4 = Grid(init_opts=opts.InitOpts(width="1024px", height="768px"))
    # 定义每个图表的位置
    # 注意：您可能需要根据您的屏幕大小和喜好调整这些值
    grid_chart1.add(
        kline,
        grid_opts=opts.GridOpts(pos_left="5%", pos_right="55%", pos_top="5%", pos_bottom="55%")
    )
    grid_chart2.add(
        MACD_line,
        grid_opts=opts.GridOpts(pos_left="5%", pos_right="55%", pos_top="55%", pos_bottom="5%")
    )
    grid_chart3.add(
        kdj_line,
        grid_opts=opts.GridOpts(pos_left="55%", pos_right="5%", pos_top="55%", pos_bottom="5%")
    )
    grid_chart4.add(
        bar,
        grid_opts=opts.GridOpts(pos_left="55%", pos_right="5%", pos_top="55%", pos_bottom="5%")
    )

    # 初始化网格布局
    grid_chart1 = Grid(init_opts=opts.InitOpts(width="900px", height="450px"))
    grid_chart2 = Grid(init_opts=opts.InitOpts(width="900px", height="450px"))
    grid_chart3 = Grid(init_opts=opts.InitOpts(width="900px", height="450px"))
    grid_chart4 = Grid(init_opts=opts.InitOpts(width="900px", height="450px"))

    # 添加K线图到网格的第一行第一列
    grid_chart1.add(kline, grid_opts=opts.GridOpts(pos_left="5%", pos_right="10%", pos_top="15%", pos_bottom="15%"))

    # 添加MACD柱状图到网格的第二行第一列
    grid_chart2.add(MACD_line, grid_opts=opts.GridOpts(pos_left="7%", pos_right="7%", pos_top="12%", pos_bottom="12%"))

    # 添加KDJ线图到网格的第二行第二列
    grid_chart3.add(kdj_line, grid_opts=opts.GridOpts(pos_left="7%", pos_right="7%", pos_top="12%", pos_bottom="12%"))

    grid_chart4.add(bar, grid_opts=opts.GridOpts(pos_left="5%", pos_right="10%", pos_top="15%", pos_bottom="15%"))

    # 渲染图表到HTML文件
    grid_chart1.render(f"./Stock-main/src/assets/html/kline_with_indicators.html")
    grid_chart2.render(f"./Stock-main/src/assets/html/kline_with_indicators_KDJ.html")
    grid_chart3.render(f"./Stock-main/src/assets/html/kline_with_indicators_MACD.html")
    grid_chart4.render(f"./Stock-main/src/assets/html/kline_with_indicators_bar.html")