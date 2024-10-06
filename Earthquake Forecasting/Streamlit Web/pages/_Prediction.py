import streamlit as st

st.title(" Earthquake Predicton ")
st.subheader("Linear Regression Algorithm")
code = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
"""
st.code(code) #display code

code1 = """
fig_hist, (ax_magnitude, ax_nst, ax_mmi) = plt.subplots(1, 3, figsize=(18, 6), dpi=100)

# Define the data and titles
plot_data = [('magnitude', ax_magnitude, "Magnitude"),
             ('nst', ax_nst, "NST"),
             ('mmi', ax_mmi, "MMI")]

# Plotting and setting titles in a loop
for data_col, axis, title in plot_data:
    sns.histplot(data=data_sampled, x=data_col, ax=axis)
    axis.set_title(title)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
"""
st.code(code1) #display code
st.image("image1.png")

code2 = """
fig, axes = plt.subplots(1, 2, figsize=(18, 6), dpi=100)

sns.histplot(data = data_sampled, x = 'sig', ax=axes[0])
axes[0].set_title("SIG")

sns.histplot(data = data_sampled, x = 'depth', ax=axes[1])
axes[1].set_title("Depth")
"""
st.code(code2) #display code
st.image("image2.png")

code3 = """
sns.boxplot(data=data_sampled,x='tsunami',y = 'magnitude')
plt.xticks(rotation=45,ha="right");
"""
st.code(code3) #display code
st.image("image3.png")

code4 = """
sns.boxplot(data=data_sampled,x='alert',y = 'depth')
plt.xticks(rotation=45,ha="right");
"""
st.code(code4) #display code
st.image("image4.png")

code5 = """
plt.figure(figsize=(15, 10))
sns.heatmap(data_sampled[['magnitude','nst','mmi','sig','depth']].corr(), annot=True, linecolor='black', cmap='magma')
plt.show()
"""
st.code(code5) #display code
st.image("image5.png")

code6 = """
X=np.array(data_sampled.loc[:,'sig'].values.reshape(-1, 1)) 
Y=np.array(data_sampled.loc[:,'magnitude'].values.reshape(-1, 1)) 

plt.scatter(X, Y)
plt.grid()
plt.xlabel("sig")
plt.ylabel("magnitude")
"""
st.code(code6) #display code
st.image("image6.png")

code7 = """
linreg = LinearRegression()

linreg.fit(X, Y) 

print('a=',linreg.coef_[0][0])  
print('b=',linreg.intercept_[0]) 

Y_hat=linreg.predict(X)
"""
st.code(code7) #display code
st.image("image7.png")

code8 = """
erro=Y_hat-Y
df_estimado=pd.DataFrame(np.concatenate((X,Y,Y_hat,erro),axis=1), columns=['X','Y','Y_hat','Erro (e)'])
df_estimado
"""
st.code(code8) #display code
st.image("image8.png")

code9 = """
plt.scatter(X, Y, label='Valor Real')
plt.scatter(X, Y_hat,color='red',  label='Valor Predito')
plt.grid()
plt.legend(loc='upper right')

plt.xlabel("Faltas por Semestre (X)")
plt.ylabel("Nota Final")
"""
st.code(code9) #display code
st.image("image9.png")

code10 = """
plt.scatter(X, Y)
plt.plot(X, Y_hat,color='red')
plt.grid()
plt.xlabel("Faltas por Semestre")
plt.ylabel("Nota Final")
"""
st.code(code10) #display code
st.image("image10.png")

code11 = """
print("MSE=",mean_squared_error(Y, Y_hat),", R^2=", r2_score(Y,Y_hat))
"""
st.code(code10) #display code
st.image("image11.png")

code12 = """
scatter_geo(data_frame=df, lat="latitude",lon="longitude",scope="world",color="magnitude",
            hover_name="magnitude")
"""
st.code(code12)
st.image("image12.png")

code13 = """
y=2004
scatter_geo(data_frame=df[df['year']==y], lat="latitude",lon="longitude",scope="world",
            color="magnitude",hover_name="magnitude",size='magnitude')
"""
st.code(code13)
st.image("image13.png")

code14 = """
y=2011
scatter_geo(data_frame=df[df['year']==y], lat="latitude",lon="longitude",scope="world",
            color="magnitude",hover_name="magnitude",size='magnitude')
"""
st.code(code14)
st.image("image14.png")