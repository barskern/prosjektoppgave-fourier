
# Grunnleggende om Fourierrekker

## Introduksjon til fourierrekker

En fourierrekke er en sum av harmoniske funksjoner med ulik frekvens og amplitude som er tilnærmet lik en periodisk funksjon. Med uendelig antall ledd i rekken så er fourierrekken til en funksjon lik funksjonen, men med en endelig mengde ledd så er fourierrekken tilnærmet lik funksjonen.

Utregningen av fourierrekker kalles _harmonisk analyse_. Fourierrekken er svært nyttig, og kan brukes til å gjøre en tilfeldig periodisk funksjon om til en sum av enkle ledd. Man kan også velge antall ledd man ønsker basert på hvor nøyaktig man ønsker å gjennomføre tilnærmingen.

## Den generaliserte fourierrekken

Hvis vi bruker den _generaliserte[^1]_ fourierrekken som benytter de ortogonale harmoniske funksjonene _sinus_ og _cosinus_ får vi at vi kan utlede fourierrekken til en funksjon ved hjelp av to koeffisienter, et konstant ledd og to summer gitt under. Hvis det er av interesse, så er utledningen av disse generaliserte formlene gjennomført av Eric W. Weisstein i sin artikkel om [_Generalized Fourier Series_](http://mathworld.wolfram.com/GeneralizedFourierSeries.html).

Anta at $f(t)$ en tilfeldig periodisk funksjon med periode $T$ og at $c \in \mathbb{R}$. Da får vi at fourierrekken til funksjonen $f(t)$ er $\psi(t)$.

$$
\psi(t) = \frac{a_0}{2} + \sum\limits_{n=1}^\infty \left(a_n \cos(n \omega t) + b_n \sin(n \omega t) \right)
$$

$$
a_0 = \frac{2}{T} \int\limits_{c}^{c+T} f(t) \; dt
$$

$$
a_n = \frac{2}{T} \int\limits_{c}^{c+T} f(t) \cdot \cos(n\omega t) \; dt
$$

$$
b_n = \frac{2}{T} \int\limits_{c}^{c+T} f(t) \cdot \sin(n\omega t) \; dt
$$

Hvis $f(t)$ har diskontinuiteter, er fourierrekken til $f(t)$

$$
\psi(t) = \frac{f(t^+) + f(t^-)}{2}
$$

Dette vil også være sant $t \in \mathbb{R}$ når funksjonen er kontinuerlig, men da vi uttrykket kunne bli faktorisert til $\psi(t) = f(t)$. Vi sier at $f(t) \sim \psi(t)$.

## Den komplekse formen for fourierrekker

Fourierrekker består av to harmoniske funksjoner, _sinus_ og _cosinus_. Ved hjelp av _eulers formel_ kan vi gjøre disse om til et utrykk av $e$. _Eulers formel_ forteller oss at

$$
\cos(x) = \frac{e^{ix} + e^{-ix}}{2}\quad\quad\sin(x) = \frac{e^{ix} - e^{-ix}}{2i} \tag{1}
$$

Når vi setter $(1)$ inn i formelen for fourierrekken, kan vi utlede den komplekse formen av fourierrekken.

$$
\begin{array}.\psi(t)
&= \frac{a_0}{2} + \sum\limits_{n=1}^\infty \left(a_n \cos(n \omega t) + b_n \sin(n \omega t) \right) \\
&= \frac{a_0}{2} + \sum\limits_{n=1}^\infty \left(a_n \frac{e^{in\omega t} + e^{-in\omega t}}{2} + b_n \frac{e^{in\omega t} - e^{-in\omega t}}{2i} \right) \\
&= \frac{a_0}{2} + \sum\limits_{n=1}^\infty \frac{a_n - ib_n}{2} e^{in\omega t} + \sum\limits_{n=1}^\infty \frac{a_n + ib_n}{2} e^{-in\omega t}\end{array} \tag{2}
$$

Får å kunne skrive fourierrekken på en enkel måte så gjør vi noen definisjoner.

$$
c_0 = \frac{a_0}{2} \\
c_n = \frac{a_n - ib_n}{2} \\
c_{-n} = \frac{a_n + ib_n}{2}
$$

Deretter setter vi disse definisjonene inn i uttrykket $(2)$ som vi utledet over.

$$
\begin{array}. \psi(t) &= \frac{a_0}{2} + \sum\limits_{n=1}^\infty \frac{a_n - ib_n}{2} e^{in\omega t} + \sum\limits_{n=1}^\infty \frac{a_n + ib_n}{2} e^{-in\omega t} \\
&= c_0 + \sum\limits_{n=1}^\infty c_n e^{in\omega t} + \sum\limits_{n=1}^\infty c_{-n} e^{-in\omega t} \\
&= \sum\limits_{n=-\infty}^\infty c_n e^{in\omega t}\end{array} \tag{3}
$$

$$
c_n = \frac{1}{T} \int\limits_{c}^{c+T} f(t) e^{-jn\omega t} \; dt \tag{4}
$$

Resultatet $(3)$ fra denne utledningen kalles den komplekse formen av fourierrekken[^2]. Den komplekse formen for fourierrekker er algebraisk enklere og mer symmetrisk, derfor brukes denne formen av fourierrekker ofte i blant annet fysikk. For å komme rett fra funksjonen til den komplekse formen av fourierrekken kan vi bruke $(4)$.

På den komplekse formen av fourierrekken så er det et teorem som heter Parsevals Teorem som er greit å ha sett. Hvis vi antar at $f(t)$ er en periodisk funksjon med en periode på $T$ og at $c \in \mathbb{R}$.

$$
\frac{1}{T} \int\limits_{c}^{c+T} |f(t)|^2 \; dt = \sum\limits_{n=-\infty}^{\infty} |C_n|^2
$$

Hvis $f(t)$ er reell, altså at det ikke har en imaginær del, får vi videre at.

$$
\sum\limits_{n=-\infty}^{\infty} |C_n|^2 = |C_0|^2 + 2\sum\limits_{n=1}^{\infty} |C_n|^2
$$

## Et eksempel på en fourierrekke

Under har vi et eksempel på en fourierrekke som er framvist gjennom programmet _Maple_. Her ser vi at vi har en periodisk funksjon med periode $T$ som skal bli tilnærmet med en fourierrekke.

<embed height="2000px" width="100%" src="EksempelPaaFourierrekke.html">

[^1]: Weisstein, Eric W. "Generalized Fourier Series." From MathWorld--A Wolfram Web Resource. <http://mathworld.wolfram.com/GeneralizedFourierSeries.html> [Lesedato: 21.09.2017]

[^2]: "Complex form of fourier series", <https://www.math24.net/complex-form-fourier-series/> [Lesedato: 21.09.2017]
