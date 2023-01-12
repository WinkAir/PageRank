import requests
import json
import time

# 私钥
private_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# 打开要分组读取的文件
with open('domains.txt') as f:
    # 读入文件的所有行
    lines = f.readlines()
    # 计算总行数
    total_lines = len(lines)

    # 初始化空列表来存储处理后的结果
    results = []

    # 使用分片的方式读取文件内容
    for i in range(0, total_lines, 50):
        # 取出一组40行
        domains = lines[i:i+50]

        # 拼接请求的URL
        url = f'https://apistore.aizhan.com/baidurank/siteinfos/{private_key}?domains='

        # 遍历域名列表
        for domain in domains:
            # 拼接请求URL
            url += domain.strip() + '|'
        # 去除最后一个多余的'|'符号
        url = url[:-1]
        # 设置重试次数
        retry = 3
        # 发送请求，如果失败则重试
        while retry > 0:
            try:
                time.sleep(1)
                response = requests.get(url)
                break
            except:
                retry -= 1

        # 解析返回数据
        data = json.loads(response.text)
        #print(data)

        # 遍历返回的success数组
        for item in data['data']['success']:
            # 拼接结果
            result = item['domain'] + '[+]' + str(item['pc_br']) + '[-]' + str(item['m_br'])
            print(result)
            # 将结果保存到列表中
            results.append(result)

        # 将结果写入文件
        with open('results.txt', 'w') as f:
            f.write('\n'.join(results))
print("success")
