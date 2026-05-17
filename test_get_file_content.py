from functions.get_file_content import MAX_CHARS, get_file_contents
import os 
import shutil 


OFFSET = 22


def generate_lorem_ipsum(characters: int=10_000) -> str:
    lorem_ipsum_text = """
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    """
    return lorem_ipsum_text*(characters//len(lorem_ipsum_text)) + lorem_ipsum_text[0:characters%len(lorem_ipsum_text)]


def set_up(characters:int=10_000, dest: str='calculator/lorem.txt'):
    test_path = os.path.join(os.getcwd(), dest)
    
    if os.path.isdir(test_path):
        shutil.rmtree(test_path)
    elif os.path.isfile(test_path):
        os.remove(test_path)

    print('Setup. Create lorems at <%s>' % (dest, ))
    with open(os.path.join('calculator', 'lorem.txt'), 'w') as f:
        lorems = generate_lorem_ipsum(characters=characters)
        f.write(lorems)


def bread_down(dest: str='calculator/lorem.txt'):
    test_path = os.path.join(os.getcwd(), dest)
    print('Break Down. Delete lorems at <%s>' % (dest, ))
    if os.path.isdir(test_path):
        shutil.rmtree(test_path)
    elif os.path.isfile(test_path):
        os.remove(test_path)



# Test truncation JUST
set_up()
result = get_file_contents(working_directory='calculator', file_path='lorem.txt')
print('---------------> ', result[0])
assert len(result[0]) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(result[0]), MAX_CHARS + OFFSET)
assert ('truncated' not in result[0])
print(f'lorem.txt length: {len(result[0])}')
print(f'lorem.txt truncated: {'truncated' in result[0]}')
bread_down()


# Test truncation BIGGER
set_up(characters=111789)
result = get_file_contents(working_directory='calculator', file_path='lorem.txt')
print('-------------->', result[0])
assert len(result[0]) > MAX_CHARS + OFFSET, '< %d != %d ' % (len(result[0]), MAX_CHARS + OFFSET)
assert ('truncated' in result[0])
print(f'lorem.txt length: {len(result[0])}')
print(f'lorem.txt truncated: {'truncated' in result[0]}')
bread_down()


# Test truncation SMALLER
set_up(characters=8_999)
result = get_file_contents(working_directory='calculator', file_path='lorem.txt')
assert len(result[0]) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(result[0]), MAX_CHARS + OFFSET)
assert ('truncated' not in result[0])
print(f'lorem.txt length: {len(result[0])}')
print(f'lorem.txt truncated: {'truncated' in result[0]}')
bread_down()


# Truncation small
result = get_file_contents(working_directory='calculator', file_path='main.py')
print(result[0])
assert len(result[0]) < 1789 + OFFSET, '< %d != %d ' % (len(result[0]), 1789 + OFFSET)
assert ('truncated' in result[0]) is False
print(f'main.py length: {len(result[0])}')
print(f'main.py truncated: {'truncated' in result[0]}')


# simple truncation works as expected
result = get_file_contents(working_directory='calculator', file_path='main.py')
print(result[0])
assert len(result[0]) < 1789 + OFFSET, '< %d != %d ' % (len(result[0]), 1789 + OFFSET)
assert ('truncated' in result[0]) is False
assert 'expression = " ".join(sys.argv[1:])' in result[0]
print(f'main.py length: {len(result[0])}')
print(f'main.py truncated: {'truncated' in result[0]}')


# fails to get dir as it does not exist
result = get_file_contents(working_directory='calculator', file_path='/bin/cat')
assert len(result[0]) < 1789 + OFFSET, '< %d != %d ' % (len(result[0]), 1789 + OFFSET)
assert ('truncated' in result[0]) is False
assert 'Error: Cannot ' in result[0]  and 'permitted working' in result[0]
print(f'/bin/cat length: {len(result[0])}')
print(f'/bin/cat truncated: {'truncated' in result[0]}')


# fails to get file since dir does not exist
result = get_file_contents(working_directory='calculator', file_path='pkg/does_not_exist.py')
print(result[0])
assert len(result[0]) < 1789 + OFFSET, '< %d != %d ' % (len(result[0]), 1789 + OFFSET)
assert ('truncated' in result[0]) is False
assert 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"' in result[0]
print(f'pkg/does_not_exist.py length: {len(result[0])}')
print(f'pkg/does_not_exist.py truncated: {'truncated' in result[0]}')


# succeeded in getting file metadata 
result = get_file_contents(working_directory='calculator', file_path='calculator/calculator.py')
print(result[0])
assert len(result[0]) < 1789 + OFFSET, '< %d != %d ' % (len(result[0]), 1789 + OFFSET)
assert ('truncated' in result[0]) is False
assert 'def _apply_operator(self, operators,' in result[0]
print(f'calculator.py length: {len(result[0])}')
print(f'calculator.py truncated: {'truncated' in result[0]}')
