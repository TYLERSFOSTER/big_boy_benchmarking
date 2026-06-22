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
3. RL training frameworks
- 3.1 RL training frameworks: General shape
- 3.2 RL training framework: REINFORCE
- 3.3 RL training framework: TRPO
- 3.4 RL training framework: PPO

## 1. Entropy, Surprise, and KL Divergence

### 1.1 Surprise at the occurence of an event
Suppose we have a space $X$ equipped with a porability measure $P$. Consider an *event* in $X$ given by a measurable subset $S\subset X$. Define $p:=P(S) \in (0,1]$.

We want an assignment that associates to $S$ and $P$ a number $I(S\mid P)$ that measures "how *surprising* it is when $S$ occurs, given the probability measure $P$." We ask for a family of functions

1. Surprise at the occurance of an event depends only on the probability of that event: $P(S)=Q(T)$ implies $I(S\mid P)=I(T\mid Q)$.
2. Certainty has zero surprise: $I(S\mid 1)=0$ for all measurable $S\subset X$.
3. Less likely events are more surprising: $P(S) \lt Q(S)$ implies $I(S\mid P) \gt I(S\mid Q)$.
4. Surprise aggregates: If $S_1$ and $S_2$ are independent events, then $I(S_{1}\cap S_{2}\mid P)=I(S_{1}\mid P)+I(S_{2}\mid P)$.

Condition 1 implies that there is a single function

```math
I:(0,1]\longrightarrow \mathbb R_{\ge 0}
```

such that $I\big(P(S)\big)=I(S\mid P)$. Let us require that this function $I:(0,1]\longrightarrow \mathbb R_{\ge 0}$ be continuous, i.e., "surprise varies continuously with respect to the value of the probability of an event. Condition 3 then says that $I:(0,1]\longrightarrow \mathbb R_{\ge 0}$ is a strictly decreasing function. Condition 2 becomes the condition that $I(1)=0$.

The interval $(0,1]$ is a continuous multiplicative monoid. Conditions 2 and 4 together imply that $I$ has no upperbound, thus it is a bijection from $(0,1]$ onto $\mathbb{R}_{\ge0}$. Thus there exists some element $\varepsilon\in(0,1)$ such that $I(\varepsilon)=1$. Note that $1=\log_{\ \!b}\ b$ for all $b\neq 1$.

Condition 4 implies that $I(\varepsilon^r)=r\ I(\varepsilon)=r$ for all $r\in\mathbb{Q}$. Thus, there exists some scalar $\lambda\in\mathbb{R}^{\times}$ such that

```math
I(p)\ \ =\ \ \lambda\cdot\log_{\ \varepsilon}(p)\quad\text{for all}\quad p\in\varepsilon^{\mathbb{Q}}
```

By continuity, this imples $I(p)\ \ =\ \ \lambda\cdot\log_{\ \varepsilon}\ \ p$ for all $p\in(0,1]$. Condition 3 implies that $I$ reverses direction, and therefore $\lambda \lt 0$. Because $\log_{\varepsilon}p=\log_{\delta}p\cdot\log_{\epsilon}\delta$, we can conclude that our measure of suprise *must be*, up to scalar multiple, just

```math
I(S\mid P)\ \ =\ \ -\log\ \ P(S),
```

or equivalently,

```math
I(S\mid P)\ \ =\ \ \log\ \ \frac{1}{P(S)}.
```

### 1.2 Entropy as expected surprise

If we fix the probability $P$, but let the event $S$ vary through singleton subsets $S=\{x\}\subset X$, we get a new function defined on our probability space,

```math
I(-|P):X\longrightarrow \mathbb{R}_{\ge 0},
```

that returns "the suprise at sampling $x$, given that we're sampling from the distribution $P$."

Thus the moment integral

```math
\mathbb E_{x\sim P}\big[I(x\mid P)\big]
\ \ =\ \
\int_{X}I(x\mid P)\ \ d\mu_{P}
```

computes the *expected surprise over all of $X$, sampling from $P$*. We call this quanitity the *entropy* of the distribution $P$ on $X$, denoted $H(P)$. For a discrete distribution, we can compute it as

```math
H(P)=-\sum_x P(x)\log P(x).
```

#### Example
> [Near Dirac]

#### Example
> [Uniform]

### 1.3 Context-relative surprise

In our integral $\int_{X}I(x\mid P)\ \ d\mu_{P}$, it is a little strange to couple the measure $\mu_{P}$ we use to compute teh integral and the probability distribution $P$ we use to measure surprise. In general, the measure on our space $X$ might come from somewhere else, and might no even be a probability measure. But the integral defining entropy still makes sesen in these cases. It becomes

```math
\mathbb E_{\mu}\big[I(x\mid Q)\big]
\ \ =\ \
\int_{X}I(x\mid Q)\ \ d\mu,
```

In the special case that the measure on $X$ comes from a probability distribution $P$, we can write this as

```math
\mathbb E_{x\sim P}\big[I(x\mid Q)\big]
\ \ =\ \
\int_{X}I(x\mid Q)\ \ dP.
```

For discrete distributions, we can compute it as

```math
H(P,Q)=-\sum_x P(x)\log Q(x).
```

#### Example
> [near-Dirac, but against a different Dirac]

### 1.4 The non-ambient part of surprise

I am far more surprised by a jump scare in a romantic comedy than a jump scare in a horror film. In fact, I'm rarely surprised by jump scares in horror films, because I'm paying close attention to all the surrounding cues: background noise changing, a pause in soundtrack, the scene action suddenly feeling *too* relexed, etc.

Consider the difference $I(S\mid Q)-I(S\mid P)$, for some event $S\subset X$ and probabilities $Q$ and $P$. The difference is asymmetric in $P$ and $Q$. We treat $P$ and $Q$ asymmetrically, thinking of $P$ as being the probability defining a probability measure $\mu_{P}$ on $X$. If we think of $\mu_{P}$ as being *mass density* in the space $X$, then the difference

```math
I(x\mid Q)-I(x\mid P)
```

becomes something like "surprise at sampling $x$ from the distribution $Q$, *ignoring* the suprise at selecting $x$ relative to the mass density of $X$ itself."

We can think of the difference $I(x\mid Q)-I(x\mid P)$ as being the "pure $Q$ part of surprise." If we integrate this pure $Q$ part of surprise across $X$, we get something like the "expected pure $Q$ part of surprise, modulo mass density in $X$":

```math
\mathbb E_{x\sim P}\big[\ \ I(x\mid Q)-I(x\mid P)\ \ \big]
\ \ :=\ \
\int_{X}\Big(\ I(x\mid Q)-I(x\mid P)\ \Big)\ \ d\mu_{P}
```

We call this the *Kullback-Leibler* (*KL*) *divergence*, and denote it $D_{\mathrm{KL}}(P\|Q)$. In the special case that $X$ is discrete, it becomes

```math
D_{\text{KL}}(P\|Q)=\sum_x P(x)\log\frac{P(x)}{Q(x)}.
```

Equivalently, $D_{\mathrm{KL}}(P\|Q)=H(P,Q)-H(P)$.

**Example.** If we define $P$ to be a sharp peak at some point $m_P\in X$, so that most of the mass in the space $X$ is centered near $m_{P}$. Let $Q$ be a distribution centered away from $m_{P}$, but nonzero at $m_{P}$. Then even though we do not expect to sample a point near $m_{{}}$ from $Q$, our surprise at sampling such a point is signifcantly dampenned by our knowledge that most of the mass of $X$ is centered near $m_{P}$. *Most* points in $X$ lie near $m_{P}$, making it a priori difficult to sample otherwise.

## 2. Surprise as the Lie algebra "*mass decay rate of repeating events*"

### 2.1 Infinitesimal multiplicative action and the *multiplicative* derivative
The maxim for the present section: Picking a base for your logarithms too early can hide what's really going on. It often makes exponentiatation and the taking of logarithms look like formal tricks instead of deep aspects of the underlying arithmetic and geometry.

The real numbers $\mathbb{R}$ or complex numbers $\mathbb{C}$ form an additive Lie group. The derivative and/or differential in these groups, introduced in first-year calculus courses, is defined relative to this additive structure:

```math
D^{+}_{t}f(t)\ \ =\lim_{h\to 0}\ \ \frac{1}{h}\ \ \Big(f(t+h)-f(t)\Big)\ \
```

But suppose I have reason to interpret the dependence of $f(t)$ on its argument $t$ as growing in a compounded manner, like radioactive decay or population growth or frquency, instead of a linear manner, like spacial position. in other words, what if we re-interpret $f(t)$ as being something more like a multiplicative transformation so that $f(1)$ is some operator that acts on some *thing* $\lvert x\rangle$, such that

```math
f(n)\ \ \lvert x\rangle
\quad=\quad
f(1)^n\ \ \lvert x\rangle.
```

This is clearly some kind of approximation at best. If $f$ is a positive differentiable function near $t$, we can try to make it precise by defining the *multiplicative derivative* of $f$ at $t$:

```math
D^{\times}_{t}f(t)
\ \ :=\ \
\lim_{h\to 0}\ \ \Big(f(t+h)\big/f(t)\Big)^{1/h}
```

The additive derivative of $f(t)$ is the "instantaneous change in $f$ at the point $t$" that I get if I imainge the value of $f$ as changing additively with respect to time, meaning that values close to $0$ get added to $f(t)$ in order to get $f(t+h)$. The multiplicative derivative of $f(t)$ is *again* the "instantaneous change in $f$ at the point $t$," but the one I get if I now imainge the value of $f$ as changing *multiplicatively* with respect to time, meaning that values close to $1$ multiply $f(t)$ in order to get $f(t+h)$.

From the definition, we immediately have an exponential version of "linearity":

1. $D^{\times}_{t}\big(\ f(t)\cdot g(t)\ \big)=D^{\times}_{t}f(t)\cdot D^{\times}_{t}g(t)$
2. $D^{\times}_{t}\big(f(t)^{a}\big)=\big(D^{\times}_{t}f(t)\big)^{a}$ for all $a\in\mathbb{R}_{\gt 0}$

Written in the language of ***mutlitplicative*** linear approximation, this says that

```math
f(t+h)
\quad=\quad
\varepsilon(h)\cdot D^{+}_{t}f(t)^{\ h}\cdot f(t)
```

where $\varepsilon(h)^{1/h^2}$ stays bounded in $\mathbb{R}_{\gt 0}$. Note that this gives us the formula

```math
D^{+}_{t}f(t)^{\ h}
\ \ =\ \
\frac{1}{\varepsilon(h)}\cdot\frac{f(t+h)}{f(t)}
```

When $h=0$, the multiplicative operator $D^{\times}_{t}f(t)^{\ h}$ becomes multiplication by $1$. This means that if we expand $D^{\times}_{t}f(t)^{h}$ as a funciton of $h$, in the standard additive way, we get

```math
D^{\times}_{t}f(t)^{\ h}
\ \ =\ \
1+A\ h+O(h^2)
```
for some coefficient $A\in\mathbb{R}$. To find this coefficient $A$, observe that the ordinary expansion of $f(t)$ at $t$ is $f(t+h)=f(t)+D^{+}_{t}f(t)\ \ h+O(h^2)$. Dividing by $f(t)$ gives
```math
\frac{f(t+h)}{f(t)}
\ \ =\ \
1+\frac{1}{f(t)}D^{+}_{t}f(t)\ \ h+O(h^2).
```

The condition that $\varepsilon(h)^{1/h^2}$ stay bounded in $\mathbb{R}_{\gt 0}$ implies that $\varepsilon(h)=1+O(h^2)$. Thus $1/\varepsilon(h)=1+O(h^2)$. Plugging all this into the defining identity relating $D^{\times}_{t}f(t)$, $\frac{f(t+h)}{f(t)}$, and $\varepsilon(h)$, we arrive an identity relating the mutlitplicative and additive derivatives,

```math
\boxed{\quad
D^{\times}_{t}f(t)^{\ h}
\ \ =\ \
1+\frac{1}{f(t)}D^{+}_{t}f(t)\ \ h+O(h^2)
\quad}
```

In words: If you have a nonegative valued, smooth (or at least second order differentiable) function $f(t)$, then at each point $t$ in the domain, there is a special base for multiplication, denoted $D^{\times}_{t}f(t)$, that can be computed as a limit, and has the property that the normal linear expanstion of $h$ successive multiplicaitons by this base $D^{\times}_{t}f(t)$ has linear coefficient $f'(t)/f(t)$.

This *is* the statement that $d\ \log_{b}\ f(t)=\frac{1}{f(t)}d\ f(t)$, but stated in a way that does not require any choice of base. In fact, it is stated in a way that produces the canonical base for you [...]

[...]

1. $D^{+}_{t}\log\big(\ f(t)\cdot g(t)\ \big)\ \ =\ \ D^{+}_{t}\log\ f(t)\ \ +\ \ D^{+}_{t}\log\ g(t)$
2. $D^{+}_{t}\log\big(\ f(t)^{a}\big)\ \ =\ \ a\cdot D^{+}_{t}\log\ f(t)$

### 2.2 Algebra or analysis? You decide

Note that $\frac{1}{f(t)}D^{+}_{t}f(t)$ is an algebraic object. It live is an alement in the vector space of Kahler differentials:

```math
\frac{1}{f(t)}D^{+}_{t}f(t)
\quad\in\quad
\Omega^{1}_{\mathbb{R}[f,f^{-1}]}
```

"But what *is* $D^{\times}_{t}f(t)$?" you ask? It's $D^{\times}_{t}f(t)=e^{D^{+}_{t}\log\ f(t)}$. This identity is true for any choice of bas3 $b$. We have

```math
D^{\times}_{t}f(t)
\ \ =\ \
b^{D^{+}_{t}\log_{\ b}\ f(t)}
\quad\text{for any}\quad b\in\mathbb{R}_{\gt 1}.
```

Since the expansion of $e^{h\ D^{+}_{t}\log\ f(t)}$ is

```math
e^{h\ \ D^{+}_{t}\log\ f(t)}
\quad=\quad
1\ \ +\ \ h\ \ D^{+}_{t}\log\ f(t)\ \ +\ \ O(h^2),
```

we get the familiar formula of the logarithmic derivative

```math
D^{+}_{t}\log\ f(t)
\ \ =\ \
\frac{1}{f(t)}D^{+}_{t}f(t)
```

Since $\frac{1}{f(t)}D^{+}_{t}f(t)$ is algebraic, we wee that this object $D^{+}_{t}\log\ f(t)$, which is manifestly analytic, is in fact algebraic. A change of base is just a scalar change of $\frac{1}{f(t)}D^{+}_{t}f(t)$. Finding the scalar might be analytic in difficulty, but applying it once you find it is a purely algebraic operation.

We can also interpret this as an identity telling us how to write the additive deriviative in terms of the logarithm derivative:

```math
\boxed{\quad
D^{+}_{t}f(t)
\ \ =\ \
\Big(\ D^{+}_{t}\log\ f(t)\ \Big)\ \cdot\ f(t)
\quad}
```

Describes how to write $D^{+}_{t}$ as a multiplicative operator on $f(t)$. If you're in a weird situation where you need to take the additive derivative $D^{+}_{t}f(t)$, but you also want your answer to have $f(t)$ as a factor, then [...]

### 2.3 The multiplicative derivative in probability theory

There is a statistical error that a lot of people make: they treat the occurence of many indpendent, relatively likely events as relatively likely. The picture they're missing, when they make this mistake, is that of *product* distributions on *product* spaces.

[...]

$\frac{1}{\ P_{\vartheta}(S)\ }D^{+}_{t}P_{\vartheta}(S)=$ the infinitesimal change of the exponential rate of repeated occurrence of $S$

[...]

```math
\mathbb{E}_{\ x\sim P}\ :\ \ L^{2}_{\mu_{P}}(X,\mathbb{R})\longrightarrow\mathbb{R}
```

Fix $G(x)$ in $L^{2}_{\mu_{P}}(X,\mathbb{R})$. If our probability distribution $P$ varies with time, so that we can write it "$P_{t}$," then the expected value of $G(x)$ with respect to $P_{t}$ becomes a function of $t$:

```math
f(t)
\ \ =\ \
\mathbb{E}_{\ x\sim P_{t}}\big[G(x)\big]
```

[...]

```math
\begin{array}{rcl}
D^{+}_{t}\ \mathbb{E}_{x\sim P_{t}}\big[G(x)\big] & = & D^{+}_{t}\int_{X}G(x)\ \ dP_{t}\\
& = & D^{+}_{t}\int_{X}G(x)\cdot P_{t}\cdot dx\\
& = & \int_{X}G(x)\cdot D^{+}_{t}(P_{t})\cdot dx\\
& = & \int_{X}G(x)\cdot \big(D^{+}_{t}\log\ P_{t}\big)\cdot P_{t}\cdot dx\\
& = & \int_{X}G(x)\cdot \big(D^{+}_{t}\log\ P_{t}\big)\cdot dP_{t}\\
& = & \mathbb{E}_{x\sim P_{t}}\big[G(x)\cdot D^{+}_{t}\log\ P_{t}\big]
\end{array}
```

[...]

```math
D^{+}_{t}\mathbb{E}_{\ x\sim P_{t}}[\ \ -\ \ ]
\quad=\quad
\mathbb{E}_{\ x\sim P_{t}}\Big[\big(D^{+}_{t}\log\ P_{t}\big)\cdot(-)\Big]
```

[...]

## 3. RL training frameworks

This section collects three central policy-gradient algorithms. The common object is a policy $\pi_\theta(a\mid s)$ and a trajectory law $P_\theta(d\tau)$ induced by running that policy in the environment.

### 3.1 Shared value and advantage

For a fixed policy $\pi$, define the *value* of state $s$ to be

```math
V^\pi(s)
\quad:=\quad
\mathbb E_\pi
\big[\
G(\gamma_{\ge t})
\ \big|\
s_t=s
\ \big],
```

and

```math
Q^\pi(s,a)
\quad:=\quad
\mathbb E_\pi
\big[\
G(\gamma_{\ge t})
\ \big|\
s_t=s,\ a_{t}=a
\ \big],
```

The *advantage* is $A^\pi(s,a):=Q^\pi(s,a)-V^\pi(s)$. Equivalently,

```math
A^\pi(s,a)
\quad:=\quad
\mathbb E_\pi
\big[\
G(\gamma_{\ge t})
\ \big|\
s_t=s,\ a_{t}=a
\ \big]
\ -\
\mathbb E_\pi
\big[\
G(\gamma_{\ge t})
\ \big|\
s_t=s
\ \big]
```

So $A^\pi(s,a)$ is the expected gain from knowing that action $a$ was chosen, beyond merely knowing the state $s$. One important feature of *advantage* is that under the policy itself, advantage is *centered*:

```math
\mathbb E_{a\sim \pi(\cdot\mid s)}
\big[\
A^\pi(s,a)
\ \big]
\ \ =\ \
0
```

### 3.2 REINFORCE

*REINFORCE increases the probability of sampled actions in proportion to their observed return or advantage.*

REINFORCE is the direct Monte Carlo policy-gradient algorithm. It uses trajectories sampled from the current policy $\tau_i\sim P_\theta$. The pure expectation form is

```math
\nabla_\theta J(\theta)
\ \ =\ \
\mathbb E_{\tau\sim P_\theta}
\left[
\sum_t
G_t(\tau)
\nabla_\theta
\log \pi_\theta(a_t\mid s_t)
\right].
```

It has gradient

```math
\nabla_\theta L_{\mathrm{REINFORCE}}(\theta)
\ \ =\ \
-
\frac{1}{N}
\sum_{i=1}^N
\sum_t
\widehat G_t^{(i)}
\nabla_\theta
\log \pi_\theta(a_t^{(i)}\mid s_t^{(i)}).
```

Gradient descent on $L_{\mathrm{REINFORCE}}$ is therefore stochastic gradient ascent on $J$:

```math
\theta
\leftarrow
\theta
+
\alpha
\frac{1}{N}
\sum_{i=1}^N
\sum_t
\widehat G_t^{(i)}
\nabla_\theta
\log \pi_\theta(a_t^{(i)}\mid s_t^{(i)}).
```

A baseline may be subtracted without changing the expected gradient: $\widehat A_t=\widehat G_t-b(s_t)$. Then the practical loss is

```math
L_{\mathrm{REINFORCE}}(\theta)
\ \ =\ \
-
\frac{1}{N}
\sum_{i=1}^N
\sum_t
\widehat A_t^{(i)}
\log \pi_\theta(a_t^{(i)}\mid s_t^{(i)}).
```

The update is

```math
\theta
\leftarrow
\theta
+
\alpha
\frac{1}{N}
\sum_{i=1}^N
\sum_t
\widehat A_t^{(i)}
\nabla_\theta
\log \pi_\theta(a_t^{(i)}\mid s_t^{(i)}).
```

### 3.3 TRPO: Trust Region Policy Optimization

*TRPO chooses the best advantage-improving policy move inside a KL ball around the old policy.*

TRPO starts with an old policy $\pi_{\mathrm{old}}=\pi_{\theta_{\mathrm{old}}}$. It collects data from $\pi_{\mathrm{old}}$, estimates the old advantage $A_{\mathrm{old}}(s,a)=A^{\pi_{\mathrm{old}}}(s,a)$, and then asks for a new policy $\pi_\theta$ that chooses positive-advantage actions at states visited by the old policy.

Let $\rho_{\mathrm{old}}(s)$ be the old state-visitation distribution. The clean surrogate objective is

```math
\mathcal J_{\mathrm{TRPO}}(\theta)
\quad=\quad
\mathbb E_{s\sim\rho_{\mathrm{old}},\,a\sim\pi_\theta(\cdot\mid s)}
\big[\
A_{\mathrm{old}}(s,a)
\ \big].
```

Expanding $A_{\mathrm{old}}$, this is

```math
\mathcal J_{\mathrm{TRPO}}(\theta)
\ \ =\ \
\mathbb E_{s\sim\rho_{\mathrm{old}},\ a\sim\pi_\theta(\cdot\mid s)}
\mathbb E_{\pi_{\mathrm{old}}}
\Big[\
\big[\
G(\gamma_{\ge t})
\big|
s_t=s,\ a_t=a
\ \big]
-
\mathbb E_{\pi_{\mathrm{old}}}
\big[\
G(\gamma_{\ge t})
\big|
s_t=s
\ \big]
\ \Big]
```

This says: at states the old policy visits, let the new policy choose actions; score those actions by how much better they were than old-policy average.

Because data are sampled from the old action distribution, the same objective is estimated using the likelihood ratio

```math
r_\theta(s,a)
\ \ =\ \
\frac{\pi_\theta(a\mid s)}
{\pi_{\mathrm{old}}(a\mid s)}.
```

Thus $\mathcal J_{\mathrm{TRPO}}(\theta)=\mathbb E_{s\sim\rho_{\mathrm{old}},\,a\sim\pi_{\mathrm{old}}(\cdot\mid s)}\left[r_\theta(s,a)A_{\mathrm{old}}(s,a)\right]$. TRPO maximizes this surrogate subject to a KL trust-region constraint:

```math
\mathbb E_{s\sim\rho_{\mathrm{old}}}
\left[
D_{\mathrm{KL}}
\left(
\pi_{\mathrm{old}}(\cdot\mid s)
\;\|\;
\pi_\theta(\cdot\mid s)
\right)
\right]
\le
\delta.
```

The gradient of the surrogate at $\theta=\theta_{\mathrm{old}}$ is

```math
g
\ \ =\ \
\nabla_\theta
\mathbb E_{\mathrm{old}}
\left[
r_\theta(s,a)A_{\mathrm{old}}(s,a)
\right]
\bigg|_{\theta=\theta_{\mathrm{old}}}.
```

Since $r_{\theta_{\mathrm{old}}}(s,a)=1$, this becomes

```math
g
\ \ =\ \
\mathbb E_{\mathrm{old}}
\left[
A_{\mathrm{old}}(s,a)
\nabla_\theta
\log \pi_\theta(a\mid s)
\right]_{\theta=\theta_{\mathrm{old}}}.
```

Let $F$ be the local Fisher/KL curvature matrix, obtained from the second-order expansion

```math
\mathbb E_{s\sim\rho_{\mathrm{old}}}
\left[
D_{\mathrm{KL}}
\left(
\pi_{\mathrm{old}}(\cdot\mid s)
\;\|\;
\pi_{\theta_{\mathrm{old}}+\Delta\theta}(\cdot\mid s)
\right)
\right]
\approx
\frac{1}{2}
\Delta\theta^\top F\Delta\theta.
```

Then the idealized TRPO step solves $\max_{\Delta\theta}\ g^\top\Delta\theta$ subject to

```math
\frac{1}{2}\Delta\theta^\top F\Delta\theta
\le
\delta.
```

The solution direction is the natural-gradient direction $\Delta\theta\propto F^{-1}g$. With the trust-region scaling,

```math
\Delta\theta
\ \ =\ \
\sqrt{
\frac{2\delta}
{g^\top F^{-1}g}
}
F^{-1}g.
```

In practice, $F^{-1}g$ is computed approximately, often by conjugate gradient, and then a line search is used to ensure the KL constraint and surrogate improvement actually hold.

### 3.4 PPO: Proximal Policy Optimization

*PPO uses the same old-state advantage surrogate as TRPO, but controls policy movement with probability-ratio clipping or a similar proximal penalty rather than a hard KL-constrained solve.*

PPO starts from the same old-policy surrogate as TRPO: $\mathcal J_{\mathrm{surr}}(\theta)=\mathbb E_{\mathrm{old}}\left[r_\theta(s,a)A_{\mathrm{old}}(s,a)\right]$. The difference is how they prevent the policy from moving too far. TRPO imposes a hard KL trust-region. PPO replaces the constrained optimization with a simpler proximal surrogate.

The clipped PPO objective is

```math
\mathcal J_{\mathrm{PPO}}^{\mathrm{clip}}(\theta)
\ \ =\ \
\mathbb E_{\mathrm{old}}
\left[
\min
\left(
r_\theta(s,a)A_{\mathrm{old}}(s,a),
\operatorname{clip}
\left(
r_\theta(s,a),
1-\epsilon,
1+\epsilon
\right)
A_{\mathrm{old}}(s,a)
\right)
\right].
```

The implementation loss is usually the negative objective:

```math
L_{\mathrm{PPO}}^{\mathrm{actor}}(\theta)
\ \ =\ \
-
\frac{1}{N}
\sum_{i=1}^N
\min
\left(
r_i(\theta)\widehat A_i,
\operatorname{clip}
\left(
r_i(\theta),
1-\epsilon,
1+\epsilon
\right)
\widehat A_i
\right).
```

When the sample is not clipped, the gradient contribution is

```math
\nabla_\theta
\left(
r_\theta(s,a)A_{\mathrm{old}}(s,a)
\right)
\ \ =\ \
r_\theta(s,a)
A_{\mathrm{old}}(s,a)
\nabla_\theta\log\pi_\theta(a\mid s).
```

So the unclipped PPO update direction is

```math
\theta
\leftarrow
\theta
+
\alpha
\frac{1}{N}
\sum_i
r_i(\theta)
\widehat A_i
\nabla_\theta
\log\pi_\theta(a_i\mid s_i).
```

The clipping rule modifies this by setting the gradient to zero, or reducing it, when the probability ratio has already moved too far in the advantage-improving direction.

In practice PPO often uses a combined actor-critic loss:

```math
L_{\mathrm{PPO}}(\theta,\phi)
\ \ =\ \
L_{\mathrm{PPO}}^{\mathrm{actor}}(\theta)
+
c_v
\frac{1}{N}
\sum_i
\left(
V_\phi(s_i)-\widehat G_i
\right)^2
-
c_H
\frac{1}{N}
\sum_i
H
\left(
\pi_\theta(\cdot\mid s_i)
\right).
```

The value term trains the critic. The entropy term encourages exploration.
