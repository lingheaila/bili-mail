from time import sleep
import sqlite3

import requests
import json

# 商品列表请求接口
url = "https://mall.bilibili.com/mall-magic-c/internet/c2c/v2/list"

conn = sqlite3.connect('biliMail.db')
cur = conn.cursor()
# 创建商品信息表
cur.execute("""CREATE TABLE IF NOT EXISTS products (
    c2cItemsId INTERGE PRIMARY KEY NOT NULL,
    c2cItemsType INTERGE,
    c2cItemsName TEXT,
    totalItemsCount INTERGE,
    price INTERGE,
    showPrice REAL,
    showMarketPrice REAL,
    uid TEXT,
    paymentTime TEXT,
    isMyPublish TEXT,
    uname TEXT,
    uspaceJumpUrl TEXT,
    uface TEXT,
    queryDate TEXT,
    isLose INTERGE,
    gotoUrl TEXT);""")
conn.commit()
# 创建商品详细信息表
cur.execute("""CREATE TABLE IF NOT EXISTS detailDto (
    c2cItemsId INTERGE,
    blindBoxId INTERGE,
    itemsId INTERGE,
    skuId INTERGE,
    detailName TEXT,
    img TEXT,
    marketPrice INTERGE,
    detailType INTERGE,
    isHidden TEXT);""")
conn.commit()

i_want = []
nextId = None
count = 0
while True:
    payload = json.dumps({
        # 类型 2312-手办 2066-模型 2331-周边 2273-3C fudai_cate_id-福袋
        # "categoryFilter": "2312",
        # 价格区间 50-100
        "priceFilters": [
            "4000-180001"
        ],
        # 折扣区间 5折到7折
        # "discountFilters": [
        #     "10-100"
        # ],
        # 排序 TIME_DESC-综合 PRICE_ASC-价格升序 PRICE_DESC-价格倒序
        # "sortType": "PRICE_DESC",
        "sortType": "PRICE_ASC",
        "nextId": nextId
    })

    headers = {
        'authority': 'mall.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4',
        'content-type': 'application/json',
        'cookie': "buvid4=53D0F02D-93BF-CEDB-6AA3-91B61EA869EA29175-023031517-9TO%2BhWhxQHP7d%2B6V2Ryv33wTfCH9mqfz%2B%2BocNNz8z9y5aJklOKNxdA%3D%3D; DedeUserID=25361414; DedeUserID__ckMd5=4d21abb6f34cd378; header_theme_version=CLOSE; buvid_fp_plain=undefined; enable_web_push=DISABLE; _uuid=B87A8115-164F-EEE2-E2BB-C314C10B74C8A67253infoc; hit-dyn-v2=1; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; buvid3=D88575AF-0884-9629-CC9C-FFA8A96518B983996infoc; b_nut=1713437884; rpdid=0zbfvTdZUR|wYG3nUeb|47q|3w1RXpKr; LIVE_BUVID=AUTO1517160370663633; home_feed_column=5; CURRENT_BLACKGAP=0; Hm_lvt_8d8d2f308d6e6dffaf586bd024670861=1728911771; fingerprint=64526bb1443f24a48a8830222f56ca36; buvid_fp=64526bb1443f24a48a8830222f56ca36; PVID=1; CURRENT_QUALITY=116; share_source_origin=QQ; bsource=share_source_qqchat; browser_resolution=2560-1271; bp_t_offset_25361414=1010425154129362944; kfcFrom=market_detail; from=market_detail; kfcSource=market_detail; msource=market_detail; canvasFp=87272e2ef42680aeb110078cd37aa0af; webglFp=89c4c764a8af37aff8bbc6a1f39de3e2; screenInfo=433*1078*24; feSign=7fb382025f70d6f8c90ab93668e6bc39; payParams=%7B%22customerId%22%3A11035%2C%22serviceType%22%3A0%2C%22orderId%22%3A%22508437543%22%2C%22orderCreateTime%22%3A1734245647798%2C%22orderExpire%22%3A120%2C%22feeType%22%3A%22CNY%22%2C%22payAmount%22%3A21997%2C%22originalAmount%22%3A21997%2C%22deviceType%22%3A2%2C%22deviceInfo%22%3A%22WEB%22%2C%22notifyUrl%22%3A%22http%3A//mall.bilibili.co/magic-trade/c2c/order/call-back%22%2C%22productId%22%3A%22136362856187%22%2C%22productUrl%22%3A%22https%3A//mall.bilibili.com/neul-next/index.html%3Fpage%3Dmagic-market_index%26noTitleBar%3D1%22%2C%22showTitle%22%3A%22GSC%20%u9ED1%u89C1%u82B9%u9999%20Q%u7248%u624B%u529E%22%2C%22showContent%22%3A%22GSC%20%u9ED1%u89C1%u82B9%u9999%20Q%u7248%u624B%u529E%22%2C%22createIp%22%3A%22240e%3A390%3A1e20%3Abc70%3Aa15f%3A2ad0%3A95ac%3Ac03b%22%2C%22createUa%22%3A%22Mozilla/5.0%20%28Linux%3B%20Android%206.0%3B%20Nexus%205%20Build/MRA58N%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/131.0.0.0%20Mobile%20Safari/537.36%22%2C%22returnUrl%22%3A%22https%3A//mall.bilibili.com/neul-next/index.html%3Fpage%3Dmagic-market_detail%26noTitleBar%3D1%26itemsId%3D136362856187%26from%3Dpay_result%22%2C%22failUrl%22%3A%22https%3A//mall.bilibili.com/neul-next/index.html%3Fpage%3Dmagic-market_detail%26noTitleBar%3D1%26itemsId%3D136362856187%26from%3Dpay_result%22%2C%22extData%22%3A%22%7B%5C%22orderId%5C%22%3A4001936329518006%7D%22%2C%22traceId%22%3A%22666897d19f9c458158a2c1769f675e7d%22%2C%22timestamp%22%3A1734245647811%2C%22version%22%3A%221.0%22%2C%22signType%22%3A%22MD5%22%2C%22sign%22%3A%22c8a1014dc26f034a466f9b0e653cef61%22%2C%22defaultChoose%22%3A%22alipay%22%2C%22extParams%22%3A%22%7B%5C%22psExt%5C%22%3A%7B%5C%22optType%5C%22%3A%5C%22jzbps_out%5C%22%7D%2C%5C%22profitSharing%5C%22%3A%5C%22jzbPs%5C%22%7D%22%2C%22uid%22%3A25361414%2C%22mobiApp%22%3Anull%7D; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ1MTU5NzcsImlhdCI6MTczNDI1NjcxNywicGx0IjotMX0.HEkt9fs8LO8tvjx9ZTLVbhHvBXGrGfpO-DOgojH7klI; bili_ticket_expires=1734515917; b_lsid=D4F54C22_193D55991A3; SESSDATA=dfad8106%2C1750006294%2Ccc590%2Ac1CjAOGdRzVuhxiMtqBEeh3ViU1_JdGGn8dctRsELTDXHnWy6TjXoDhPu3MOQQAFq3op4SVnNZT3NXSDBhZUFMZGdJbE4yTURTdkQzQkNVUURhdHM4a0FiOU1pc0JndlhMQUt6bWVXTlR4eGMxRXdhVU8wampVMHRZcnl4dFJGQTg0ZTN5ZFJpWW1BIIEC; bili_jct=7d9c46cbc7041ffbde43598b1e4798c1; CURRENT_FNVAL=2000; sid=5hhpb749",
        'origin': 'https://mall.bilibili.com',
        'referer': 'https://mall.bilibili.com/neul-next/index.html?page=magic-market_index',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        
        response = response.json()

        # 返回标志 success
        message = response["message"]
        # 下一页起始id
        nextId = response["data"]["nextId"]
        
        sleep(2)
        print(count)
        count += 1
        if message == "success":
            if nextId is None:
                break
            data = response["data"]["data"]
            with conn:
                for item in data:
                    # 商品Id
                    c2cItemsId = item['c2cItemsId']
                    # 商品类型
                    c2cItemsType =item['type']
                    # 商品名
                    c2cItemsName = item["c2cItemsName"]
                    # 总数
                    totalItemsCount = item['totalItemsCount']
                    # 实际价格（单位：分）
                    price = item["price"]
                    # 实际价格（单位：元，带两位小数）
                    showPrice = item["showPrice"]
                    # 原价（单位：元，带两位小数）
                    showMarketPrice = item["showMarketPrice"]
                    # 用户id 
                    uid = item['uid']
                    # 用户名称 
                    uname = item['uname']
                    # 用户空间跳转链接
                    uspaceJumpUrl = item['uspaceJumpUrl']
                    # 用户头像
                    uface = item['uface']
                    # 付款时间
                    paymentTime = item['paymentTime']
                    # 是否我的公开 
                    isMyPublish = item['isMyPublish']
                    # 商品详细信息
                    detailDtoList = item['detailDtoList']
                    # 查询时间
                    queryDate = '2024-12-18'
                    # 是否失效 0-否，1-是
                    isLose = 0
                    # 跳转链接
                    gotoUrl = f'https://mall.bilibili.com/neul-next/index.html?page=magic-market_detail&noTitleBar=1&itemsId={c2cItemsId}&from=market_index'

                    # 删除历史数据
                    cur.execute("""DELETE FROM products WHERE 1 != 1 OR c2cItemsId = :c2cItemsId;""", dict(c2cItemsId = c2cItemsId))
                    cur.execute("""DELETE FROM detailDto WHERE 1 != 1 OR c2cItemsId = :c2cItemsId;""", dict(c2cItemsId = c2cItemsId))
                    print(f'{c2cItemsId} ## {c2cItemsName} ## {showPrice}')
                    # 插入商品数据
                    cur.execute("""INSERT INTO products VALUES (
                        :c2cItemsId,
                        :c2cItemsType,
                        :c2cItemsName,
                        :totalItemsCount,
                        :price,
                        :showPrice,
                        :showMarketPrice,
                        :uid,
                        :paymentTime,
                        :isMyPublish,
                        :uname,
                        :uspaceJumpUrl,
                        :uface,
                        :queryDate,
                        :isLose,
                        :gotoUrl);""", 
                        dict (
                            c2cItemsId = c2cItemsId,
                            c2cItemsType = c2cItemsType,
                            c2cItemsName = c2cItemsName,
                            totalItemsCount = totalItemsCount,
                            price = price,
                            showPrice = showPrice,
                            showMarketPrice = showMarketPrice,
                            uid = uid,
                            paymentTime = paymentTime,
                            isMyPublish = isMyPublish,
                            uname = uname,
                            uspaceJumpUrl = uspaceJumpUrl,
                            uface = uface,
                            queryDate = queryDate,
                            isLose = isLose,
                            gotoUrl = gotoUrl
                        )
                        )
                    for detailDto in detailDtoList:
                        # 盲盒id
                        blindBoxId = detailDto['blindBoxId']
                        # 物品组id
                        itemsId = detailDto['itemsId']
                        # skuId
                        skuId = detailDto['skuId']
                        # 商品名称
                        detailName = detailDto['name']
                        # 商品图片
                        img = 'https:' + detailDto['img']
                        # 商品价格
                        marketPrice = detailDto['marketPrice']
                        # 商品类型
                        detailType = detailDto['type']
                        # 是否隐藏
                        isHidden = detailDto['isHidden']
                        if (totalItemsCount > 1):
                            print(f'---- {itemsId} ## {detailName} ## {marketPrice}')
                        # 插入商品详情数据
                        cur.execute("""INSERT INTO detailDto VALUES (
                            :c2cItemsId,
                            :blindBoxId,
                            :itemsId,
                            :skuId,
                            :detailName,
                            :img,
                            :marketPrice,
                            :detailType,
                            :isHidden);""", 
                        dict (
                            c2cItemsId = c2cItemsId, 
                            blindBoxId = blindBoxId, 
                            itemsId = itemsId, 
                            skuId = skuId, 
                            detailName = detailName, 
                            img = img, 
                            marketPrice = marketPrice, 
                            detailType = detailType, 
                            isHidden = isHidden
                            )
                            )

        #             if "GSC" in c2cItemsName or "梅柳" in c2cItemsName or "爱丽丝" in c2cItemsName or "蓝档案" in c2cItemsName:
        #                 if item not in i_want:
        #                     i_want.append(item)
        #                     print(str(item["c2cItemsId"]) + " ##" + item["c2cItemsName"] + "##" + item["showPrice"])
        #                 # 插入数据
        #                 conn.commit()
        # if count % 10 == 0:
        #     print("--------------------" + response["data"]["data"][0]["showPrice"])

    except Exception as e:
        sleep(3)
conn.close()

#print(i_want)

# min_element = min(i_want, key=lambda x: x["price"])
# for item in i_want:
#     print(f"{item['c2cItemsName']},{item['c2cItemsId']},{item['price']}")
# print(min_element)


# https://mall.bilibili.com/neul-next/index.html?page=magic-market_index
