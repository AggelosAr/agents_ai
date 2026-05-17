from functions.get_files_info import DirInfo, Item
import unittest


format_string = lambda x: '\n'.join(l.strip() for l in x.split('\n')) 


class TestGetFilesInfo(unittest.TestCase):

    # def setUp(self):
    #     self.addTypeEqualityFunc(typeobj=Item, function=Item.__eq__)

    def test_success_current_dir(self):
        (is_err, result_code), _ = DirInfo.get_files_info(working_directory="calculator", dest_directory=".")

        self.assertEqual(is_err, False)
        self.assertEqual(('\tSuccess: "calculator" is within the working directory'), 
                         (result_code))
        
    def test_error_normal(self):
        (is_err, result_code), _ = DirInfo.get_files_info(working_directory="calculator", dest_directory="/bin")

        self.assertEqual(is_err, True)
        self.assertEqual(('\tError: Cannot list "/bin" as it is outside the permitted working directory'), 
                         (result_code))

    def test_error_double_dot(self):
        (is_err, result_code), _ = DirInfo.get_files_info(working_directory="calculator", dest_directory="../")
        
        self.assertEqual(is_err, True)
        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (result_code))
    
    # TODO update
    # def test_success_nested_file(self):
    #     result_code, _ = DirInfo.get_files_info(working_directory="calculator", dest_directory="main.py")

    #     self.assertEqual(('\tError: "main.py" is not a directory'), 
    #                      (result_code))
    
    #///////////////////////////////////////////////////////////
    #//////////////////////////////////////////////////////////
    #///// above tests, test the error logic
    #///// below tests, test the return values and logic !!
    #////////////////////////////////////////////////////////
    #///////////////////////////////////////////////////////

    def test_success_dot_current(self):
        (_, result_code), result = DirInfo.get_files_info(working_directory="calculator", dest_directory=".")

        self.assertEqual(('\tSuccess: "calculator" is within the working directory'), 
                         (result_code))

        self.assertEqual(Item(abs_path="__init__.py", 
                              size=0, 
                              is_dir=False), 
                        result[0])
        self.assertEqual(Item(abs_path="main.py", 
                              size=741, 
                              is_dir=False), 
                        result[1])
        self.assertEqual(Item(abs_path="tests.py", 
                              size=1354, 
                              is_dir=False), 
                        result[2])
        self.assertEqual(Item(abs_path="pkg", 
                              size=4096, 
                              is_dir=True), 
                        result[3])        
    
    def test_success_nest(self):
        (_, result_code), result = DirInfo.get_files_info(working_directory="calculator", dest_directory="pkg")

        self.assertEqual(('\tSuccess: "pkg" is within the working directory'), 
                         (result_code))

        self.assertEqual(Item(abs_path="__init__.py", 
                              size=0, 
                              is_dir=False), 
                        result[0])
        self.assertEqual(Item(abs_path="render.py", 
                              size=403, 
                              is_dir=False), 
                        result[1])
        self.assertEqual(Item(abs_path="calculator.py", 
                              size=1753, 
                              is_dir=False), 
                        result[2])   
        self.assertEqual(Item(abs_path="__pycache__", 
                              size=4096, 
                              is_dir=True), 
                        result[3])                      

    def test_error_one(self):
        (_, _), result = DirInfo.get_files_info(working_directory="calculator", dest_directory="/bin")
        self.assertEqual([], result)
        
    def test_error_two(self):
        (_, result_code), result = DirInfo.get_files_info(working_directory="calculator", dest_directory="../")

        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (result_code))
        self.assertEqual([], 
                         result)

if __name__ == '__main__':

    # print()
    # print()
    # result_code, result = DirInfo.get_files_info(working_directory="calculator", dest_directory=".")
    # print(result)
    # print(result_code)
    # print()
    # print('--------------------------------------')

    # result_code, result = DirInfo.get_files_info(working_directory="calculator", dest_directory="pkg")
    # print(result)
    # print(result_code)
    # print()
    # print('--------------------------------------')

    # result_code, result = DirInfo.get_files_info(working_directory="calculator", dest_directory="/bin")
    # print(result)
    # print(result_code)
    # print()
    # print('--------------------------------------')

    # result_code, result = DirInfo.get_files_info(working_directory="calculator", dest_directory="../")
    # print(result)
    # print(result_code)
    # print()
    # print('--------------------------------------')

    unittest.main()
