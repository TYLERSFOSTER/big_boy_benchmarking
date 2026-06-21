# Mathematical notes on RL training


1. Entropy, Surprise, and KL Divergence
- 1.1 Surprise at the occurence of an event
- 1.2 Entropy as expected surprise
- 1.3 Context-relative surprise
- 1.4 The non-ambient part of surprise
2. Surprise as the Lie algebra "*mass decay rate of repeating events*"
- 2.1 Infinitesimal multiplicative action and the *multiplicative* derivative
- 2.2 Algebra or analysis? You decide
- 2.3 The multiplicative derivative in probability theory
3. Dee Jay

## 1. Entropy, Surprise, and KL Divergence

### 1.1 Surprise at the occurence of an event
Suppose we have a space $X$ equipped with a porability measure $P$. Consider an *event* in $X$ given by a measurable subset $S\subset X$. Define $p:=P(S) \in (0,1]$. 

We want an assignment that associates to $S$ and $P$ a number $I(S|P)$ that measures "how *surprising* it is when $S$ occurs, given the probability measure $P$." We ask for a family of functions

1. Surprise at the occurance of an event depends only on the probability of that event: $P(S)=Q(T)$ implies $I(S\mid P)=I(T\mid Q)$.
2. Certainty has zero surprise: $I(S|1)=0$ for all measurable $S\subset X$.
3. Less likely events are more surprising: $P(S)<Q(S)$ implies $I(S|P)>I(S|Q)$.
4. Surprise aggregates: If $S_1$ and $S_2$ are independent events, then $I(S_{1}\cap S_{2}|P)=I(S_{1}|P)+I(S_{2}|P)$.

Condition 1 implies that there is a single function

$$
I:(0,1]\longrightarrow \mathbb R_{\ge 0}
$$

such that $I\big(P(S)\big)=I(S\mid P)$. Let us require that this function $I:(0,1]\longrightarrow \mathbb R_{\ge 0}$ be continuous, i.e., "surprise varies continuously with respect to the value of the probability of an event. Condition 3 then says that $I:(0,1]\longrightarrow \mathbb R_{\ge 0}$ is a strictly decreasing function. Condition 2 becomes the condition that $I(1)=0$. 

The interval $(0,1]$ is a continuous multiplicative monoid. Conditions 2 and 4 together imply that $I$ has no upperbound, thus it is a bijection from $(0,1]$ onto $\mathbb{R}_{\ge0}$. Thus there exists some element $\varepsilon\in(0,1)$ such that $I(\varepsilon)=1$. Note that $1=\text{log}_{\ \!b}\ b$ for all $b\neq 1$.

Condition 4 implies that $I(\varepsilon^r)=r\ I(\varepsilon)=r$ for all $r\in\mathbb{Q}$. Thus, there exists some scalar $\lambda\in\mathbb{R}^{\times}$ such that

$$
I(p)\ \ =\ \ \lambda\cdot\text{log}_{\ \varepsilon}(p)\quad\text{for all}\quad p\in\varepsilon^{\mathbb{Q}}
$$

By continuity, this imples $I(p)\ \ =\ \ \lambda\cdot\text{log}_{\ \varepsilon}\ \ p$ for all $p\in(0,1]$. Condition 3 implies that $I$ reverses direction, and therefore $\lambda<0$. Because $\log_{\varepsilon}p=\log_{\delta}p\cdot\log_{\epsilon}\delta$, we can conclude that our measure of suprise *must be*, up to scalar multiple, just

$$
I(S|P)\ \ =\ \ -\text{log}\ \ P(S),
$$

or equivalently,

$$
I(S|P)\ \ =\ \ \text{log}\ \ \frac{1}{P(S)}.
$$

### 1.2 Entropy as expected surprise

If we fix the probability $P$, but let the event $S$ vary through singleton subsets $S=\{x\}\subset X$, we get a new function defined on our probability space,

$$
I(-|P):X\longrightarrow \mathbb{R}_{\ge 0},
$$

that returns "the suprise at sampling $x$, given that we're sampling from the distribution $P$."

Thus the moment integral

$$
\mathbb E_{x\sim P}\big[I(x|P)\big]
\ \ =\ \ 
\int_{X}I(x|P)\ \ d\mu_{P}
$$
computes the *expected surprise over all of $X$, sampling from $P$*. We call this quanitity the *entropy* of the distribution $P$ on $X$, denoted $H(P)$. For a discrete distribution, we can compute it as

$$
H(P)=-\sum_x P(x)\log P(x).
$$

#### Example
> [Near Dirac]

#### Example
> [Uniform]

### 1.3 Context-relative surprise

In our integral $\int_{X}I(x|P)\ \ d\mu_{P}$, it is a little strange to couple the measure $\mu_{P}$ we use to compute teh integral and the probability distribution $P$ we use to measure surprise. In general, the measure on our space $X$ might come from somewhere else, and might no even be a probability measure. But the integral defining entropy still makes sesen in these cases. It becomes

$$
\mathbb E_{\mu}\big[I(x|Q)\big]
\ \ =\ \ 
\int_{X}I(x|Q)\ \ d\mu,
$$

In the special case that the measure on $X$ comes from a probability distribution $P$, we can write this as

$$
\mathbb E_{x\sim P}\big[I(x|Q)\big]
\ \ =\ \ 
\int_{X}I(x|Q)\ \ dP.
$$

For discrete distributions, we can compute it as

$$
H(P,Q)=-\sum_x P(x)\log Q(x).
$$

#### Example
> [near-Dirac, but against a different Dirac]

### 1.4 The non-ambient part of surprise

I am far more surprised by a jump scare in a romantic comedy than a jump scare in a horror film. In fact, I'm rarely surprised by jump scares in horror films, because I'm paying close attention to all the surrounding cues: background noise changing, a pause in soundtrack, the scene action suddenly feeling *too* relexed, etc.

Consider the difference $I(S|Q)-I(S|P)$, for some event $S\subset X$ and probabilities $Q$ and $P$. The difference is asymmetric in $P$ and $Q$. We treat $P$ and $Q$ asymmetrically, thinking of $P$ as being the probability defining a probability measure $\mu_{P}$ on $X$. If we think of $\mu_{P}$ as being *mass density* in the space $X$, then the difference

$$
I(x|Q)-I(x|P)
$$

becomes something like "surprise at sampling $x$ from the distribution $Q$, *ignoring* the suprise at selecting $x$ relative to the mass density of $X$ itself." 

We can think of the difference $I(x|Q)-I(x|P)$ as being the "pure $Q$ part of surprise." If we integrate this pure $Q$ part of surprise across $X$, we get something like the "expected pure $Q$ part of surprise, modulo mass density in $X$":

$$
\mathbb E_{x\sim P}\big[\ \ I(x|Q)-I(x|P)\ \ \big]
\ \ :=\ \ 
\int_{X}\Big(\ I(x|Q)-I(x|P)\ \Big)\ \ d\mu_{P}
$$

We call this the *Kullback-Leibler* (*KL*) *divergence*, and denote it $D_{\mathrm{KL}}(P\|Q)$. In the special case that $X$ is discrete, it becomes

$$
D_{\mathrm{KL}}(P\|Q)
=
\sum_x P(x)\log\frac{P(x)}{Q(x)}.
$$

Equivalently, $D_{\mathrm{KL}}(P\|Q)=H(P,Q)-H(P)$.

**Example.** If we define $P$ to be a sharp peak at some point $m_P\in X$, so that most of the mass in the space $X$ is centered near $m_{P}$. Let $Q$ be a distribution centered away from $m_{P}$, but nonzero at $m_{P}$. Then even though we do not expect to sample a point near $m_{{}}$ from $Q$, our surprise at sampling such a point is signifcantly dampenned by our knowledge that most of the mass of $X$ is centered near $m_{P}$. *Most* points in $X$ lie near $m_{P}$, making it a priori difficult to sample otherwise.

## 2. Surprise as the Lie algebra "*mass decay rate of repeating events*"

### 2.1 Infinitesimal multiplicative action and the *multiplicative* derivative
The maxim for the present section is as follows.

> ***MAXIM:*** Picking a base for your logarithms too early can hide what's really going on. It often makes exponentiatation and the taking of logarithms look like formal tricks instead of deep aspects of the underlying arithmetic and geometry.

The real numbers $\mathbb{R}$ or complex numbers $\mathbb{C}$ form an additive Lie group. The derivative and/or differential in these groups, introduced in first-year calculus courses, is defined relative to this additive structure:

$$
D^{+}_{t}f(t)\ \ =\lim_{h\to 0}\ \ \frac{1}{h}\ \ \Big(f(t+h)-f(t)\Big)\ \ 
$$

But suppose I have reason to interpret the dependence of $f(t)$ on its argument $t$ as growing in a compounded manner, like radioactive decay or population growth or frquency, instead of a linear manner, like spacial position. in other words, what if we re-interpret $f(t)$ as being something more like a multiplicative transformation so that $f(1)$ is some operator that acts on some *thing* $\lvert x\rangle$, such that

$$
f(n)\ \ \lvert x\rangle
\quad=\quad
f(1)^n\ \ \lvert x\rangle.
$$

This is clearly some kind of approximation at best. If $f$ is a positive differentiable function near $t$, we can try to make it precise by defining the *multiplicative derivative* of $f$ at $t$:

$$
D^{\times}_{t}f(t)
\ \ :=\ \ 
\lim_{h\to 0}\ \ \Big(f(t+h)\big/f(t)\Big)^{1/h}
$$

The additive derivative of $f(t)$ is the "instantaneous change in $f$ at the point $t$" that I get if I imainge the value of $f$ as changing additively with respect to time, meaning that values close to $0$ get added to $f(t)$ in order to get $f(t+h)$. The multiplicative derivative of $f(t)$ is *again* the "instantaneous change in $f$ at the point $t$," but the one I get if I now imainge the value of $f$ as changing *multiplicatively* with respect to time, meaning that values close to $1$ multiply $f(t)$ in order to get $f(t+h)$. 

From the definition, we immediately have an exponential version of "linearity":

1. $D^{\times}_{t}\big(\ f(t)\cdot g(t)\ \big)=D^{\times}_{t}f(t)\cdot D^{\times}_{t}g(t)$
2. $D^{\times}_{t}\big(f(t)^{a}\big)=\big(D^{\times}_{t}f(t)\big)^{a}$ for all $a\in\mathbb{R}_{>0}$

Written in the language of ***mutlitplicative*** linear approximation, this says that

$$
f(t+h)
\quad=\quad
\varepsilon(h)\cdot D^{+}_{t}f(t)^{\ h}\cdot f(t)
$$

where $\varepsilon(h)^{1/h^2}$ stays bounded in $\mathbb{R}_{>0}$. Note that this gives us the formula

$$
D^{+}_{t}f(t)^{\ h}
\ \ =\ \ 
\frac{1}{\varepsilon(h)}\cdot\frac{f(t+h)}{f(t)}
$$

When $h=0$, the multiplicative operator $D^{\times}_{t}f(t)^{\ h}$ becomes multiplication by $1$. This means that if we expand $D^{\times}_{t}f(t)^{h}$ as a funciton of $h$, in the standard additive way, we get

$$
D^{\times}_{t}f(t)^{\ h}
\ \ =\ \ 
1+A\ h+O(h^2)
$$
for some coefficient $A\in\mathbb{R}$. To find this coefficient $A$, observe that the ordinary expansion of $f(t)$ at $t$ is $f(t+h)=f(t)+D^{+}_{t}f(t)\ \ h+O(h^2)$. Dividing by $f(t)$ gives
$$
\frac{f(t+h)}{f(t)}
\ \ =\ \ 
1+\frac{1}{f(t)}D^{+}_{t}f(t)\ \ h+O(h^2).
$$

The condition that $\varepsilon(h)^{1/h^2}$ stay bounded in $\mathbb{R}_{>0}$ implies that $\varepsilon(h)=1+O(h^2)$. Thus $1/\varepsilon(h)=1+O(h^2)$. Plugging all this into the defining identity relating $D^{\times}_{t}f(t)$, $\frac{f(t+h)}{f(t)}$, and $\varepsilon(h)$, we arrive an identity relating the mutlitplicative and additive derivatives, 

$$
\boxed{\quad
D^{\times}_{t}f(t)^{\ h}
\ \ =\ \ 
1+\frac{1}{f(t)}D^{+}_{t}f(t)\ \ h+O(h^2)
\quad}
$$

In words:

> If you have a nonegative valued, smooth (or at least second order differentiable) function $f(t)$, then at each point $t$ in the domain, there is a special base for multiplication, denoted $D^{\times}_{t}f(t)$, that can be computed as a limit, and has the property that the normal linear expanstion of $h$ successive multiplicaitons by this base $D^{\times}_{t}f(t)$ has linear coefficient $f'(t)/f(t)$.

This *is* the statement that $d\ \log_{b}\ f(t)=\frac{1}{f(t)}d\ f(t)$, but stated in a way that does not require any choice of base. In fact, it is stated in a way that produces the canonical base for you [...]

[...]

1. $D^{+}_{t}\log\big(\ f(t)\cdot g(t)\ \big)\ \ =\ \ D^{+}_{t}\log\ f(t)\ \ +\ \ D^{+}_{t}\log\ g(t)$
2. $D^{+}_{t}\log\big(\ f(t)^{a}\big)\ \ =\ \ a\cdot D^{+}_{t}\log\ f(t)$

### 2.2 Algebra or analysis? You decide

Note that $\frac{1}{f(t)}D^{+}_{t}f(t)$ is an algebraic object. It live is an alement in the vector space of Kahler differentials:

$$
\frac{1}{f(t)}D^{+}_{t}f(t)
\quad\in\quad
\Omega^{1}_{\mathbb{R}[f,f^{-1}]}
$$

"But what *is* $D^{\times}_{t}f(t)$?" you ask? It's $D^{\times}_{t}f(t)=e^{D^{+}_{t}\log\ f(t)}$. This identity is true for any choice of bas3 $b$. We have

$$
D^{\times}_{t}f(t)
\ \ =\ \ 
b^{D^{+}_{t}\log_{\ b}\ f(t)}
\quad\text{for any}\quad b\in\mathbb{R}_{>1}.
$$

Since the expansion of $e^{h\ D^{+}_{t}\log\ f(t)}$ is

$$
e^{h\ \ D^{+}_{t}\log\ f(t)}
\quad=\quad
1\ \ +\ \ h\ \ D^{+}_{t}\log\ f(t)\ \ +\ \ O(h^2),
$$

we get the familiar formula of the logarithmic derivative

$$
D^{+}_{t}\log\ f(t)
\ \ =\ \ 
\frac{1}{f(t)}D^{+}_{t}f(t)
$$

Since $\frac{1}{f(t)}D^{+}_{t}f(t)$ is algebraic, we wee that this object $D^{+}_{t}\log\ f(t)$, which is manifestly analytic, is in fact algebraic. A change of base is just a scalar change of $\frac{1}{f(t)}D^{+}_{t}f(t)$. Finding the scalar might be analytic in difficulty, but applying it once you find it is a purely algebraic operation.

We can also interpret this as an identity telling us how to write the additive deriviative in terms of the logarithm derivative:

$$
\boxed{\quad
D^{+}_{t}f(t)
\ \ =\ \ 
\Big(\ D^{+}_{t}\log\ f(t)\ \Big)\ \cdot\ f(t)
\quad}
$$

Describes how to write $D^{+}_{t}$ as a multiplicative operator on $f(t)$. If you're in a weird situation where you need to take the additive derivative $D^{+}_{t}f(t)$, but you also want your answer to have $f(t)$ as a factor, then [...]

### 2.3 The multiplicative derivative in probability theory

There is a statistical error that a lot of people make: they treat the occurence of many indpendent, relatively likely events as relatively likely. The picture they're missing, when they make this mistake, is that of *product* distributions on *product* spaces.

[...]

$\frac{1}{\ P_{\vartheta}(S)\ }D^{+}_{t}P_{\vartheta}(S)=$ the infinitesimal change of the exponential rate of repeated occurrence of $S$

[...]

$$
\mathbb{E}_{\ x\sim P}\ :\ \ L^{2}_{\mu_{P}}(X,\mathbb{R})\longrightarrow\mathbb{R}
$$

Fix $G(x)$ in $L^{2}_{\mu_{P}}(X,\mathbb{R})$. If our probability distribution $P$ varies with time, so that we can write it "$P_{t}$," then the expected value of $G(x)$ with respect to $P_{t}$ becomes a function of $t$:

$$
f(t)
\ \ =\ \ 
\mathbb{E}_{\ x\sim P_{t}}\big[G(x)\big]
$$

[...]

$$
\begin{array}{rcl}
D^{+}_{t}\ \mathbb{E}_{x\sim P_{t}}\big[G(x)\big] & = & D^{+}_{t}\int_{X}G(x)\ \ dP_{t}\\ 
& = & D^{+}_{t}\int_{X}G(x)\cdot P_{t}\cdot dx\\ 
& = & \int_{X}G(x)\cdot D^{+}_{t}(P_{t})\cdot dx\\ 
& = & \int_{X}G(x)\cdot \big(D^{+}_{t}\log\ P_{t}\big)\cdot P_{t}\cdot dx\\ 
& = & \int_{X}G(x)\cdot \big(D^{+}_{t}\log\ P_{t}\big)\cdot dP_{t}\\ 
& = & \mathbb{E}_{x\sim P_{t}}\big[G(x)\cdot D^{+}_{t}\log\ P_{t}\big]
\end{array}
$$

[...]

$$
D^{+}_{t}\mathbb{E}_{\ x\sim P_{t}}[\ \ -\ \ ]
\quad=\quad
\mathbb{E}_{\ x\sim P_{t}}\Big[\big(D^{+}_{t}\log\ P_{t}\big)\cdot(-)\Big]
$$

[...]

## 3. Dee Jay

We return to [...]


### 3.1 RL training frameworks: General shape

All the RL training frameworks have the same broad shape: *ptimize the expected value* $\mathbb{E}_{\mu}[\mathcal{L}]$, *for some measure* $mu$ *and some funciton* $\mathcal{L}$. the differences between the frameworks below are due, in large part, to the choices of $\mu$ and $\mathcal{L}$ relative to epsiode index, episode time step index, etc.


### 3.2 RL training framework: REINFORCE

The name *REINFORCE* is written in all caps because it's some acronym, but it's one of those derangedly cute acronyms that techies like. It's stupid and not helpful.

#### 3.2.1 

$$
\boxed{\ \ 
\text{Choose a policy}\ \ \pi\ \ \text{that maximizes expected return.}
\ \ }
$$
In symbols:
$$
\boxed{\ \ 
\theta_{\text{sol}}
\quad=\quad
\argmax_{\theta}\ \ \mathbb{E}_{\gamma\sim P_{\theta}{}}\big[R(\gamma)\big]
\ \ }
$$


[...]

#### 3.2.2 Probabilistic policy's associated measure on path space

$$
J(\theta)
\quad:=\quad
\mathbb{E}_{\ \gamma\sim \P_{\theta}}\big[\ \ R(\gamma)\ \ \big]
$$

[...]

$$
\nabla_{\theta}\ J
\quad=\quad
\nabla_{\theta}\int_{\text{Path}(X,x_0)}R(\gamma)\ \ P_{\vartheta}\ \ d\gamma
$$

[...]

### 3.2.3 Monte Carlo gradient update

### 3.3 RL training framework: TRPO

The acronym *TRPO*stands for *Trust Region Policy Optimization*.


### 3.4 RL training framework: PPO

The acronym *PPO* stands for *Proximal Policy Optimization*.