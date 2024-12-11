# Accelerating N-Body in Python


## Overview

This repository provides an analysis of **N-Body** benchmarks originally featured on the [Programming Language Benchmarks](https://programming-language-benchmarks.vercel.app/) website. It includes three additional Python implementations to offer a more comprehensive comparison of the performance achievable using Python libraries and Rust bindings. This project was developed as part of the coursework for MPCS 56430 Introduction to Scientific Computing.

## Motivation

Python has a reputation for being a slow programming language, especially when compared to languages such as C++ and Fortran. This makes Python's widespread adoption in scientific computing seem counterintuitive, since large-scale scientific codebases often require high performance.

The Python benchmarks featured on the [Programming Language Benchmarks](https://programming-language-benchmarks.vercel.app/) website are written in pure Python and do not leverage any of the libraries commonly used in scientific Python code. In this project, I wanted to see if the performance gap between Python and compiled code could be reduced by using packages such as NumPy, Numba, and PyO3/Maturin for accessing Rust code. 

The ["The Counter-Intuitive Rise of Python in Scientific Computing"](https://cerfacs.fr/coop/fortran-vs-python) post from The COOP Blog is a fantastic read and served as an inspiration for choosing this project.

## Features

- **Original Benchmarks**: Basic N-Body implementations in C++, Rust, and Python.
- **Enhanced Benchmarks**: Three new implementations leveraging advanced Python libraries and Rust bindings:
  - **NumPy**: Optimized numerical computations using NumPy arrays.
  - **Numba**: Just-In-Time (JIT) compilation with Numba for accelerated performance.
  - **Rust-Python Binding**: High-performance Rust code accessible from Python via [Maturin](https://github.com/PyO3/maturin) and [PyO3](https://github.com/PyO3/pyo3).

## Benchmark Implementations

### Original Implementations

The repository includes the following basic N-Body implementations sourced from the [Programming Language Benchmarks](https://programming-language-benchmarks.vercel.app/) website:

- **C++**: [(1.cpp)](https://github.com/hanabi1224/Programming-Language-Benchmarks/blob/main/bench/algorithm/nbody/1.cpp)

- **Rust**: [(1.rs)](https://github.com/hanabi1224/Programming-Language-Benchmarks/blob/main/bench/algorithm/nbody/1.rs)

- **Python**: [(2.py)](https://github.com/hanabi1224/Programming-Language-Benchmarks/blob/main/bench/algorithm/nbody/2.py)

While there are faster implementations in Rust and C++, I chose to go with the simpler implementations that do not leverage SIMD or parallelism.

### Enhanced Implementations

1. **NumPy Implementation**
   - Utilizes NumPy's optimized array operations to handle numerical computations efficiently.


2. **Numba Implementation**
   - Applies Numba's JIT compilation to accelerate Python code execution.


3. **Rust-Python Binding**
   - Creates Python bindings to the Rust implementation using Maturin and PyO3.
  

## Results

### Local Machine

Execution Time (in seconds)

| Implementation/ N Iterations | 500,000 | 5,000,000 | 50,000,000 |
|-----------------------------|---------|-----------|------------|
| C++                         | 0.132       | 0.274         | 1.625          |
| Rust                        | 0.146      | 0.583         |  5.035         |
| Rust Binding                | 0.145       | 0.753         | 6.854          |
| Python                      | 1.997       | 19.615         | N/A          |
| Numba                       | 0.688       | 2.082         | 16.349          |
| NumPy                       | 11.534       | N/A        | N/A          |





