from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps

def check_value_range(func):
    @wraps(func)
    def wrapped(x):
        type_hints = get_type_hints(func, include_extras=True)
        hint = type_hints['x']
        if get_origin(hint) is Annotated:
            hint_types, *hint_args = get_args(hint)
            low, high = hint_args[0]

            if not low <= x <= high:
                raise ValueError(f"{x} falls outside boundary {low}-{high}")
        
        return func(x)
    return wrapped


@check_value_range
def double(x: Annotated[int,(0,10)]) -> int:
    return x * 2


result = double(4)
print(result)