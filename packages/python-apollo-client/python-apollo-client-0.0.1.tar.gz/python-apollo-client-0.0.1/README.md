python-apollo-client
================

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Python连接 [Apollo配置中心](https://github.com/ctripcorp/apollo)  
站在巨人的肩膀上  
基于https://github.com/BruceWW/pyapollo修改  
感谢原作者  


# 安装

```shell
pip install python-apollo-client
```


# 用法

- 启动客户端长连接监听

```python
client = ApolloClient(username=<username>, password=<password>, app_id=<appId>, cluster=<clusterName>, config_server_url=<configServerUrl>)
client.start()
```

- 获取Apollo的配置

```python
client.get_value(Key, DefaultValue)
```


# 参考
https://github.com/ctripcorp/apollo  
https://github.com/filamoon/pyapollo  
https://github.com/BruceWW/pyapollo  
