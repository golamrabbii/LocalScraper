import pandas as pd
import requests
import time
import glob
import csv

def parser(addr):
    url = "http://3.1.115.160/bkoi/transformer"
    r = requests.post(url, data={'addr': addr})
    parsed = r.text
    return parsed

def reverse_geo(lat,lon):

    url = "https://barikoi.xyz/v1/api/search/reverse/geocode/server/MTQ4NjpIRUdRVzFEMVoz/place?longitude={}&latitude={}&post_code=true&union=true"
    
    requrl = url.format(lon,lat)

    time.sleep(2)

    r= requests.get(requrl)
    data = r.json()
    
    result=[]

    result.append(data['place']['city'])

    result.append(data['place']['area'])

    result.append(data['place']['postCode'])
    result.append(data['place']['union'])

    return result


if __name__ == "__main__":

    #Read all csv files name of this folder

    files = glob.glob("*.csv")

    with open('parsed_data.csv', 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames = ['longitude','latitude','name','Address','sub_area','city','area','postCode','category','ratings'])
        writer.writeheader()

    for file_name in files:
    
        name,lat,lon,rating,city,area,postcode,address,sub_area,category=[],[],[],[],[],[],[],[],[],[]

        df = pd.read_csv(file_name)

        for index,i in df.iterrows():

            address.append(parser(i['Street Address']))
            name.append(parser(i['Name']))
            
            if i['Rating']:
                rating.append(i['Rating'])
            else:
                rating.append('0')
            
            result = reverse_geo(i['Lat'],i['Long'])
            
            longitude = str(i['Long']).replace('&amp;ec=GAZAcQ','')
            
            lat.append(i['Lat'])

            lon.append(longitude)
            
            city.append(result[0])
            area.append(result[1])
            postcode.append(result[2])
            sub_area.append(result[3])

            category.append(parser(i['Category']))

            print('success')
            
        df1 = pd.DataFrame({'longitude':lon,'latitude':lat,'name':name,'Address':address,'sub_area':sub_area,'city':city,'area':area,'postCode':zip,'category':category,'ratings':rating})
        with open('parsed_data.csv','a') as output:
            df1.to_csv(output,index=False,header=None)


    #Remove duplicate entry from csv file and keep only first one
    
    df1 = pd.read_csv("parsed_data.csv")
    df1.drop_duplicates(subset=None,keep='first',inplace=True)
    df1.to_csv("parsed_data.csv",index=False)


