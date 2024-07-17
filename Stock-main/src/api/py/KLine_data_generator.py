import pymysql
from alpha_vantage.timeseries import TimeSeries

def insert_to_database(symbols):
    ts = TimeSeries(key='你的API Key', output_format='pandas', indexing_type='date')

    # 用户输入要搜索的股票符号列表，例如 ['AAPL', 'GOOGL', ...]

    #, "TSLA", "AMZN", "FB", "NVDA", "PYPL", "BABA", "JPM"

    # 连接到MySQL数据库
    db_connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="KLine_database"
    )

    # 创建一个游标对象
    cursor = db_connection.cursor()

    try:
        for symbol in symbols:
            # 获取股票数据示例
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')

            # 将日期索引重置为列
            data.reset_index(inplace=True)

            # 将数据插入到数据库表中
            for index, row in data.iterrows():
                insert_data_query = """
                INSERT INTO kline_data (symbol, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                data_to_insert = (
                symbol, row['date'], row['1. open'], row['2. high'], row['3. low'], row['4. close'], row['5. volume'])
                cursor.execute(insert_data_query, data_to_insert)

        # 提交更改
        db_connection.commit()
    except Exception as e:
        return False
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        db_connection.close()
        return True