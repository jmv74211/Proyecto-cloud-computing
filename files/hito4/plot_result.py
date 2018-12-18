import numpy as np
from matplotlib import pyplot as plt


file1='./abTest_WEST_EU.txt'
file2='./abTest_NORTH_EU.txt'
file3='./abTest_EAST_US.txt'
file4='./abTest_CENTRAL_FRANCE.txt'
file5='./abTest_WEST_UK.txt'


num_peticiones1 = np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[0])
req_s1= np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[1])
lat1= np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones2 = np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[0])
req_s2= np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[1])
lat2= np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones3 = np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[0])
req_s3= np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[1])
lat3= np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones4 = np.loadtxt(file4, delimiter='\t', skiprows=2,usecols=[0])
req_s4= np.loadtxt(file4, delimiter='\t', skiprows=2,usecols=[1])
lat4= np.loadtxt(file4, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones5 = np.loadtxt(file5, delimiter='\t', skiprows=2,usecols=[0])
req_s5= np.loadtxt(file5, delimiter='\t', skiprows=2,usecols=[1])
lat5= np.loadtxt(file5, delimiter='\t', skiprows=2,usecols=[2])

## GRÁFICO NÚMERO DE PETICIONES/SEGUNDO

plt.figure(1)

plt.subplot(211)

plt.plot(num_peticiones1,req_s1, label="WEST_EU")
plt.plot(num_peticiones2,req_s2, label="NORTH_EU")
plt.plot(num_peticiones3,req_s3, label="EAST_US")
plt.plot(num_peticiones4,req_s4, label="CENTRAL-FRANCE")
plt.plot(num_peticiones5,req_s5, label="WEST-UK")

plt.title("Número de peticiones/s dependiendo de la región")
plt.xlabel("Número de peticiones")
plt.ylabel("peticiones/s")

plt.legend()

plt.subplot(212)

plt.plot(num_peticiones1,lat1, label="WEST_EU")
plt.plot(num_peticiones2,lat2, label="NORTH_EU")
plt.plot(num_peticiones3,lat3, label="EAST_US")
plt.plot(num_peticiones4,lat4, label="CENTRAL-FRANCE")
plt.plot(num_peticiones5,lat5, label="WEST-UK")

plt.title("Latencia dependiendo de la región")
plt.xlabel("Número de peticiones")
plt.ylabel("Latencia (ms)")

plt.legend()

# Para reajustar los márgenes
plt.tight_layout()

plt.savefig('./grafica_peticiones_.png')
