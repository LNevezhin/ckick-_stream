from csv import reader as reader
from sys import path as path
import plotly.express as px
import pandas as pd
import plotly

path = path[0]


def get_data():
    with open(path + '/click_stream3.csv', 'r') as csv_file:
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

def set_data():
    temp_list = get_data()
    data = temp_list[0]
    dict_keys = temp_list[1]
    pages = dict_keys[0]

    for i in range(4):
        number1 = []
        number2 = []
        for j in range(4):
            number1.append(count_clicks(data, dict_keys[0][j], dict_keys[2][0], dict_keys[1][i]))
            number2.append(count_clicks(data, dict_keys[0][j], dict_keys[2][1], dict_keys[1][i]))

        desktop = pd.DataFrame(dict(number=number1, page=pages))
        desktop['device'] = 'Desktop'
        mobile = pd.DataFrame(dict(number=number2, page=pages))
        mobile['device'] = 'Mobile'
        device = pd.concat([desktop, mobile], axis=0)
        fig = px.funnel(device, x='number', y="page", color='device')
        plotly.offline.plot(fig)
        # fig.show()


set_data()
