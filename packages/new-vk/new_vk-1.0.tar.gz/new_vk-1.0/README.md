new_vk (Модификация библиотеки vk_api) ![Python 2.7, 3.4+](https://img.shields.io/pypi/pyversions/vk_api.svg) 
=================================================================================================================================================================================
**new_vk** – **vk_api – Python модуль для создания скриптов для социальной сети Вконтакте (vk.com API wrapper)**

* [Примеры использования](https://github.com/Warale/new_vk/tree/master/examples)
* [Официальная документация по методам API](https://vk.com/dev/methods)

```python
import new_vk

vk_session = new_vk.VkApi('+71112223344', 'mypassword')
vk_session.auth()

vk = vk_session.get_api()

print(vk.wall.post(message='Hello world!'))
```

Установка
------------
    $ pip install new-vk
