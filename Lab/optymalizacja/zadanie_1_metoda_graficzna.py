import numpy as np
import matplotlib.pyplot as plt
import re


class ograniczenie:

    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.a = 0
        self.b = 0
        self.sign = ""

    def parser_ograniczen(self, function_string):
        if (v := "<=") in function_string:
            self.sign = "lower"
            eq_sign = v
        elif (v := ">=") in function_string:
            self.sign = "greater"
            eq_sign = v
        elif (v := "=") in function_string:
            self.sign = "equals"
            eq_sign = v
            raise ValueError("nie zaimplementowano ograniczenia 'rowne' ")
        else:
            print("brak nierownosci")
            raise ValueError

        function_string = function_string.replace(" ", "")
        lhs, c0 = function_string.split(eq_sign)
        lhs = re.sub("[a-z]", "?", lhs)
        # coefficients from string
        str_c = lhs.split("?")
        c = [float(i) for i in str_c if i]
        c.append(float(c0))

        self.A = c[0]
        self.B = c[1]
        self.C = c[2]

        self.a = -c[0]/c[1]
        self.b = c[-1]/c[1]

    def znajdz_przeciecie(self, f2):
        a1, b1, c1 = self.get_wsp_kanoniczna()
        a2, b2, c2 = f2.get_wsp_kanoniczna()
        x = (b1*c2-b2*c1)/(a2*b1-a1*b2)
        y = (c1-a1*x)/b1
        return x, y

    def dystans_od_0(self):
        return np.abs(self.C)/np.sqrt(self.A**2+self.B**2)

    def f_kanoniczna(self):
        return f'{self.A}x+ {self.B}y {self.sign} {self.C}'

    def f_liniowa(self):
        return f'y = {self.a}x + {self.b}'

    def get_wsp_kanoniczna(self):
        return self.A, self.B, self.C

    def get_wsp_liniowe(self):
        return self.a, self.b

    def przeciecie_z_x0y0(self):
        x = self.C/self.A
        y = self.C/self.B
        return (x, 0), (0, y)

    def get_value(self, x0):
        y0 = (self.C - self.A*x0)/self.B
        return y0

    def czy_spelnia_ograniczenie(self, p):
        x0, y0 = p
        if self.sign == 'lower':
            return self.get_value(x0) >= y0
        elif self.sign == 'greater':
            return self.get_value(x0) <= y0
        else:
            raise Exception("nie ma innych")

    @classmethod
    def from_string(cls, text):
        me = cls()
        me.parser_ograniczen(text)
        return me

    @classmethod
    def from_coeffs(cls, A, B, C, sign):
        me = cls()
        me.A = A
        me.B = B
        me.C = C
        me.sign = sign
        return me

    def __repr__(self) -> str:
        return self.f_kanoniczna()


def parser_funkcji_celu(function_string):
    s = re.sub("[a-z]", "?", function_string)
    str_c = s.split("?")
    c = [float(i) for i in str_c if i]
    return c


def f_prostopadla_do_wektora_w_punkcie(wekt, p):
    x0, y0 = p
    a_wekt = wekt[1]/wekt[0]
    a = -1/a_wekt
    b = y0 - a*x0
    return a, b


def dystans_prostej_od_0(A, B, C):
    return np.abs(C)/np.sqrt(A**2+B**2)

def wartosc_f_celu(p, c):
    x, y = p
    return x*c[0]+y*c[1]


f = "10a+10b"
s1 = "-1a+6b<=60"
s2 = "5a+2b<=24"
s3 = "4a+ 1b>=8"
s4 = "1a+ 1b<=4"

ciagi_ograniczen = [s1, s2, s3, s4]

c_celu = parser_funkcji_celu(f)

# gradient to wspolczynniki postaci kanonicznej
grad_f = c_celu

ograniczenia = []
for i in ciagi_ograniczen:
    ograniczenia.append(ograniczenie.from_string(i))

proste_prostopadle_do_grad = []
for s in ograniczenia:
    a, _ = s.get_wsp_liniowe()
    tg_grad = grad_f[1]/grad_f[0]
    if a == -1/tg_grad:
        proste_prostopadle_do_grad.append(s)

# znajdzmy wszystkie punkty przeciecia funkcji ograniczen z osiami i ze soba
punkty = []
for indx, si in enumerate(ograniczenia):
    px0, py0 = si.przeciecie_z_x0y0()
    if min(px0) >= 0:
        punkty.append(px0)
    if min(py0) >= 0:
        punkty.append(py0)

    for indx, sj in enumerate(ograniczenia):
        if si.a != sj.a:
            x, y = si.znajdz_przeciecie(sj)
            if x >= 0 and y >= 0:
                punkty.append((x, y))

# odrzucmy punkty nie spełniające ograniczeń
p_do_sprawdzenia = punkty
punkty = []
for p in p_do_sprawdzenia:
    flag = True
    for s in ograniczenia:
        if not s.czy_spelnia_ograniczenie(p):
            flag = False
            continue
    if flag:
        punkty.append(p)

# znajdzmy punkt o najwiekszym dystansie od zera wzdluz gradientu
max_d = -10
rozwiazania = []
max_x, max_y = 0, 0
for p in punkty:
    x, y = p
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

    a, b = f_prostopadla_do_wektora_w_punkcie(grad_f, p)
    # przejście z postaci liniowej na kanoniczną A=-a B=1 C=-b ...
    d = dystans_prostej_od_0(-a, 1, -b)
    if d > max_d:
        rozwiazania = [p]
        max_d = d
    elif d == max_d:
        rozwiazania.append(p)

proste_rozwiazania = []
for s in proste_prostopadle_do_grad:
    if max_d == s.dystans_od_0():
        proste_rozwiazania.append(s)

# rysuje OX
x = np.linspace(0-max_x*0.1, max_x+100, 2)
y = 0*x
plt.plot(x, y, c="black")

# rysuje OY
y = np.linspace(0-max_y*0.1, max_y+100, 2)
x = 0*y
plt.plot(x, y, c="black")

for s in ograniczenia:
    a, b = s.get_wsp_liniowe()
    x = np.linspace(0-max_x*0.1, max_x+100, 2)
    y = a*x+b
    plt.plot(x, y)

for p in punkty:
    plt.scatter(*p)
    x, y = p
    plt.text(x, y, f"({x}, {y}), z = {wartosc_f_celu(p, c_celu)}", size=9)

# wyznaczmy górną i dolną granicę obszaru rozwiazan
x = np.linspace(0, max_x+max_x*0.1, 100)
lower_bound = np.zeros_like(x)
upper_bound = np.full_like(x, max_y)

for indx, x0 in enumerate(x):
    for _, s in enumerate(ograniczenia):
        if s.sign == "greater":
            val = s.get_value(x0)
            if val >= lower_bound[indx]:
                lower_bound[indx] = val

        if s.sign == "lower":
            val = s.get_value(x0)
            if val <= upper_bound[indx]:
                if val < 0:
                    upper_bound[indx] = 0
                else:
                    upper_bound[indx] = val

plt.fill_between(x, lower_bound, upper_bound, color="teal", alpha=0.3)

for p in rozwiazania:
    plt.scatter(*p, s=100, c="red", label="rozwiazanie")

for s in proste_rozwiazania:
    a, b = s.get_wsp_liniowe()
    x = np.linspace(0-max_x*0.1, max_x+100, 2)
    y = a*x+b
    plt.plot(x, y, c="red", label="funkcja rozwiazan")

center_x = max_x//2
center_y = max_y//2
grad_len = np.sqrt(grad_f[0]**2 + grad_f[1]**2)
grad_x = [center_x, center_x+grad_f[0]/grad_len*max_x*0.3]
grad_y = [center_y, center_y+grad_f[1]/grad_len*max_y*0.3]
plt.annotate("", xytext=(grad_x[0], grad_y[0]),
             xy=(grad_x[1], grad_y[1]),
             arrowprops=dict(arrowstyle="->"))
plt.text(center_x, center_y, "$\\nabla f$")

plt.ylim(0-0.1*max_y, max_y+0.1*max_y)
plt.xlim(0-0.1*max_x, max_x+0.1*max_x)

# lim = max([max_x, max_y])
# plt.ylim(0-0.1*lim, lim+0.1*lim)
# plt.xlim(0-0.1*lim, lim+0.1*lim)

plt.grid()
plt.legend()
plt.show()

print(rozwiazania)
print(proste_rozwiazania)
