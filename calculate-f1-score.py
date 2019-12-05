def Convert(string):
    li = list(string.split(","))
    return li


str1 = "Kublai,Khan,Chengiz,Chengiz,Khan"
str2 = "Khan,Nayan,Nayan,Achmac"
convert_str1 = sorted(Convert(str1))
convert_str2 = sorted(Convert(str2))
print(" ")
print("========== Two lists to compare==========")
print(" ")
print((convert_str1))
print((convert_str2))

print(" ")
print(" ")
print("========== Calculation of precision, recall and F1 ==========")
print(" ")
l1 =[]
l2 = ['test1','test2']
l1 = l1 + l2

common = sorted(set(convert_str2) & set(convert_str1))
unique_in_second_list = [x for x in convert_str2 if x not in common]

final = sorted(convert_str1 + unique_in_second_list)
#print(final)

list1 = []
list2 = []

for x in final:
    if x in convert_str1:
        list1.append(x)
        convert_str1.remove(x)
    else:
        list1.append(None)

for x in final:
    if x in convert_str2:
        list2.append(x)
        convert_str2.remove(x)
    else:
        list2.append(None)

true_positive_list = [i == j for i, j in zip(list1, list2)]
true_positive = len([x for x in true_positive_list if x is True])
print("true positive = " + str(true_positive))

false_positive = len([x for x in list1 if x is None])
print("false positive = " + str(false_positive))

false_negative = len([x for x in list2 if x is None])
print("false negative = " + str(false_negative))

precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
F1 = 2 * ((precision*recall) / (precision+recall))

print("precision = " + str(precision))
print("recall = " + str(recall))
print("F1 score = " + str(F1))