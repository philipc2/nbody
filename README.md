# Accelerating N-Body Python Code 


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

- **C++**
  - Basic implementation without leveraging SIMD or parallelism.

- **Rust**
  - Basic implementation without leveraging SIMD or parallelism.

- **Python**
  - A pure Python implementation
  - Serves as a baseline for comparing the performance of optimized Python approaches.

### Enhanced Implementations

To explore the performance enhancements achievable with modern tools and libraries, three new N-Body implementations have been developed:

1. **NumPy Implementation**
   - **Description**: Utilizes NumPy's optimized array operations to handle numerical computations efficiently.
   - **Advantages**:
     - Leverages vectorized operations for faster calculations.
     - Reduces the overhead of Python loops.

2. **Numba Implementation**
   - **Description**: Applies Numba's JIT compilation to accelerate Python code execution.
   - **Advantages**:
     - Transforms Python functions into optimized machine code at runtime.
     - Achieves performance closer to compiled languages like C++ and Rust.

3. **Rust-Python Binding**
   - **Description**: Creates Python bindings to the Rust implementation using Maturin and PyO3.
   - **Advantages**:
     - Combines Rust's high performance with Python's ease of use.
     - Allows seamless integration of Rust code into Python workflows.



