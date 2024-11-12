import csv
import subprocess
import os


def load_config(config_path):
    # Читаем CSV с разделителем ";"
    with open(config_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # Читаем первую строку конфигурационного файла
        config = next(reader)
        # Удаляем лишние пробелы и кавычки
        return [item.strip().strip('"') for item in config]


def get_commit_dependencies(repo_path, branch_name):
    # Проверим, существует ли путь
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Репозиторий не найден по пути: {repo_path}")

    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "log", "--name-only", "--pretty=format:%H", branch_name],
        capture_output=True, text=True
    )
    return result.stdout.splitlines()


def generate_plantuml_graph(commit_data, output_puml_path):
    with open(output_puml_path, "w") as file:
        file.write("@startuml\n")
        prev_commit = None
        for line in commit_data:
            if line:
                if not line.startswith(" "):
                    commit = line
                    file.write(f'"{commit}"\n')
                    if prev_commit:
                        file.write(f'"{prev_commit}" --> "{commit}"\n')
                    prev_commit = commit
                else:
                    file.write(f'"{line.strip()}" --> "{commit}"\n')
        file.write("@enduml\n")


def visualize_graph(visualizer_path, puml_path, output_image_path):
    subprocess.run(['java', '-jar', visualizer_path, '-tpng', puml_path, "-o", output_image_path])


def main(config_path):
    # Загружаем конфигурацию из CSV
    visualizer_path, repo_path, output_image_path, branch_name = load_config(config_path)

    # Получаем данные коммитов
    commit_data = get_commit_dependencies(repo_path, branch_name)

    # Генерируем puml файл
    puml_path = "graph.puml"
    generate_plantuml_graph(commit_data, puml_path)

    # Визуализируем граф
    visualize_graph(visualizer_path, puml_path, output_image_path)

    print("Граф зависимостей успешно построен и сохранён!")


if __name__ == "__main__":
    main("config.csv")