#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import requests

from elasticsearch import Elasticsearch, helpers

esUrl = 'http://localhost:9200'

es = Elasticsearch(esUrl)

index = 'users'


# 创建索引
if (es.indices.exists(index) == False):
    # dynamic 表示自动创建索引
    mapping = {
        'dynamic': '',
        'properties': {
            'title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word',
                "store": "yes",  # 是否存储
            },
            'url': {
                'type': 'string'
            },
            'date': {
                'type': 'date'
            }
        }
    }
    result = es.indices.create(index)
    es.indices.analyze(index, body=mapping)

datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16',
    }, {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16',
    }, {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17',
    }, {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18',
    }
]

for k, row in enumerate(datas):
    es.index(index, body=row, doc_type='user', id=(k + 1))

search = {
    'query': {
        'match': {
            'title': '各地校车'
        }
    },
    'highlight': {
        'fields': {
            'title': {}
        }
    }
}

'''定制 highlight

下面的参数可以改变返回的结果。即可以为单独的字段设置不同的参数，也可以作为 highlight 的属性统一定义。

number_of_fragments
        fragment 是指一段连续的文字。返回结果最多可以包含几段不连续的文字。默认是5。

fragment_size
       一段 fragment 包含多少个字符。默认100。

pre_tags
       标记 highlight 的开始标签。例如上面的<em>。

post_tags
       标记 highlight 的结束标签。例如上面的</em>。

encoder
       说明字段是否为 html 格式，default：不是，html： 是。

no_match_size
       即使字段中没有关键字命中，也可以返回一段文字，该参数表示从开始多少个字符被返回。'''

result = es.search(index, search)
print(result)


def read_es(host, port, index, query=""):
    url = {"host": host, "port": port, "timeout": 1500}
    es = Elasticsearch([url])
    if es.ping():
        print("Successfully connect!")
    else:
        print("Failed.....")
        exit()
    if query == "":  # query为es的搜索条件
        query = {
            "query": {
                "match_all": {

                }
            },
            # "size":1000
        }
    else:
        query = {
            "query": {
                "match": {
                    'title': query,
                }
            },
            # 'highlight': {
            #     'fields': {
            #         'title': {}
            #     }
            # },

            "size": 1000
        }

    res = helpers.scan(es, index=index, scroll="20m", query=query)
    return res


data = read_es('127.0.0.1', 9200, "users", query="1")
for i in data:
    # print (i)
    print(i.get('_source').get('title'))
