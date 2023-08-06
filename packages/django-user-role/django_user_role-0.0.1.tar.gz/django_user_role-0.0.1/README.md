# django-user-role

此项目受 [django-role-permissions](https://github.com/vintasoftware/django-role-permissions) 启发，参考其编写

django-role-permissions 使用的是标准的django user group permissions的模型

group为人员分组，permissions为权限，group 与 permissions关联

此项目增加一个Role表，permissions将主要与Role表进行关联，同时也保留user和group其上的permissions使用
同时将user和group与role表进行关联，将django的三角关系 user group permissions 换成 user group role

user group role 这三者都可以体现出某些permissions的聚合，因此将permissions提取出去之后，将看起来好一些

暂未完成
