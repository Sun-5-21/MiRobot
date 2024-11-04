import math

center_x = 8.6
center_y = 4.3
radius = 0.5

# 步长
step = 0.05

# 初始x值
y = center_y - radius

# 存储结果的列表
points = []

while y  <= center_y + radius:
    # 计算y的两个可能值
    x = center_x + math.sqrt(radius**2 + (y-center_y)**2)
    
    # 添加到结果列表
    points.append((x, y))
    
    # 增加x值
    x += step
    y +=0.05

# 打印结果
for point in points:
    print(points)