import urllib.request
import json
import re

url = "https://s.shopee.vn/5AspSCyLEp"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req)
    final_url = res.geturl()
    print("Final URL:", final_url)
    
    # URL format usually has -i.<shopid>.<itemid>
    match = re.search(r'-i\.(\d+)\.(\d+)', final_url)
    if match:
        shopid = match.group(1)
        itemid = match.group(2)
        print(f"ShopID: {shopid}, ItemID: {itemid}")
        
        api_url = f"https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}"
        api_req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        api_res = urllib.request.urlopen(api_req)
        data = json.loads(api_res.read().decode('utf-8'))
        print("API Name:", data['data']['name'])
        print("API Description:", data['data']['description'][:100])
except Exception as e:
    print("Error:", e)
