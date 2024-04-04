import os
import configparser
from datetime import datetime
import shutil
import sys

class FileManager:
    def __init__(self, config_file="settings.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        working_directory = self.config.get("FileManager", "working_directory")
        if not os.path.exists(working_directory):
            print(f"Ошибка: рабочий каталог '{working_directory}' не существует.")
            exit(1)

        self.working_directory = working_directory
        self.current_directory = self.working_directory       
           
    def list_files(self):
        print("Файлы и директории в текущей директории:")
        print(f"{'Имя':<25} {'Размер':<10} {'Изменено'}")
        for item in os.listdir(self.current_directory):
            item_path = os.path.join(self.current_directory, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else "-"
            modified_time = datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{item:<25} {size:<10} {modified_time}")
    
    def show_error(self, message):
        print(f"****** Ошибка: {message} ******")
        
    def is_valid_path(self, path):
        full_path = os.path.join(self.current_directory, path)
        return os.path.abspath(full_path).startswith(os.path.abspath(self.working_directory))
    
    def show_help(self):
        print("Доступные команды:")
        print(f"{'create_dir <directory_name>':40} - Создать директорию")
        print(f"{'delete_dir <directory_name>':40} - Удалить директорию")
        print(f"{'cd <directory_name>':40} - Перейти в директорию")
        print(f"{'create_file <file_name>':40} - Создать файл")
        print(f"{'write_to_file <file_name>':40} - Записать в файл")
        print(f"{'read_file <file_name>':40} - Прочитать файл")
        print(f"{'delete_file <file_name>':40} - Удалить файл")
        print(f"{'copy_file <source> <destination>':40} - Копировать файл")
        print(f"{'move_file <source> <destination>':40} - Переместить файл")
        print(f"{'rename_file <source> <new_name>':40} - Переименовать файл")
        print(f"{'exit':40} - Выйти")

    def clear_screen(self):
        if os.name == 'nt':  # для Windows
            os.system('cls')
        else:  # для UNIX-систем
            os.system('clear')
            
    def get_relative_path(self, path):
        relative_path = os.path.relpath(path, self.working_directory)
        return relative_path if relative_path.startswith(os.sep) else os.sep + relative_path
    
    def create_directory(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.is_valid_path(directory_name):
            self.show_error("Невозможно создать директорию за пределами рабочей папки.")
        elif os.path.exists(full_path):
            self.show_error("Директория уже существует.")
        else:
            os.mkdir(full_path)
            print("Директория успешно создана.")

    def delete_directory(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.is_valid_path(directory_name):
            self.show_error("Невозможно удалить директорию за пределами рабочей папки.")
        elif not os.path.exists(full_path):
            self.show_error("Директория не существует.")
        elif not os.path.isdir(full_path):
            self.show_error("Указан не директория.")
        else:
            shutil.rmtree(full_path)
            print("Директория успешно удалена вместе с ее содержимым.")
            
    def change_directory(self, directory_name):
        full_path = os.path.join(self.current_directory, directory_name)
        if not self.is_valid_path(directory_name):
            self.show_error("Невозможно перейти в директорию за пределами рабочей папки.")
        elif not os.path.exists(full_path):
            self.show_error("Директория не существует.")
        elif not os.path.isdir(full_path):
            self.show_error("Указана не директория.")
        else:
            self.current_directory = full_path
            
    def create_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.is_valid_path(file_name):
            self.show_error("Невозможно создать файл за пределами рабочей папки.")
        elif os.path.exists(full_path):
            self.show_error("Файл уже существует.")
        else:
            open(full_path, 'a', encoding='utf-8').close()
            print("Файл успешно создан.")
            
    def delete_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.is_valid_path(file_name):
            self.show_error("Невозможно удалить файл за пределами рабочей папки.")
        elif not os.path.exists(full_path):
            self.show_error("Файл не существует.")
        elif os.path.isdir(full_path):
            self.show_error("Указан не файл.")
        else:
            os.remove(full_path)
            print("Файл успешно удален.")
            
    def write_to_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.is_valid_path(file_name):
            self.show_error("Невозможно записать в файл за пределами рабочей папки.")
        elif not os.path.exists(full_path):
            self.show_error("Файл не существует. Создайте файл перед записью.")
        elif os.path.isdir(full_path):
            self.show_error("Указан не файл.")
        else:
            print("Введите текст для добавления в файл. Завершите ввод с помощью Ctrl+D (в UNIX-системах) или Ctrl+Z (в Windows).")
            text = sys.stdin.read()
            with open(full_path, 'a', encoding='utf-8') as file:
                file.write(text)
            print("Текст успешно добавлен в файл.")

    def read_file(self, file_name):
        full_path = os.path.join(self.current_directory, file_name)
        if not self.is_valid_path(file_name):
            self.show_error("Невозможно прочитать файл за пределами рабочей папки.")
        elif not os.path.exists(full_path):
            self.show_error("Файл не существует.")
        elif os.path.isdir(full_path):
            self.show_error("Указан не файл.")
        else:
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print("Содержимое файла:")
            print(content)
            
    def copy_file(self, source_file_name, destination_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, destination_file_name)

        if not self.is_valid_path(source_file_name):
            self.show_error("Невозможно копировать файл за пределами рабочей папки.")
        elif not os.path.exists(source_full_path):
            self.show_error("Исходный файл не существует.")
        elif os.path.isdir(source_full_path):
            self.show_error("Указан не файл.")
        elif not self.is_valid_path(destination_file_name):
            self.show_error("Невозможно копировать файл за пределами рабочей папки.")
        elif os.path.exists(destination_full_path):
            self.show_error("Файл с таким именем уже существует.")
        else:
            shutil.copy(source_full_path, destination_full_path)
            print("Файл успешно скопирован.")

    def move_file(self, source_file_name, destination_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, destination_file_name)

        if not self.is_valid_path(source_file_name):
            self.show_error("Невозможно переместить файл за пределами рабочей папки.")
        elif not os.path.exists(source_full_path):
            self.show_error("Исходный файл не существует.")
        elif os.path.isdir(source_full_path):
            self.show_error("Указан не файл.")
        elif not self.is_valid_path(destination_file_name):
            self.show_error("Невозможно переместить файл за пределами рабочей папки.")
        elif os.path.exists(destination_full_path):
            self.show_error("Файл с таким именем уже существует.")
        else:
            shutil.move(source_full_path, destination_full_path)
            print("Файл успешно перемещен.")
            
    def rename_file(self, source_file_name, new_file_name):
        source_full_path = os.path.join(self.current_directory, source_file_name)
        destination_full_path = os.path.join(self.current_directory, new_file_name)

        if not self.is_valid_path(source_file_name):
            self.show_error("Невозможно переименовать файл за пределами рабочей папки.")
        elif not os.path.exists(source_full_path):
            self.show_error("Исходный файл не существует.")
        elif os.path.isdir(source_full_path):
            self.show_error("Указан не файл.")
        elif not self.is_valid_path(new_file_name):
            self.show_error("Невозможно переименовать файл за пределами рабочей папки.")
        elif os.path.exists(destination_full_path):
            self.show_error("Файл с таким именем уже существует.")
        else:
            os.rename(source_full_path, destination_full_path)
            print("Файл успешно переименован.")

    def run(self):
        while True:
            relative_current_directory = self.get_relative_path(self.current_directory)
            print(f"Текущая директория: {relative_current_directory}")
            print("-------------------------------")
            self.list_files()
            print("-------------------------------")
            self.show_help()
            command = input("Введите команду: ").split()

            if len(command) == 0:
                continue

            command_name = command[0]
            command_args = command[1:]
            
            self.clear_screen()
            print("===============================")

            if command_name == "exit":
                break
            elif command_name == "create_dir":
                directory_name = command_args[0]
                self.create_directory(directory_name)
            elif command_name == "delete_dir":
                directory_name = command_args[0]
                self.delete_directory(directory_name)
            elif command_name == "cd":
                directory_name = command_args[0]
                self.change_directory(directory_name)
            elif command_name == "create_file":
                file_name = command_args[0]
                self.create_file(file_name)
            elif command_name == "delete_file":
                file_name = command_args[0]
                self.delete_file(file_name)
            elif command_name == "write_to_file":
                file_name = command_args[0]
                self.write_to_file(file_name)
            elif command_name == "read_file":
                file_name = command_args[0]
                self.read_file(file_name)
            elif command_name == "copy_file" :
                source, destination = command_args
                self.copy_file(source, destination)
            elif command_name == "move_file":
                source, destination = command_args
                self.move_file(source, destination)
            elif command_name == "rename_file":
                source, new_name = command_args
                self.rename_file(source, new_name)
            else:
                self.show_error("Неверная команда. Пожалуйста, введите команду еще раз.")


if __name__ == "__main__":
    manager = FileManager()
    manager.run()
