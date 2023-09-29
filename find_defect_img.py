# TODO отделить только картинки, т.к. могут быть другие файлы
# TODO разобраться почему не работают пути с пробелами и русскими буквами!



# Pillow-SIMD намного быстрее чем Pillow.
# Для ускорения работы можно удалить Pillow и установить Pillow-SIMD
# при этом изменять в коде ничего не надо!
# https://github.com/uploadcare/pillow-simd

import argparse
from PIL import Image as ImagePIL
import os
import cv2
import shutil

BROKEN_DIR = "broken"
EMPTY_DIR = "empty"
ANIMAL_DIR = "animal"

def check_file_size(filename):
    filesize = os.stat(filename).st_size
    if os.stat(filename).st_size:
        raise SyntaxError("Zero size file")
    return filesize

def test_PIL(filename):
    img = ImagePIL.open(filename)
    img.verify()  # используем для проверки встроенную ф-ю verify()
    img.close()

    img = ImagePIL.open(filename)  
    img.transpose(ImagePIL.FLIP_LEFT_RIGHT) # делаем преобразование изображение. Выдает ошибку если есть некоторые дефекты в файле
    img.close()
    
def calc_number_identical_bytes(filename):
    f = open(filename, "rb")
    bin_data = f.read()
    f.close()
    n = 1
    maxnum = 0
    prev = None
    
    for i in bin_data:
        if prev == i:
            n += 1
        else:
            if n > maxnum:
                maxnum = n
            
            n = 1
            prev = i
    if n > maxnum:
        maxnum = n

    return maxnum

  

def arg_parser():
    epilog_text = """
    Детальное описание параметров
    здесь
    """

    parser = argparse.ArgumentParser(description='Определение дефектных фото', epilog=epilog_text)
    parser.add_argument('srcpath', metavar='SOURCE_PATH', type=str,
                        help='Путь к папке - источнику изображений')
    parser.add_argument('targetpath', metavar='TARGET_PATH', type=str,
                        help='Путь к целевой папке найденных (дефектных) изображений')
    parser.add_argument("-tb", "--threshold_blur", type=int, default=280,
                        help="Порог 'размытости' изображений (по умолчанию = 280)")
    parser.add_argument("-ni", "--threshold_identical_bytes", type=int, default=65000,
                        help="Порог 'размытости' изображений (по умолчанию = 65000)")                       
 
    return parser.parse_args()

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def main():
    global ARG

    ARG = arg_parser()
    
    # TODO добавить проверку на версию Pillow
    print("Recommended installing Pillow-SIMD to speed up")

    # TODO добавить проверку на существование уже таких целевых папок
    full_broken_dir = os.path.join(ARG.targetpath, BROKEN_DIR)
    full_empty_dir = os.path.join(ARG.targetpath, EMPTY_DIR)
    full_animal_dir = os.path.join(ARG.targetpath, ANIMAL_DIR)
    
    # Создаем директории для каждого класса
    os.makedirs(full_broken_dir, exist_ok=True)
    os.makedirs(full_empty_dir, exist_ok=True)
    os.makedirs(full_animal_dir, exist_ok=True)
     

#     pathlist = Path(ARG.srcpath).rglob('*.*')
#     for path in pathlist:
#          path_in_str = str(path)
#          print(path_in_str)
   

    # TEST проверить обрабатывает ли подкаталоги?
    for root, dirs, files in os.walk(ARG.srcpath):
        path = root.split(os.sep)
        print((len(path) - 1) * '--', os.path.basename(root))
        for file in files:
            #print(len(path) * '--', file) 
            full_filename = os.path.join(root, file)
            print(full_filename)
            try:
                test_PIL(full_filename)
            except:
                print("test_PIL: обнаружена ошибка в файле!")
                shutil.copy(full_filename, os.path.join(full_broken_dir, file)) # копируем файл в директорию сломанных
            else: # если не было ошибок
                
                number_identical_bytes = calc_number_identical_bytes(full_filename)
                if number_identical_bytes > ARG.threshold_identical_bytes: # если количество повторяющихся байт в файле больше заданного порога
                    print("{}: {:d}".format("Вероятно поврежденный файл! calc_number_identical_bytes ", number_identical_bytes))
                    shutil.copy(full_filename, os.path.join(full_broken_dir, file)) # копируем файл в директорию сломанных
                    continue
                    
                # TODO перенести в отдельную ф-ю
                image = cv2.imread(full_filename)
                # TODO знась ОЧЕНЬ НУЖНО выловить сообщения об ошибке вида:
                # Corrupt JPEG data:
                # .imread() посылает их в поток сообщений, но не вызывает никаких ошибок и исключений!
                # это решит проблему с частично битыми изображениями, где остальные методы не сработали
                
                if len(image.shape) == 2: # значит изображение черно-белое
                    gray = image
                else: # если не делать проверку, то ч/б изображения вызывают ошибку здесь
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                fm = variance_of_laplacian(gray)
                
                if fm < ARG.threshold_blur:
                    text = "Blurry"
                    shutil.copy(full_filename, os.path.join(full_broken_dir, file)) # копируем файл в директорию сломанных
                    continue
                else:
                    text = "Not Blurry"
                    print("Файл прошел проверки без замечаний")
                    
                cv2.putText(image, "{}: {:.2f}".format(text, fm), (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                cv2.putText(image, "{}: {:.2f}".format("number_identical_bytes", number_identical_bytes), (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                #cv2.imshow("Image", image) # показать на экране
                cv2.imwrite(os.path.join(ARG.targetpath, file), image)
    

    
        
    print("\nThe End")
    print("Press any key to continue")
    key = cv2.waitKey(0)    
           
if __name__ == "__main__":
    main()
