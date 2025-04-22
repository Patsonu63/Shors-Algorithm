# Shors-Algorithm
Quantum computing
Alright! Let's walk through **Shor's Algorithm** — both **theory** and a **working code example** to factor **15**, using Qiskit in **Google Colab** or your local machine.

---

## ⚛️ What is Shor’s Algorithm?

Shor’s algorithm is a **quantum algorithm for integer factorization**. It provides an **exponential speedup** over classical factoring algorithms.

## ✅ Working Shor's Algorithm Example (Factoring 15)

We'll use a **simulated version**, since real quantum computers can't yet factor large numbers.

### 👇 Code (run this in Colab)

```python
!pip install qiskit qiskit-aer --quiet

from qiskit_aer import AerSimulator
from qiskit.algorithms import Shor
from qiskit.primitives import Sampler
from qiskit import QuantumCircuit, transpile

# Create simulator
simulator = AerSimulator()

# Create instance of Shor’s algorithm
shor = Shor()

# Run Shor’s algorithm to factor 15
result = shor.factor(N=15)

print("✅ Factors of 15:", result.factors)
```

> Output will be something like: `✅ Factors of 15: [[3, 5]]`

---

## 💡 Notes:
- **Qiskit 0.44+** or later is needed for this version of `Shor`.
- If you're using a newer version and it still doesn't work, use the manual circuit version below.

---

## ⚙️ Manual (Educational) Version of Shor's Algorithm

If you'd like to **build it manually using quantum gates**, I can walk you through:
- Superposition
- Modular exponentiation
- Inverse QFT
- Period finding
- Classical post-processing



