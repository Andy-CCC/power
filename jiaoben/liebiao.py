# 学习数据结构：列表
from numpy.ma.extras import average

scores = []


# 定义功能函数
def show_menu():
    '''显示菜单'''
    print("\n==========学生成绩管理系统==========")
    print("1 添加成绩")
    print("2 查看所有成绩")
    print("3 统计信息：最高，最低，平均")
    print("4 删除成绩")
    print("5 退出")
    print("====================================")


def add_score():
    '''添加成绩'''
    try:
        score = float(input("请输入成绩："))
        scores.append(score)
        print(f'已添加：{score}')
    except ValueError:
        print('请输入有效数字！')


def show_scores():
    '''查看所有成绩'''
    if len(scores) == 0:
        print("\n 当前没有成绩记录")
    else:
        print(f"\n 所有成绩：{scores}")


def show_stats():
    '''显示统计信息'''
    if len(scores) == 0:
        print("暂无成绩，无法统计")
        return
    h = max(scores)
    l = min(scores)
    average = sum(scores) / len(scores)
    print("\n 统计信息")
    print(f"最高分：{h}")
    print(f"最低分：{l}")
    print(f"平均分：{average:.1f}")


def delete_score():
    """删除成绩"""
    if len(scores) == 0:
        print("\n📋 没有成绩可以删除")
        return

    try:
        score = float(input("请输入要删除的成绩: "))
        if score in scores:
            scores.remove(score)
            print(f"🗑️ 已删除: {score}")
        else:
            print(f"❌ 未找到成绩: {score}")
    except ValueError:
        print("❌ 请输入有效的数字！")

# 3. 主程序
while True:
    show_menu()
    choice = input("请选择操作 (1-5): ")

    if choice == "1":
        add_score()
    elif choice == "2":
        show_scores()
    elif choice == "3":
        show_stats()
    elif choice == "4":
        delete_score()
    elif choice == "5":
        print("\n👋 再见！")
        break
    else:
        print("❌ 无效输入，请输入 1-5")
