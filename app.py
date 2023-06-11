import sklearn
#from sklearn.ensemble import GradientBoostingClassifier
import streamlit as st
import pickle
import numpy as np

import base64
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return
set_png_as_page_bg('6.jpg')


classifier_name=['Сatboost']
option = st.sidebar.selectbox('Модель прогнозирования оттока клиентов', classifier_name)
st.subheader(option)



model=pickle.load(open("model_saved","rb"))



def predict_churn(CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary):
    input = np.array([[CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary]])
    prediction = model.predict_proba(input)[:, 1] * 100
    return float(prediction)    



def main():
    st.title("Прогноз оттока клиентов")
    html_temp = """
    <div style="background-color:white ;padding:5px">
    <h2 style="color:black;text-align:center;">Заполни форму</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

   
    st.sidebar.subheader("Итоговая работа в рамках курса Diving into Darkness of Data Science")
    st.sidebar.text("Разработчик - Дубовцов А.А.")

    CreditScore = st.slider('Скоринговый балл', 0, 400)
    Geography = st.selectbox('География/регион', ['Минск', 'Брест', 'Могилев'])
    #Gender = st.selectbox('Пол',  ['1', '2'])
    Gen = st.selectbox('Пол',  ['Женский', 'Мужской'])
    if Gen == 'Женский':
        Gender = 0
    else:
        Gender = 1

    Age = st.number_input('Возраст', min_value=18, max_value=100, step=1)
    #st.slider("Возраст", 10, 100)
    Tenure = st.number_input('Длительность обслуживания в банке:', min_value=1, max_value=35, step = 1)
    Bal = st.number_input('Баланс', min_value=0.00)
    if Bal < 100:
        Balance = 100
    elif Bal >= 100 and Bal < 6000:
        Balance = Bal
    else:
        Balance = 6000
    Num = st.selectbox('Количество продуктов', ['1', '2 и более'])
    if Num == '1':
        NumOfProducts = 1
    else:
        NumOfProducts = 2
    HasCr = st.selectbox("Есть кредитная БПК ?", ['Нет', 'Да'])
    if HasCr == 'Нет':
        HasCrCard = 0
    else:
        HasCrCard = 1
    IsActive = st.selectbox("Активный клиент ?", ['Нет', 'Да'])
    if IsActive == 'Нет':
        IsActiveMember = 0
    else:
        IsActiveMember = 1
    Salary = st.number_input('Зарплата', min_value=0.00)
    if Salary < 100:
        EstimatedSalary = 100
    elif Salary >= 100 and Salary < 6000:
        EstimatedSalary = Salary
    else:
        EstimatedSalary = 6000

    churn_html = """  
              <div style="background-color:#f44336;padding:20px >
               <h2 style="color:red;text-align:center;"> Жаль, но теряем клиента. <br>Добавить клиента в СРМ кампанию: потенциально потерянные клиенты.</h2>
               </div>
            """
    
    no_churn_html = """  
              <div style="background-color:#94be8d;padding:20px >
               <h2 style="color:green ;text-align:center;"> Клиент остаётся в банке.</h2>
               </div>
            """
    
    mb_churn_html = """  
              <div style="background-color:#8dc9f7;padding:20px >
              <h2 style="color:blue ;text-align:center;"> Клиент может уйти из банка. <br>Добавить клиента в СРМ кампанию: удержание клиентов.</h2>
              </div>
            """

    
    if st.button('Сделать прогноз'):
    
        if Balance < 300 and EstimatedSalary < 300 and IsActiveMember == 0 and NumOfProducts == 1:
            st.success('Вероятность оттока составляет более 90%.'.format(output))
            st.markdown(churn_html, unsafe_allow_html= True)


        else:
            output = predict_churn(CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
            st.success('Вероятность оттока составляет {:.2f} %'.format(output))
            if output >= 85:
                st.markdown(churn_html, unsafe_allow_html= True)
            elif output >= 40:
                st.markdown(mb_churn_html, unsafe_allow_html= True)
            else:
                st.markdown(no_churn_html, unsafe_allow_html= True)
                st.balloons()


if __name__=='__main__':
    main()

