import streamlit as st

st.markdown(r"""
# Answers to Questions

1. In the graph, we see that the average frequency of allele A after 100 generations seems to have reached an equilibrium around 0.4. This indicates that $\mu$, the forward mutation rate, is higher than $\nu$, the back mutation rate. Recall from [Lecture 8](canvas.sfu.ca/courses/1729/files/1770875) that the equilibrium frequency for allele A with mutation is given by $\frac{\mu}{\mu + \nu}$. So, we can infer that in this case $\frac{\mu}{\mu + \nu} \approx 0.4$.

2. In the graph, we see that the average frequency of allele A remains around 0.5 over time, and does not become eliminated or fixed. This is a case of overdominant selection or heterozygote advantage, where the heterozygote genotype has higher fitness than either of the homozygote genotypes. It is also called balancing, stabilizing, or diversifying selection, as it keeps the frequency of both alleles close to 0.5, maximimizing the frequency of heterozygotes. 
 
3. In the graph, we see that allele A is quickly fixed or eliminated in all populations, and that fixation and elimination occur with approximately equal probability. This is a case of underdominant selection or heterozygote inferiority, in which only the fitness of heterozygotes is reduced compared to the homozygotes.    

4. To calculate the probability of selecting an 'A' allele for the new population ($p_{t+1}$), we can use the formula from Lecture 9:            
""")

st.image("fitness_equation_from_slides.png")

st.markdown(r"""
First, we need to use the fact that $q_t = 1 - p_t = 1 - 0.6 = 0.4$. Then, substituting the given values into the formula, we get:
""")

st.latex(r"""
\frac{(0.6)^2 \cdot 1.0 + (0.6)(0.4) \cdot 0.75}{1.0 \cdot (0.6)^2 + 0.75 \cdot 2 \cdot (0.6)(0.4) + 0.5 \cdot (0.4)^2} = \frac{0.36 + 0.18}{0.36 + 0.36 + 0.08} = \frac{0.54}{0.8} = 0.675
""")


