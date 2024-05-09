from collections import Counter

# 假设这是你的列表
arrays = [[1, 2, 3], [2, 3, 4], [1, 2, 3], [2, 3, 4], [1, 2, 3]]

# 统计数组出现的次数
counter = Counter(map(tuple, arrays))

# 找出出现次数最多的数组
most_common_array = counter.most_common(1)[0][0]

print("出现次数最多的数组是:", list(most_common_array))