import pandas as pd
import numpy as np
import jieba.analyse as aa
import pymysql


# 连接数据库，需要先在数据库中定义好一张表
def get_con():
    con = pymysql.connect(host = 'localhost', user = 'root', password = '092099aa', database = '51job', charset = 'utf8')
    cursor = con.cursor()
    return con, cursor


# 关闭数据库
def con_close(con, cursor):
    if cursor:
        cursor.close()
    if con:
        con.close()


def job51_store(datatable):
    # 首先读取处理后的数据集
    df = pd.read_csv(f'./data/{datatable}/51job_{datatable}_preprocessing.csv', encoding = 'gb18030')
    con, cursor = get_con()
    for i in range(len(df)):
        # 将每行数据都转变为tuple数据类型，然后遍历把每条数据都添加到sql中，有多次存数因而不使用上方函数
        s = tuple(df.iloc[i, :])
        sql = f'insert into {datatable} values{s}'
        cursor.execute(sql)
    con.commit()
    con_close(con, cursor)


def liepin_store(datatable):
    # 下面把词云部分数据也存放进数据库中
    df_cloud = pd.read_csv(f'./data/{datatable}/liepin_{datatable}_detail.csv', encoding = 'gb18030')
    # 将每一列英文全部转换为大写的
    df_cloud = df_cloud.apply(lambda x: [i.upper() for i in x])
    # 对文本进行去重操作
    s = np.unique(df_cloud.sum().tolist()).tolist()
    # 由于后期使用echarts绘制词云需要知道各个关键词的权重大小，所以下面使用jieba下的extract_tags来挖掘各个关键词和权重大小，注意extract_tags输入的是一个字符串，我们挑选出前150个关键词及权重
    ss = aa.extract_tags(' '.join(s), topK = 150, withWeight = True)
    # 将数据存储到excel表格中，发现一直存不进sql中
    # text, weight = [], []
    # for i in range(len(ss)):
    #     text.append(ss[i][0])
    #     weight.append(ss[i][1])
    # df_cloud_clean = pd.DataFrame({'词语': text, '权重': weight})
    # df_cloud_clean.to_csv(f'./data/{datatable}/{datatable}_wordcloud.csv', encoding = 'gb18030', index = None)

    con, cursor = get_con()
    for i in range(len(ss)):
        # 使用repr方法可以自动帮我们加上引号
        sql = f"insert into {datatable}_cloud values {ss[i]}"
        cursor.execute(sql)
    con.commit()
    con_close(con, cursor)


