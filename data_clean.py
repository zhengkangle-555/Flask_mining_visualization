import jieba
import re
import numpy as np
import pandas as pd


def job51_clean(datatable):
    # 读取数据
    data = pd.read_csv(f'./data/{datatable}/51job_{datatable}.csv', encoding = 'gb18030')
    # 考虑舍弃薪水和工作职责上的缺失数据
    data.dropna(subset = ['薪水'], inplace = True)
    # 去除重复值
    data.drop_duplicates(inplace = True)
    # 索引重置
    data.index = range(data.shape[0])

    # 接下来，我们对薪水这一列的表示方法都统一规范为数字（千/月）
    for i in range(len(data)):
        data['薪水'][i] = str(data['薪水'][i])
        if re.findall(r'(.*)\-(.*)\万\/\年', data['薪水'][i]):
            # 注意下面的findall返回的是一个list of list的结构
            s = re.findall(r'(.*)\-(.*)\万\/\年', data['薪水'][i])[0]
            # 保留小数点后两位
            salary = np.round((float(s[0]) + float(s[1])) / 2 * 10 / 12, 2)
            data['薪水'][i] = salary
        # 注意elif写法（else if）
        elif re.findall(r'(.*)\-(.*)\万\/\月', data['薪水'][i]):
            s = re.findall(r'(.*)\-(.*)\万\/\月', data['薪水'][i])[0]
            salary = np.round((float(s[0]) + float(s[1])) / 2 * 10, 2)
            data['薪水'][i] = salary
        elif re.findall(r'(.*)\-(.*)\千\/\月', data['薪水'][i]):
            s = re.findall(r'(.*)\-(.*)\千\/\月', data['薪水'][i])[0]
            salary = np.round((float(s[0]) + float(s[1])) / 2, 2)
            data['薪水'][i] = salary
        # 注意：findall查找返回单个元组时只是一个list结构
        elif re.findall(r'(.*)\万\以\上\/\年', data['薪水'][i]):
            s = re.findall(r'(.*)\万\以\上\/\年', data['薪水'][i])[0]
            salary = np.round(float(s) * 10 / 12, 2)
            data['薪水'][i] = salary
        elif re.findall(r'(.*)\万\以\上\/\月', data['薪水'][i]):
            s = re.findall(r'(.*)\万\以\上\/\月', data['薪水'][i])[0]
            salary = np.round(float(s) * 10, 2)
            data['薪水'][i] = salary
        elif re.findall(r'(.*)\万\以\下\/\年', data['薪水'][i]):
            s = re.findall(r'(.*)\万\以\下\/\年', data['薪水'][i])[0]
            salary = np.round(float(s) * 10 / 12, 2)
            data['薪水'][i] = salary
        # 一个月默认按30天计算
        elif re.findall(r'(.*)\元\/\天', data['薪水'][i]):
            s = re.findall(r'(.*)\元\/\天', data['薪水'][i])[0]
            salary = np.round(float(s) * 30 / 1000, 2)
            data['薪水'][i] = salary
        # 一天默认工作8小时
        elif re.findall(r'(.*)\元\/\小时', data['薪水'][i]):
            s = re.findall(r'(.*)\元\/\小时', data['薪水'][i])[0]
            salary = np.round(float(s) * 8 * 30 / 1000, 2)
            data['薪水'][i] = salary
        elif re.findall(r'(.*)\千\以\下\/\月', data['薪水'][i]):
            s = re.findall(r'(.*)\千\以\下\/\月', data['薪水'][i])[0]
            salary = np.round(float(s), 2)
            data['薪水'][i] = salary

    # 对地域这一列进行字段重编码
    data['地区'] = data['地域'].apply(lambda x: x.split('-')[0])
    # 进行省份的划分，注意增加北京、天津、上海这三个地级市
    anhui = list(pd.read_csv('./区域划分/省级划分/安徽.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    fujian = list(pd.read_csv('./区域划分/省级划分/福建.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    gansu = list(pd.read_csv('./区域划分/省级划分/甘肃.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    guangdong = list(pd.read_csv('./区域划分/省级划分/广东.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    guangxi = list(pd.read_csv('./区域划分/省级划分/广西.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    guizhou = list(pd.read_csv('./区域划分/省级划分/贵州.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    hainan = list(pd.read_csv('./区域划分/省级划分/海南.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    hebei = list(pd.read_csv('./区域划分/省级划分/河北.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    henan = list(pd.read_csv('./区域划分/省级划分/河南.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    heilongjiang = list(pd.read_csv('./区域划分/省级划分/黑龙江.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    hubei = list(pd.read_csv('./区域划分/省级划分/湖北.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    hunan = list(pd.read_csv('./区域划分/省级划分/湖南.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    jilin = list(pd.read_csv('./区域划分/省级划分/吉林.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    jiangsu = list(pd.read_csv('./区域划分/省级划分/江苏.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    jiangxi = list(pd.read_csv('./区域划分/省级划分/江西.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    liaoning = list(pd.read_csv('./区域划分/省级划分/辽宁.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    neimenggu = list(pd.read_csv('./区域划分/省级划分/内蒙古.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    ningxia = list(pd.read_csv('./区域划分/省级划分/宁夏.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    qinghai = list(pd.read_csv('./区域划分/省级划分/青海.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    shandong = list(pd.read_csv('./区域划分/省级划分/山东.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    shanxi = list(pd.read_csv('./区域划分/省级划分/山西.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    shangxi = list(pd.read_csv('./区域划分/省级划分/陕西.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    sichuan = list(pd.read_csv('./区域划分/省级划分/四川.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    xizang = list(pd.read_csv('./区域划分/省级划分/西藏.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    xinjiang = list(pd.read_csv('./区域划分/省级划分/新疆.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    yunnan = list(pd.read_csv('./区域划分/省级划分/云南.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    zhejiang = list(pd.read_csv('./区域划分/省级划分/浙江.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    chongqing = list(pd.read_csv('./区域划分/省级划分/重庆.txt', sep='aa', names=['txt'], engine='python', encoding='utf8').txt)
    # 对31个省市进行遍历
    sheng_list = []
    for i in range(len(data)):
        if data['地区'][i] in anhui:
            sheng_list.append('安徽')
        elif data['地区'][i] in fujian:
            sheng_list.append('福建')
        elif data['地区'][i] in gansu:
            sheng_list.append('甘肃')
        elif data['地区'][i] in guangdong:
            sheng_list.append('广东')
        elif data['地区'][i] in guangxi:
            sheng_list.append('广西')
        elif data['地区'][i] in guizhou:
            sheng_list.append('贵州')
        elif data['地区'][i] in hainan:
            sheng_list.append('海南')
        elif data['地区'][i] in hebei:
            sheng_list.append('河北')
        elif data['地区'][i] in henan:
            sheng_list.append('河南')
        elif data['地区'][i] in heilongjiang:
            sheng_list.append('黑龙江')
        elif data['地区'][i] in hubei:
            sheng_list.append('湖北')
        elif data['地区'][i] in hunan:
            sheng_list.append('湖南')
        elif data['地区'][i] in jilin:
            sheng_list.append('吉林')
        elif data['地区'][i] in jiangsu:
            sheng_list.append('江苏')
        elif data['地区'][i] in jiangxi:
            sheng_list.append('江西')
        elif data['地区'][i] in liaoning:
            sheng_list.append('辽宁')
        elif data['地区'][i] in neimenggu:
            sheng_list.append('内蒙古')
        elif data['地区'][i] in ningxia:
            sheng_list.append('宁夏')
        elif data['地区'][i] in qinghai:
            sheng_list.append('青海')
        elif data['地区'][i] in shandong:
            sheng_list.append('山东')
        elif data['地区'][i] in shanxi:
            sheng_list.append('山西')
        elif data['地区'][i] in shangxi:
            sheng_list.append('陕西')
        elif data['地区'][i] in sichuan:
            sheng_list.append('四川')
        elif data['地区'][i] in xizang:
            sheng_list.append('西藏')
        elif data['地区'][i] in xinjiang:
            sheng_list.append('新疆')
        elif data['地区'][i] in yunnan:
            sheng_list.append('云南')
        elif data['地区'][i] in zhejiang:
            sheng_list.append('浙江')
        elif data['地区'][i] in chongqing:
            sheng_list.append('重庆')
        elif data['地区'][i] == '北京':
            sheng_list.append('北京')
        elif data['地区'][i] == '天津':
            sheng_list.append('天津')
        elif data['地区'][i] == '上海':
            sheng_list.append('上海')
        else:
            sheng_list.append('其它')
    data['省份'] = sheng_list

    # 生成人数这一列
    num_list = []
    k = 0
    for i in range(len(data)):
        s = str(data['其他信息'][i])
        num_str = s.split(' ')[-1]
        if re.findall(r'\d', num_str):
            num_list.append(int(re.findall(r'\d', num_str)[0]))
        else:
            num_list.append(np.nan)
            k += 1
    data['人数'] = num_list

    # 为了后续招聘人数的分析，这里我们也选择遗弃掉这部分数据
    # data['人数'].fillna(np.round(np.mean(num_mean_list), 0), inplace=True)

    # print('招聘人数缺失数量有%s条，占总样本比例为%s' %(k, k / data.shape[0]))

    # 生成学历这一列
    k = 0
    edu_list = []
    for i in range(len(data)):
        s = str(data['其他信息'][i])
        edu_str = s.split(' ')[-2]
        if edu_str in ['博士', '硕士', '本科', '大专', '中专', '高中', '初中及以下']:
            edu_list.append(edu_str)
        else:
            edu_list.append(np.nan)
            k += 1
    data['学历'] = edu_list
    # print('学历未标明的数量有%s条，占总样本比例为%s' %(k, k / data.shape[0]))

    # 生成经验这一列
    jingyan_list = []
    for i in range(len(data)):
        try:
            ss = data['其他信息'][i].split(' ')[-3]
            if '经验' in ss:
                if re.findall(r'(.*)\-(.*)\年', ss):
                    ss_num = re.findall(r'(.*)\-(.*)年', ss)[0]
                    jingyan = np.round((float(ss_num[0]) + float(ss_num[1])) / 2, 0)
                    jingyan_list.append(format(jingyan, '.0f'))
                elif re.findall(r'(.*)\年', ss):
                    ss_num = re.findall(r'(.*)\年', ss)[0]
                    jingyan_list.append(format(float(ss_num), '.0f'))
                else:
                    jingyan_list.append(0)
            else:
                jingyan_list.append(0)
        except:
            jingyan_list.append(0)
    data['经验'] = jingyan_list

    # 将人数和学历的缺失值全部去除
    data.dropna(subset = ['人数', '学历'], inplace = True)
    data.index = range(data.shape[0])

    # 去除无意义的字段
    data.drop(labels = ['其他信息', '地域', '地区'], axis = 1, inplace = True)
    # 公司类型从前文来看缺失的比例很小，所以直接使用众数进行填充
    data['公司类型'] = data['公司类型'].fillna(data['公司类型'].mode().values[0])

    data.to_csv(f'./data/{datatable}/51job_{datatable}_preprocessing.csv', encoding = 'gb18030', index = None)


# 自定义函数来实现分词和去除停用词操作
def m_cut(tmpstr, stoplist):
    return [w.strip() for w in jieba.lcut(tmpstr) if w not in stoplist and len(w) > 1]


def liepin_clean(datatable):
    df = pd.read_csv(f'./data/{datatable}/liepin_{datatable}.csv', encoding = 'gb18030')
    # 考虑到工作职责上爬取信息时出现的空缺或爬取不到数据的情况，接下来，我们需要对工作职责这一列进行数据清洗
    for i in range(len(df)):
        df['岗位要求'][i] = str(df['岗位要求'][i])
        # 遍历工作职责这一列，若发现字符串长度小于30，则删除掉这一行的数据，若字符串大于30且匹配到的？占字符串长度的40%以上，同样删除掉这一行的数据
        if len(df['岗位要求'][i]) < 30 or len(re.findall(r'\?', df['岗位要求'][i])) / len(df['岗位要求'][i]) > 0.4:
            df.drop(i, axis=0, inplace=True)
    # 索引重置
    df.index = range(df.shape[0])
    # 导入停用词，借用哈工大停用词，同时自己也手动添加部分词汇进去
    stoplist = pd.read_csv('data/hit_stopwords.txt', names = ['txt'], sep ='aa', engine ='python', encoding ='utf8').txt.tolist()
    # 导入自定义词典
    dic = './data/自定义词典.txt'
    jieba.load_userdict(dic)
    # 先去除部分不相关的词汇，之后调用上述函数进行分词及去除停用词的操作
    df0 = df['岗位要求'].str.replace(r'[/-/\n/\t/\r\d·]', '').apply(lambda x: m_cut(x, stoplist))
    # 将处理后的数据保存下来
    df0.to_csv(f'./data/{datatable}/liepin_{datatable}_detail.csv', encoding = 'gb18030', index = None)



