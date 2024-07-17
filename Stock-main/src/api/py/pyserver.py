from flask import Flask, jsonify, request
from KLine_data_generator import insert_to_database
from flask_cors import cross_origin
import pymysql
import openai
from diagram_generator import *
from RNN import createPredict
from openai import OpenAI

app = Flask(__name__)


@app.route('/aichat', methods=['POST'])
@cross_origin()
def aichat():
    data = request.json
    user_message = data['message']

    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="sk-8fR0hIwKGblmiv3DgRfepyurfiahfYVu5mU3a3KsDvdaFkLN",
        base_url="https://api.chatanywhere.tech/v1"
        # base_url="https://api.chatanywhere.cn/v1"
    )

    prompt = "You are an AI meeting assistant. Please answer questions in Chinese.\n\n" + user_message

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    ai_message = response.choices[0].message.content
    return jsonify({'response': ai_message})


@app.route('/querystock', methods=['POST'])
@cross_origin()
def querystock():
    data = request.json
    plot_kline_with_indicators(data['message'])
    return jsonify({'response': 'success'})


@app.route('/addselect', methods=['POST'])
@cross_origin()
def addselect():
    data = request.json
    username = data['username']
    symbol = data['symbol']

    db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         database="kline_database")
    cursor = db.cursor()
    tag = True

    sql = "select * from kline_data where symbol = '%s'" % symbol
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        tmp = insert_to_database(symbol)
        if tmp == False:
            return jsonify({'response': 'wrong'})

    sql = "select * from selfselect where username = '%s' and symbol = '%s'" % (username, symbol)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results != ():
            tag = False
        sql = "insert into selfselect values(0, '%s', '%s')" % (username, symbol)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            tag = False
            db.rollback()

    except:
        tag = False

    cursor.close()
    db.close()
    return jsonify({'response': 'success' if tag else 'fail'})


@app.route('/aipredict', methods=['POST'])
@cross_origin()
def aipredict():
    data = request.json
    symbol = data['message']

    db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         database="kline_database")
    cursor = db.cursor()

    sql = "select * from kline_data where symbol = '%s'" % symbol
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        if not results:
            return jsonify({'response': 'fail'})
    except:
        return jsonify({'response': '???'})

    createPredict(symbol)
    return jsonify({'response': 'success'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
