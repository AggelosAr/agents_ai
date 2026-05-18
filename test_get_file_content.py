from functions.get_file_content import MAX_CHARS, get_file_contents
import os 
import shutil 
from pathlib import Path


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


def main():
    # Test truncation JUST
    set_up()
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('lorem.txt'))
    print(f'{err=}')
    print(f'{status=}')
    print(f'{contents=}')
    assert err is False
    assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET)
    assert ('truncated' not in contents)
    print(f'lorem.txt length: {len(contents)}')
    print(f'lorem.txt truncated: {'truncated' in contents}')
    bread_down()


    # Test truncation BIGGER
    set_up(characters=111789)
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('lorem.txt'))
    assert err is False
    assert len(contents) > MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET)
    assert ('truncated' in contents)
    print(f'lorem.txt length: {len(contents)}')
    print(f'lorem.txt truncated: {'truncated' in contents}')
    bread_down()


    # Test truncation SMALLER
    set_up(characters=8_999)
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('lorem.txt'))
    assert err is False
    assert len(contents) < MAX_CHARS + OFFSET, '< %d != %d ' % (len(contents), MAX_CHARS + OFFSET)
    assert ('truncated' not in contents)
    print(f'lorem.txt length: {len(contents)}')
    print(f'lorem.txt truncated: {'truncated' in contents}')
    bread_down()


    # Truncation small
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('main.py'))
    assert err is False
    assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET)
    assert ('truncated' in contents) is False
    print(f'main.py length: {len(contents)}')
    print(f'main.py truncated: {'truncated' in contents}')


    # simple truncation works as expected
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('main.py'))
    assert err is False
    assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET)
    assert ('truncated' in contents) is False
    assert 'expression = " ".join(sys.argv[1:])' in contents
    print(f'main.py length: {len(contents)}')
    print(f'main.py truncated: {'truncated' in contents}')


    # fails to get dir as it does not exist
    (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
                                                    file_path=Path('/bin/cat'))
    assert err is True
    assert contents is None
    assert 'Error: Cannot ' in status  and 'permitted working' in status


    # # fails to get file since dir does not exist
    # (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
    #                                                 file_path=Path('pkg/does_not_exist.py'))
    # assert err is True
    # assert contents is None
    # assert 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"' in status


    # # succeeded in getting file metadata 
    # (err, status), (contents, ) = get_file_contents(working_directory=Path('calculator'), 
    #                                                 file_path=Path('calculator/calculator.py'))
    # assert err is False
    # assert len(contents) < 1789 + OFFSET, '< %d != %d ' % (len(contents), 1789 + OFFSET)
    # assert ('truncated' in contents) is False
    # assert 'def _apply_operator(self, operators,' in contents
    # print(f'calculator.py length: {len(contents)}')
    # print(f'calculator.py truncated: {'truncated' in contents}')


if __name__=='__main__':
    main()
