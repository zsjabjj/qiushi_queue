# -*- coding: utf-8 -*-
# 队列queue复习
from queue import Queue


# 创建一个队列
q = Queue()
q1 = Queue(maxsize=10)
#
# for i in range(10):
#     q.put(i)
#     q1.put(i)
#
# # 查看队列是否满
# print(q.full())
# print(q1.full())


# q1.put(11)  # 因为限制了10个, 所以会一直等待挂起
q1.put_nowait(11)  # 虽然限制了10个, 但是nowait, 所以不会挂起等待, 如果满了, 会抛出full信息

# 查看操作未完成的队列 unfinished_tasks
print(q.unfinished_tasks)
q.put(1)
print(q.unfinished_tasks)
data = q.get()
print(q.unfinished_tasks)
# 宣告队列的操作完毕
q.task_done()
print(q.unfinished_tasks)

# 让主线程等待队列的操作完毕之后再退出
# 若队列未宣告操作完毕, join一直挂起
q.join()