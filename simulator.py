# Library imports
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

st.markdown(r"""
# Wright-Fisher Simulator
You can adjust the parameters of the simulation using the sliders below, and then click "Run Simulation" to see the results. If the simulation is taking too long to run, try reducing the population size or the number of replicates.
""")

# User input for the parameters of the simulation
# We contain them within a form, so that the simulation only runs when the user clicks the "Run Simulation" button
with st.form("wf_form"):
    N_e = st.slider("Population size", min_value=100, max_value=10000, value=1000, step=10)
    u = st.slider("Forward mutation rate", min_value=0.000, max_value=1.000, value=0.000, step=0.001)
    v = st.slider("Backward mutation rate", min_value=0.000, max_value=1.000, value=0.000, step=0.001)
    w_AA = st.slider("Fitness of AA genotype", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    w_Aa = st.slider("Fitness of Aa genotype", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    w_aa = st.slider("Fitness of aa genotype", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    generations = st.slider("Number of generations", min_value=10, max_value=10000, value=100, step=10)
    num_trajectories = st.slider("Number of replicates", min_value=1, max_value=100, value=10, step=1)
    N_A0 = st.slider("Initial number of allele A copies", min_value=0, max_value=N_e*2, value=N_e, step=1)
    submit_button = st.form_submit_button(label="Run Simulation")

# Function: build the W-F transition matrix based on input parameters
def wright_fisher_transition(N, u, v, w_AA, w_Aa, w_aa):
    
    # Vectorized computation of the transition probabilities
    i = np.arange(N+1)
    p_selection = ((i/N) ** 2 * w_AA + (i/N) * (1 - i/N) * w_Aa) / (w_AA * (i/N) ** 2 + w_Aa * 2 * (i/N) * (1 - i/N) + w_aa * (1 - i/N) ** 2)
    p = p_selection * (1 - u) + (1 - p_selection) * v # Final allele frequency after selection and mutation
    
    j = np.arange(N+1)              # shape (N+1,)
    
    # Broadcast: p is (N+1, 1), j is (1, N+1) → P is (N+1, N+1)
    P = binom.pmf(j[np.newaxis, :], N, p[:, np.newaxis])
    return P


# Function: simulate allele frequency trajectories using the transition matrix
def simulate_trajectories(P, N_A0, generations, num_trajectories):
    P_cumsum = np.cumsum(P, axis=1) # Turn the probability matrix into a cumulative distribution for sampling
    
    trajectories = np.zeros((num_trajectories, generations+1), dtype=int)
    trajectories[:, 0] = N_A0
    
    for g in range(1, generations+1):
        current = trajectories[:, g-1] # Current state (allele copy number) for each trajectory
        r = np.random.random(num_trajectories) # Sample uniform random numbers for each trajectory
        rows = P_cumsum[current] # Get the cumulative probabilities for the current states
        trajectories[:, g] = np.sum(rows < r[:, np.newaxis], axis=1) # Sample the next state based on where the random number falls in the cumulative distribution
    
    return trajectories

def calculate_simulated_stats(trajectories, N):

    n_fixations = np.sum(trajectories[:, -1] == N) # Number of trajectories that end with allele A fixed
    n_eliminations = np.sum(trajectories[:, -1] == 0) # Number of trajectories that end with allele A lost
    time_to_fixation = np.mean(np.where(trajectories == N)[1]) # Average time to fixation for trajectories that fix
    time_to_elimination = np.mean(np.where(trajectories == 0)[1]) # Average time to elimination for trajectories that are lost
    return n_fixations, n_eliminations, time_to_fixation, time_to_elimination

def calculate_theoretical_stats(P, N_A0, u, v):
    # Calculate the theoretical fixation probability and expected time to fixation
    # Only for the case where there is no mutation
    if u == 0 and v == 0:
        absorption_probabilities = calculate_absorption_probabilities(P)
        expected_times = calculate_expected_times_to_absorption(P)
        fixation_probability = absorption_probabilities[N_A0, 1] # Fixation probability from the initial state
        elimination_probability = absorption_probabilities[N_A0, 0] # Elimination probability from the initial state
        expected_time_to_absorption = expected_times[N_A0] # Expected time to absorption from the initial state
    else:
        fixation_probability = None
        elimination_probability = None
        expected_time_to_absorption = None
    return fixation_probability, elimination_probability, expected_time_to_absorption

def calculate_absorption_probabilities(P):
    # Calculate the absorption probabilities for fixation and elimination from the transition matrix
    Q = P[1:-1, 1:-1] # Probability of moving from transient states to transient states
    R = P[1:-1, [0, -1]] # Probability of moving from transient states to absorbing states
    I = np.identity(Q.shape[0]) # Identity matrix
    N = np.linalg.inv(I - Q) # Fundamental matrix
    absorption_probabilities = N @ R # Absorption probabilities for each transient state
    return absorption_probabilities

def calculate_expected_times_to_absorption(P):
    # Calculate the expected times to absorption for fixation and elimination from the transition matrix
    Q = P[1:-1, 1:-1] # Probability of moving from transient states to transient states
    I = np.identity(Q.shape[0]) # Identity matrix
    N = np.linalg.inv(I - Q) # Fundamental matrix
    expected_times = N.sum(axis=1) # Expected time to absorption for each transient state
    return expected_times


# When the user clicks "Run simulation"
if submit_button:
    
    # Number of alleles in the population (2N for diploids)
    N = 2 * N_e
    
    # Build the transition matrix
    P = wright_fisher_transition(N, u, v, w_AA, w_Aa, w_aa)
    
    # Simulate the trajectories
    trajectories = simulate_trajectories(P, N_A0, generations, num_trajectories)
    
    # Convert allele copy numbers to frequencies for plotting
    trajectories_freqs = trajectories / N

    # Plot the trajectories
    plt.figure(figsize=(10, 6))
    for t in range(num_trajectories):
        plt.plot(trajectories_freqs[t], alpha=0.5)
    plt.xlabel("Generation")
    plt.ylabel("Frequency of allele A")
    plt.title("Wright-Fisher Simulation with Mutation")
    plt.grid()
    st.pyplot(plt)

    # Calculate and display statistics
    n_fixations, n_eliminations, time_to_fixation, time_to_elimination = calculate_simulated_stats(trajectories, N)
    st.write(f"Number of fixations: {n_fixations}")
    st.write(f"Number of eliminations: {n_eliminations}")
    st.write(f"Average time to fixation (simulated): {time_to_fixation:.2f} generations")
    st.write(f"Average time to elimination (simulated): {time_to_elimination:.2f} generations")
    fixation_probability, elimination_probability, expected_time_to_absorption = calculate_theoretical_stats(P, N_A0, u, v)
    if fixation_probability is not None:
        st.write(f"Theoretical fixation probability: {fixation_probability:.4f}")
        st.write(f"Theoretical elimination probability: {elimination_probability:.4f}")
        st.write(f"Theoretical expected time to either fixation or elimination: {expected_time_to_absorption:.2f} generations")


