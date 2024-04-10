from flask import Flask,request

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 定义一个简单的路由
@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        return data
    return 'Hello, World!'

# 运行应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

