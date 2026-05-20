# 这是一个简单的待办事项管理程序，用来复习列表和循环
# 1. 创建一个空列表，用来存放待办事项
todo_list = []


# 2. 打印功能菜单
def show_menu():
    print("\n" + "=" * 30)
    print("      待办事项管理器")
    print("=" * 30)
    print("1. 查看所有事项")
    print("2. 添加事项")
    print("3. 删除事项")
    print("4. 退出程序")
    print("=" * 30)


# 3. 查看所有事项
def show_todos():
    if len(todo_list) == 0:
        print("\n📌 当前没有待办事项，添加一个吧！")
    else:
        print("\n📋 你的待办事项：")
        for i, todo in enumerate(todo_list, 1):
            print(f"   {i}. {todo}")


# 4. 添加事项
def add_todo():
    todo = input("请输入要添加的事项: ")
    todo_list.append(todo)
    print(f"✅ 已添加: {todo}")


# 5. 删除事项
def delete_todo():
    if len(todo_list) == 0:
        print("\n📌 没有事项可以删除")
        return

    show_todos()  # 先显示列表，让用户看到编号
    try:
        num = int(input("请输入要删除的事项编号: "))
        if 1 <= num <= len(todo_list):
            removed = todo_list.pop(num - 1)
            print(f"🗑️ 已删除: {removed}")
        else:
            print("❌ 编号无效")
    except ValueError:
        print("❌ 请输入正确的数字")


# 6. 主程序（复习 while 循环）
while True:
    show_menu()
    choice = input("请选择操作 (1-4): ")

    if choice == "1":
        show_todos()
    elif choice == "2":
        add_todo()
    elif choice == "3":
        delete_todo()
    elif choice == "4":
        print("\n👋 再见！")
        break
    else:
        print("❌ 无效输入，请输入 1-4 之间的数字")
