# py2so

通过 `Cython` 将 `py` 代码转 `c` 后编译成 `so` 文件 , 可以隐藏源码以及提升性能

## 开始

安装 `Cython`

```shell
pip install Cython
```

## 使用

将 `py2so.py` 放入项目根目录 , 执行

```shell
python py2so.py
```

### 可选参数

`-i` , 不进行编译的目录或文件

`-d` , 指定编译后的结果目录

`-v` , 指定 `python` 版本

`-c` , 指定需要复制的 `py` 文件或目录 ( 默认非 `py` 文件会全部复制 , `py` 文件则不会复制  )

默认参数为

```shell
python py2so.py -i py2so.py -d dist -v 3
```

## 注意事项

1. 如果有导入包行为 , 每个包下必须有 `__init__.py` , 否则编译后的代码执行将可能出现导入失败
2. 代码中不能有注解方式编写的代码 , 如 : `def func(a:int) -> int:` 
3. 代码中不能有错误代码, 否则编译会失败
4. 如果使用了类似模板文件 , 请注意路径问题 , 最好通过配置暴露文件路径
5. 打好的包必须在相同的平台上运行, Windows/Mac OS/Linux 不可跨平台执行


