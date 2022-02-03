import csv
import urllib3
http = urllib3.PoolManager()

url = 'https://www.diorvett.com.ec/StockReporte/StockProductos.csv'
r = http.request('GET', url, preload_content=False)
data_json = []
print(r.readline())
while True:
    data = str(r.readline()).strip()
    if len(data)>4:
        data = data[0:len(data)-1]
        cols = data[3:].split('","')
        print(f"cols:{cols}") 
        if len(cols)>3:
            sku = cols[0]
            qty = cols[3]
            data_json.append({"sku":sku, "qty":float(qty)})
        else:
            break
    else:
        break

print(f"data_json:{data_json}") 