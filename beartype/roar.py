#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Hear beartype roar** as it handles errors and warnings.

This submodule defines hierarchies of :mod:`beartype`-specific exceptions
and warnings emitted by the :func:`beartype.beartype` decorator.
'''

# ....................{ IMPORTS                           }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from abc import ABCMeta as _ABCMeta

# See the "beartype.__init__" submodule for further commentary.
__all__ = ['STAR_IMPORTS_CONSIDERED_HARMFUL']

# ....................{ EXCEPTIONS                        }....................
class BeartypeException(Exception, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype exceptions.**

    Instances of subclasses of this exception are raised either:

    * At decoration time from the :func:`beartype.beartype` decorator.
    * At call time from the new callable generated by the
      :func:`beartype.beartype` decorator to wrap the original callable.
    '''

    pass

# ....................{ EXCEPTIONS ~ cave                 }....................
class BeartypeCaveException(BeartypeException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype cave exceptions.**

    Instances of subclasses of this exception are raised at usage time from
    various types published by the :func:`beartype.cave` submodule.
    '''

    pass

# ....................{ EXCEPTIONS ~ cave : nonetypeor    }....................
class BeartypeCaveNoneTypeOrException(
    BeartypeCaveException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype cave** ``None`` **tuple factory
    exceptions.**

    Instances of subclasses of this exception are raised at usage time from
    the :func:`beartype.cave.NoneTypeOr` tuple factory.
    '''

    pass


class BeartypeCaveNoneTypeOrKeyException(BeartypeCaveNoneTypeOrException):
    '''
    **Beartype cave** ``None`` **tuple factory key exception.**

    This exception is raised when indexing the :func:`beartype.cave.NoneTypeOr`
    dictionary with an invalid key, including:

    * The empty tuple.
    * Arbitrary objects that are neither:

      * **Types** (i.e., :class:`beartype.cave.ClassType` instances).
      * **Tuples of types** (i.e., tuples whose items are all
        :class:`beartype.cave.ClassType` instances).
    '''

    pass


class BeartypeCaveNoneTypeOrMutabilityException(
    BeartypeCaveNoneTypeOrException):
    '''
    **Beartype cave** ``None`` **tuple factory mutability exception.**

    This exception is raised when attempting to explicitly set a key on the
    :func:`beartype.cave.NoneTypeOr` dictionary.
    '''

    pass

# ....................{ EXCEPTIONS ~ decor                }....................
class BeartypeDecorException(BeartypeException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype decorator exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator.
    '''

    pass

# ....................{ EXCEPTIONS ~ wrapp[ee|er]         }....................
class BeartypeDecorWrappeeException(BeartypeDecorException):
    '''
    **Beartype decorator wrappee exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator when passed a **wrappee** (i.e., object
    to be decorated by this decorator) of invalid type.
    '''

    pass


class BeartypeDecorWrapperException(BeartypeDecorException):
    '''
    **Beartype decorator parse exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on accidentally generating an **invalid
    wrapper** (i.e., syntactically invalid new callable to wrap the original
    callable).
    '''

    pass

# ....................{ EXCEPTIONS ~ decor : hint         }....................
class BeartypeDecorHintException(BeartypeDecorException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype decorator type hinting exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    type-hinted with invalid annotations.
    '''

    pass


class BeartypeDecorHintValueException(BeartypeDecorHintException):
    '''
    **Beartype decorator "full" type hinting exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable type-hinted
    with an invalid object (e.g., which is neither a class, fully-qualified
    classname, nor tuple of classes and/or classnames).
    '''

    pass

# ....................{ EXCEPTIONS ~ decor : param        }....................
class BeartypeDecorParamException(BeartypeDecorException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype decorator parameter exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    declaring invalid parameters.
    '''

    pass


class BeartypeDecorParamNameException(BeartypeDecorParamException):
    '''
    **Beartype decorator hinted tuple item invalid exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable declaring
    parameters with invalid names.
    '''

    pass

# ....................{ EXCEPTIONS ~ decor : pep          }....................
class BeartypeDecorPepException(BeartypeDecorException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype decorator Python Enhancement Proposal
    (PEP) exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    violating a specific PEP.
    '''

    pass


class BeartypeDecorPep563Exception(BeartypeDecorPepException):
    '''
    **Beartype decorator** `PEP 563`_ **evaluation exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on failing to dynamically evaluate a
    postponed annotation of the decorated callable when `PEP 563`_ is active
    for that callable.

    .. _PEP 563:
       https://www.python.org/dev/peps/pep-0563
    '''

    pass

# ....................{ EXCEPTIONS ~ decor : pep : 484    }....................
class BeartypeDecorPep484Exception(
    BeartypeDecorPepException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype decorator** `PEP 484`_
    **exceptions.**

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    violating either `PEP 484`_ itself or our implementation of `PEP 484`_.

    .. _PEP 484:
       https://www.python.org/dev/peps/pep-0484
    '''

    pass


class BeartypeDecorPep484TypeUnsupportedException(
    BeartypeDecorPep484Exception):
    '''
    **Beartype decorator** `PEP 484`_ **unsupported type exception.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on failing to dynamically evaluate a
    postponed annotation of the decorated callable when `PEP 563`_ is active
    for that callable.

    Instances of subclasses of this exception are raised at decoration time
    from the :func:`beartype.beartype` decorator on receiving a callable
    annotated with one or more `PEP 484`_ types (i.e., classes and objects
    defined by the stdlib :mod:`typing` module) currently unsupported by this
    decorator.

    .. _PEP 484:
       https://www.python.org/dev/peps/pep-0484
    '''

    pass

# ....................{ EXCEPTIONS ~ call                 }....................
class BeartypeCallException(BeartypeException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartyped callable exceptions.**

    Instances of subclasses of this exception are raised from the **wrapper
    function** (i.e., generated by the :func:`beartype.beartype` decorator to
    wrap the callable decorated by that decorator).
    '''

    pass


class BeartypeCallBeartypistryException(BeartypeCallException):
    '''
    **Beartyped callable beartypistry exception.**

    This exception is raised from the wrapper function when that function
    erroneously accesses the **beartypistry** (i.e.,
    :class:`beartype._decor._typistry.BEARTYPISTRY` singleton).

    This exception denotes a critical issue and should thus *never* be raised.
    '''

    pass

# ....................{ EXCEPTIONS ~ call : type          }....................
class BeartypeCallTypeException(BeartypeCallException, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartyped callable type exceptions.**

    This exception is raised from the wrapper function when either passed a
    parameter or returning an object whose value is of **unexpected type**
    (i.e., violating type hints annotated for that parameter or return value).
    '''

    pass


class BeartypeCallTypeParamException(BeartypeCallTypeException):
    '''
    **Beartyped callable parameter type exception.**

    This exception is raised from the wrapper function when passed a parameter
    whose value is of unexpected type.
    '''

    pass


class BeartypeCallTypeReturnException(BeartypeCallTypeException):
    '''
    **Beartyped callable return type exception.**

    This exception is raised from the wrapper function when returning an object
    whose value is of unexpected type.
    '''

    pass

# ....................{ EXCEPTIONS ~ util                 }....................
class BeartypeCallableCachedException(BeartypeException):
    '''
    **Beartype memoization exception.**

    This exception is raised by the
    :func:`beartype._util.utilcache.callable_cached` decorator when the
    signature of the callable being decorated is unsupported.
    '''

    pass

# ....................{ WARNINGS                          }....................
class BeartypeWarning(UserWarning, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype warnings.**

    Instances of subclasses of this warning are emitted either:

    * At decoration time from the :func:`beartype.beartype` decorator.
    * At call time from the new callable generated by the
      :func:`beartype.beartype` decorator to wrap the original callable.
    '''

    pass