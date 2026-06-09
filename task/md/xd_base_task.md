# 模块描述
这是一个基于Python实现的代码块，是心动任务的基类

# 代码路径
task/xd/xd_base_task.py 

# 模块依赖
logger/xd_logger_cfg.py

# 父属性
xd_steam_ids: xd steam 游戏id列表

# 抽象方法
_get_data(): 获取指定数据
_handle_data(records): 处理和清洗数据
_save_data(records): 保存数据

# 父类方法
execute: 任务执行的模板方法
1. _get_data: 获取指定数据
2. _handle_data: 处理和清洗数据
3. _save_data: 保存数据
每一步抽象方法的调用和结束都要将必要的信息记录到logger