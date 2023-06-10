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
set_png_as_page_bg('6.JPG')


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
    <div style="background-color:white ;padding:10px">
    <h2 style="color:red;text-align:center;">Заполни форму</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

   
    st.sidebar.subheader("Итоговая работа в рамках курса Diving into Darkness of Data Science")
    st.sidebar.text("Разработчик - Дубовцов А.А.")

    CreditScore = st.slider('Скоринговый балл', 0, 400)
    Geography = st.selectbox('География/регион', ['Минск', 'Брест', 'Могилев'])
    Gender = st.selectbox('Пол',  ['1', '2'])
    Age = st.number_input('Возраст', min_value=18, max_value=100, step=1)
    #st.slider("Возраст", 10, 100)
    Tenure = st.number_input('Длительность обслуживания в банке:', min_value=0, max_value=35, step=1)
    Balance = st.number_input('Баланс', min_value=0.00)
    #st.slider("Баланс", 0.00, 10000.00)
    NumOfProducts = st.selectbox('Количество продуктов', ['1', '2'])
    HasCrCard = st.selectbox("Есть кредитная БПК ?", ['0', '1'])
    IsActiveMember = st.selectbox("Активный клиент ?", ['0', '1'])
    EstimatedSalary = st.number_input('Зарплата', min_value=0.00)
    #= st.slider("Зарплата", 0.00, 10000.00)

    churn_html = """  
              <div style="background-color:#f44336;padding:20px >
               <h2 style="color:red;text-align:center;"> Жаль, но теряем клиента.</h2>
               </div>
            """
    no_churn_html = """  
              <div style="background-color:#94be8d;padding:20px >
               <h2 style="color:green ;text-align:center;"> Ура, клиент остаётся в банке !!!</h2>
               </div>
            """

    if st.button('Сделать прогноз'):
        output = predict_churn(CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
      # st.success('Вероятность оттока составляет {}'.format(output))
        st.success('Вероятность оттока составляет {:.2f} %'.format(output))
        if output >= 50:
            st.markdown(churn_html, unsafe_allow_html= True)


        else:
            st.markdown(no_churn_html, unsafe_allow_html= True)
            st.balloons()


if __name__=='__main__':
    main()

