import requests
from bs4 import BeautifulSoup
import pandas

current_page = 1
end_page_num = 78
all_rest = []

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

while(current_page <= end_page_num):
    response = requests.get("https://www.zomato.com/baton-rouge-la/restaurants?page="+format(current_page),headers=headers)

    content = response.content
    soup = BeautifulSoup(content,"html.parser")

    top_rest = soup.find_all("div",attrs={"class": "ui cards"})
    list_tr = top_rest[0].find_all("div",attrs={"class": "card search-snippet-card search-card"})

    list_rest =[]
    for tr in list_tr:
        dataframe ={}
        try:
            dataframe["name"] = (tr.find("a",attrs={"class": "result-title hover_feedback zred bold ln24 fontsize0"})).text.replace('\n', ' ')
            dataframe["address"] = (tr.find("div",attrs={"class": "col-m-16 search-result-address grey-text nowrap ln22"})).text.replace('\n', ' ')
            dataframe["food_type"] = (tr.find("span",attrs={"class":"col-s-11 col-m-12 nowrap pl0"})).text.replace('\n', ' ')
            dataframe["food_type"] = dataframe["food_type"].split(",")
            dataframe["cost"] = (tr.find("span", attrs={"itemprop": "priceRange"})).text.replace('\n', ' ')
        except AttributeError:
            #del dataframe
            dataframe["cost"] = "Unknown"
        #else:
            #if dataframe["cuisine_type"] == "" or dataframe["rest_name"] == "" or dataframe["rest_address"] == "":
                #del dataframe
        #if dataframe["food_type"] == "":
        if '' in dataframe["food_type"]:
            dataframe["food_type"] = "Unknown"
        
        list_rest.append(dataframe)
    all_rest += list_rest
    print(current_page)
    current_page += 1

print(len(all_rest))
print(all_rest)

df = pandas.DataFrame(all_rest)
df.to_csv("br_res.csv",index=False)