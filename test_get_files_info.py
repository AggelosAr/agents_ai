import unittest

from functions.get_files_info import DirInfo, PathItem, StatusCode

# # # TODO dest has dot inside e.g. pkg/./k

class TestGetFilesInfo(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(typeobj=PathItem, function=PathItem.__eq__)

    def test_success_current_dir(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory=".")
        (is_err, status_code, msg), _ = dir_info

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_IS, status_code)
        # TODO **5** maybe we want to show "calculator" instead of "." or vice versa?
        self.assertEqual(('\tSuccess: "calculator" is the working directory'), 
                         (msg))
        
    def test_error_normal(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="/bin")
        (is_err, status_code, msg), _ = dir_info

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "/bin" as it is outside the permitted working directory'), 
                         (msg))

    def test_error_double_dot(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="../")
        (is_err, status_code, msg), _ = dir_info

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (msg))
    
    def test_success_nested_file(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="main.py")
        (is_err, status_code, msg), _ = dir_info

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.NOT_A_DIR, status_code)
        self.assertEqual(('\tError: Cannot list "main.py" as it is not a dir'), 
                         (msg))
                          
    # ///////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////
    # ///// above tests, test the error logic
    # ///// below tests, test the return values and logic !!
    # ////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////

    def test_success_dot_current(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory=".")
        (_, _, msg), files = dir_info
        # TODO **5** maybe we want to show "calculator" instead of "." or vice versa?
        self.assertEqual(('\tSuccess: "calculator" is the working directory'), 
                         (msg))

        self.assertEqual(PathItem(abs_path="__init__.py", 
                                  size=0, 
                                  is_dir=False), 
                        files[0])
        self.assertEqual(PathItem(abs_path="main.py", 
                                  size=741, 
                                  is_dir=False), 
                        files[1])
        self.assertEqual(PathItem(abs_path="tests.py", 
                                  size=1354, 
                                  is_dir=False), 
                        files[2])
        self.assertEqual(PathItem(abs_path="pkg", 
                                  size=4096, 
                                  is_dir=True), 
                        files[3])        
    
    def test_success_nest(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="pkg")
        (is_err, status_code, msg), files = dir_info

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg" is within the working directory'), 
                         (msg))

        self.assertEqual(PathItem(abs_path="__init__.py", 
                                  size=0, 
                                  is_dir=False), 
                        files[0])
        self.assertEqual(PathItem(abs_path="render.py", 
                                  size=403, 
                                  is_dir=False), 
                        files[1])
        self.assertEqual(PathItem(abs_path="calculator.py", 
                                  size=1753, 
                                  is_dir=False), 
                        files[2])   
        self.assertEqual(PathItem(abs_path="__pycache__", 
                                  size=4096, 
                                  is_dir=True), 
                        files[3])             

    def test_success_nest_nest_same_name(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="pkg/pkg")
        (is_err, status_code, msg), _ = dir_info

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg/pkg" is within the working directory'), 
                         (msg))

    # TODO maybe we want to apply formatting to the resulting string?
    def test_success_nest_nest_same_name(self):

        dir_info = DirInfo(working_directory="calculator", dest_directory="/calculator")
        (is_err, status_code, msg), _ = dir_info
        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)

        dir_info = DirInfo(working_directory="calculator", dest_directory="calculator/")
        (is_err, status_code, msg), _ = dir_info
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/" is within the working directory'), 
                         (msg))
        
        dir_info = DirInfo(working_directory="calculator/", dest_directory="calculator")
        (is_err, status_code, msg), _ = dir_info
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator" is within the working directory'), 
                         (msg))
        
        dir_info = DirInfo(working_directory="calculator/", 
                           dest_directory="calculator/calculator/")
        (is_err, status_code, msg), _ = dir_info
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/calculator/" is within the working directory'), 
                         (msg))
        
        dir_info = DirInfo(working_directory="calculator/", 
                           dest_directory="calculator/calculator/calculator/")
        (is_err, status_code, msg), _ = dir_info
        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "calculator/calculator/calculator/" is within the working directory'), 
                         (msg))
        
    # TODO add a test to list files of deeply nested dir
    def test_success_nest_nest(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="pkg/new")
        (is_err, status_code, msg), files = dir_info

        self.assertEqual(False, is_err)
        self.assertEqual(StatusCode.SUCCESS_DIR_WITHIN, status_code)
        self.assertEqual(('\tSuccess: "pkg/new" is within the working directory'), 
                         (msg))

    def test_error_one(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="/bin")
        (is_err, status_code, _), files = dir_info

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual([], files)
        
    def test_error_two(self):
        dir_info = DirInfo(working_directory="calculator", dest_directory="../")
        (is_err, status_code, msg), files = dir_info

        self.assertEqual(True, is_err)
        self.assertEqual(StatusCode.OUTSIDE, status_code)
        self.assertEqual(('\tError: Cannot list "../" as it is outside the permitted working directory'), 
                         (msg))
        self.assertEqual([], files)


if __name__ == '__main__':

    unittest.main()
