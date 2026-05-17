from functions.write_file import write_file
from test_get_file_content import set_up, bread_down


# Test: successfully wrote to dir when dir existed (overwrite). 
set_up()
msg, contents = write_file(working_directory='calculator', 
                           file_path='lorem.txt', 
                           content="wait, this isn't lorem ipsum")
print('--------------------> ', msg)
print('--------------------> ', contents)
assert 'Successfully wrote to' in msg and 'haracters wr' in msg
assert "wait, this isn't lorem ipsum" in contents
bread_down()


# Test: successfully wrote to dir when dir did not exist. 
msg, contents = write_file(working_directory='calculator', 
                           file_path='lorem.txt', 
                           content="wait, this isn't lorem ipsum")
print('-----------> ', msg)
print('-----------> ', contents)
assert 'Successfully wrote to' in msg and 'haracters wr' in msg
assert "wait, this isn't lorem ipsum" in contents
bread_down()


# Test: successfully wrote to dir
set_up(dest='pkg/morelorem.txt')
msg, contents = write_file(working_directory='calculator', 
                           file_path='pkg/morelorem.txt', 
                           content='lorem ipsum dolor sit amet')
assert 'Successfully wrote to' in msg
assert 'lorem ipsum dolor sit amet' in contents
bread_down(dest='pkg/morelorem.txt')


# Test: can write a new file
msg, contents = write_file(working_directory='calculator', 
                           file_path='pkg/morelorem.txt', 
                           content='lorem ipsum dolor sit amet')
assert 'Successfully wrote to' in msg
assert 'lorem ipsum dolor sit amet' in contents
bread_down(dest='pkg/morelorem.txt')


# Test: Illegal action
msg, contents = write_file(working_directory='calculator', 
                           file_path='/tmp/temp.txt', 
                           content='this should not be allowed')
assert 'ror: Cannot' in msg
assert 'this should not be allowed' in msg
assert None == contents



