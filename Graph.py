import matplotlib.pyplot as plt

import pandas as pd 

y = pd.read_csv('./data.csv')

# print(y)
# d = y["Time"]

fig, ax = plt.subplots(2,1)

# y.plot(kind='line',x='Time',y='Temperatura1',color='blue',ax=ax)
# y[['Temperatura1','Temperatura2']].plot(kind='line',x='Time',color='red')

ax[0].plot(y['Time']-1574223934,y['Temperatura1'],color='red',label="Temperatura bulbo seco")
ax[0].plot(y['Time']-1574223934,y['Temperatura2'],color='blue',label="Temperatura bulbo úmido")
ax[0].legend(loc='best')
ax[0].grid()

ax[1].plot(y['Time']-1574223934,y['Umidade'],color='blue',label="Umidade Calculada")
ax[1].plot(y['Time']-1574223934,y['Umidade BMP'],color='lightblue',label="Umidade BMP")
ax[1].legend(loc='best')
ax[1].grid()


plt.savefig('output.png',dpi=300)


# plt.grid()
# plt.show()