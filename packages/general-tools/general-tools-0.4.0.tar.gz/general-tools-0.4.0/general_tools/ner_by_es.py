#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                                                                             
Author: xuwei                                        
Email: 18810079020@163.com                                 
File: answer_by_es.py
Date: 2020/3/30 8:33 下午
'''

from .es import BaseSearcher
from elasticsearch_dsl.query import Match

class GetResByEs(object):
    # ['总论', '自然', '自然辩证法', '自然辩证法总论']
    @classmethod
    def str_list_element_drop_contain_sorted(cls, str_list: list):
        if len(str_list) < 2:
            return str_list
        str_list = sorted(str_list, key=lambda e: len(e), reverse=True)
        res_list = []
        for i in range(1, len(str_list) + 1):
            exist = False
            for j in range(len(str_list) - i):
                if str_list[-1 * i] in str_list[j]:
                    exist = True
                    break
            if not exist:
                res_list.insert(0, str_list[-1 * i])
        return res_list

    @classmethod
    def getResOfNameInQuery(cls, text, es_model, limit=40):
        es_search = BaseSearcher(es_model.Index.using, doc_model=es_model)
        total, query_list = es_search.search_by_multi_bool(should=[Match(name=text)], limit=limit)
        query_list = [r['_source'] for r in query_list]
        name_dict = dict()
        name_list = []
        for x in query_list:
            if x.get('name') and x.get('name') in text:
                name_list.append(x['name'])
                name_dict[x['name']] = x
        name_list = cls.str_list_element_drop_contain_sorted(name_list)
        return {'name_list': name_list, 'name_map': name_dict}

    @classmethod
    def getNerList(cls, text, es_model, limit=40):
        res_map = cls.getResOfNameInQuery(text, es_model, limit=limit)
        return res_map['name_list']


