# 🔍 Verfeinerung von Schleifeninvarianten mit adaptivem Feedback, Codevergleich und Caching: Integration von LLMsund Verifizierern

# 🔍 Refining Loop Invariants with Adaptive Feedback, Code Comparison & Caching: Integrating LLMs and Verifiers

Welcome to the **LLM-Driven Invariant Generation and Verification Framework**! This repository explores the intersection of formal verification and machine learning, leveraging the power of **Large Language Models (LLMs)** to automate and enhance the process of generating and validating loop invariants. Whether you’re a researcher, engineer, or student, this framework offers tools and insights to push the boundaries of software verification.

🚨 Disclaimer: This repository is a replica of a private project, developed as part of a Master’s thesis by Milan Bhardwaj. 
The work presented here is partial, strictly copyrighted and should not be reproduced, distributed, or used for commercial purposes.
---

## 🚀 **Overview**

### What Are Invariants?
Invariants are logical properties that hold true at specific points during a program's execution, particularly within loops. These properties are crucial for **formal verification**, ensuring programs behave as expected under all conditions.

### Why This Framework?
Traditional invariant generation methods, such as ICE-based learning, require significant computational effort and domain-specific expertise. Our approach integrates LLMs with **feedback loops**, **semantic caching**, and **code similarity analysis** to:
- **Automate invariant generation**.
- Refine invalid invariants iteratively.
- Reuse validated invariants for similar programs.
- Improve verification accuracy and scalability.

---

## 🛠️ **Key Features**

1. **LLM-Powered Invariant Generation**:
    - Automatically generate invariants for C programs using state-of-the-art LLMs.
    - Fine-tune prompts for better accuracy and relevance.

2. **Feedback-Driven Refinement**:
    - Correct invalid invariants by leveraging feedback from verification tools like Frama-C.
    - Iteratively improve predictions and enhance program verification results.

3. **Semantic Caching and Reuse**:
    - Store valid and invalid invariants in an in-memory database (Redis) with metadata.
    - Use AST-based similarity metrics to identify reusable invariants for new programs.

4. **Integration with Verification Tools**:
    - Seamlessly interface with **Frama-C** for validation.
    - Analyze performance and convergence using real-world benchmarks (e.g., SV-COMP).

---

## 📈 **Results at a Glance**
TBD

---

## 💻 **Getting Started**

### Prerequisites
- **Python 3.9+**
- **Redis** (for caching invariants and metadata)
- **Docker** (for running verification tools like Frama-C)

### Installation
```bash
# Clone the repository

# Navigate to the project directory

# Install dependencies

# Run main program, alter path to dataset before accordingly
