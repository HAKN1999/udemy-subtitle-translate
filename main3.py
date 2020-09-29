from googletrans import Translator
from termcolor import colored
import subprocess
import os


ts = Translator()

CHECK = "\u2713"
START = "*"
RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"

FOLDER_NAME = "subtitle_translate"


def cari_seluruh_file_srt(base_path):
    """mencari file srt di lokasi yg ditentukan"""

    # list dir
    list_dir = os.listdir(base_path)

    # masuk ketiap folder dan cari file srt
    for i in range(0, len(list_dir)):
        os.chdir(base_path+"/"+list_dir[i])
        current_dir = os.getcwd()
        # print lokasi dir yg sedang aktif
        warna(START, "{}".format(current_dir), RED)

        # membuat folder backup file srt original
        membuat_folder_backup_subtitle(current_dir)

        # mencari semua file srt di
        for path, dirs, files in os.walk(current_dir):
            # print(files)

            # filter srt file saja
            for nfile in files:
                if nfile.endswith(".srt"):

                    # absolute path
                    path_file = os.path.join(current_dir, nfile)
                    # print(path_file)
                    dest_folder = os.path.join(current_dir, FOLDER_NAME)
                    # print(dest_folder)

                    # bagian terjemahkan file
                    # terjemahkan_file(current_dir+nfile)
                    datas = terjemahkan_file(path_file)

                    # setelah file berhasil di terjemahkan
                    # pindahkan file ke folder backup
                    pindahkan_file_srt_ori(path_file, dest_folder)

                    # setelah file berhasil di pindahkan tulis
                    # terjemahkan file dengan nama file yg sama
                    warna(START, "Mencoba menyimpan hasil terjemahan", GREEN)
                    for x in range(0, len(datas)):
                        # print(datas[x])
                        tulis_hasil_translate(path_file, datas[x])

                    warna(CHECK, "File hasil terjemahan berhasil disimpan", GREEN)


def tulis_hasil_translate(path_file, data):
    """Menulis terjemahan ke file"""

    with open("{path}".format(path=path_file), 'a') as f:
        f.write(data + '\n')


def terjemahkan_file(path):
    """terjemahkan file srt"""

    # hasil dari terjemahan akan di simpan di list
    translate_file = []

    warna(START, "Sedang menterjemahkan file: {path}".format(path=path), BLUE)

    with open("{path}".format(path=path), 'r') as read_file:
        for i, name in enumerate(read_file.readlines()):
            translate_file.append(ts.translate(name.strip(), dest="id").text)

    warna(CHECK, "Berhasil di terjemahkan: {path}".format(path=path), BLUE)

    return translate_file


def membuat_folder_backup_subtitle(path):
    """membuat folder backup setelah file srt di terjemahkan"""

    try:
        warna(START, "Membuat folder backup", GREEN)
        os.makedirs(r"{path}/{folder}".format(path=path, folder=FOLDER_NAME))
    except Exception as e:
        warna(CHECK, "Folder backup telah dibuat", GREEN)


def pindahkan_file_srt_ori(path, dest_path):
    """setelah file berhasil diterjemahkan pindah kan file original subtittles ke folder backup"""

    warna(START, "Mencoba memindahkan file srt dari {path}".format(
        path=path), YELLOW)

    os.system("mv '{source_path}' '{dest_path}'".format(
        source_path=path, dest_path=dest_path))

    warna(CHECK, "File telah berhasil di pindahkan ke folder backup {path}".format(
        path=path), YELLOW)


def warna(icon, msg, color):
    print(colored("[{icon}] {msg}".format(
        icon=icon, msg=msg), "{color}".format(color=color)))


def main():
    base_path = ""

    cari_seluruh_file_srt(base_path)


if __name__ == "__main__":
    main()
