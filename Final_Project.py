#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from sklearn.linear_model import LinearRegression

st.title("Does Drinking Affect Students' Education?")
st.markdown("Today, we will be determining whether alcohol consumption, as well as some other factors, affect students' grades. Below is a study done in 2 secondary schools in Portugal, where the legal drinking age is 16 for wine and beer, and 18 for all alcoholic beverages.")

df = pd.read_csv("student-mat.csv")

# I decided to only focus on certain columns of the dataframe, and removed the unnecessary columns.
st.markdown("We will be focusing on the students' age, family relationship, amount of free time, weekday alcohol consumption, weekend alcohol consumption, health status, and finally, their final grade.")
df = df[["age","famrel","freetime","Dalc","Walc","health","G3"]]
# Wanted to replace the name of G3 to finalgrade to make it look nicer.
df.rename(columns={'G3': 'finalgrade'}, inplace=True)
# Created a column that combined weekday and weekend alcohol consumption.
df["alccon"] = df["Walc"] + df["Dalc"]
df

st.subheader("Charting It Out")
st.markdown("First, I decided to make a chart to see the correlation between a student's weekend alcohol consumption and their final grade. The color and tooltip helps us determine the age of each datapoint.")
e = alt.Chart(df).mark_circle().encode(
    x = "alccon",
    y = "finalgrade",
    color = "age:N", 
    tooltip = ["age","finalgrade"])
st.altair_chart(e, use_container_width=True)
st.markdown("However, after charting the data, it is difficult to see whether the different age groups are affected by alcohol consumption. There are some outlier individuals that do really well or really poor, despite the age and alcohol consumption.")
st.markdown("The chart below shows the linear regression of the data. Since it slopes downward, that means higher alcohol consumption leads to lower grades.")

reg = LinearRegression()
X = np.array(df["alccon"]).reshape(-1,1)
y = np.array(df["finalgrade"]).reshape(-1,1)
reg.fit(X,y)
coef = float(reg.coef_)
intercept = float(reg.intercept_)

x = np.arange(15)
lr = pd.DataFrame({
    'x': x,
    'f(x)': (coef)*x+(intercept)})

f = alt.Chart(lr).mark_line().encode(
    x = "x",
    y = "f(x)")
full_chart = e + f
st.altair_chart(full_chart)

st.subheader("Underage vs. Legally Allowed")
st.markdown("Below is a subset of the above dataset where the age of the students is below the legal drinking age. In this case, the age is 15.")
A = df[df["age"]==15]
A
a = A["finalgrade"].mean()
st.write(f"The average final grade for this age group is {a}.")
st.markdown("The numeric scale for the final grade is from 0-20. As you can see, the average final grade for the underage group is slightly above 50%.")

st.markdown("This age group is only allowed to drink wine and beer, as they are still underage for hard liquor, and also cannot purchase it.")
B = df[(df["age"]==16) | (df["age"]==17)]
B
b = B["finalgrade"].mean()
st.write(f"The average final grade for this age group is {b}.")
st.markdown("The average final grade for this age group is about 50%")

st.markdown("In Portugal, the legal age to drink and purchase all types of alcohol is 18.")
C = df[df["age"]>17]
C
c = C["finalgrade"].mean()
st.write(f"The average final grade for this age group is {c}.")
st.markdown("As you can see, the final grade of this age group is lower than both of the previous age groups.")

st.subheader("Conclusion")
st.markdown("According to the linear regression chart and the average final grades of the different age groups, we can infer that alcohol consumption is a big factor in education. You can also see that the other factors, such as family relationship, freetime, etc., are vastly different for everyone. Therefore, there's a chance that those factors also affect alcohol consumption and final grades. For example, a bad family relationship and a lot of free time could lead to binge drinking which leads to bad grades. However, it is difficult to pinpoint since there are some students who have good grades, despite a bad family relationship and a higher alcohol intake.")

st.subheader('Estimate your final grade.')
with st.form('Survey'):
    st.selectbox('What is the quality of your family relationship? (1 - very bad to 5 - excellent)', [1,2,3,4,5])
    st.selectbox('How much free time do you have after school? (1 - very low to 5 - very high )', [1,2,3,4,5])
    dalc = st.selectbox('What is your alcohol consumption on an average weekday? (1 - very low to 5 - very high)', [1,2,3,4,5])
    walc = st.selectbox('What is your alcohol consumption on an average weekend? (1 - very low to 5 - very high)', [1,2,3,4,5])
    st.selectbox('How would you describe your health status? (1 - very bad to 5 - very good)', [1,2,3,4,5])
    good = st.checkbox('Check if you are of legal drinking age in your country of residence.')
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success('Complete')
        if good:
            st.write('Great! You are of age, so drink safely!', value = True)
            if (dalc + walc) > 5:
                st.write("Your final grade may be below 50%.")
            else:
                st.write("Your final grade may be above 50%.")
        else:
            st.write('Wait a few years to consume alcohol, child.')
            if (dalc + walc) > 5:
                st.write("Your final grade may be below 50%.")
            else:
                st.write("Your final grade may be above 50%.")
        
            
st.subheader("References")
st.markdown("The dataset was found on [Kaggle](https://www.kaggle.com/uciml/student-alcohol-consumption?select=student-mat.csv).")
st.markdown("Information about the legal drinking age in Portugal was found [here](https://www.tripadvisor.com/ShowTopic-g189158-i203-k11732586-Drinking_Age_in_Portugal-Lisbon_Lisbon_District_Central_Portugal.html).")
st.markdown("The [linear regression](https://christopherdavisuci.github.io/UCI-Math-10/Week5/Week5-Wednesday.html) portion was done in class.")

st.subheader("GitHub")
st.markdown("[GitHub repository](https://github.com/melodyen/Math-10-Final-Project)")
    
 
