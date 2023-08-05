# flat-tree

[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/flat-tree/status.svg)](https://drone.autonomic.zone/hyperpy/flat-tree)

## Utilities for navigating flat trees

> Flat Trees are the core data structure that power Hypercore feeds. They allow
> us to deterministically represent a tree structure as a vector. This is
> particularly useful because vectors map elegantly to disk and memory. Because
> Flat Trees are deterministic and pre-computed, there is no overhead to using
> them. In effect this means that Flat Trees are a specific way of indexing
> into a vector more than they are their own data structure. This makes them
> uniquely efficient and convenient to implement in a wide range of languages.

## Install

```sh
$ pip install flat-tree
```

## Example

```python
from flat_tree.accessor import FlatTreeIterator

tree_iter = FlatTreeIterator()
assert tree_iter.index == 0
assert tree_iter.parent() == 1
assert tree_iter.parent() == 3
```
