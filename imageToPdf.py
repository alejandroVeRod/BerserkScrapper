from PIL import Image
import glob
import os
import sys
import re



def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def toPDF(img_list, path):
    img_list[0].save(path,save_all=True, append_images=img_list)

def read_images(path):
    img_list = []
    images = sorted_alphanumeric(os.listdir(path))
    for i in images:
        image_path = os.path.join(path,i)
        if image_path.endswith(".jpg"):
            image = Image.open(image_path)
            #im = image.convert('RGB')
            img_list.append(image)
    return img_list

def read_folders(path):
    paths = []
    for d in os.listdir(path):
        folder_path = os.path.join(path,d)
        paths.append(folder_path)
    return paths

def convert_images_to_pdf(path):
    images = read_images(path)
    path_splitted = path.split("\\")
    chapter_name = path_splitted[len(path_splitted) - 1]
    pdf_path = os.path.join(path,chapter_name + ".pdf")
    try:
        images[0].save(pdf_path, save_all = True, append_images = images)
        print(f'Saved pdf file {pdf_path}\n')
    except Exception as e:
        print(f'ERROR Could not save {pdf_path} file {e}\n')


def main():
    EXIT = False
    if len(sys.argv) >= 2:
        for i in range(1,len(sys.argv)):
            path = sys.argv[i]
            convert_images_to_pdf(path)
    else:
        while(EXIT == False):
            print("Insert a path with images to transform into a .pdf\nInsert 'q' to exit the program\n")
            path = input()
            if(path != 'q'):
                if not os.path.exists(path):
                    print(f"ERROR Insert a valid path\n")
                else:
                    convert_images_to_pdf(path)
            else:
                EXIT = True    
            
if __name__ == "__main__":
    main()