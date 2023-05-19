"""
Generates performance reports for your stock portfolio.
"""
import csv
import argparse
import requests
parser = argparse.ArgumentParser()
parser.add_argument("--source", help="source file")
parser.add_argument("--target", help="target file")
try:
    args = parser.parse_args()
except SystemExit:
    pass


IEX_TOKEN = 'pk_0772026b4ce94b1eab01766092adeb02'

def read_portfolio(filename):
    """Returns data from a CSV file"""
    data_lst = []
    with open(filename, encoding="utf8") as filein:
        reader = csv.DictReader(filein)
        for row in reader:
            data_lst.append(row)
    return data_lst

def get_names(data):
    """get names of companies"""
    temp_names = ''
    for i in data:
        temp_names += i['symbol']+','
    temp_names = temp_names[:-1]
    return temp_names

def get_csvdata(data, query):
    """get symbols of companies"""
    temp = {}
    for i in data:
        temp[i['symbol']] = i[query]
    return temp

def get_current_data(names):
    """gets symbol, price, size, time"""
    url = "https://cloud.iexapis.com/stable/tops?token=pk_0772026b4ce94b1eab01766092adeb02&symbols="+names
    response = requests.get(url)
    data = response.json()
    return data

def get_book_value(csvdata):
    """get previous value units*cost"""
    bookvaluedict = {}
    for i in csvdata:
        value = (int(round(float(i['units'])))*float(i['cost']))
        bookvaluedict[i['symbol']] = value
    return bookvaluedict

def get_market_value(currentdata, csvdata):
    """current value * previous shares"""
    marketvaluedict = {}
    for i in csvdata: #names
        for j in currentdata:
            if i['symbol'] == j['symbol']:
                value = int(i['units']) * j['lastSalePrice']
                marketvaluedict[i['symbol']] = value
    return marketvaluedict

def get_gainloss(book, current):
    """get gain/loss"""
    gainlossdict = {}
    for company in list(book.keys()):
        gainlossdict[company] = int(round(current[company] - book[company]))
    return gainlossdict

def get_gainlosschange(gldict, bookdict):
    """get change in gain/loss"""
    glchangedict = {}
    for name in list(bookdict.keys()):
        glchangedict[name] = gldict[name] / bookdict[name]
    return glchangedict

def format_data(csvfile, bookvalue, marketvalue, gainl, glch, output_file):
    """format the data to be stored in csv."""
    with open(output_file, 'w', encoding="utf8") as file:
        namefield = ['symbol',
                     'cost',
                     'book value',
                     'market value',
                     'gain/loss',
                     'gain/loss change']
        csvwriter = csv.writer(file)
        csvwriter.writerow(namefield)
        for i in csvfile:
            tempdict = {}
            temp = []
            temp.append(i['symbol'])
            temp.append(i['cost'])
            temp.append(bookvalue[i['symbol']])
            temp.append(marketvalue[i['symbol']])
            temp.append(gainl[i['symbol']])
            temp.append(glch[i['symbol']])
            tempdict[i['symbol']] = temp
            #print(tempdict)
            csvwriter.writerow(temp)

def save_portfolio(datas, filename):
    """save the data into the csv file"""
    with open(filename, 'w', encoding="utf8") as filesin:
        fieldnames = ['symbol', 'units', 'cost']
        csvwrite = csv.DictWriter(filesin, fieldnames=fieldnames)
        csvwrite.writeheader()
        csvwrite.writerow(datas)

def return_status():
    """returns site status"""
    response = requests.get("https://cloud.iexapis.com/stable/tops?token=pk_0772026b4ce94b1eab01766092adeb02&symbols=AAPL")
    return response

def return_names(output):
    """return names"""
    with open(output, encoding="utf8") as filee:
        alist = []
        csvreader = csv.DictReader(filee)
        for line in csvreader:
            alist.append(line['symbol'])
    return alist


def main():
    """
    Entrypoint into program.
    """
    csvdata = read_portfolio(args.source)
    names = get_names(csvdata)
    current_data = get_current_data(names)
    bookvalue = get_book_value(csvdata)
    marketvalue = get_market_value(current_data, csvdata)
    gainl = get_gainloss(bookvalue, marketvalue)
    glch = get_gainlosschange(gainl, bookvalue)

    format_data(csvdata, bookvalue, marketvalue, gainl, glch, args.target)

if __name__ == '__main__':
    main()
