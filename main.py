import csv
import subprocess
import os
import re
from collections import defaultdict


def load_config(config_path):
    with open(config_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        config = next(reader)
        return {
            "visualizer_path": config['visualizer_path'].strip().strip('"'),
            "repo_path": config['repo_path'].strip().strip('"'),
            "output_image_path": config['output_image_path'].strip().strip('"'),
            "branch_name": config['branch_name'].strip().strip('"')
        }


def get_commit_dependencies(repo_path, branch_name):
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Репозиторий не найден по пути: {repo_path}")

    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "log", "--name-only", "--pretty=format:%H", branch_name],
        capture_output=True, text=True
    )

    commits = {}
    file_commit_count = defaultdict(int)
    current_commit = None
    for line in result.stdout.splitlines():
        if re.match(r'^[a-f0-9]{40}$', line):  # Идентификатор коммита
            current_commit = line
            commits[current_commit] = []
        elif current_commit:
            if line.strip():  # Добавляем только непустые строки
                commits[current_commit].append(line)
                file_commit_count[line] += 1

    # Фильтруем файлы, которые появляются более одного раза
    filtered_commits = {
        commit: [f for f in files if file_commit_count[f] > 1]
        for commit, files in commits.items()
    }

    return filtered_commits


def generate_plantuml_graph(commit_data, output_puml_path):
    print("Генерация .puml файла с коммитами и файлами...")

    with open(output_puml_path, "w") as file:
        file.write("@startuml\n")
        file.write("skinparam linetype ortho\n")
        file.write("top to bottom direction\n")  # Задаем направление сверху вниз

        previous_commit = None
        for commit, files in commit_data.items():
            # Игнорируем коммиты с пустыми файлами после фильтрации
            if not files:
                continue
            commit_node = f"commit_{commit[:7]}"
            file.write(f'entity "{commit_node}" as {commit_node}\n')

            # Добавляем связь между текущим и предыдущим коммитом
            if previous_commit:
                file.write(f"{previous_commit} --> {commit_node}\n")

            # Обработка файлов и их директорий
            for file_path in files:
                parts = file_path.split('/')
                parent = commit_node  # Связываем с текущим коммитом
                full_path = ""

                for part in parts:
                    full_path = f"{full_path}/{part}".lstrip('/')
                    node_id = full_path.replace("/", "_").replace(".", "_")
                    file.write(f'entity "{full_path}" as {node_id}\n')
                    file.write(f"{parent} --> {node_id}\n")
                    parent = node_id  # Следующий уровень связывается с текущей директорией

            previous_commit = commit_node  # Обновляем предыдущий коммит

        file.write("@enduml\n")

    print(f"Файл .puml успешно создан: {output_puml_path}")



def render_plantuml(visualizer_path, puml_file_path, output_image_dir):
    print("Рендеринг .puml файла в изображение...")
    subprocess.run(["java", "-jar", visualizer_path, puml_file_path, "-o", output_image_dir], check=True)
    print(f"Изображение сохранено в {output_image_dir}")


def visualize_dependencies(config_path):
    config = load_config(config_path)
    commit_data = get_commit_dependencies(config['repo_path'], config['branch_name'])

    output_image_dir = os.path.dirname(config['output_image_path'])
    output_puml_path = os.path.join(output_image_dir, "graph.puml")

    generate_plantuml_graph(commit_data, output_puml_path)

    # Печать содержимого .puml файла для отладки
    with open(output_puml_path, "r") as file:
        print("Содержимое .puml файла:\n", file.read())

    render_plantuml(config['visualizer_path'], output_puml_path, output_image_dir)
    print(f"Граф успешно визуализирован и сохранен в {config['output_image_path']}")


if __name__ == "__main__":
    visualize_dependencies('config.csv')
