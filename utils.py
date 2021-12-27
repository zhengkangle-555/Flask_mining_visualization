import numpy as np
import pymysql
import time
import datetime
import os
import data_collection
import data_clean
import data_store


def get_time():
    # python不支持直接在日期中使用中文，下面使用占位符来规范化一下
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


# 连接数据库，需要先在数据库中定义好一张表
def get_con():
    connect = pymysql.connect(host='localhost', user='root', password='092099aa', database='51job', charset='utf8')
    cursor = connect.cursor()
    return connect, cursor


# 关闭数据库
def con_close(connect, cursor):
    if cursor:
        cursor.close()
    if connect:
        connect.close()


# 定义函数来执行单独一条sql语句
def query(sql):
    con, cursor = get_con()
    cursor.execute(sql)
    con.commit()
    res = cursor.fetchall()
    con_close(con, cursor)
    return res


def get_c1_data(datatable):
    sql = f'select count(岗位链接), round(avg(薪水), 2), (select 省份 from {datatable} group by 省份 having count(*) >= all(select count(*) from {datatable} group by 省份)), (select 学历 from {datatable} group by 学历 having count(*) >= all(select count(*) from {datatable} group by 学历)) from {datatable}'
    res = query(sql)
    return res[0]


def get_c2_data(datatable):
    sql = f'select 省份, count(*) from {datatable} group by 省份'
    res = query(sql)
    return res


# 这个为绘制折线图的代码
# def get_l1_data():
#     sql = "select 学历, round(avg(薪水), 2) from data_mining where 学历 <> '初中及以下' group by 学历 order by instr('高中, 中专, 大专, 本科, 硕士, 博士', 学历)"
#     res = query(sql)
#     return res
def get_l1_data(datatable):
    sql = f"select 学历, count(公司名称), round(avg(薪水), 2) from {datatable} where 学历 <> '初中及以下' group by 学历 order by instr('高中, 中专, 大专, 本科, 硕士, 博士', 学历)"
    res = query(sql)
    return res


def get_l2_data(datatable):
    sql = f"select 学历, sum(人数), round(avg(经验), 2) from {datatable} where 学历 <> '初中及以下' group by 学历 order by instr('高中, 中专, 大专, 本科, 硕士, 博士', 学历) "
    res = query(sql)
    return res


def get_r1_data(datatable):
    sql = f'select 公司类型, count(*) from {datatable} group by 公司类型 order by count(*) desc limit 8'
    res = query(sql)
    return res


# 由于这部分数据当时找不到方法插入到sql中，所以直接使用csv格式来存取数据，每次调用都会随机从csv中取出30个
def get_r2_data(datatable):
    # df = pd.read_csv(f'data/{datatable}/{datatable}_wordcloud.csv', encoding ='gb18030')
    sql = f"select 词语, round(权重, 5) from {datatable}_cloud"
    res = query(sql)
    text, weight = [], []
    for i in range(len(res)):
        text.append(res[i][0])
        weight.append(float(res[i][1]))
    random_choice = np.random.choice(range(len(text)), 30, replace = False)
    text = [text[i] for i in random_choice]
    weight = [weight[i] for i in random_choice]
    return text, weight


def create_datatable(datatable):
    sql1 = f"CREATE TABLE `51job`.`{datatable}`  ( `岗位链接` varchar(100) NULL, `发布时间` timestamp NULL, `岗位名称` varchar(30) NULL, `公司名称` varchar(30) NULL, `公司类型` varchar(30) NULL, `公司领域` varchar(30) NULL, `薪水` float(10, 4) NULL, `省份` varchar(10) NULL,  `人数` int(10) NULL, `学历` varchar(10) NULL, `经验` int(10) NULL)"
    res1 = query(sql1)
    sql2 = f"CREATE TABLE `51job`.`{datatable}_cloud`  (  `词语` varchar(10) NULL,  `权重` float(20, 16) NULL)"
    res2 = query(sql2)
    return '数据表已创建完毕！'


def exist_table(datatable):
    sql = f"show tables"
    res = query(sql)
    for i in range(len(res)):
        if datatable in res[i][0]:
            return '数据库存在此表！'
    i = input('数据库中不存在此表，是否需要重新创建？是为1，否为0：')
    if i == '1':
        path = './data/'
        os.mkdir(path + datatable)
        return create_datatable(datatable)
    else:
        return '已安全退出！'


if __name__ == '__main__':
    datatable = input('请输入你想保存的数据表单名称（英文名称）：')
    ss = exist_table(datatable)
    k = input('你是否想要对数据进行更新或插入数据？是为1，否为0：')
    if ss == '数据表已创建完毕' or k == '1':
        start_time = datetime.datetime.now()
        print(f'系统启动时间为：{start_time}')
        print('*' * 50)
        print('本系统将依次进行数据采集、数据清洗、数据存储操作，下面先进行数据的采集操作~(　＾∀＾)')
        # 通过输入岗位名称和页数来爬取对应的网页内容
        job_name = input('请输入你想要查询的岗位（中文名称）：')
        page = input('请输入你想要下载的页数（建议10-100页之间）：')
        data_collection.job51(datatable, job_name, page)
        # 默认在猎聘网站上只爬取8页，一页有40个招聘岗位，而且大多数为文本，这部分信息不要求太多
        data_collection.liepin(datatable, job_name, '8')
        print('*' * 50)
        print('数据采集完毕，下面进行数据的清洗操作~O(∩_∩)O')
        data_clean.job51_clean(datatable)
        data_clean.liepin_clean(datatable)
        print('*' * 50)
        print('数据清洗完毕，下面进行数据的存储操作~ヽ(≧Д≦)ノ')
        data_store.job51_store(datatable)
        data_store.liepin_store(datatable)
        print('*' * 50)
        print('数据存储完毕，接下来需要您修改app.py中的datatable和job_name，之后运行该文件进行该招聘岗位的可视化展示~ლ(╹◡╹ლ)')
        end_time = datetime.datetime.now()
        print(f'进行数据采集、数据清洗和数据储存共耗费：{end_time - start_time}')

