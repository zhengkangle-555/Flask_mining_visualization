from flask import Flask as _Flask, jsonify, render_template
from flask.json import JSONEncoder as _JSONEncoder
import decimal
import utils


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(_JSONEncoder, self).default(o)


class Flask(_Flask): 
    json_encoder = JSONEncoder


app = Flask(__name__)
# 这里发现flask根本不会调用我在utils中处理数据的代码，所以直接就在这里定义了两个常量
# 如果想要爬取其它招聘岗位信息的话，先运行utils中的代码，然后运行app.py代码，同时，更改下面的datatable和job_name
datatable = 'data_mining'
job_name = '数据挖掘'


# 路由解析，每映射到一个路由就调用一个函数
@app.route('/')
def index():
    return render_template("main.html")


@app.route('/title')
def get_title1():
    return job_name


# 获取系统当前时间，每隔1s刷新一次
@app.route('/time')
def get_time1():
    return utils.get_time()


# 对数据库中的数据进行计数、薪资取平均值、省份和学历取众数
@app.route('/c1')
def get_c1_data1():
    data = utils.get_c1_data(datatable)
    return jsonify({"employ": data[0], "avg_salary": data[1], "province": data[2], "edu": data[3]})


# 对省份进行分组，之后统计其个数，使用jsonify来将数据传输给ajax（中国地图）
@app.route('/c2')
def get_c2_data1():
    res = []
    for tup in utils.get_c2_data(datatable):
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


# 统计每个学历下公司数量和平均薪资（上下坐标折线图）
@app.route('/l1')
# 下面为绘制折线图的代码，如果使用这个的话需要在main.html中引入ec_left1.js，然后在controller.js中重新调用
# def get_l1_data1():
#     data = utils.get_l1_data()
#     edu, avg_salary = [], []
#     for s in data:
#         edu.append(s[0])
#         avg_salary.append(s[1])
#     return jsonify({"edu": edu, "avg_salary": avg_salary})
def get_l1_data1():
    data = utils.get_l1_data(datatable)
    edu, sum_company, avg_salary = [], [], []
    for s in data:
        edu.append(s[0])
        sum_company.append(int(s[1]))
        avg_salary.append(float(s[2]))
    return jsonify({"edu": edu, "sum_company": sum_company, "avg_salary": avg_salary})


# 统计不同学历下公司所招人数和平均经验（折线混柱图）
@app.route('/l2')
def get_l2_data1():
    data = utils.get_l2_data(datatable)
    edu, num, exp = [], [], []
    # 注意sql中会存在decimal的数据类型，我们需要将其转换为int或者float的格式
    for s in data:
        edu.append(s[0])
        num.append(float(s[1]))
        exp.append(float(s[2]))
    return jsonify({'edu': edu, 'num': num, 'exp': exp})


# 统计不同类型公司所占的数量（饼图）
@app.route('/r1')
def get_r1_data1():
    res = []
    for tup in utils.get_r1_data(datatable):
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


# 对猎聘网上的“岗位要求”文本进行分词后，使用jieba.analyse下的extract_tags来获取全部文本的关键词和权重，再用echarts来可视化词云
@app.route('/r2')
def get_r2_data1():
    cloud = []
    text, weight = utils.get_r2_data(datatable)
    for i in range(len(text)):
        cloud.append({'name': text[i], 'value': weight[i]})
    return jsonify({"kws": cloud})


if __name__ == '__main__':
    app.run()

