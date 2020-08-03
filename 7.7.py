from csv import reader as reader
from json import dump as dump
from sys import path as path

path = path[0]


def get_data():
    with open(path + '/click_stream3.csv', 'r') as csv_file:  # открываем файл
        csv_reader = reader(csv_file)
        data = []
        for row in csv_reader:
            data.append(list(row))

    dict_keys = [[], [], [], [], []]
    for i in range(len(data)):
        data[i][2] = data[i][2][:7]
        for j in range(len(data[0])):
            dict_keys[j].append(data[i][j])

    for i, item in enumerate(dict_keys):
        dict_keys[i] = sorted(list(set(item)))

    dict_keys = dict_keys[1:]
    return data, dict_keys


def count_clicks(*args):
    count = 0
    list_check = list(args[:1])
    colums = list(args[1:])
    print(colums)
    for i in range(len(list_check[0])):
        count2 = 0
        for arg in range(len(colums)):
            if colums[arg] in list_check[0][i]:
                count2 += 1
        if count2 == len(colums):
            count += 1
    return count

# для удобства:
# dict_keys[0] - страница ('1_home_page', '2_search_page', '3_payment_page', '4_payment_confirmation_page')
# dict_keys[1] - месяц ('2015-01', '2015-02', '2015-03', '2015-04')
# dict_keys[2] - устройство ('Desktop', 'Mobile')
# dict_keys[3] - пол ('Female', 'Male')


def print_json_file():
    temp_list = get_data()
    data = temp_list[0]
    dict_keys = temp_list[1]
    result_dict = {}

    def set_json_keys(_dict, main_key, *args):
        result_dict.update({main_key: {}})
        for a in range(len(args[0])):
            _dict[main_key].update({args[0][a]: {}})
            for b in range(len(args[1])):
                _dict[main_key][args[0][a]].update({args[1][b]: {}})
                for c in range(len(args[2])):
                    _dict[main_key][args[0][a]][args[1][b]].update(
                        {args[2][c]: count_clicks(data, args[0][a], args[1][b], args[2][c])})
        return

    set_json_keys(result_dict, "month", dict_keys[1], dict_keys[0], dict_keys[3])
    set_json_keys(result_dict, "page", dict_keys[0], dict_keys[1], dict_keys[2])
    set_json_keys(result_dict, "device", dict_keys[2], dict_keys[1], dict_keys[0])
    set_json_keys(result_dict, "sex", dict_keys[3], dict_keys[1], dict_keys[0])

    with open(path + '/result.json', "w") as write_file:
        dump(result_dict, write_file)
    return


print_json_file()
