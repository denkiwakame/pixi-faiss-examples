# faiss-cpu

## Installation

```sh
pixi install
```

## How to switch BLAS backends (OpenBLAS || MKL) in numpy
### TL;DR

Modern `conda-forge` packages for `numpy` provide a mechanism to flexibly switch between different BLAS library backends (OpenBLAS, MKL, etc.) via the `libblas` virtual package. This enables selecting an optimal BLAS implementation for your environment by specifying the appropriate `libblas` package.

For more details, refer to the [conda-forge knowledge base](https://conda-forge.org/docs/maintainer/knowledge_base/#switching-blas-implementation).

### So what?

By specifying the `libblas` package alongside the target package, you can configure BLAS to use MKL:

```bash
pixi add faiss-cpu=1.9.0 "libblas=*=*mkl"
# Alternatively, you can use "blas=*=*mkl" (legacy syntax).
```

In `pixi.toml`, this would look like:

```toml
[dependencies]
faiss-cpu = "1.9.0"
libblas = { version = "*", build = "*mkl" }
# result: libblas = { version = "3.9.0", build = "26_linux64_mkl" }
```

```plaintext
$ pixi tree faiss

└── faiss-cpu 1.9.0
    └── faiss 1.9.0
        ├── __glibc
        ├── _openmp_mutex 4.5
        │   ├── _libgcc_mutex 0.1
        │   └── llvm-openmp 19.1.6
        │       └── __glibc  (*)
        ├── libfaiss 1.9.0
        │   ├── __glibc  (*)
        │   ├── _openmp_mutex 4.5 (*)
        │   ├── libblas 3.9.0
        │   │   └── mkl 2024.2.2
...
```

### 1. numpy installed via pip

When installing `numpy` via PyPI (pip package), BLAS is preconfigured (e.g., `scipy-openblas`):

```bash
pixi add python
pixi add numpy --pypi
```

```bash
pixi run python -c "import numpy; print(numpy.__config__.show())"
```

```plaintext
"Build Dependencies": {
  "blas": {
    "name": "scipy-openblas",
    "found": true,
    "version": "0.3.28",
    "detection method": "pkgconfig",
    "include directory": "/opt/_internal/cpython-3.13.0/lib/python3.13/site-packages/scipy_openblas64/include",
    "lib directory": "/opt/_internal/cpython-3.13.0/lib/python3.13/site-packages/scipy_openblas64/lib",
    "openblas configuration": "OpenBLAS 0.3.28  USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
    "pc file directory": "/project/.openblas"
  }
}
```

### 2. numpy from conda-forge (OpenBLAS)

When installing from `conda-forge`, `numpy` dynamically links to the BLAS backend via the virtual `libblas` package:

```bash
pixi add numpy
```

```plaintext
"Build Dependencies": {
  "blas": {
    "name": "blas",
    "found": true,
    "version": "3.9.0",
    "detection method": "pkgconfig",
    "include directory": "/path/to/env/include",
    "lib directory": "/path/to/env/lib",
    "openblas configuration": "unknown",
    "pc file directory": "/path/to/env/lib/pkgconfig"
  }
}
```

By default, `version=*` and `build=*openblas` are selected.

```bash
pixi list | grep blas
libblas           3.9.0       26_linux64_openblas
libcblas          3.9.0       26_linux64_openblas
liblapack         3.9.0       26_linux64_openblas
libopenblas       0.3.28      pthreads_h94d23a6_1
```

```plaintext
pixi tree numpy

numpy 1.26.4
├── libblas 3.9.0
│   └── libopenblas 0.3.28
│       ├── __glibc
│       ├── libgcc 14.2.0
│       │   ├── _libgcc_mutex 0.1
│       │   └── _openmp_mutex 4.5
│       │       ├── _libgcc_mutex 0.1 (*)
│       │       └── libgomp 14.2.0
│       │           └── _libgcc_mutex 0.1 (*)
│       ├── libgfortran 14.2.0
│       │   └── libgfortran5 14.2.0
│       │       └── libgcc 14.2.0 (*)
│       └── libgfortran5 14.2.0 (*)
```

### 3. numpy from conda-forge (MKL)

To use MKL as the BLAS backend:

```bash
pixi add numpy "libblas=*=*mkl"
```

```bash
pixi list | grep mkl
libblas           3.9.0       26_linux64_mkl
libcblas          3.9.0       26_linux64_mkl
liblapack         3.9.0       26_linux64_mkl
mkl               2024.2.2    ha957f24_16
```

```plaintext
$ pixi tree numpy

numpy 1.26.4
├── libblas 3.9.0
│   └── mkl 2024.2.2
│       ├── _openmp_mutex 4.5
│       │   ├── _libgcc_mutex 0.1
│       │   └── llvm-openmp 19.1.6
│       │       └── __glibc
│       ├── llvm-openmp 19.1.6 (*)
```
