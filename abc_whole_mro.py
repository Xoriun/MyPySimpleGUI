"""Copyright 2026 <Xoriun>"""

import abc


class ABCWholeMroMeta(abc.ABCMeta):
    r"""
    Modification of the abc.ABCMeta metaclass that conciders all superclasses for conrete implementations of abstract methods.

    With ABCMeta and inheritance like `class C(A, B)`, `class A(ABC)`, if `A` defines an abstract `foo` and `B` defines a concrete `foo`,
    one cannot create an instance of `C` since abstract `foo` in `A` is found first.\
    This is the reason d'être for `ABCWholeMroMeta`, since with `class A(ABCWholeMro)`, one now can create instances `c` of `C`
    and calling `c.foo` evaluates to the conrete implementation in `B` instead of the abstract implementation inf `A`.
    This is by design, although there might be a setting in the future to toggle this behaviour.

    This implementation is only tested for the so far limited usecase in this repo
    and might exhibit unexpected behaviour for more complex inheritance structures.
    """
    def __new__(cls, name, bases, attrs):
        # let abc.ABCMeta do its thing
        actual_class = super().__new__(cls, name, bases, attrs)

        # here come the new stuff that also accepts non-abstract implementations
        # in base-classes that come later in the mro than the abstract implementation
        new_abstracts = set(actual_class.__abstractmethods__)
        for abstract_method_name in actual_class.__abstractmethods__:
            # iterate over the whole mro (bases only includes direct inheritance)
            # don't include actual_class (index 0) and object (index -1)
            for super_class in actual_class.__mro__[1:-1]:
                # use __dict__ instead of getattr in order to only get those implementations
                # that are defined by super_class itself and not those that are reachable through super_class
                potential_abstract_method_obj = super_class.__dict__.get(abstract_method_name, None)

                if potential_abstract_method_obj is None or getattr(potential_abstract_method_obj, "__isabstractmethod__", False):
                    # abstract_method_name does not exist for super_class
                    # OR it is abstract in super_class
                    # -> nothing to do, go to next super_class
                    continue

                new_abstracts.discard(abstract_method_name)

                # make sure mro-lookup doesn't find prev abstract implementations
                # this is the only part that might mess with things
                # but is necessary since otherwise calling the abstract_method_name might call some abstract implementation
                setattr(actual_class, abstract_method_name, potential_abstract_method_obj)

                # make sure that later non-abstract implementations don't overwrite this
                break

        actual_class.__abstractmethods__ = frozenset(new_abstracts)
        return actual_class

class ABCWholeMro(abc.ABC, metaclass=ABCWholeMroMeta):
    r"""
    Modification of the abc.ABCM class that conciders all superclasses for conrete implementations of abstract methods.

    With ABC and inheritance like `class C(A, B)`, `class A(ABC)`, if `A` defines an abstract `foo` and `B` defines a concrete `foo`,
    one cannot create an instance of `C` since abstract `foo` in `A` is found first.\
    This is the reason d'être for `ABCWholeMro`, since with `class A(ABCWholeMro)`, one now can create instances `c` of `C`
    and calling `c.foo` evaluates to the conrete implementation in `B` instead of the abstract implementation inf `A`.
    This is by design, although there might be a setting in the future to toggle this behaviour.

    This implementation is only tested for the so far limited usecase in this repo
    and might exhibit unexpected behaviour for more complex inheritance structures.
    """
