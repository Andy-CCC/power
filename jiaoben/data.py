from operator import truediv


def liebiao():
    '''增删查改
    append,insert,remove,
    '''
    fruits = ['apple', 'banner', 'orange']
    # f-string（格式化字符串字面量）,如果不使用的话，就通过+的方案进行拼接
    print(f"原始列表：{fruits}")
    # 访问元素，第一个水果，最后一个水果
    print(f"第一个水果：{fruits[0]}")
    print(f"第一个水果：{fruits[-1]}")
    # 添加元素
    fruits.append('葡萄')
    print(f"添加后：{fruits}")
    # 在某个索引中加入元素
    fruits.insert(1, '西瓜')
    print(f'添加后:{fruits}')
    # 修改元素
    fruits[2] = '哈密瓜'
    print(f'修改后：{fruits}')
    # 删除元素
    fruits.remove('西瓜')
    print(f"删除后：{fruits}")
    # 删除并返回最后一个
    popped = fruits.pop()
    print(f"pop后：{fruits}，被删除的：{popped}")
    # 切片
    print(f'前两个元素：{fruits[:2]}')
    print(f'从索引1开始：{fruits[1:]}')
    # 遍历列表
    print('遍历列表：')
    for fruit in fruits:
        print(f'---{fruit}')
    # 常用方法
    numbers = [2, 4, 10, 3, 0, 1, 1, 1, 1, 1, ]
    # 排序
    numbers.sort()
    print(f'排序后：{numbers}')
    # 反转
    numbers.reverse()
    print(f'反转后：{numbers}')
    print(f'列表长度：{len(numbers)}')
    # 查看某个元素出现的个数
    print(f'元素1出现的个数：{numbers.count(1)}')


def yuanzu():
    '''元组'''
    # 创建元组
    colors = ("白色", "红色", "粉色", "黑色")
    print(f'元组：{colors}')
    # 修改元组
    # colors[0]="绿色"
    # 访问第一个元组元素
    print(f"第一个元素：{colors[0]}")
    # 遍历元组
    for color in colors:
        print(f'--- {color}')
    # 元组解包
    point = (10, 20)
    x, y = point
    print(f'解包： x={x}，y={y}')
    single = (5,)
    print(f'单元素元组：{single}')


def renwu_liebiao():
    '''
    记录一周的心情，并打印出多少天
    '''
    weeken_list = []
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('开心')
    weeken_list.append('伤心')
    print(f'本周心情记录：{weeken_list}')
    print(f'已经记录了多少天：{len(weeken_list)}')
    print(f'开心了多少天：{weeken_list.count("开心")}')


def liebiao_renwu1():
    '''你从数据库或 API 拿到了一份用户年龄的原始数据，包含一些无效值。你需要对这个列表进行清洗和分析。
    过滤无效数据：删除小于0或大于120的年龄（年龄范围应为1-120）
    分类统计：分别统计成年（≥18岁）和未成年（<18岁）的人数
    转换数据：生成一个新列表，里面是每个年龄加上"岁"字（比如 "23岁"）
    计算平均年龄：只计算有效数据的平均年龄，保留1位小数
    '''
    ages = [23, -5, 45, 0, 67, 120, 18, 99, -1, 34, 17, 200, 25]
    print(f'原始列表数据：{ages}')
    ages1 = []
    for age in ages:
        if 1 <= age <= 120:
            ages1.append(age)
    ages1.sort()
    print(f'清洗后的列表数据：{ages1}')
    # 分类统计成年和未成年
    adult_count = 0
    child_count = 0
    for age in ages1:
        if age >= 18:
            adult_count += 1
        else:
            child_count += 1
    print(f'年成人数量：{adult_count}')
    print(f'未成年人数量：{child_count}')
    # 每个参数加一个岁字
    sui_list = []
    for age in ages1:
        sui_list.append(f'{age} 岁')
    print(f'加了岁字：{sui_list}')
    # 计算平均年龄
    total = 0
    for age in ages1:
        total += age
    average = total / len(ages1)
    print(f'平均年龄为：{average:.1f} 岁')


def list_requiremen1():
    '''
    需求（6个）
    统计：分别统计"已完成"、"已发货"、"已取消"的订单数量
    筛选：找出金额大于100元的订单，打印出来
    求和：计算所有"已完成"订单的总金额
    转换：生成一个新列表，里面是每个订单的简化信息：订单号-金额元（比如 A001-299元）
    排序：按金额从高到低排序，打印前3个最贵的订单
    提取：只提取所有订单号，生成一个单独的列表
    '''
    orders = [
        ["A001", 299, "已发货"],
        ["A002", 45, "已完成"],
        ["A003", 1299, "已取消"],
        ["A004", 89, "已发货"],
        ["A005", 25, "已完成"],
        ["A006", 799, "已完成"],
        ["A007", 59, "已取消"],
        ["A008", 399, "已发货"],
    ]
    print('=' * 50)
    print('电商订单数据')
    print('=' * 50)
    # 需求1，统计各种状态的订单数量
    status_count = {
        "已完成": 0,
        "已发货": 0,
        "已取消": 0
    }
    key = status_count['已完成']
    print(key)
    for order in orders:
        # 确定索引值
        status = order[2]
        # 核心：判断这个键是否在字典里面
        if status in status_count:
            status_count[status] += 1
            print(status_count)
    print("各状态订单数量：")
    print(f'----- 已完成：{status_count["已完成"]} 单')
    print(f'----- 已发货：{status_count["已发货"]} 单')
    print(f'----- 已取消：{status_count["已取消"]} 单')

    #需求2：找出金额大于100元的订单
    for order in orders:
        if order[1]>100:
            print(f'{order[0]}------   {order[1]}   ---{order[2]}')
    #需求3：计算已完成订单的总金额
    num=0
    for order in orders:
        if order[2]=='已完成':
            num+=order[1]
    print(f'已完成订单总金额：{num}')
    #按金额排序，取前3个最贵的
    #用sorted排序，key，告诉它按照金额排序，reverse=true，表示从大到小
    sorted_order=sorted(orders,key=lambda x:x[1],reverse=True)
    top3=sorted_order[:3]
    print(top3)
    print('提取前3个订单')
    for i,order in enumerate(top3,1):
        print(f'---第{i}名--{order[0]}--{order[1]}--{order[2]}')

if __name__ == '__main__':
    # liebiao()
    # yuanzu()
    # renwu_liebiao()
    # liebiao_renwu1()
    list_requiremen1()
