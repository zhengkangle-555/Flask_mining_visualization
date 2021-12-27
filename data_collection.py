import requests
import re
import json
import time
import pandas as pd
from lxml import etree


# 为了防止被封IP，下面使用基于redis的IP代理池来获取随机IP，然后每次向服务器请求时都随机更改我们的IP（该ip_pool搭建相对比较繁琐，此处省略搭建细节）
# 假如不想使用代理IP的话，则直接设置下方的time.sleep，并将proxies参数一并删除
proxypool_url = 'http://127.0.0.1:5555/random'
# 定义获取ip_pool中IP的随机函数
def get_random_proxy():
    proxy = requests.get(proxypool_url).text.strip()
    proxies = {'http': 'http://' + proxy}
    return proxies


# 前程无忧网站上用来获取每个岗位的字段信息
def job51(datatable, job_name, page):
    # 浏览器伪装
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'
    }
    # 每个页面提交的参数，降低被封IP的风险
    params = {
        'lang': 'c',
        'postchannel': '0000',
        'workyear': '99',
        'cotype': '99',
        'degreefrom': '99',
        'jobterm': '99',
        'companysize': '99',
        'ord_field': '0',
        'dibiaoid': '0'
    }
    href, update, job, company, salary, area, company_type, company_field, attribute = [], [], [], [], [], [], [], [], []
    # 使用session的好处之一便是可以储存每次的cookies，注意使用session时headers一般只需放上user-agent
    session = requests.Session()
    # 查看是否可以完成网页端的请求
    # print(session.get('https://www.51job.com/', headers=headers, proxies=get_random_proxy()))
    # 爬取每个页面下所有数据
    for i in range(1, int(page) + 1):
        url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{job_name},2,{i}.html'
        response = session.get(url, headers=headers, params=params, proxies=get_random_proxy())
        # 使用正则表达式提取隐藏在html中的岗位数据
        ss = '{' + re.findall(r'window.__SEARCH_RESULT__ = {(.*)}', response.text)[0] + '}'
        # 加载成json格式，方便根据字段获取数据
        s = json.loads(ss)
        data = s['engine_jds']
        for info in data:
            href.append(info['job_href'])
            update.append(info['issuedate'])
            job.append(info['job_name'])
            company.append(info['company_name'])
            salary.append(info['providesalary_text'])
            area.append(info['workarea_text'])
            company_type.append(info['companytype_text'])
            company_field.append(info['companyind_text'])
            attribute.append(' '.join(info['attribute_text']))
    #     time.sleep(np.random.randint(1, 2))
    # 保存数据到DataFrame
    df = pd.DataFrame(
        {'岗位链接': href, '发布时间': update, '岗位名称': job, '公司名称': company, '公司类型': company_type, '公司领域': company_field,
         '薪水': salary, '地域': area, '其他信息': attribute})
    # 保存数据到csv文件中
    df.to_csv(f'./data/{datatable}/51job_{datatable}.csv', encoding='gb18030', index=None)


# 猎聘网上用来获取每个岗位对应的详细要求文本
def liepin(datatable, job_name, page):
    # 浏览器伪装和相关参数
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'
    }
    job, salary, area, edu, exp, company, href, content = [], [], [], [], [], [], [], []
    # 使用session的好处之一便是可以储存每次的cookies，注意使用session时headers一般只需放上user-agent
    session = requests.Session()
    # print(session.get('https://www.liepin.com/zhaopin/', headers=headers, proxies = get_random_proxy()))
    # 通过输入岗位名称和页数来爬取对应的网页内容
    # job_name = input('请输入你想要查询的岗位：')
    # page = input('请输入你想要下载的页数：')
    # 遍历每一页上的数据
    for i in range(int(page)):
        url = f'https://www.liepin.com/zhaopin/?key={job_name}&curPage={i}'
        # time.sleep(np.random.randint(1, 2))
        response = session.get(url, headers=headers, proxies = get_random_proxy())
        html = etree.HTML(response.text)
        # 每页共有40条岗位信息
        for j in range(1, 41):
            # job.append(html.xpath(f'//ul[@class="sojob-list"]/li[{j}]/div/div[1]/h3/@title')[0])
            # info = html.xpath(f'//ul[@class="sojob-list"]/li[{j}]/div/div[1]/p[1]/@title')[0]
            # ss = info.split('_')
            # salary.append(ss[0])
            # area.append(ss[1])
            # edu.append(ss[2])
            # exp.append(ss[-1])
            # company.append(html.xpath(f'//ul[@class="sojob-list"]/li[{j}]/div/div[2]/p[1]/a/text()')[0])
            href.append(html.xpath(f'//ul[@class="sojob-list"]/li[{j}]/div/div[1]/h3/a/@href')[0])
    # 遍历每一个岗位的数据
    for job_href in href:
        # time.sleep(np.random.randint(1, 2))
        # 发现有些岗位详细链接地址不全，需要对缺失部分进行补齐
        if 'https' not in job_href:
            job_href = 'https://www.liepin.com' + job_href
        response = session.get(job_href, headers=headers, proxies = get_random_proxy())
        html = etree.HTML(response.text)
        content.append(html.xpath('//section[@class="job-intro-container"]/dl[1]//text()')[3])
    # 保存数据
    # df = pd.DataFrame({'岗位名称': job, '公司': company, '薪水': salary, '地域': area, '学历': edu, '工作经验': exp, '岗位要求': content})
    df = pd.DataFrame({'岗位要求': content})
    df.to_csv(f'./data/{datatable}/liepin_{datatable}.csv', encoding='gb18030', index=None)


