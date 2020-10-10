#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright 2014-2020 by Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype decorator noop unit tests.**

This submodule unit tests edge cases of the :func:`beartype.beartype` decorator
efficiently reducing to a noop.
'''

# ....................{ IMPORTS                           }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS                             }....................
def test_decor_noop_unhinted() -> None:
    '''
    Test that the :func:`beartype.beartype` decorator efficiently reduces to a
    noop on **unannotated callables** (i.e., callables with *no* annotations).
    '''

    # Defer heavyweight imports.
    from beartype import beartype

    # Undecorated unannotated function.
    def khorne(gork, mork):
        return gork + mork

    # Decorated unannotated function.
    khorne_typed = beartype(khorne)

    # Assert that @beartype efficiently reduces to a noop (i.e., the identity
    # decorator) when decorating this function.
    assert khorne_typed is khorne

    # Call this function and assert the expected return value.
    assert khorne_typed('WAAAGH!', '!HGAAAW') == 'WAAAGH!!HGAAAW'


def test_decor_noop_redecorated() -> None:
    '''
    Test that the :func:`beartype.beartype` decorator efficiently reduces to a
    noop on wrappers generated by prior calls to this decorator.
    '''

    # Defer heavyweight imports.
    from beartype import beartype

    # Arbitrary function.
    @beartype
    def xenos(interex: str, diasporex: str):
        print(interex + diasporex)

    # Assert that attempting to redecorate this function yields the same
    # wrapper generated by the above decoration.
    assert xenos is beartype(xenos)

    # Call this function and assert no value to be returned.
    assert xenos('Luna Wolves', diasporex='Iron Hands Legion') is None

# ....................{ TESTS ~ ignorable                 }....................
def test_decor_noop_hint_ignorable_iter() -> None:
    '''
    Test that the :func:`beartype.beartype` decorator efficiently reduces to a
    noop on callables annotated with only ignorable type hints in a manner
    generically exercising non-trivial edge cases with iteration.
    '''

    # Defer heavyweight imports.
    from beartype import beartype
    from beartype_test.unit.data.data_hint import HINTS_IGNORABLE

    # Assert that @beartype efficiently reduces to a noop when passed only
    # type hints known to be ignorable.
    for hint_ignorable in HINTS_IGNORABLE:
        def revenant_scout_titan(
            antecedent:  hint_ignorable,
            preposition: hint_ignorable,
            succedent:   hint_ignorable,
        ) -> hint_ignorable:
            return antecedent + preposition + succedent

        # Decorated annotated functions with ignorable type hints.
        revenant_scout_titan_typed = beartype(revenant_scout_titan)

        # Assert these functions efficiently reduces to their untyped variants.
        assert revenant_scout_titan_typed is revenant_scout_titan

        # Assert these functions return the expected values.
        assert revenant_scout_titan_typed(
            'Hearts Armoured', ' for ', 'Battle') == (
            'Hearts Armoured for Battle')


def test_decor_noop_hint_ignorable_order() -> None:
    '''
    Test that the :func:`beartype.beartype` decorator efficiently reduces to a
    noop on callables annotated with only ignorable type hints in a manner
    specifically exercising non-trivial edge cases with respect to ordering
    that would be pragmatically infeasible to exercise with generic iteration
    in the :func:`test_decor_noop_hint_ignorable_iter` test.
    '''

    # Defer heavyweight imports.
    from beartype import beartype
    from beartype.cave import AnyType
    from typing import Any

    # Undecorated annotated function with ignorable type hints.
    def gork(stompa: AnyType, gargant: object) -> Any:
        return stompa + gargant

    # Undecorated annotated function with ignorable type hints (in the reverse
    # direction of the previously defined function). Since low-level decorator
    # code necessarily handles parameters differently from return values *AND*
    # since the return value for any function may be annotated with at most one
    # type hint, exercising all edge cases necessitates two or more functions.
    def mork(gargant: Any, stompa: object) -> AnyType:
        return stompa + gargant

    # Decorated annotated functions with ignorable type hints.
    gork_typed = beartype(gork)
    mork_typed = beartype(mork)

    # Assert that @beartype efficiently reduces to a noop (i.e., the identity
    # decorator) when decorating these functions.
    assert gork_typed is gork
    assert mork_typed is mork

    # Assert these functions return the expected values.
    assert gork_typed('Goff Klawstompa: ', 'Mega-Gargant') == (
        'Goff Klawstompa: Mega-Gargant')
    assert mork_typed('Killa Kan', "Big Mek's Stompa: ") == (
        "Big Mek's Stompa: Killa Kan")
