# winney
![pypi](https://img.shields.io/pypi/v/winney?color=blue) ![Codacy Badge](https://app.codacy.com/project/badge/Grade/6e1a16da7b3747e0b69440fd3826e8f3)

## Install
> pip install winney

## Tutorial
``` python
from winney import Winney

baidu = Winney(host="baidu.com")
baidu.register(method="get", name="get_home", uri="/home", use_mock=True, mock_data=MockData())
r = baidu.get_home()
print(r.json())
print(t)
```
