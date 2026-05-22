import os
import shutil
import traceback
from functools import partial
from typing import Any, Callable


def generate_lorem_ipsum(characters: int=10_000) -> str:
    lorem_ipsum_text = """
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    """
    return lorem_ipsum_text*(characters//len(lorem_ipsum_text)) + lorem_ipsum_text[0:characters%len(lorem_ipsum_text)]


def set_up(characters:int=10_000, dest: str='calculator/lorem.txt') -> None:
    print('\n\n\t-> SET UP START\n\n')

    test_path = os.path.join(os.getcwd(), dest)
    
    if os.path.isdir(test_path):
        shutil.rmtree(test_path)
    elif os.path.isfile(test_path):
        os.remove(test_path)

    print('\t\t->Create lorems at <%s>' % (dest, ))
    with open(os.path.join('calculator', 'lorem.txt'), 'w') as f:
        lorems = generate_lorem_ipsum(characters=characters)
        f.write(lorems)

    print('\n\n\t->  SET UP FINISH\n\n')


def break_down(dest: str='calculator/lorem.txt') -> None:
    print('\n\n\t-> BREAK DOWN START\n\n')

    test_path = os.path.join(os.getcwd(), dest)
    print('Break Down. Delete lorems at <%s>' % (dest, ))
    if os.path.isdir(test_path):
        shutil.rmtree(test_path)
    elif os.path.isfile(test_path):
        os.remove(test_path)

    print('\n\n\t-> BREAK DOWN FINISH\n\n')



TOTAL_TESTS = 0
TEST_FAILS = 0
# TODO add utility to add test counter
# TODO also sort tests (e.g. at the bottom the failures)
# TODO also remove the test calls inside the main


def test_case(name,  func: Callable[[Any, ], Any]) -> Callable[[Any, ], Any]:

    NEGATIVE = "\033[7m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    
    # if func.__name__ not in {'s'}:
    #     return lambda : ...
    
    def wrapper(*args, **kwargs) -> Any:

        print('Running test: <%s>.<%s>\n\n' % (os.path.split(name)[-1], func.__name__, ))

        results = None

        try:
            results = func(*args, **kwargs)
        except Exception as e:
            print('\n\n\n\n\t\t*** EXCEPTION DURING TEST <%s> ***' % (func.__name__, ))

            traceback.print_exc()

            print('\n\n\n\n\n\n\t\t\t %s--------- [FAIL] ---------%s' % (RED, RESET, ))
        else:
            print('\n\n\n\n\n\n\t\t\t %s--------- [PASS] ---------%s' % (GREEN, RESET, ))
        finally:
            print('%s%s%s%s' % (NEGATIVE, CYAN, 120*'=', RESET))
        
        return results

    return wrapper



def discover(globals):

    globals['test_case'] = partial(test_case, globals['__file__'])

    def wrapper(main):
        
        def _wrapper(*args, **kwargs):
            a_main = main
            return a_main(*args, **kwargs)

        return _wrapper
    return wrapper
