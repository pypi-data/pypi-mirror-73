from typing import TypeVar, Tuple, List, Union, Dict, overload, get_type_hints, Optional, get_args
from abc import abstractmethod, ABCMeta
from types import FunctionType

T = TypeVar('T')


class Checker(metaclass=ABCMeta):
    """Main abstract class for inheritance"""

    def __init__(self, check, match):
        self.var = check
        self.match = match
        self.matched = 0

    @abstractmethod
    def check(self):
        pass

    @staticmethod
    @abstractmethod
    def arg_check(check, match):
        pass


class TypeCheck(Checker):
    """TypeCheck is main class for checkers

        It can be used for self-using or inheritance"""

    def __init__(self, check: T, match: T):
        super().__init__(check, match)

    @staticmethod
    def _check(var: T, match: T) -> bool:
        var_t = type(var)
        match_t = type(match)
        return isinstance(var_t, match_t) if match == type and var == type else var_t == match

    def check(self) -> bool:
        return self._check(self.var, self.match)

    @staticmethod
    def arg_check(check, match):
        return TypeCheck._check(check, match)


class IterCheck(TypeCheck):

    def __init__(self, check: Union[Tuple, List], match: T):
        super().__init__(check, match)

    def check(self) -> bool:
        checker = self.arg_check
        for item in self.var:
            if checker(item, self.match):
                self.matched += 1
        return self.matched == len(self.var)


class FullIterCheck(TypeCheck):

    def __init__(self, check: Union[Tuple, List], match: Union[Tuple, List]):
        super().__init__(check, match)

    def check(self) -> bool:
        checker = self.arg_check
        for var_index, var_item in enumerate(self.var):
            if isinstance(var_item, (tuple, list)) and isinstance(self.match[var_index], (tuple, list)):
                self.matched += 1 if FullIterCheck(var_item, self.match[var_index]).check() else 0
            else:
                self.matched += 1 if checker(var_item, self.match[var_index]) else 0
        return self.matched == len(self.var)


class DictCheck(TypeCheck):

    def __init__(self, check: Dict, match: Dict):
        super().__init__(check, match)

    def check(self) -> bool:
        checker = self.arg_check
        match_items = list(self.match.values())
        match_keys = list(self.match.keys())
        for var_index, var_key in enumerate(self.var.keys()):
            if var_key == match_keys[var_index]:
                if isinstance(self.var[var_key], dict) and isinstance(match_items[var_index], dict):
                    self.matched += 1 if DictCheck(self.var[var_key], match_items[var_index]).check() else 0
                else:
                    self.matched += 1 if checker(self.var[var_key], match_items[var_index]) else 0
        return self.matched == len(self.var)


@overload
def type_check(check: Union[Tuple, List], match: Union[Tuple, List]) -> bool:
    ...


@overload
def type_check(check: Union[Tuple, List], match: T) -> bool:
    ...


@overload
def type_check(check: Dict, match: Dict) -> bool:
    ...


def type_check(check: T, match: T) -> bool:
    if isinstance(check, (tuple, list)) and isinstance(match, (tuple, list)):
        return FullIterCheck(check, match).check()
    elif isinstance(check, (tuple, list)):
        return IterCheck(check, match).check()
    elif isinstance(check, dict) and isinstance(match, dict):
        return DictCheck(check, match).check()
    else:
        return TypeCheck(check, match).check()


def _args_merger(args: List, kwargs: Dict, hints: Dict) -> List:
    ret: List = []
    if len(args) != 0 or len(kwargs) != 0:
        for hints_key in hints.keys():
            try:
                kw_value = kwargs.pop(hints_key)
                ret.append(kw_value)
            except KeyError:
                ret.append(args.pop(0))
    return ret


def checktypes(func: FunctionType):
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        result = _wrap_backend(hints, args, kwargs)
        if result[0]:
            return func(*args, **kwargs)
        else:
            raise TypeError(f"typecheck: some error occurred - {result[1]} at {func.__name__} function")

    def _wrap_backend(hints: dict, args: tuple, kwargs: dict) -> Tuple[bool, Optional[str]]:
        if 'return' in hints:
            hints.pop('return')
        if hints == {}:
            return False, 'need type annotation'
        all_args = _args_merger(list(args), kwargs.copy(), hints)
        if len(all_args) == 0:
            return True, None
        hints_len = len(hints)
        if len(all_args) != hints_len:
            return False, "don't use default params or you missed some argument"
        matched: int = 0
        for hint_index, hint_key in enumerate(hints.keys()):
            hint_value = hints[hint_key]
            hint_args = get_args(hint_value)
            hint_value = hint_value if hint_args == () else hint_args
            arg = all_args[hint_index]
            matched += 1 if type_check(arg, hint_value) else 0
        return (True, None) if matched == hints_len else (False, 'type checking error')

    return wrapper


if __name__ == '__main__':
    print("that's a don't executable script, please import this")
    exit(0)
