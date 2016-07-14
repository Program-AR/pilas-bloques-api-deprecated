# coding: utf-8
from app import app, db, models

lista = models.Solution.query.all();

print("")
print("Hay %d soluciones cargadas en el sistema" %(len(lista)))
print("")

for x in lista:
    print(x)
print("")
