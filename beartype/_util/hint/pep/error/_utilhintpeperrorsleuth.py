#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype type-checking error cause sleuth** (i.e., object recursively
fabricating the human-readable string describing the failure of the pith
associated with this object to satisfy this PEP-compliant type hint also
associated with this object) classes.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
from beartype.roar import _BeartypeUtilRaisePepException
from beartype._util.hint.pep.utilhintpepget import get_hint_pep_typing_attr
from beartype._util.hint.pep.utilhintpeptest import is_hint_pep
from copy import copy

# See the "beartype.__init__" submodule for further commentary.
__all__ = ['STAR_IMPORTS_CONSIDERED_HARMFUL']

# ....................{ CLASSES                           }....................
class CauseSleuth(object):
    '''
    **Type-checking error cause sleuth** (i.e., object recursively fabricating
    the human-readable string describing the failure of the pith associated
    with this object to satisfy this PEP-compliant type hint also associated
    with this object).

    Attributes
    ----------
    cause_indent : str
        **Indentation** (i.e., string of zero or more spaces) preceding each
        line of the string returned by this getter if this string spans
        multiple lines *or* ignored otherwise (i.e., if this string is instead
        embedded in the current line).
    exception_label : str
        Human-readable label describing the parameter or return value from
        which this object originates, typically embedded in exceptions raised
        from this getter in the event of unexpected runtime failure.
    hint : object
        Type hint to validate this object against.
    hint_attr : object
        Argumentless :mod:`typing` attribute identifying this hint if this hint
        is PEP-compliant *or* ``None`` otherwise.
    pith : object
        Arbitrary object to be validated.
    '''

    # ..................{ INITIALIZERS                      }..................
    def __init__(
        self,
        pith: object,
        hint: object,
        cause_indent: str,
        exception_label: str,
    ) -> None:
        '''
        Initialize this object.
        '''
        assert isinstance(cause_indent, str), (
            f'{repr(cause_indent)} not string.')
        assert isinstance(exception_label, str), (
            f'{repr(exception_label)} not string.')

        # Classify all passed parameters.
        self.pith = pith
        self.hint = hint
        self.cause_indent = cause_indent
        self.exception_label = exception_label

        # Argumentless "typing" attribute identifying this hint if this hint is
        # PEP-compliant *or* ``None`` otherwise.
        self.hint_attr = (
            get_hint_pep_typing_attr(self.hint)
            if is_hint_pep(self.hint) else
            None
        )

    # ..................{ GETTERS                           }..................
    def get_cause_or_none(self) -> 'Optional[str]':
        '''
        Human-readable string describing the failure of this pith to satisfy
        this PEP-compliant type hint if this pith fails to satisfy this pith
        *or* ``None`` otherwise (i.e., if this pith satisfies this hint).

        Design
        ----------
        This getter is intentionally generalized to support objects both
        satisfying and *not* satisfying hints as equally valid use cases. While
        the parent :func:`.utilhintpeperror.raise_pep_call_exception` function
        calling this getter is *always* passed an object *not* satisfying the
        passed hint, this getter is under no such constraints. Why? Because
        this getter is also called to find which of an arbitrary number of
        objects transitively nested in the object passed to
        :func:`.utilhintpeperror.raise_pep_call_exception` fails to satisfy the
        corresponding hint transitively nested in the hint passed to that
        function.

        For example, consider the PEP-compliant type hint ``List[Union[int,
        str]]`` describing a list whose items are either integers or strings
        and the list ``list(range(256)) + [False,]`` consisting of the integers
        0 through 255 followed by boolean ``False``. Since this list is a
        standard sequence, the
        :func:`._utilhintpeperrorsequence.get_cause_or_none_sequence_standard`
        function must decide the cause of this list's failure to comply with
        this hint by finding the list item that is neither an integer nor a
        string, implemented by by iteratively passing each list item to the
        :func:`._utilhintpeperrorunion.get_cause_or_none_union` function. Since
        the first 256 items of this list are integers satisfying this hint,
        :func:`._utilhintpeperrorunion.get_cause_or_none_union` returns
        ``None`` to
        :func:`._utilhintpeperrorsequence.get_cause_or_none_sequence_standard`
        before finally finding the non-compliant boolean item and returning the
        human-readable cause.

        Returns
        ----------
        Optional[str]
            Either:

            * If this object fails to satisfy this hint, human-readable string
            describing the failure of this object to do so.
            * Else, ``None``.

        Raises
        ----------
        _BeartypeUtilRaisePepException
            If this type hint is either:

            * PEP-noncompliant (e.g., tuple union).
            * PEP-compliant but no getter function has been implemented to
              handle this category of PEP-compliant type hint yet.
        '''

        # Getter function returning the desired string.
        get_cause_or_none = None

        # If *NO* argumentless "typing" attribute identifies this hint, this
        # hint is PEP-noncompliant. In this case...
        if self.hint_attr is None:
            # Avoid circular import dependencies.
            from beartype._util.hint.pep.error._utilhintpeperrortype import (
                get_cause_or_none_type)

            # If this hint is *NOT* a non-"typing" class, this hint is an
            # unsupported PEP-noncompliant type hint. In this case, raise an
            # exception.
            if not isinstance(self.hint, type):
                raise _BeartypeUtilRaisePepException(
                    f'{self.exception_label} type hint '
                    f'{repr(self.hint)} unsupported '
                    f'(i.e., neither PEP-compliant nor non-"typing" class).'
                )

            # Defer to the getter function supporting non-"typing" classes.
            get_cause_or_none = get_cause_or_none_type
        # Else, this hint is PEP-compliant. In this case...
        else:
            # Avoid circular import dependencies.
            from beartype._util.hint.pep.error.utilhintpeperror import (
                _TYPING_ATTR_TO_GETTER)

            # Getter function returning the desired string for this attribute
            # if any *OR* "None" otherwise.
            get_cause_or_none = _TYPING_ATTR_TO_GETTER.get(
                self.hint_attr, None)

            # If no such function has been implemented to handle this attribute
            # yet, raise an exception.
            if get_cause_or_none is None:
                raise _BeartypeUtilRaisePepException(
                    f'{self.exception_label} PEP type hint '
                    f'{repr(self.hint)} unsupported (i.e., no '
                    f'"get_cause_or_none_"-prefixed getter function defined '
                    f'for this category of hint).'
                )
            # Else, a getter function has been implemented to handle this
            # attribute.

        # Call this getter function with ourselves and return the string
        # returned by this getter.
        return get_cause_or_none(self)

    # ..................{ PERMUTERS                         }..................
    def permute(self, **kwargs) -> 'CauseSleuth':
        '''
        Shallow copy of this object such that each the passed keyword argument
        overwrites the instance variable of the same name in this copy.

        Parameters
        ----------
        Keyword arguments of the same name and type as instance variables of
        this object (e.g., ``hint``, ``pith``).

        Returns
        ----------
        CauseSleuth
            Shallow copy of this object such that each keyword argument
            overwrites the instance variable of the same name in this copy.

        Examples
        ----------
            >>> sleuth = CauseSleuth(
            ...     pith=[42,]
            ...     hint=typing.List[int],
            ...     cause_indent='',
            ...     exception_label='List of integers',
            ... )
            >>> sleuth_copy = sleuth.permute(pith=[24,])
            >>> sleuth_copy.pith
            [24,]
            >>> sleuth_copy.hint
            typing.List[int]
        '''

        # Shallow copy of this object.
        sleuth_copy = copy(self)

        # For each passed variable name and value, overwrite the instance
        # variable of the same name in this copy.
        for var_name, var_value in kwargs.items():
            setattr(sleuth_copy, var_name, var_value)

        # Return this copy.
        return sleuth_copy