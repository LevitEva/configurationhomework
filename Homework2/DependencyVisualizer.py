import os
import subprocess
import configparser

class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.repo_path = self.config['Paths']['repo_path']
        self.graphviz_path = self.config['Paths']['graphviz_path']
        self.output_path = self.config['Paths']['output_path']

    def _load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def get_commits(self):
        """Получение списка коммитов в хронологическом порядке"""
        os.chdir(self.repo_path)
        result = subprocess.run(
            ["git", "log", "--reverse", "--pretty=format:%H"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split('\n')
        return commits

    def generate_graph(self, commits):
        """Генерация файла .dot для визуализации графа"""
        dot_content = "digraph G {\n"
        for i in range(len(commits) - 1):
            dot_content += f'    "{commits[i]}" -> "{commits[i + 1]}";\n'
        dot_content += "}\n"

        dot_file = self.output_path.replace('.png', '.dot')
        with open(dot_file, 'w') as file:
            file.write(dot_content)
        return dot_file

    def visualize_graph(self, dot_file):
        """Создание изображения графа с помощью Graphviz"""
        subprocess.run(
            [self.graphviz_path, "-Tpng", dot_file, "-o", self.output_path],
            check=True
        )

    def run(self):
        commits = self.get_commits()
        dot_file = self.generate_graph(commits)
        self.visualize_graph(dot_file)
        print(f"Граф зависимостей успешно сохранён в {self.output_path}")


if __name__ == "__main__":
    config_path = "config.ini"
    visualizer = DependencyVisualizer(config_path)
    visualizer.run()
