import unittest
from unittest.mock import patch, MagicMock
import DependencyVisualizer
import os

class TestDependencyVisualizer(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_commits(self, mock_run):
        mock_run.return_value.stdout = "abc123\ndef456\nghi789\n"
        visualizer = DependencyVisualizer.DependencyVisualizer("config.ini")
        commits = visualizer.get_commits()
        self.assertEqual(commits, ["abc123", "def456", "ghi789"])

    def test_generate_graph(self):
        visualizer = DependencyVisualizer.DependencyVisualizer("config.ini")
        commits = ["abc123", "def456", "ghi789"]
        dot_file = visualizer.generate_graph(commits)
        self.assertTrue(os.path.exists(dot_file))
        with open(dot_file, 'r') as file:
            content = file.read()
        self.assertIn('"abc123" -> "def456";', content)
        self.assertIn('"def456" -> "ghi789";', content)

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_run):
        visualizer = DependencyVisualizer.DependencyVisualizer("config.ini")
        dot_file = "/tmp/test.dot"
        with open(dot_file, 'w') as file:
            file.write("digraph G {}")
        visualizer.visualize_graph(dot_file)
        mock_run.assert_called_once_with(
            [visualizer.graphviz_path, "-Tpng", dot_file, "-o", visualizer.output_path],
            check=True
        )


if __name__ == "__main__":
    unittest.main()
