import numpy as np
import matplotlib.pyplot as plt

def QPSK_modulate(Fs,fc,I_data,Q_data):
    Ts = 1/Fs
    samples = I_data.size
    t = np.arange(0,Ts*samples,Ts)          # start, stop, step
    cos_kantoaalto = np.cos(2*np.pi*fc*t)
    sin_kantoaalto = np.sin(2*np.pi*fc*t)
    moduloitu_I = (I_data*cos_kantoaalto)
    moduloitu_Q = (Q_data*sin_kantoaalto)
    moduloitu = moduloitu_I + moduloitu_Q
    return moduloitu

def QPSK_demodulate(Fs,fc,moduloitu,suodatin):
    Ts = 1/Fs
    samples = moduloitu.size
    t = np.arange(0,Ts*samples,Ts)          # start, stop, step
    cos_kantoaalto = np.cos(2*np.pi*fc*t)
    sin_kantoaalto = np.sin(2*np.pi*fc*t)
    demoduloitu_I = (moduloitu*cos_kantoaalto)
    demoduloitu_Q = (moduloitu*sin_kantoaalto)
  
    #Simuloidaan radiokanavan vaikutusta lisätään kohinaa
    demoduloitu_I = addNoise(demoduloitu_I,1)
    demoduloitu_Q = addNoise(demoduloitu_Q,1)
    #Ja käännetään signaalin vaihetta sillä vastaanottimen vaihetta ei tiedetä
    j = complex(0,1)
    vaihevirhe = complex(1,1)
    kompleksinen = demoduloitu_I + demoduloitu_Q*j
    kompleksinen = kompleksinen * vaihevirhe
    
    # Tehtävä opiskelijalle. Keksi kompleksilukuarvo, jolla
    # kanavan vaihevirhe korjaantuu.

    korjattuVaihe = complex(1,-1)
    kompleksinen = kompleksinen * korjattuVaihe

    demoduloitu_I = np.real(kompleksinen)
    demoduloitu_Q = np.imag(kompleksinen)

    suodatettu_I = np.convolve(demoduloitu_I,np.ones(suodatin,))
    suodatettu_Q = np.convolve(demoduloitu_Q,np.ones(suodatin,))
    return demoduloitu_I,demoduloitu_Q,suodatettu_I,suodatettu_Q


def makeRandomData(bits):
    # 
    N = 100                    # NÄin monta näytettä / bitti
    Idata = np.zeros(bits*N,)
    Qdata = np.zeros(bits*N,)
    for I in range(bits):
        Idata[I*N:(I+1)*N] = (2*np.round(np.random.rand(1,))-1)*np.ones(N,)
        Qdata[I*N:(I+1)*N] = (2*np.round(np.random.rand(1,))-1)*np.ones(N,)

    return Idata,Qdata    


def addNoise(signal,SNR):
    signalPower = np.average(np.power(signal,2))
    pituus = signal.size
    noise = signal/SNR
    return signal+noise*np.random.rand(pituus,)


if __name__ == '__main__':
    Idata,Qdata = makeRandomData(10)
    #print(Idata)
    Fs = 1000
    fc = 100
    Sp = 10
    moduloitu = QPSK_modulate(Fs,fc,Idata,Qdata)
    #moduloitu = addNoise(moduloitu,1)
    I,Q,SI,SQ = QPSK_demodulate(Fs,fc,moduloitu,Sp)
    plt.subplot(4,2,1)
    plt.plot(Idata),plt.title('Kosinihaaran data signaali')
    plt.subplot(4,2,2)
    plt.plot(Qdata),plt.title('Sinihaaran data signaali')
    plt.subplot(4,2,3)
    plt.plot(I),plt.title('Kosinihaaran demoduloitu signaali')
    plt.subplot(4,2,4),plt.plot(Q),plt.title('Sinihaaran demoduloitu signaali')
    plt.subplot(4,2,5),plt.plot(SI),plt.title('Kosinihaaran suodatettu demoduloitu signaali')
    plt.subplot(4,2,6),plt.plot(SQ),plt.title('Sinihaaran suodatettu demoduloitu signaali')

    SB = SI[55:-1:100]
    CB = SQ[55:-1:100]


    plt.subplot(4,2,7),plt.plot(CB,SB,'*'),plt.title('Vastaanotetut symbolit')
    plt.show()

    print('reaalihaaraan lähetettiin')
    print(Idata[1:1000:100])
    print('ja reaalihaarasta vastaanotettiin')
    print(SI[55:1005:100])
    # Tehtävä opiskelijalle
    # Tee tähän koodi, joka osaa tehdä bittipäätökset reaalihaaran (SI) tuloksista.
    for i in SI[55:1005:100]:
        #print((i > 0 ? 1 : -1))
        print(("1" if i > 0 else "0"))