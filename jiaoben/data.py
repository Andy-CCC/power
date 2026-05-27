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
        if 0 <= age <= 120:
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


if __name__ == '__main__':
    # liebiao()
    # yuanzu()
    # renwu_liebiao()
    liebiao_renwu1()
