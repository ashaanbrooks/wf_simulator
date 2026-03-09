import streamlit as st

st.markdown(r"""
# The Wright-Fisher Model

We learned in class that the Wright-Fisher model can be used to model genetic drift, and simulate the fixation or elimination of alleles over time. But, how does the Wright-Fisher model actually work, and how can we integrate other concepts, like mutation and selection, into this model?

## Assumptions of the Wright-Fisher Model

Before we begin to dive into the mathematics, it is important to first understand the assumptions of the Wright-Fisher model. As we shall soon see, these assumptions are fundamental to the way that the mathematics of the model works, and also give you a better sense of when it might or might not be appropriate to apply this model. 

The assumptions are:
* Constant population size. The population can't grow or shrink, only allele frequencies change.
* Random mating.
* Individuals can mate more than once (theoretically, the entire population in the next generation could be the offspring of a single individual in the current generation).
* Equal ratio of males to females, and equal generation time for males and females. In fact, the model makes no distinction between "male" and "female" alleles or individuals at all.
* Non-overlapping generations. This means that as one generation is born, it completely replaces the previous generation.

## Choosing the next generation: The Wright-Fisher Transition Probabilities

To determine the alleles in the next generation, we select alleles from the previous population. With the Wright-Fisher model, rather than selecting diploid individuals for the next generation, we actually build the next generation on an allele-by-allele basis. This is a simplification that lets us simplify the mathematics and make the simulation easier. The way that we select each allele is a "child selects parent" approach. Since the population size is fixed, we know exactly how many total alleles we will have in the new population. Then, for each new "child" allele, we sample a "parent" allele from the old population. Since we allow individuals to mate more than once, we sample from the old population with replacement. What does this look like mathematically?

Consider a two-allele model with alleles A and a, and population size $N$, so the number of alleles in the population is $2N$. Let $i$ be the number of copies of allele A in the old population. Then, for each allele in the new population, $P(A) = \frac{i}{2N}$. Since there are only two alleles, $P(a) = 1 - P(A) = 1 - \frac{i}{2N}$. 

Now, how can we use this to create the entire new population at once? The number of copies of allele A in the new population follows a binomial distribution with probability of success $P(A)$: 
$$P(X = j) = \binom{2N}{j}(P(A))^j(1 - P(A))^{2N-j} = P(X = j) = \binom{2N}{j}(\frac{i}{2N})^j(1 - \frac{i}{2N})^{2N-j}$$
In words, the probability that there are $j$ copies of the A allele in the new population, given that there are $i$ copies of the A allele in the old population, follows this binomial distribution. To choose the next generation, then, all we have to do is take a random sample from the binomial distribution that corresponds to the number of alleles in our current generation. Generally, you might see this in a matrix form, where each row corresponds to the number of alleles in the old generation, each column represents the number of alleles in the new generation, and each entry, $\mathbf{P}_{ij}$ is the probability of having $j$ alleles in the new generation if there were $i$ alleles in the old generation. 

## The Wright-Fisher Model with Selection

How do we integrate additional forces, like mutation and selection, into the model? All we have to do is adjust P(A) in the formula from before, and then we can still use the binomial distribution to sample the number of alleles in the new population.
""")

st.image("fitness_equation_from_slides.png")

st.markdown(r"""

This image comes from the [Lecture 9 slides](https://canvas.sfu.ca/courses/1729/files/1770877?wrap=1), and essentially gives us the answer. Essentially, the probability of selecting an 'A' allele for the new population is $p_{t+1}$ here, and $P(A)$ can be substituted for $p_t$. What this formula tells us is that the probability of selecting an A allele can be found by multiplying the frequencies of genotypes containing the 'A' allele by their fitness values, multiplying them together, and dividing by the average fitness of the entire population. All we have to do is substitute this new P(A) into our binomial distribution from before, and selection is accounted for. We can see that if all fitnesses are equal, so that $\omega_{11} = \omega_{12} = \omega_{22} = 1$, the equation reduces to $$p_{t+1} = \frac{p_t^2 + p_t(1-p_t)}{p_t^2 + 2p_t(1-p_t) + (1-p_t)^2} = \frac{p_t}{1}$$
Which is just no selection. 

## The Wright-Fisher Model with Mutation

As in the lectures, let $\mu$ be the forward mutation rate (mutation from A to a), and $\nu$ be the back mutation rate (mutation from a to A). Then, when we go to pick a "parent" allele for each "child" allele in the new population, it can be an A allele in two ways. The first way is to have an 'A' parent and no mutation, which happens with probability $(p_{t+1})(1 - \mu)$, using the value after selection from the formula in the previous section. The second way is to have an 'a' parent and then undergo a back mutation, which happens with probability $(1 - p_{t+1})(\nu)$. Adding these together, we get that
$$P(A) = (p_{t+1})(1 - \mu) + (1 - p_{t+1})(\nu)$$
All we have to do is substitute this $P(A)$ into our binomial distribution from before, and mutation is accounted for.

## Calculating Probabilities of Fixation/Elimination

We saw in class a formula for the probability of fixation or elimination of allele A where there is only one copy of the allele, ie, it arose from a new mutation. However, there is a general way to calculate the probability that an allele will be fixed or eliminated starting from any copy number. 

## Calculating Time to Fixation/Elimination

Similarly, we saw in class a formula for the time to fixation or elimination of allele A where there is only one copy of the allele. There is also a formula to calculate the expected time to fixation or elimination starting from any copy number. 

""")

