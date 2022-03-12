import json
import tkinter as tk

import requests


def allowOnlyNumber(c):
    return c.isdigit() or c == '.'


def getCurrencyCode(c):
    file_p = open("data.json", "r")
    currency_symbol = json.load(file_p)
    key_list = list(currency_symbol.keys())
    value_list = list(currency_symbol.values())
    index = value_list.index(c)
    return key_list[index]


def getRate(curr, res):
    symb = getCurrencyCode(curr)
    return res['rates'][symb]


url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"


def currenciesList():
    file_p = open("data.json", "r")
    currency_symbol = json.load(file_p)
    return currency_symbol.values()


def divideString(string):
    arr = string.split(" ")
    l = len(arr) // 3
    l = l * 2
    st = " ".join(arr[:l])
    st += "\n" + " ".join((arr[l:]))
    return st


def convert():
    inp = entry.get()
    if inp == "":
        return
    curr_from = str1.get()
    curr_to = str2.get()
    headers = {
        'x-rapidapi-host': "exchangerate-api.p.rapidapi.com",
        'x-rapidapi-key': "YOUR API KEY"
    }
    response = requests.request('GET', url, headers=headers)
    if response.json()['result'] == 'success':
        response = response.json()
        rate1 = getRate(curr_from, response)
        rate2 = getRate(curr_to, response)
        inp = float(inp)
        x = inp / rate1
        y = x * rate2
        text = f"{inp} {str1.get()} = {round(y, 7)} {str2.get()}"
        if len(text) > 30:
            text = divideString(text)
        label6.config(text=text)
    else:
        label6.config(text=f"Error Encountered")


root = tk.Tk()
root.title("Currency Converter App")
root.geometry('420x420')
validation = root.register(allowOnlyNumber)
label1 = tk.Label(root, text="Currency Converter App", font=('bold', 20))
label1.pack(pady=15)

label2 = tk.Label(root, text="Choose the currencies", font=('bold', 15))
label2.pack(pady=4)

currency = list(currenciesList())

label3 = tk.Label(root, text="From", font=('bold', 10), fg='blue')
label3.pack(pady=4)

str1, str2 = tk.StringVar(), tk.StringVar()

str1.set(currency[0])
str2.set(currency[0])

drop1 = tk.OptionMenu(root, str1, *currency)
drop1.pack()

label4 = tk.Label(root, text="To", font=('bold', 10), fg='blue')
label4.pack(pady=4)

drop2 = tk.OptionMenu(root, str2, *currency)
drop2.pack()

label5 = tk.Label(root, text="Enter the Amount", font=('bold', 14), fg='blue', width=70)
label5.pack(pady=6)

entry = tk.Entry(root, font=('bold', 14), fg='black', width=30, validate="key", validatecommand=(validation, '%S'))
entry.pack(pady=6, padx=8)

button = tk.Button(root, text="Calculate", font=('bold', 14), width=20, fg='black', command=convert)
button.pack(pady=4, padx=8)

label6 = tk.Label(root, text=f"{entry.get()} {str1.get()} = \n{str2.get()}", font=('bolder', 11), fg='blue', width=70)
label6.pack(pady=6)

root.mainloop()
