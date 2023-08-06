# unithandler

This is a package for managing and interacting with units. The focus of
the package is to provide numeric type objects (e.g. `float` and `int`)
which also have a `unit` attribute. The three core classes of this
package are `Unit`, `UnitFloat`, and `UnitInt`.

While there are a variety of packages which support units, this
package focused on enabling straightforward implementation of units
without affecting Pythonic functionality of the numbers.

Additionally, the `UnitFloat` class was designed to represent the
magnitude of the stored value as best as possible with an appropriate
SI prefix. The value stored is scaled in its representation, but remains
locked to a specified prefix when operated upon. For example, `0.005`
with the unit `'L'` would be represented as `5 mL` if printed, but will
behave as `0.005` for any numeric operations. This was implemented to
automatically keep track of the scale of a unit while allowing the user
to easily visualize the magnitude of the stored value.

## Installation

`unithandler` is registered on PyPI.
```
pip install unithandler
```

Source files may be found in the [GitLab repository](https://gitlab.com/larsyunker/unithandler).

## The `Unit` class

This class handles all unit-associated attributes and methods. The `unit`
attribute returns an appropriately formatted unit (complete with
superscripts) as a string. Units are managed in dictionary format,
associating a power to each unit denoted. The class (and its subclasses)
are structured) so that the units may be easily modified using python
built-in multiplication and division operators (exactly as one would
track units with pen and paper).

## The `UnitFloat` class

The `UnitFloat` class is a `float`-like numeric class that has an
associated unit. The class has all defined Python magic methods, which
enable all appropriate modifications and operations on or by `UnitFloat`
objects. Typically, the return of each magic method is another `UnitFloat`
instance, but see the `UnitFloat` documentation for further details.

## Known limitations

Since this package is written entirely in Python, it does not provide
direct access to values as the true `float` and `int` would. As such,
some errors or unintended functionality may be encountered.

Currently `numpy` support is limited to basic `ufunc` implementation.
Unexpected behaviour may be encountered when performing `numpy`
operations on `UnitFloat` or `UnitInt`. We are working to implement full
support for vectorized operations on the numeric classes in this package.
To the best of our knowledge, the `math` package is fully supported, so
any numeric operations should be performed with that package while we
work to enable numpy support.