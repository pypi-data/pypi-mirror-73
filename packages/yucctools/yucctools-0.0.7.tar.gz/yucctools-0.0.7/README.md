## yucctools

常用的工具分享。可以方便的调用本工具去记录日志等。


### 安装

直接使用pip安装即可

```python
pip install yucctools
```


### 使用示例

#### 日志工具

可以方便的去初始化记录日志，并记录日志，样例：

```python
# 导入包
import yucctools as yt

# 初始化logger实例
logger = yt.logger(filepath='test.log')

# 记录信息，只要这么调用就可以使用了
logger.info('this is a test log!')
```


### 附录

pypi网页：https://pypi.org/project/yucctools/
