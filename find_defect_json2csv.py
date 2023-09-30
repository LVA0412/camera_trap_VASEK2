
# Pillow-SIMD намного быстрее чем Pillow.
# Для ускорения работы можно удалить Pillow и установить Pillow-SIMD
# при этом изменять в коде ничего не надо!
# https://github.com/uploadcare/pillow-simd

import argparse
from PIL import Image as ImagePIL
import os
import cv2
import shutil
import numpy as np
import json
import csv

THRESHOLD_BLUR = 280
THRESHOLD_IDENTICAL_BYTES = 65000

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

def bad_color_areas(gray_image): #функция искать одноцветные области брака
    b=0
    n=np.array(gray_image)
    unique, counts = np.unique(np.ravel(gray_image), return_counts=True)

    for i in range(len(n[:,0])):
        if len(np.unique(np.array(n[i,:])))==1 :
            uno=np.unique(np.array(n[i,:]), return_counts=False)
            if uno!=0:
                if uno!=255:
                    b+=1

    #print(b)
    br=0
    if b>25:
        br=1

    elif len(np.array(unique))<7:
        br=1
    elif (max(np.array(counts))/len(np.ravel(gray_image)))>0.25:

        if np.mean(n)<240:
            br=0
            if np.mean(n)<70:
                br=0
            else: br=1

        else: br=1
        # print(max(np.array(counts))/len(n))
        #  br=1

    return br  

def koeff(gray_image):#соотношения белого, черного, серединки
    n=np.ravel(gray_image)
    av=np.mean(n)
    koef_bl=sum(n>240)/len(n)
    koef_wt=sum(n<10)/len(n)
    koef_av=(sum(n<(av+10))-sum(n<(av-10)))/len(n)
    return (av,koef_bl,koef_wt,koef_av)

def color_channel_bad(img): #ошибки в цветовых каналах
    r = img[:,:,0]
    g= img[:,:,1]
    b= img[:,:,2]
    rr=np.ravel(r)
    gr=np.ravel(g)
    br=np.ravel(b)
    #print(np.mean(rr),np.mean(br),np.mean(gr))
    if np.mean(rr)>2*np.mean(gr) or np.mean(rr)>2*sum(br):
        br=1
    elif np.mean(gr)>2*np.mean(rr) or np.mean(gr)>2*np.mean(br):
        br=1
    elif np.mean(br)>2*np.mean(gr) or np.mean(br)>2*np.mean(rr):
        br=1
    else:
        br=0
    return br


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def copy_file(full_filename, target_dir, sub_dir):
    full_dir = os.path.join(target_dir, sub_dir)
    os.makedirs(full_dir, exist_ok=True)
    shutil.copy2(full_filename, full_dir)

    
def processing_dataset(srcpath, targetpath, jsonpath):

    # TODO добавить проверку на существование уже таких целевых папок
    full_broken_dir = os.path.join(targetpath, BROKEN_DIR)
    full_empty_dir = os.path.join(targetpath, EMPTY_DIR)
    full_animal_dir = os.path.join(targetpath, ANIMAL_DIR)
    
    # Создаем директории для каждого класса
    os.makedirs(full_broken_dir, exist_ok=True)
    os.makedirs(full_empty_dir, exist_ok=True)
    os.makedirs(full_animal_dir, exist_ok=True)
     
     
    with open(jsonpath, 'r') as file:
        # Parse JSON data
        jsondata = json.load(file)     
     

    csv_data = []
    break_count = 10 # для отладки установить сколько строк обработать в json файле или -1 для всех

    for json_image in jsondata['images'] :
        if not break_count:
            break
        break_count -= 1   
        #path = root.split(os.sep)
        img_filename_json = json_image['file']
        # отделяем относительный путь от имени файла изображения
        path, file = os.path.split(img_filename_json)
        
        full_filename = os.path.join(srcpath, img_filename_json)

        print(full_filename)
        
        num_animals=0
        detections = json_image['detections']
        for i in range(len(detections)):
            kategoria=(detections[i]['category'])
            uverennost= (detections[i]['conf'])
            if int(kategoria) == 1 and float(uverennost)>0.7:
                num_animals += 1
                print("{}: {:.2f}".format("Обнаружены животные с уверенностью", uverennost))
            #i+=1
        
        if num_animals > 0:
            copy_file(full_filename, full_animal_dir, path) # копируем файл в директорию животных
            csv_data.append([img_filename_json,0,0,1])
            continue           
               
        
        
        try:
            # Техническая проверка возможности считывания файла и работы с ним библиотекой PIL
            test_PIL(full_filename)
        except:
            print("test_PIL: обнаружена ошибка в файле!")
            copy_file(full_filename, full_broken_dir, path) # копируем файл в директорию сломанных
            csv_data.append([img_filename_json,1,0,0])
        else: # если файл нормально считывается
            
            image = cv2.imdecode(np.fromfile(full_filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            #image = cv2.imread(full_filename)
            # TODO знась ОЧЕНЬ НУЖНО выловить сообщения об ошибке вида:
            # Corrupt JPEG data:
            # .imread() посылает их в поток сообщений, но не вызывает никаких ошибок и исключений!
            # это решит проблему с частично битыми изображениями, где остальные методы не сработали
            
            # Наиболее частая проблема в датасете - это размытые и засвеченные кадры
            # Проанализируем размытость изображения, для этого сперва преобразуем изображение в градации серого
            
            if len(image.shape) == 2: # проверка если изображение с одним каналом
                gray_image = image
            else: # если не делать проверку, то ч/б изображения вызывают ошибку здесь
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
                
            # сворачиваем изображение с помощью следующего ядра, размерностью 3х3
            # 0  1  0
            # 1 -4  1
            # 0  1  0
            # и вычислим дисперсию Лапласа, чем она меньше, тем более размытое изображение 
            # Оператор Лапласа выделяет области изображения, содержащие быстрые изменения интенсивности
            
            fm = variance_of_laplacian(gray_image)
            
            if fm < THRESHOLD_BLUR:
                text = "Blurry"
                print("{}: {:.2f}".format("Размытое изображение variance_of_laplacian", fm))
                
                copy_file(full_filename, full_broken_dir, path) # копируем файл в директорию сломанных
                csv_data.append([img_filename_json,1,0,0])
                continue
            else:
                text = "Not Blurry"

            # Проверим, файл на бинарном уровне на наличие длинных повторяющихся последовательностей (битый канал или однородный цвет) 
            
            number_identical_bytes = calc_number_identical_bytes(full_filename)
            if number_identical_bytes > THRESHOLD_IDENTICAL_BYTES: # если количество повторяющихся байт в файле больше заданного порога
                print("{}: {:d}".format("Вероятно поврежденный файл! calc_number_identical_bytes ", number_identical_bytes))
                copy_file(full_filename, full_broken_dir, path)# копируем файл в директорию сломанных
                csv_data.append([img_filename_json,1,0,0])
                continue
                
            
          
            
            # здесь идеи Кати
            br = 0
            av, koef_bl, koef_wt, koef_av = koeff(gray_image)
            if av <=10 or av>=240:
                br=1
            elif koef_bl>0.8 or koef_av>0.8 or koef_wt>0.8:
                br=1
            else :
                br = bad_color_areas(gray_image)

            if br == 0:
                br = color_channel_bad(image)
                
            if br:
                copy_file(full_filename, full_broken_dir, path) # копируем файл в директорию сломанных
                csv_data.append([img_filename_json,1,0,0])
                continue
            
            
            print("На изображении не обнаружено животных и нет дефектов. Помещаем в класс Empty.")
            copy_file(full_filename, full_empty_dir, path) # копируем файл в директорию пустых
            csv_data.append([img_filename_json,0,1,0])
                
            # cv2.putText(image, "{}: {:.2f}".format(text, fm), (30, 30),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # cv2.putText(image, "{}: {:.2f}".format("number_identical_bytes", number_identical_bytes), (30, 60),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            # #cv2.imshow("Image", image) # показать на экране
            # cv2.imwrite(os.path.join(targetpath, file), image)
            
    
    with open(os.path.join(targetpath, 'submission.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['filename','broken','empty','animal'])
        for s in csv_data:
            csv_writer.writerow(s)
    

    
        
    print("\nThe End")
    print("Press any key to continue")
    key = cv2.waitKey(0)    

def arg_parser():
    epilog_text = """
    Скрипт фильтрации изображений
    """

    parser = argparse.ArgumentParser(description='Определение дефектных фото', epilog=epilog_text)
    parser.add_argument('srcpath', metavar='SOURCE_PATH', type=str,
                        help='Путь к папке - источнику изображений')
    parser.add_argument('targetpath', metavar='TARGET_PATH', type=str,
                        help='Путь к целевой папке найденных (дефектных) изображений')
    parser.add_argument('json', metavar='JSON_PATH', type=str,
                        help='Путь к json файлу с результатами распознавания животных')                        
    parser.add_argument("-tb", "--threshold_blur", type=int, default=280,
                        help="Порог 'размытости' изображений (по умолчанию = 280)")
    parser.add_argument("-ni", "--threshold_identical_bytes", type=int, default=65000,
                        help="Порог 'размытости' изображений (по умолчанию = 65000)")                       
 
    return parser.parse_args()

def main():
    global ARG
    ARG = arg_parser()
    
    # TODO добавить проверку на версию Pillow
    print("Recommended installing Pillow-SIMD to speed up")
    
    processing_dataset(ARG.srcpath, ARG.targetpath, ARG.json)

    
if __name__ == "__main__":
    main()
