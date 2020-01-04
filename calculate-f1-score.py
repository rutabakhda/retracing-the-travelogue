"""
Implementation of F1 score

Calculating F1 score to compare the manual annotations.
Also comparing efficiency of different algorithms against manual annotations.

"""


def Convert(string):
    """

    :param string: Input string
    :return: list from the string
    """
    li = list(string.split(","))
    print(li)
    return li


def combine_lists(list1,list2):

    """
    :param list1: 1st list
        first list with unique values
    :param list2: 2nd list
        second list with unique values
    :return: list
    """
    common_words = list(set(list2).intersection(list1))

    unique_in_list1 = [x for x in list1 if x not in common_words]

    final_list = (unique_in_list1 + list2)
    final_list = sorted(final_list)
    return final_list


def change_list_size(bigger_list,smaller_list):
    """

    :param bigger_list: Big / Combined list
    :param smaller_list: list which is converted to the size of bigger list
    :return: converted smaller list
    """
    converted_list = []
    for x in bigger_list:
        if x in smaller_list:
            converted_list.append(x)
            smaller_list.remove(x)
        else:
            converted_list.append(None)
    return converted_list


def compare_calculate_f1_score(converted_list1,convrted_list2):

    """

    :param converted_list1: List 1 to be compared
    :param convrted_list2: List 2 to be compared
    :return: F1 score
    """

    true_positive_list = [i == j for i, j in zip(converted_list1, convrted_list2)]
    true_positive = len([x for x in true_positive_list if x is True])
    print("true positive = " + str(true_positive))

    false_positive = len([x for x in converted_list1 if x is None])
    print("false positive = " + str(false_positive))

    false_negative = len([x for x in convrted_list2 if x is None])
    print("false negative = " + str(false_negative))

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    F1 = 2 * ((precision * recall) / (precision + recall))

    print("precision = " + str(precision))
    print("recall = " + str(recall))
    print("F1 score = " + str(F1))

    return F1
str1 = "Kublai,Khan,Chengiz,Chengiz,Khan"
str2 = "Khan,Nayan,Nayan,Achmac"

print(" ")
print("========== Two lists to compare==========")

list_of_str1 = sorted(Convert(str1))
list_of_str2 = sorted(Convert(str2))

print(" ")
print(" ")
print("========== Calculation of precision, recall and F1 ==========")
print(" ")
#l1 = []
#l2 = ['test1', 'test2']
#l1 = l1 + l2

#common = sorted(set(list_of_str2) & set(list_of_str2))
#unique_in_second_list = [x for x in list_of_str2 if x not in common]

#final = sorted(list_of_str1 + unique_in_second_list)
# print(final)
combined_list = combine_lists(list_of_str1, list_of_str2)
print(combined_list)

converted_list1 = change_list_size(combined_list,list_of_str1)
converted_list2 = change_list_size(combined_list,list_of_str2)

F1 = compare_calculate_f1_score(converted_list1,converted_list2)