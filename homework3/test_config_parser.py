import unittest
import subprocess
import os
import yaml


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        """Thiết lập các file test trước mỗi bài kiểm tra"""
        self.input_file = "test_input.txt"
        self.output_file = "test_output.yaml"
        
        # Dữ liệu đầu vào cho file test
        self.sample_data = """
        ; Đây là comment dòng đơn
        global CONSTANT 42
        struct {
            field1 [CONSTANT],
            field2 100
        }
        """
        
        with open(self.input_file, "w") as f:
            f.write(self.sample_data)

    def tearDown(self):
        """Xóa các file test sau khi kiểm tra"""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_output_file_creation(self):
        """Kiểm tra xem file đầu ra có được tạo không"""
        subprocess.run(["python3", "config_parser.py", self.input_file, self.output_file], check=True)
        self.assertTrue(os.path.exists(self.output_file), "File đầu ra không được tạo")

    def test_output_content(self):
        """Kiểm tra nội dung file đầu ra có đúng không"""
        subprocess.run(["python3", "config_parser.py", self.input_file, self.output_file], check=True)
        
        with open(self.output_file, "r") as f:
            output_data = yaml.safe_load(f)
        
        expected_data = {
            "field1": 42,
            "field2": 100
        }
        self.assertEqual(output_data, expected_data, "Nội dung file YAML không khớp với mong đợi")

    def test_invalid_input(self):
        """Kiểm tra xử lý đầu vào không hợp lệ"""
        invalid_data = """
        struct {
            field1 [VALUE]
        """
        with open(self.input_file, "w") as f:
            f.write(invalid_data)

        result = subprocess.run(["python3", "config_parser.py", self.input_file, self.output_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        self.assertNotEqual(result.returncode, 0, "Chương trình không xử lý đúng lỗi")
        self.assertIn("Error", result.stderr.decode(), "Thông báo lỗi không được hiển thị đúng cách")

if __name__ == "__main__":
    unittest.main()
