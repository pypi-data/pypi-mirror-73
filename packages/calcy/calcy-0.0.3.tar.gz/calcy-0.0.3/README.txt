Calcy is a basic calculator library that allows to add, subtract, multipy and divide MULTIPLE numbers all at once.

Installation
============

Use the package manager `pip <https://pip.pypa.io/en/stable/>`_ to install calcy

```
pip install calcy
```

Usage
=====

```python
import calcy
calcy.help()
```

Calling calcy will list out all the details of the library.

```
Following are the available functionalities with this library

1. add_numbers(*args)\t\t - takes variable agruments and adds them.
2. subtract_numbers(*args)\t - takes variable agruments and subtracts them.
3. multiply_numbers(*args)\t - takes variable agruments and multiplies them.
4. divide_numbers(*args)\t - takes variable agruments and divides them.

In all the above functions, if argument size = 0, function returns float('-inf')
```

Sample Code
===========

```python
import calcy

x = calcy.add_numbers(2,4,5,10,7)
print(x)
```
