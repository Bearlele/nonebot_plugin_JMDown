# JMDown

## 项目简介
JMDown 基于 Nonebot2 + OneBot 自动下载 JM 本子并发送到 QQ 群聊。使用 PyPDF2 对下载的文件进行加密，以减少 TX 直接检测文件内容的可能性。

## 使用方法
### 1. 下载插件文件
直接下载 `JM.py` 放到插件文件夹内。

### 2. 配置 `jmcomic` 参数
在 `option.yml` 文件中进行配置，路径如下：
```
项目目录/config/JM/option.yml
```
配置指南请参考：[配置文件指南](https://github.com/hect0x7/JMComic-Crawler-Python/blob/master/assets/docs/sources/option_file_syntax.md)

## 解密密码
密码就是本子的id，jm114514密码就是114514

## 使用库
```python
pip install jmcomic
pip install hashlib
pip install PyPDF2
pip install os
pip install nonebot2
pip install nonebot_adapter_onebot
pip install nonebot_plugin_localstore
```

## 鸣谢
- [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python)
- [Nonebot2](https://github.com/nonebot/nonebot2)
- [OneBot](https://github.com/botuniverse/onebot)

## 免责声明
本项目仅供学习和交流使用，请勿用于任何非法用途。请确保您的使用行为符合相关法律法规，开发者不对任何滥用行为负责。

