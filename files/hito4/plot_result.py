import numpy as np
from matplotlib import pyplot as plt


file1='/home/jmv74211/Escritorio/salida_WEST_EU.txt'
file2='/home/jmv74211/Escritorio/salida_NORTH_EU.txt'
file3='/home/jmv74211/Escritorio/salida_EAST_US.txt'


num_peticiones1 = np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[0])
req_s1= np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[1])
lat1= np.loadtxt(file1, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones2 = np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[0])
req_s2= np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[1])
lat2= np.loadtxt(file2, delimiter='\t', skiprows=2,usecols=[2])

num_peticiones3 = np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[0])
req_s3= np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[1])
lat3= np.loadtxt(file3, delimiter='\t', skiprows=2,usecols=[2])

## GRÁFICO NÚMERO DE PETICIONES/SEGUNDO

plt.figure()
plt.plot(num_peticiones1,req_s1, label="WEST_EU")
plt.plot(num_peticiones2,req_s2, label="NORTH_EU")
plt.plot(num_peticiones3,req_s3, label="EAST_US")

plt.title("Número de peticiones/s dependiendo de la región")
plt.xlabel("peticiones/s")
plt.ylabel("Número de peticiones")

plt.legend()

plt.savefig('./grafica_peticiones_s.png')


## GRÁFICO LATENCIA

plt.figure()
plt.plot(num_peticiones1,lat1, label="WEST_EU")
plt.plot(num_peticiones2,lat2, label="NORTH_EU")
plt.plot(num_peticiones3,lat3, label="EAST_US")

plt.title("Latencia dependiendo de la región")
plt.xlabel("Latencia (ms)")
plt.ylabel("Número de peticiones")

plt.legend()

plt.savefig('./grafica_latencia.png')
