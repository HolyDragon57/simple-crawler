user_input = input("请输入一个字符串和一个整数，以空格分隔： ")
inputs_list = user_input.split()

if len(inputs_list) != 2:
    print("请提供一个字符串和一个整数，以空格分隔。")
else:
    input_string, input_integer = inputs_list[0], int(inputs_list[1])

hash_table = {}
# 初始化前k个字符出现频率的哈希表
i = len(input_string) - 1
while i >= 0:
    if input_string[i]  not in hash_table:
        hash_table[input_string[i]] = 1
    else:
        hash_table[input_string[i]] += 1
    if len(input_string) - i == input_integer:
        break
    i -= 1

i = len(input_string) - 1
while i >= 0:
    # 维护哈希表：去尾加头
    hash_table[input_string[i]] -= 1
    if hash_table[input_string[i]] == 0:
        del hash_table[input_string[i]]
    if i-input_integer >= 0:
        if input_string[i-input_integer] in hash_table:
            hash_table[input_string[i-input_integer]] += 1
        else:
            hash_table[input_string[i-input_integer]] = 1
    # 改变字符串
    if input_string[i] in hash_table:
        input_string = input_string[:i] + '-' + input_string[i+1:]

    i -= 1

print(input_string)