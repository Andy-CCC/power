# 1. 打印欢迎信息
print("=" * 30)
print("     简单计算器 v1.0")
print("=" * 30)

# 2. 获取用户输入（复习 input 和类型转换）
num1 = float(input("请输入第一个数字: "))
operator = input("请输入运算符 (+, -, *, /): ")
num2 = float(input("请输入第二个数字: "))

# 3. 根据运算符计算结果（复习 if-elif-else 条件判断）
if operator == "+":
    result = num1 + num2
    print(f"\n{num1} + {num2} = {result}")
elif operator == "-":
    result = num1 - num2
    print(f"\n{num1} - {num2} = {result}")
elif operator == "*":
    result = num1 * num2
    print(f"\n{num1} * {num2} = {result}")
elif operator == "/":
    # 复习：除数不能为0的判断
    if num2 != 0:
        result = num1 / num2
        print(f"\n{num1} / {num2} = {result}")
    else:
        print("\n错误：除数不能为0！")
else:
    print("\n错误：不支持的运算符！")

# 4. 打印结束语
print("\n程序运行结束。")