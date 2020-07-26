#!/usr/bin/env python3
import getpass
from watchdog.observers import Observer
import os
import time
from watchdog.events import FileSystemEventHandler


# Создаем класс наследник, через него может отслеживать изменения в папках
class Handler(FileSystemEventHandler):
    """
    Сортирует файлы по расширениям
    """
    # При любых изменениях в папке
    def on_modified(self, event):
        for filename in os.listdir(folder_track):
            extension = filename.split(".")[-1].lower()

            # если это не папка, а файл
            if os.path.isfile(folder_track + filename):
                print(filename)

                if (extension == 'jpg' or
                        extension == 'png' or
                        extension == 'svg'):
                    file = folder_track + filename
                    new_path = f'{folder_delivery}Pictures/{filename}'
                    os.rename(file, new_path)

                elif (extension == 'mp4' or
                        extension == 'mpg' or
                        extension == 'flv'):
                    file = folder_track + filename
                    new_path = f'{folder_delivery}Videos/{filename}'
                    os.rename(file, new_path)

                elif (extension == 'pdf' or
                        extension == 'docs' or
                        extension == 'txt'):
                    file = folder_track + filename
                    new_path = f'{folder_delivery}Documents/{filename}'
                    os.rename(file, new_path)

                elif "." in filename:
                    file = folder_track + filename
                    new_folder = f'{folder_track}{extension}_folder/'  # для создания папки
                    try:
                        os.makedirs(new_folder)
                    except FileExistsError:
                        pass
                    finally:
                        new_path = new_folder + filename  # новое полное имя
                        os.rename(file, new_path)

                else:
                    file = folder_track + filename
                    new_folder = f'{folder_track}Without_dot_folder/'
                    try:
                        os.makedirs(new_folder)
                    except FileExistsError:
                        print('# Потерял файл из виду')
                    finally:
                        try:
                            new_path = new_folder + filename
                            os.rename(file, new_path)
                        except OSError:
                            print('# Пытался переместить папку саму в себя')
            else:
                pass
                # print(filename + '/')
                # многократное прохождение, отключено

    def pictures(self, filename, extension):
        pass


reset = '\033[0m'
blue = '\033[0;34m'

user = getpass.getuser()

folder_track = rf'/home/{user}/Sort_Folder/'
folder_delivery = rf'/home/{user}/'


def main():
    handle = Handler()
    observer = Observer()
    observer.schedule(handle, folder_track, recursive=False)
    # recursive=True для подпапок
    observer.start()
    try:
        print(f'{blue}Отслеживание папки "{folder_track}" назначено{reset}\n'
              f'\t{blue}Остановить - Ctrl + C{reset}')
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        # Ctrl + C
        print(f'\n{blue}Отслеживание папки "{folder_track}" остановлено{reset}')
        observer.stop()
        observer.join()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
