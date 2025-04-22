# Implementation of Shor's Algorithm using Qiskit
# For educational purposes

from qiskit import QuantumCircuit, Aer, execute, transpile
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT
from math import gcd
import numpy as np
from fractions import Fraction

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must be 2, 4, 7, 8, 11 or 13")
    
    U = QuantumCircuit(4)
    
    for iteration in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    
    return U

def qft_dagger(n):
    """Inverse Quantum Fourier Transform"""
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    
    return qc

def create_shors_circuit(a, n=15, counting_qubits=8):
    """Create quantum circuit for Shor's algorithm"""
    total_qubits = counting_qubits + 4  # 4 qubits for working register (for n=15)
    qc = QuantumCircuit(total_qubits, counting_qubits)
    
    # Initialize counting qubits in superposition
    for q in range(counting_qubits):
        qc.h(q)
    
    # Initialize the working register to |1>
    qc.x(counting_qubits)
    
    # Apply controlled U operations
    for q in range(counting_qubits):
        power = 2**(counting_qubits-q-1)
        controlled_u = c_amod15(a, power).control()
        qc.append(controlled_u, [q] + list(range(counting_qubits, counting_qubits+4)))
    
    # Apply inverse QFT to the counting register
    qc.append(qft_dagger(counting_qubits), range(counting_qubits))
    
    # Measure the counting register
    qc.measure(range(counting_qubits), range(counting_qubits))
    
    return qc

def find_period(a, n=15, counting_qubits=8, shots=1024):
    """Find the period of a^r mod n = 1"""
    qc = create_shors_circuit(a, n, counting_qubits)
    
    # Execute the quantum circuit
    backend = Aer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=shots).result()
    counts = results.get_counts()
    
    # Post-processing to find the period
    measured_phases = []
    
    for output in counts:
        decimal = int(output, 2)
        phase = decimal / (2**counting_qubits)
        measured_phases.append((phase, counts[output]))
    
    # Get the most common phases
    measured_phases.sort(key=lambda x: x[1], reverse=True)
    
    # Try to find the period from the measured phases
    for phase, _ in measured_phases[:5]:  # Consider top 5 results
        frac = Fraction(phase).limit_denominator(n)
        r = frac.denominator
        
        # Check if this is a valid period
        if r % 2 == 0 and a**(r//2) % n != n - 1 and a**r % n == 1:
            return r
    
    return None

def shor_algorithm(N):
    """Full implementation of Shor's algorithm for factoring N"""
    if N % 2 == 0:
        return 2, N // 2
    
    # Step 1: Choose a random number a < N
    import random
    a = random.randint(2, N-1)
    
    # Step 2: Check if a and N are coprime
    factor = gcd(a, N)
    if factor > 1:
        return factor, N // factor
    
    # Step 3: Use quantum subroutine to find the period of a^r mod N = 1
    r = find_period(a, N)
    
    if r is None:
        return "Failed to find period, try again."
    
    # Step 4: If r is odd, try again
    if r % 2 != 0:
        return "r is odd, try again with a different a."
    
    # Step 5: If a^(r/2) mod N = -1, try again
    if (a ** (r // 2)) % N == N - 1:
        return "a^(r/2) mod N = -1, try again with a different a."
    
    # Step 6: Calculate factors of N
    factor1 = gcd(a ** (r // 2) - 1, N)
    factor2 = gcd(a ** (r // 2) + 1, N)
    
    return factor1, factor2

# Example: factoring 15
def run_shors_example():
    """Run Shor's algorithm to factor N=15"""
    N = 15
    a = 7  # Choose a coprime to N
    print(f"Factoring N = {N} with a = {a}")
    
    # Create and draw circuit
    circuit = create_shors_circuit(a, n=N, counting_qubits=8)
    print("Quantum circuit created with", circuit.num_qubits, "qubits")
    
    # Execute the quantum circuit
    backend = Aer.get_backend('qasm_simulator')
    # Transpile for optimization
    transpiled_circuit = transpile(circuit, backend)
    print("Circuit depth after transpilation:", transpiled_circuit.depth())
    
    shots = 2048
    print(f"Running with {shots} shots...")
    results = execute(circuit, backend, shots=shots).result()
    counts = results.get_counts()
    
    # Calculate the period from results
    period = find_period(a, N, counting_qubits=8, shots=shots)
    print(f"Estimated period r = {period}")
    
    if period and period % 2 == 0:
        # Calculate factors
        guess1 = gcd(a**(period//2) - 1, N)
        guess2 = gcd(a**(period//2) + 1, N)
        print(f"Factors of {N} = {guess1} × {guess2}")
    else:
        print("Failed to find factors. Try again with different parameters.")
    
    return counts

if __name__ == "__main__":
    results = run_shors_example()
    print("Measurement results:", results)
