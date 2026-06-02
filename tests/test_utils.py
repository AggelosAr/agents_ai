import os
import shutil


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
