# -*- coding: utf-8 -*-

latein = []
deutsch = []

anzahl_zeilen = 0
anzahl_zeilen2 = 0

with open("liste_latein.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    latein.append(stripped_line)
    anzahl_zeilen += 1
print("Anzahl Zeilen im Latein-Dokument:",anzahl_zeilen)


with open("liste_deutsch.txt", "r") as a_file:
  for line in a_file:
    stripped_line2 = line.strip()
    deutsch.append(stripped_line2)
    anzahl_zeilen2 += 1
print("Anzahl Zeilen im Deutsch-Dokument:",anzahl_zeilen2)

dictionary = dict(zip(latein, deutsch))

for key in dictionary:
  print('"'+str(key)+'": "'+str(dictionary[key])+'",').decode("utf-8")
