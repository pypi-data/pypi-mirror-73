# samABPhfunction

Package used to compute the h-function of steady-state active brownian
particles (ABPs), according to the derivations made by Tannie and I.

The true steady-state of ABPs can be taken to have the form P_{ss}= e^{-h}/Z,
where h is what we are talking about when we refer to the h function.

We simplify h a great deal, assuming a separable form as

<img src="https://latex.codecogs.com/svg.latex?h(\{\mathbf{r}_i\},\{\mathbf{u}_i\})&space;=&space;\frac{1}{2}\sum_{i}\sum_{j\neq&space;i}\left&space;(\mathcal{V}(r_{ij})&space;&plus;&space;\lambda&space;w(r_{ij})\mathbf{u}_{ij}\cdot\mathbf{r}_{ij}\right&space;)" title="h(\{\mathbf{r}_i\},\{\mathbf{u}_i\}) = \frac{1}{2}\sum_{i}\sum_{j\neq i}\left (\mathcal{V}(r_{ij}) + \lambda w(r_{ij})\mathbf{u}_{ij}\cdot\mathbf{r}_{ij}\right )" />

so we are really only concerned with calculating w(r_{ij}) from above.