#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
df = pd.read_csv('鄉鎮市區.csv')
data_list = df.values.tolist()
# print(len(data_list[24][0]))


# In[9]:


import flet as ft
import pickle

#-------linear regression model----------------------------------------------------------------------------
def predict_price(total_value, value3):
    # import the model and scalar
    model = pickle.load(open('model.pkl','rb'))
    scaler = pickle.load(open('scaler.pkl','rb'))
    
    district = np.zeros(37)
    district[value3] = 1           # 所在地區=1
    features = np.array(total_value)
    real = np.concatenate((features, district))
    real = np.array([real])
    real_norm = scaler.transform(real)
    # print(real)
    # print("real_norm:", real_norm)
    global price
    price = model.predict(real_norm)
    print(price)
    return price[0]
# show_price(price)

#-----------------------------------------------------------------------------------------------------------
# value0:土地面積,總樓層數,建物面積,房,廳,衛
# value1:建物型態
# value2:有無管理,車位,電梯
# value3:鄉鎮地區
# total_value:土地面積,總樓層數,建物型態,建物面積,房,廳,衛,有無管理,車位,電梯,鄉鎮地區
# price:最後預測價格

global value0, value1, value2, value3, total_value, price

def main(page: ft.Page):
    page.title = "買房小幫手 - 房價預測"
    head_t = ft.Text(size = 25, weight=ft.FontWeight.BOLD, color="BLUE")
    head_t.value = f"房價預測系統"
    head_t1 = ft.Text(size = 10, weight=ft.FontWeight.NORMAL, color="#B0C4DE")
    head_t1.value = f"Designed by 工科112 蔡文潼"
    head_t2 = ft.Text(size = 20, weight=ft.FontWeight.BOLD, color="BLUE")
    head_t2.value = f"系統功能"
    head_t3 = ft.Text(size = 15, weight=ft.FontWeight.NORMAL, color="#B0C4DE")
    head_t3.value = f"房價預測在房地產市場和房屋買賣交易中具有重要意義。                    \n通過機器學習模型來預測房價，可以幫助房地產開發商、房屋買賣代理人、投資者和買家等利益相關者                    \n做出更明智的決策。這樣的預測模型可以提供市場趨勢、價格趨勢和房價走勢等有價值的洞察，幫助使                    \n用者進行風險評估、資產配置和房地產投資。現代人在購買房屋時會考慮許多重要因素，本系統可以為                    \n您預測台南市的房價，提供您在買房時作為參考依據。"
    head_t4 = ft.Text(size = 15, weight=ft.FontWeight.NORMAL, color="#B0C4DE")
    head_t4.value = f"請您依照底下指示輸入您的需求，我們將會給您一個預測的房價做為參考。"
    null_t = ft.Text()

#------使用者要手動輸入的內容--------------------------------------------------------------------------------
    def textbox_changed(e):
        t.value = tb1.value, tb2.value, tb3.value, tb4.value, tb5.value, tb6.value   
        global value0, total_value, price
        value0 = []    # 存放得到的值
        value0 = list(t.value)            # tuple轉成list 
        value0 = [int(x) for x in value0] # str轉成int
        print("要輸入的值:", value0)
        
        total_value = []
        total_value = value0
        total_value.insert(2, value1[0])  # 建物型態
        if len(value2) != 0:
            total_value = total_value + value2
        print("所有的輸入:", total_value)
        
        price = predict_price(total_value, value3)  # model->predict price
        result_t.value = f"預測價格為 : "
        result_t1.value = f"{round(price, 2)}萬元"
        page.update()
#-------輸入地區----------------------------------------------------------------------------------------
    def textbox_changed1(e):   
        global value3
        value3 = []
        for i in range(37):
            if tb7.value == data_list[i][0]:
                value3.append(i)
                district_t.value = f"您所想要的地區為 :"
                district_t1.value = f"{tb7.value}"
                print("所在地區", i)
            page.update()
#-------Text field---------------------------------------------------------------------------------------      
    tb1 = ft.TextField(label="土地面積", hint_text="請輸入土地面積", suffix_text="平方公尺")#0
    tb2 = ft.TextField(label="建築總樓層數", hint_text="請輸入建築總樓層數", suffix_text="層")  #1
    tb3 = ft.TextField(label="建物面積", hint_text="請輸入建物面積", suffix_text="平方公尺") #3
    tb4 = ft.TextField(label="房間數量", hint_text="請輸入房間數量")         #4
    tb5 = ft.TextField(label="客廳數量", hint_text="請輸入客廳數量")         #5
    tb6 = ft.TextField(label="衛浴數量", hint_text="請輸入衛浴數量")         #6            
    
    tb7 = ft.TextField(label="所在地區", hint_text="例如:永康區")
# -------for建物型態-------------------------------------------------------------------------------------
    def dropdown_changed1(e):
        global value1
        value1 = []
        t.value = d1.value
        if t.value == '透天厝':
            value1.append(1)
        elif t.value == '住宅大樓':
            value1.append(2)
        elif t.value == '華夏':
            value1.append(3)
        elif t.value == '公寓':
            value1.append(4)
        print("建物型態的值:", value1)
        
# -------for有無----------------------------------------------------------------------------------------
    yes_no = []    
    a = []
    def dropdown_changed2(e):
        global value2
        value2 = []    # 存放得到的值
        t.value = d2.value, d3.value, d4.value
        yes_no.append(t.value)
        if len(yes_no) == 3:
            a = yes_no[2]
            for i in range(len(a)):
                if a[i] == '無':
                    value2.append(0)
                else:
                    value2.append(1)
            print("有無的值:", value2)
        
#---------選單-----------------------------------------------------------------------------------------------
    d1_text = ft.Text("建物型態")    #2
    d1 = ft.Dropdown(
        on_change=dropdown_changed1,
        width=100,
        options=[
            ft.dropdown.Option("透天厝"),
            ft.dropdown.Option("住宅大樓"),
            ft.dropdown.Option("華夏"),
            ft.dropdown.Option("公寓"),
        ],
    )
    d2_text = ft.Text("有無管理員")    #7
    d2 = ft.Dropdown(
        on_change=dropdown_changed2,
        width=100,
        options=[
            ft.dropdown.Option("有"),
            ft.dropdown.Option("無"),
        ],
    )
    d3_text = ft.Text("有無車位")    #8
    d3 = ft.Dropdown(
        on_change=dropdown_changed2,
        width=100,
        options=[
            ft.dropdown.Option("有"),
            ft.dropdown.Option("無"),
        ],
    )
    d4_text = ft.Text("有無電梯")    #9
    d4 = ft.Dropdown(
        on_change=dropdown_changed2,
        width=100,
        options=[
            ft.dropdown.Option("有"),
            ft.dropdown.Option("無"),
        ],
    )
#----Button--------------------------------------------------------------------------------------------------
    b1 = ft.OutlinedButton(text="確認地區", on_click=textbox_changed1)
    b = ft.OutlinedButton(text="預測房價", on_click=textbox_changed)
    
    t = ft.Text()
    district_t = ft.Text(color="#B0C4DE")
    district_t1 = ft.Text(color="#B0C4DE", size = 20, weight=ft.FontWeight.NORMAL)
    result_t = ft.Text(color="#B0C4DE")
    result_t1 = ft.Text(color="#B0C4DE", size = 20, weight=ft.FontWeight.NORMAL)
#----排版-----------------------------------------------------------------------------------------------------    
    page.add(
        ft.Row([head_t], alignment = "center"),
        ft.Row([head_t1], alignment = "center"),
        ft.Divider(height=9, thickness=3),
        ft.Row([head_t2, head_t3], alignment = "center"),
        ft.Divider(height=9, thickness=3),
        ft.Row([head_t4], alignment = "center"),
        ft.Row([tb7, b1], alignment = "center"),  # district
        ft.Row([district_t, district_t1], alignment = "center"),
        ft.Row([tb1, tb2, tb3], alignment = "center"),
        ft.Row([tb4, tb5, tb6], alignment = "center"),
        ft.Row([d1_text, d1, d2_text, d2, d3_text, d3, d4_text, d4, b], alignment = "center"),
        ft.Row([result_t, result_t1], alignment = "center"),
    )
#--------------------------------------------------------------------------------------------------------------
ft.app(target=main)


# In[ ]:





# In[ ]:




