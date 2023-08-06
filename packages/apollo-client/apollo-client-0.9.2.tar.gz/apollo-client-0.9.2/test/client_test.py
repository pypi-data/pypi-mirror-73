#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/
# @Author  : Lin Luo/ Bruce Liu
# @Email   : 15869300264@163.com
from pyapollo import ApolloClient

client = ApolloClient(config_server_url='http://106.54.227.205:8000', app_id='bruce_test')
print(client.get_value('a'))
print(client.get_value('t', namespace='yes'))