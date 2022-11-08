# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

def type_input (message: str, type_, max_iter: int = 10):
    """
    Input loop with type check
    :param message: input message
    :param type_: requested type
    :param max_iter: maximum number of input iterations
    :return: input of type type_
    """

    val = None
    iter_nb = 0
    
    while True:
        val = input(message)

        try:
            val = type_(val)
            return val
        except:
            print('Invalid input')

        iter_nb += 1

        if iter_nb > max_iter:
            raise InterruptedError('Invalid input')
