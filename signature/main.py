import  os
import  zipfile
import hashlib

#elimizde olan bilgiler ve bulundukları dosya adresleri
## 138 . satırda bu kısma dahildir

json_file_content=open(r"C:\Users\eren.yargil\PycharmProjects\signutere_t\test.json","r").read()
txt_file_content=open(r"C:\Users\eren.yargil\PycharmProjects\signutere_t\test.txt","r").read()
password_file_content=open(r"C:\Users\eren.yargil\PycharmProjects\signutere_t\pasword test.txt","r").read()
json_file=r"C:\Users\eren.yargil\PycharmProjects\signutere_t\test.json"
txt_file=r"C:\Users\eren.yargil\PycharmProjects\signutere_t\test.txt"
password_file=r"C:\Users\eren.yargil\PycharmProjects\signutere_t\pasword test.txt"
# sha larını rahatça almak için hazrılanan fonksiyon

def get_sha(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda:f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

#elimizdeki dosyalarlaın sha ları ile şifre oluşturmak için olan fonksiyon
def get_pasword(filenames) :
    list=[]
    for file_lo in filenames:
        list.append(get_sha(file_lo))
    son = ""
    don = 0
    i = 0
    for_counter = 0

    for eleman in list:
        for_counter += 1
        index = 0
        for kip in eleman:

            if for_counter % 2 == 0:
                son += eleman[index]

            else:
                son += eleman[-index]
            index = index + 1
            for_counter += 1



    k=hashlib.sha256(son.encode()).hexdigest()
    return k


#test için hazırlanan altyapının  bir parçası

def take_file_from_zip(zip_file,file):
    with zipfile.ZipFile(zip_file,"r") as zip :
        zip_list = zip.namelist()

        if file in zip_list:
            zip.extract(file,path="temp_dir/")
            return  "temp_dir/"+file
        else:
            return None


# gelen dosyaların sha larının kıyaslamak için kulanılan fonksiyon
def check_password(files,pasword_filename):
    norgin = get_pasword(files)
    fil1=open(pasword_filename,"r")
    fil=fil1.read()
    if (fil == norgin):
        fil1.close()
        return True
    else:
        fil1.close()
        return False

#test için hazırlanan altyapının  bir parçası

def up_zip(json_file,txt_file,password):
    with open("t1.json", "w") as f1, open("t2.txt","w") as f2, open("pt.txt","w") as f3:
        f1.write(open(json_file).read())
        f2.write(open(txt_file).read())
        f3.write(password)
    zip_file_name= os.path.join(os.path.expanduser('~'), 'Desktop', 'npas.zip')
    with zipfile.ZipFile(zip_file_name,"w") as zip:
        zip.write("t1.json")
        zip.write("t2.txt")
        zip.write("pt.txt")
    os.remove("t1.json")
    os.remove("t2.txt")
    os.remove("pt.txt")

#test için hazırlanan altyapının  bir parçası
def check_zip_signiture(files,pasword_file_name):
    zip_file = r"C:\Users\eren.yargil\Desktop\npas.zip"

    list_1=[]
    for eleman in files:
        list_1.append(take_file_from_zip(zip_file,eleman))


    temp3 = take_file_from_zip(zip_file, pasword_file_name)
# check paswordu liste yap
    if check_password(list_1, temp3):
        print("dosyalar güvenli")
    else:
        print("!!!  dosyalar değiştirilmiştir   !!!")

password=get_pasword([json_file,txt_file])

file_names=["t1.json","t2.txt","pt.txt"]

#dosya yüklemek için yorum satırını kaldırın test etmek için ise yorum satırı haline getirin


#up_zip(json_file,txt_file,password)

#6 satıra dahildir ilk defa zip dosyası oluşturulduktan sonra zip dosyasının adresi ile değiştirerek test edebilirsiniz
zip_file = r"C:\Users\eren.yargil\Desktop\npas.zip"

print("zip açılınca alınan şifre    :",get_pasword([take_file_from_zip(zip_file,"t1.json"),take_file_from_zip(zip_file,"t2.txt")]))
print("kayıtlı olan şifre           :",open( take_file_from_zip(zip_file, "pt.txt")).read())
print("dosyada yazılı olanlar       :",open(take_file_from_zip(zip_file,"t2.txt")).read())

check_zip_signiture(["t1.json","t2.txt"],"pt.txt")

