import os
import psutil

"""
    杀python进程的脚本9
"""

# 杀掉占用最高的进程
print("kill the biggest python process")
# 遍历所有进程
py_procs = {}
for proc in psutil.process_iter():
    # 获取进程信息
    info = proc.as_dict(attrs=['pid', 'name', 'memory_percent'])
    # 如果是python进程，添加到字典中
    if info['name'] in ['python', 'python3']:
        py_procs[info['pid']] = info['memory_percent']

# 定义一个计数器变量
count = 1
# 如果字典不为空且计数器大于0
while py_procs and count > 0:
    # 找到memory_percent最大的键值对
    max_pid = max(py_procs, key=py_procs.get)
    max_mem = py_procs[max_pid]
    # 杀掉该进程
    os.system(f'sudo kill -9 {max_pid}')
    # 打印结果
    print(f'Killed process {max_pid} with memory_percent {max_mem}')
    # 从字典中删除该键值对
    del py_procs[max_pid]
    # 计数器加一
    count -= 1