import numpy as np
import matplotlib.pyplot as plt

lahetettySymboli = complex(1, 1)

kanavanImpulssivaste = complex(15, -0.2)

demoduloituSymboli = lahetettySymboli*kanavanImpulssivaste

'''
 Kanava kääntää vaihetta ja vaimentaa (tai vahvistaa) signaalin amplitudia
 Vaihe saadaan korjattua kanavan impulssivasteen kompleksikonjugaatilla kertoen
 Vihje: käytä np.conj komentoa

 Kanavan vaimennus saadaan kompensoitua jakamalla impulssivasteen itseisarvon neliöllä
 Vihje: käytä np.abs ja np.power komentoja

 Sinun tehtävänäsi on siis avata alla olevat kommentit ja kehittää oikea koodi ??? merkeillä
 merkattuihin kohtiin siten, että vaikka muuttelet miten tuota kanavan impulssivastetta, niin
 vaihe- ja amplitudikorjattu signaali palautuu aina lahetettySymboli muotoon.

'''

Vaihekorjattu = demoduloituSymboli * np.conj(kanavanImpulssivaste)
print("Vaihekorjattu signaali = ", Vaihekorjattu)

AmplitudiKorjattu = Vaihekorjattu / np.power(np.abs(kanavanImpulssivaste), 2)
print("Vaihe ja amplitudikorjattu signaali = ", AmplitudiKorjattu)

'''
Ja toisena tehtävänä tutkitaan miten MIMO signaali voidaan vastaanottaa.
Tarvitaan siis tieto millaista kanavaa pitkin signaali on edennyt:
- Antennista 1 antenniin 1 => kanavanImpulssivaste h11
- Antennista 1 antenniin 2 => kanavanImpulssivaste h12
- Antennista 2 antenniin 1 => kanavanImpulssivaste h21
- Antennista 2 antenniin 2 => kanavanImpulssivaste h22

Tiedetään vain se mitä on vastaanotettu eli demoduloidut symbolit
- Mitä on vastaanotettu antennista 1 => r1
- Mitä on vastaanotettu antennista 2 => r2

Halutaan tietää mitä on lähetetty:
- Antennista 1 => s1
- Antennista 2 => s2

Lähetetään antennista 1 symboli 1+j ja antennista 2 2+2j,
Keksitään kanavan impulssivasteet ja lasketaan vastaanotetut symbolit, jotka
sitten korjataan (tai ratkaistaan yhtälöparista)
'''

l1 = complex( (1 if np.random.randn(1) >= 0.5 else -1),  (1 if np.random.randn(1) >= 0.5 else -1))
l2 = complex( (1 if np.random.randn(1) >= 0.5 else -1),  (1 if np.random.randn(1) >= 0.5 else -1))
# alustetaan kanava satunnaisesti
h11 = complex(np.random.randn(1), np.random.randn(1))
# alustetaan kanava satunnaisesti
h12 = complex(np.random.randn(1), np.random.randn(1))
# alustetaan kanava satunnaisesti
h21 = complex(np.random.randn(1), np.random.randn(1))
# alustetaan kanava satunnaisesti
h22 = complex(np.random.randn(1), np.random.randn(1))
#h11 = complex(1, 1)
#h12 = complex(0.5, 0.5)
#h21 = complex(-0.5, -0.5)
#h22 = complex(1, 0.2)


# Laitetaan kaikki matriisimuotoon

transmittedValues = np.array([[l1], [l2]])

print("lähetetty = ", transmittedValues)

channelMatrix = np.array([[h11, h12], [h21, h22]])
print("kanavamatriisi = ", channelMatrix)

invertedChannelMatrix = np.linalg.inv(channelMatrix)
print("käännetty kanavamatriisi = ", invertedChannelMatrix)

receptionMatrix = np.matmul(channelMatrix, transmittedValues)
print("Kanavalta vastaanotetaan = ", receptionMatrix)

correctedByInvChannelMatrix = np.matmul(invertedChannelMatrix, receptionMatrix)
print("Kanavamatriisilla korjattu = ", correctedByInvChannelMatrix)

def solveSymbol(inputComplex):
    if(inputComplex.real > 0):
        msb = 1
    else:
        msb = 0
    if(inputComplex.imag > 0):
        lsb = 1
    else:
        lsb = 0
    return msb, lsb

receivedSymbols = []
for each in correctedByInvChannelMatrix:
    receivedSymbols.append(solveSymbol(each))
print("Vastanotetut symbolit: ", receivedSymbols)
