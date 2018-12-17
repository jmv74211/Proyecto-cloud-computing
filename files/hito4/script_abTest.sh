#!/bin/bash

#IP MV WEST-EU          CC-01:      51.136.25.13
#IP MV NORTH-EU         CC-02:      137.116.232.139
#IP MV EAST-US          CC-03:      40.121.10.71
#IP MV CENTRAL-FRANCE   CC-04:      40.89.158.99
#IP MV WEST-UK          CC-05:      51.141.31.225

echo -e Número de peticiones '\t' Peticiones/sh '\t' LatenciaMedia > salida.txt
echo ------------------------------------------------------------------------ >> salida.txt

for (( c=500; c<=5000; c=c+500 ))
do
  `ab -n $c -c 20 http://51.141.31.225/ > aux.txt`
  pts=`cat aux.txt | grep "Requests per second" | cut -d " " -f 7`
  ltm=`cat aux.txt | grep "Time per request" | head -n 1 | cut -d " " -f 10`
  echo -e $c '\t' $pts '\t' $ltm >> salida.txt
done

rm aux.txt
