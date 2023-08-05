from functools import singledispatch


@singledispatch
def val_it(obj):
    raise NotImplementedError()


@val_it.register
def _(l: list):
    return l


@val_it.register
def _(t: tuple):
    return t


@val_it.register
def _(d: dict):
    return d.values()


@val_it.register
def _(s: set):
    return s


def count_members(obj) -> int:
    nmembers = 0
    for el in val_it(obj):
        if is_complex(el):
            nmembers += count_members(el)
        else:
            nmembers += 1
    return nmembers


def is_complex(obj) -> bool:
    return type(obj) in empty.registry.keys()


@singledispatch
def summary(obj):
    raise NotImplementedError()


@summary.register
def _(d: dict) -> str:
    return "{" f"{count_members(d)}" + "}"


@summary.register
def _(l: list) -> str:
    return "[" f"{count_members(l)}" + "]"


@summary.register
def _(t: tuple) -> str:
    return "(" f"{count_members(t)}" + ")"


@summary.register
def _(s: set) -> str:
    return "set(" f"{count_members(s)}" + ")"


@singledispatch
def it(object):
    raise NotImplementedError


@it.register
def _(d: dict):
    return d.items()


@it.register
def _(l: list):
    return enumerate(l)


@it.register
def _(t: tuple):
    return enumerate(t)


@it.register
def _(s: set):
    return enumerate(s)


@singledispatch
def empty(obj):
    raise NotImplementedError


@empty.register
def _(obj: dict):
    return {}


@empty.register
def _(obj: list):
    return []


@empty.register
def _(obj: tuple):
    return tuple()


@empty.register
def _(obj: set):
    return set()


@singledispatch
def agg(struct, key, el):
    raise NotImplementedError()


@agg.register
def _(l: list, key, el):
    l.append(el)
    return l


@agg.register
def _(l: tuple, key, el):
    return l + (el,)


@agg.register
def _(d: dict, key, el):
    d[key[0]] = el
    return d


@agg.register
def _(s: set, key, el):
    s.add(el)
    return s


def projection(obj, max_level: int, curr_level: int):
    projections = empty(obj)
    for el in it(obj):
        v = el[1]
        if is_complex(v) and curr_level < max_level:
            projections = agg(projections, el, projection(v, max_level, curr_level + 1))
        elif is_complex(v) and curr_level >= max_level:
            projections = agg(projections, el, summary(v))
        else:
            projections = agg(projections, el, v)
    return projections


def nestview(d: dict, level: int = 1) -> dict:
    return projection(d, max_level=level, curr_level=1)
