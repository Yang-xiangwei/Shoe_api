# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 00:00:24 2025

@author: andy9
"""# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "0963143241",
    "database": "topic_db",
}

@app.route('/get_data', methods=['GET', 'OPTIONS'])
def get_data():
    if request.method == 'OPTIONS':
        # 處理預檢請求
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    try:
        # 連接數據庫
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # 查詢數據庫
        query = "SELECT * FROM Shoe_information"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # 獲取列名
        column_names = [desc[0] for desc in cursor.description]
        
        # 將結果轉換為字典列表
        data = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            data.append(row_dict)

        # 關閉數據庫連接
        cursor.close()
        connection.close()

        # 返回 JSON 響應
        response = make_response(jsonify(data))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        return response

    except Exception as e:
        # 錯誤處理
        if 'connection' in locals():
            connection.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)


