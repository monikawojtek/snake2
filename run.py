#Te rzeczy możesz zmieniać, aby uzyskiwać różne układy :)

Rzm = 800 #rozmiar okna: Rzm x Rzm (domyslnie 800x800)
s = 40 #rozmiar planszy: s x s, Rzm musi byc podzielne przez s (inaczej moze byc krzywo albo nie pokazywac czegos albo cos)
Seed = "Zwykły Seed" #seed do losowania - liczba albo string
Kratki = 800 #ile kratek bedzie poczatkowo "zywych" - musi byc mniej, niz s^2 (inaczej pokaze ValueError)
czas = 50 #ile milisekund czekac do zrobienia nowej generacji
#Uwaga - podany czas to czas po akualizacji i narysowniu kolejnej generacji - wiec nalezy uwzglednic, ze realny czas zawsze bedzie (czasami duzo) wiekszy
Pattern = "23/3" #Przed ukośnikiem umieszcza się ilości żywych sąsiadów, aby komórka nie umarła, a po ukośniku ilość żywych sąsiadów, aby martwa komórka ożyła
#Domyślny pattern oryginalnej "Gry w Życie" wg reguł Conwaya to "23/3"



#Nizej faktyczny kod


import tkinter as tk
import random as rnd


#Klasa okna:
class Application:
    def __init__(self, rozmiar):
        self.Arr = [ [False for x in range(s)] for y in range(s) ] #Tablica o wymiarach s x s, poczatkowo falsz (martwa)

        self.window = tk.Tk()
        self.window.resizable(width = False, height = False)
        self.window.geometry(rozmiar)
        self.window.title("Game of Life")

        self.canvas = tk.Canvas(self.window, width = Rzm, height = Rzm)
        self.canvas.pack()

        self.createArray()

        #Tutaj sa ladne sobie kwadraty ktore beda sobie malowane
        self.Rct = [ [self.canvas.create_rectangle(x*krSz, y*krSz, krSz*(x+1), krSz*(y+1), fill="white") for x in range(s)] for y in range(s) ]

        self.updated()

        self.window.mainloop()

    #Funckja do uzupelnienia tablicy
    def createArray(self):
        #Wybiera *Kratki* liczb od 0 do s*s i odpowiednie miejsca w tablicy daje tam prawde (zywa)
        for z in rnd.sample(range(s*s), Kratki):
            self.Arr[z%s][z//s] = True

        #vvv tutaj byly customowe figury
        #self.Arr[1][0] = True
        #self.Arr[2][1] = True
        #self.Arr[2][2] = True
        #self.Arr[1][2] = True
        #self.Arr[0][2] = True


    #Dla kratki o koord. x, y oblicza, ile jest zywych dookola niej
    def liczObok(self, x, y):
        #Mniejsze i wieksze pola - przejscia, jezeli wychodza poza granice: (ifFalse, ifTrue)[condition]
        xm = ( x-1, s-1 )[ (x-1) == -1 ]
        xw = ( x+1, 0   )[ (x+1) ==  s ]
        ym = ( y-1, s-1 )[ (y-1) == -1 ]
        yw = ( y+1, 0   )[ (y+1) ==  s ]
        #Zwrocenie liczby pol
        wynik  = int(self.Arr[xm][ym]) + int(self.Arr[x][ym]) + int(self.Arr[xw][ym])
        wynik += int(self.Arr[xm][y])  +          0           + int(self.Arr[xw][y])
        wynik += int(self.Arr[xm][yw]) + int(self.Arr[x][yw]) + int(self.Arr[xw][yw])

        return wynik


    #Funkcja update
    def updated(self):

        #Rysowanie
        for x in range(s):
            for y in range(s):
                if self.Arr[x][y]:
                    self.canvas.itemconfig(self.Rct[x][y], fill="black") #Jeżeli jest żywe, robi czarne
                else:
                    self.canvas.itemconfig(self.Rct[x][y], fill="white") #A jak nie, to bialy


        #Tymczasowa tablica zawierajaca odswiezone stany
        OdswArr = [ [False for x in range(s)] for y in range(s) ]

        #Uzupelnienie tymczasowej tablicy nowa warstwa
        for x in range(s):
            for y in range(s):
                sasiedzi = self.liczObok(x, y)

                if self.Arr[x][y]:              #Pozostawanie przy żywych - jezeli licba sasiadow jest w "stay"
                    if sasiedzi in stay:
                        OdswArr[x][y] = True
                else:                           #Jeżeli nie jesteś żywy, ale liczba sasiadow jest w "born" - ożyj
                    if sasiedzi in born:
                        OdswArr[x][y] = True

        #Podmiana tablicy
        self.Arr = OdswArr.copy()

        #Odpalenie ponownie po *podanej ilosci* ms
        self.window.after(czas, self.updated)



#Aktualne dzialanie programu - koniec definicji


krSz = Rzm/s #Wymiar jednej kratki - zeby bylo prosciej pisac

rnd.seed(Seed)

stTab, bnTab = Pattern.split("/") #Dzielenie patternu na 2 czesci
#Zmienienie tych czesci na liczby
stay = [int(x) for x in stTab] #To jest ile ma być obok, aby przeżyć
born = [int(x) for x in bnTab] #To jest ile ma być obok, aby ożyć

#String rozmiaru okna
rozmiar = str(Rzm) + "x" + str(Rzm)

#Tworzenie obiektu aplikacji
apl = Application(rozmiar)