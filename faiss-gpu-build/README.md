# faiss-gpu-build


## installation

```sh
pixi install -a
```

## build

```sh
pixi run configure
```

```sh
pixi run build
```

```sh
pixi run build-python
```

## test

### install swigfaiss

```sh
pixi run install

```

### import test

```sh
pixi run import
```

### gpu test

```sh
pixi run test
```
