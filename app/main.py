import os

from flask import Flask, request, jsonify
import urllib.parse

app = Flask(__name__)

@app.route("/")
def read_root():
    return {"Hello": "World"}

# 返回当前系统信息，以及python版本，pandas版本
@app.route("/info")
def info():
    import sys
    import pandas as pd
    # 返回当前文件夹包含的文件，和目录结构
    path = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(path)
    # 返回当前系统信息，以及python版本，pandas版本
    
    return {"sys": sys.platform, "python": sys.version, "pandas": pd.__version__,"files":files}

# 传入姓名参数，并打印出来
@app.route("/hello/<name>")
def hello_name(name):
    return {"Hello": name}

# 计算种子用户
@app.route("/seed/<name>")
def seed_list(name):

    # 捕捉异常
    try:   
        import pandas as pd
        path = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_excel(path+'/list.xlsx')
        # 遍历所有行，查询邀请人为name的用户，返回每一行的数据和统计总数，返回json格式
        count = 0
        result = []

        for index, row in df.iterrows():
            if row['邀请人'] == name:
                count += 1
                result.append(row.to_dict())
        return {"seed count": count, "seed list":result, "name1":name}
    except Exception as e:
        return {"error": str(e)}



# 计算种子用户数量
@app.route("/seed_count/<name>")
def seed_count(name):
    import pandas as pd
    path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(path+'/list.xlsx')
    # 遍历所有行，查询邀请人为name的用户，返回统计总数，返回json格式
    count = 0
    for index, row in df.iterrows():
        if row['邀请人'] == name:
            count += 1
    return {"count": count}


# 计算裂变用户数量
@app.route("/count/<name>")
def fission_count(name):
    import pandas as pd
    path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(path+'/list.xlsx')
    
    # 匹配name等于群成员昵称列表的记录，
    # 遍历所有行，查询邀请人为name的用户，返回每一行的数据和统计总数，返回json格式
    seed_count = 0
    fission_count = 0
    all_count = 0
    result = []
    for index, row in df.iterrows():
        # 如果该行的群成员昵称是name，跳过
        if row['群成员昵称'] == name:
            continue
        if row['邀请人'] == name:
            seed_count += 1
            result.append(row.to_dict())
            # fission_count 与每一条的邀请人数列相加
            fission_count += row['邀请人数']
    all_count = seed_count + fission_count
    return {"seed count": seed_count, "fission count":fission_count,"all count":all_count,"result": result}
    
# 计算GMV
@app.route("/gmv/<name>")
def gmv(name):
    import pandas as pd
    sdlist = seed_list(name)
    # 将sdlist解构
    sdlist = sdlist["seed list"]
    path = os.path.dirname(os.path.abspath(__file__))
    store = pd.read_csv(path+'/store_data.csv')

    gmv = 0
    for index, row in store.iterrows():
        if row["交易状态"] == "支付成功" and (row['买家'] == name or row['买家'] in sdlist):
            gmv += row['订单总金额']

    return {"gmv": gmv}

# 统计销量
@app.route("/sales/<name>")
def sales(name):
    import pandas as pd
    # 筛选出买家为name或者是种子用户的记录，并用交易状态为支付成功的记录个数-支付状态为已退款的记录个数
    sdlist = seed_list(name)
    # 将sdlist解构
    sdlist = sdlist["seed list"]
    path = os.path.dirname(os.path.abspath(__file__))
    store = pd.read_csv(path+'/store_data.csv')

    buyer = []

    sales = 0
    for index, row in store.iterrows():
        if row["交易状态"] == "支付成功" and (row['买家'] == name or row['买家'] in sdlist):
            buyer.append(row['买家'])
            sales += 1
        if row["交易状态"] == "已退款" and (row['买家'] == name or row['买家'] in sdlist):
            sales -= 1
    
    return {"sales": sales}

# 下单用户数
@app.route("/order/<name>")
def order(name):
    import pandas as pd
    sdlist = seed_list(name)
    # 将sdlist解构
    sdlist = sdlist["seed list"]
    path = os.path.dirname(os.path.abspath(__file__))
    store = pd.read_csv(path+'/store_data.csv')

    buyer = []

    for index, row in store.iterrows():
        if row["交易状态"] == "支付成功" and (row['买家'] == name or row['买家'] in sdlist):
            buyer.append(row['买家'])
    
    # 去重
    buyer = list(set(buyer))
    
    return {"order": len(buyer)}
    
# 线索用户
@app.route("/clue/<name>")
def clue_user(name):
    import pandas as pd
    # 种子用户列表
    sdlist = seed_list(name)

    # 将sdlist解构
    sdlist = sdlist["seed list"]
    path = os.path.dirname(os.path.abspath(__file__))
    store = pd.read_csv(path+'/store_data.csv')

    # 筛选出买家在种子用户列表中的记录，不反悔买家为name的记录，不反悔交易状态为支付成功的记录，返回买家和联系电话和交易状态
    buyer = []
    for index, row in store.iterrows():
        if row["交易状态"] != "支付成功" and (row['买家'] != name and row['买家'] in sdlist):
            buyer.append([row['买家'],row['联系电话']])

    return {"buyer": buyer}

# 线索细节
@app.route("/clue_detail/<name>")
def clue_detail(name):
    import pandas as pd
    path = os.path.dirname(os.path.abspath(__file__))
    store = pd.read_csv(path+'/store_data.csv')

    # 筛选出买家为name且交易状态不为支付成功的记录，返回交易状态和全部产品名称
    detail = []
    for index, row in store.iterrows():
        if row["交易状态"] != "支付成功" and row['买家'] == name:
            detail.append([row['交易状态'],row['全部商品名称'],row["创建时间"]])
    return {"buyer": detail}


# indexpage,种子用户数，裂变用户数，GMV，销量，下单用户数，线索用户数
@app.route("/index/<name>")
def index(name):

    try:
        import pandas as pd
        seed = seed_count(name)
        fission = fission_count(name)
        gmv_count = gmv(name)
        sales_count = sales(name)
        order_count = order(name)
        clue = clue_user(name)
        return {"seed": seed, "fission":fission,"gmv":gmv_count,"sales":sales_count,"order":order_count,"clue":clue}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))