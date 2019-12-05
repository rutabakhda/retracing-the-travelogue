from sklearn.metrics import cohen_kappa_score

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
        list1.append("No")

for x in final:
    if x in convert_str2:
        list2.append(x)
        convert_str2.remove(x)
    else:
        list2.append("No")


print(list1)
print(list2)

print("cohen kappa score")
print(cohen_kappa_score(list1, list2))
