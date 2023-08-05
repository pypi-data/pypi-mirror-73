#!/usr/bin/env python
# -*- coding: utf-8 -*-


def token(cls):
    class TokenMeta(type(cls)):
        @property
        def is_token(self):
            return True
    cls.__metaclass__ = TokenMeta
    return cls


def is_token(t):
    return hasattr(t, 'is_token') and t.is_token


class binary_operator:

    _operator_rules = {
        '+': 'add',
        '-': 'sub',
        '*': 'mul',
        '/': 'div',
        '//': 'truediv',
        '@': 'matmul',
        '**': 'pow',
    }

    class BinaryDispatcher:
        def __init__(self, f, t_other, next=None):
            self.f = f
            self.t_other = t_other
            self.next = next

        def __call__(self, other):

            if issubclass(type(other), self.t_other):
                self.f(self, other)
            elif self.next:
                self.next(other)
            else:
                raise TypeError(
                    f'Unsupported operands {self} and {other}.'
                )

    class ReverseBinaryDispatcher:
        def __init__(self, f, t_other, next=None):
            self.f = f
            self.t_other = t_other
            self.next = next

        def __call__(self, other):

            if issubclass(type(other), self.t_other):
                self.f(other, self)
            elif self.next:
                self.next(other)
            else:
                raise TypeError(
                    f'Unsupported operands {other} and {self}.'
                )

    def __init__(self, t1, op, t2):
        if op not in self._operator_rules:
            raise ValueError(f'Unknown binary operator {op}')
        if is_token(t1):
            rule = f'__{self._operator_rules[op]}__'
            t1.__dict__[rule] = self.dispatcher = self.BinaryDispatcher(
                None,
                t2,
                next=t1.__dict__.pop(rule, None)
            )
        elif is_token(t2):
            rule = f'__r{self._operator_rules[op]}__'
            t2.__dict__[rule] = self.dispatcher = self.ReverseBinaryDispatcher(
                None,
                t1,
                next=t2.__dict__.pop(rule, None)
            )
        else:
            raise ValueError(
                f'At least one operand must be a token, got {t1} and {t2}.'
            )

    def __call__(self, action):
        self.dispatcher.f = action
        return action
