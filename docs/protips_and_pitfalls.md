# Pro tips and Pitfalls



- **Science:**<br>Goal of *control* is *epistemic clarity*
- **Engineering:**<br>Goal of *control* is *operational reliability*

## Preflight checklist

### What is your environment?

#### What are your rewards?
- Are they order-$1$ Markovian?
- Are they order-$n\ge 2$ Markovian?
- Are they not Markovian at all?

#### How are states/actions recorded and encoded from environment?

#### What is your inference model is modelling?
- Is it modelling $v$?
- Is it modelling $\pi$?
- Is it modelling $Q$?

### What model are you using?
#### How are individual states endocded?
#### How are individual actions encoded?

### What exploration policy?...

## Tier-0 *fibers* get no logarithmic speed-up

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 start state"
      src="../assets/images/image_001.svg"
      width="350"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>THe tower does no put any kind of extra, "vertical" search structure on fibers lying in the uppermost tier.</em></sub>
    </td>
  </tr>
</table>

[This has a tropical counterpart...]

### Example

### Example

## A tower *cannot* boost the *RATE* of exploration

### Example

### Example

## A tower can alter *WHERE* an agent explores

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 start state"
      src="../assets/images/image_003.svg"
      width="450"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>[...]</em></sub>
    </td>
  </tr>
</table>

### Example

### Example

## Tower train can adjust global direct policy faster than direct itself can

<p align="center">
  <picture>
    <img
      alt="Warehouse Gridlock 001 start state"
      src="../assets/images/image_002.svg"
      width="1000"
    >
  </picture>
</p>

<table align="center">
  <tr>
    <td width="520" align="center">
      <sub><em>[...]</em></sub>
    </td>
  </tr>
</table>

The length of a path is *roughly* equal the exploration cost we pay for discovering that a given path it is better than all previously discovered paths, since we have to traverse the path in order to discover that it is omptimal. The tower architecture lets us find *potential* optimal paths at lower search cost.
$$
\int_{H}d\rho_{\mathcal{S}}\;d\pi(\alpha|s)
$$
You should think of this as being like
$$
\int_{TX}d\rho_{X}\;d\rho_{T_{x}X}
$$
for a gas flowing through a space $X$. At a given time $t$, we encode the "arrangement" of the gas particles throughout $X$ as a probability distribution $\rho_{X}$ on $X$. At a given position $x\in X$, the gas' behavior is statistical, and so the instantaneous change in $\rho_{X}$ at time $t$ is governed by a probability distribution $\rho_{T_{x}X}$ on the tangent space $T_{x}X$.
$$
\int_{X}d\rho_{X}
\!\!
\underset{\text{at the point}\;x}{\underset{\text{total change in}\;\rho_{X}}{\underbrace{\ \ \int_{T_{x}X}d\rho_{T_{x}X}\ }}}
$$
### Example

### Example

## Tower train can adjust global direct policy faster than direct itself can

### Example

### Example