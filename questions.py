import streamlit as st

st.markdown(r"""
# Questions
1. The following image comes from the Wright-Fisher simulator, showing simulated allele frequencies of 10 replicate populations with no selection. What explains the results you see? Explain in terms of relative values of $\mu$ and $\nu$.
""")

st.image("question_1_graph.png")

st.markdown(r"""
2. The following image also comes from the Wright-Fisher simulator, showing simulated allele frequencies of 10 replicate populations with selection but no mutation. What kind of selection is occurring here? Explain in terms of the relative fitness values of the genotypes.
""")

st.image("question_2_graph.png")

st.markdown(r"""
3. The following image also comes from the Wright-Fisher simulator, showing simulated allele frequencies of 10 replicate populations with selection but no mutation. What kind of selection is occurring here? Explain in terms of the relative fitness values of the genotypes.     
""")

st.image("question_3_graph.png")

st.markdown(r"""
4. Calculate the probability of selecting an 'A' allele for the new population ($p_{t+1})$ given that the frequency of allele A in the current population is 0.6, and the fitness values of the genotypes are $\omega_{AA} = 1.0$, $\omega_{Aa} = 0.75$, and $\omega_{aa} = 0.5$.
""")
