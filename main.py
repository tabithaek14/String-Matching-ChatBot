from asyncio.windows_events import NULL
import csv
import pwinput

def showMenu():
    print("================================================")
    print("                Awesome Chatbot                 ")
    print("================================================")
    print("Main menu:")
    print("1. Login")
    print("2. Register")
    print("3. Quit App")

def show_menu():
    print("===== Pilih Fitur =====")
    print("1. Tambah Pertanyaan")
    print("2. Delete Pertanyaan")
    print("3. Masukan Pertanyaan")
    print("4. Exit")
    return

def signIn():
    print("Masukkan akun anda:")
    username = str(input("User ID: "))
    password = pwinput.pwinput(prompt="Password: ", mask="*")

    with open('User.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if((row['user_id'] == username) and row['password'] == password):
                print("Login sukses, Selamat datang", row['nama'], "!!")
                print()
                return True
            
        print("Akun belum terdaftar, ingin register?")
        print("1. Ya")
        print("2. Tidak")
        opsi = int(input("Pilih Opsi: "))
        while (opsi != 1 and opsi != 2):
            print("Masukkan angka yang valid")
            opsi = int(input("Pilih Opsi: "))
        if (opsi == 1):
            signUp()
        else:
            return False

def signUp():
    print("====== Masukkan User ID, password, dan nama ======")
    username = str(input("Username: "))
    password = pwinput.pwinput(prompt="Password: ", mask="*")
    nama = str(input("Nama: "))
    temp = [("user_id","password","nama")]
    with open('User.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp.append((row['user_id'],row['password'],row['nama']))
            if (row['user_id'] == username):
                print("User ID sudah terdaftar !!")
                print()
                return
            
    temp.append((username,password,nama))
    with open('User.csv', 'w+') as file:
        myFile = csv.writer(file)
        for row in temp:
            myFile.writerow(row)
    print("Registrasi Sukses")
    print()

def input_question(pat,jwb):
    temp_input = [("Pertanyaan","Jawaban")]
    with open('Daftar Pertanyaan.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp_input.append((row['Pertanyaan'],row['Jawaban']))
            if (row['Pertanyaan'].lower() == pat.lower()):
                print("Pertanyaan Sudah Ada!")
                print()
                return 
            
    temp_input.append((pat,jwb))
    with open('Daftar Pertanyaan.csv', 'w+') as file:
        myFile = csv.writer(file)
        for row in temp_input:
            myFile.writerow(row)
    print("Input Sukses")
    print()

def kmp_search(pattern,text):
    n = len(text)
    m = len(pattern)
    failure = build_failure_table(pattern)
    i = 0
    j = 0

    while i < n:
        if text[i] == pattern[j]:
            if j == m - 1:
                return i - j
            i += 1
            j += 1
        else:
            if j != 0:
                j = failure[j - 1]
            else:
                i += 1

    return -1
 
def build_failure_table(pattern):
    failure = [0] * len(pattern)
    i = 0

    for j in range(1, len(pattern)):
        if pattern[i] == pattern[j]:
            i += 1
            failure[j] = i
        else:
            if i != 0:
                i = failure[i - 1]
                j -= 1
            else:
                failure[j] = 0

    return failure

def hamming_distance(s1, s2):
    distance = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            distance += 1
    return distance

def hamming_dist_int(str1, str2):
	i = 0
	count = 0

	while(i < len(str1)):
		if(str1[i] != str2[i]):
			count += 1
		i += 1
	return count

def check_string(threshold,pat):
    temp= []
    similar_sentences = []
    with open('Daftar Pertanyaan.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp.append(row['Pertanyaan'].lower())
        for s in temp:
            distance = hamming_distance(pat, s)
            if distance <= threshold and s!='':
                similar_sentences.append(s)
        return similar_sentences

def read_question():
    list_pertanyaan = [list(("Pertanyaan","Jawaban"))]
    with open('Daftar Pertanyaan.csv', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            list_pertanyaan.append(list((row['Pertanyaan'],row['Jawaban'])))
    return list_pertanyaan

def write_question(list_pertanyaan):
    with open('Daftar Pertanyaan.csv', 'w+') as file:
        myFile = csv.writer(file)
        for row in list_pertanyaan:
            myFile.writerow(row)
    print("Delete Sukses")
    print()

def closest(pat,similiar_sentence):
    temp = 100
    index = 0
    for i in range(len(similiar_sentence)):
        x = hamming_dist_int(pat,similiar_sentence[i])
        if(temp>x):
            temp = x
            index = i
    return index

def main():
    pat = ""
    global loggedInUser
    quit = False
    while(not quit):
        loggedIn = False
        showMenu()
        
        try:
            menu = int(input("Pilih Opsi: "))
            print()
            if (menu == 1):
                if (signIn()):
                    loggedIn = True
            elif (menu == 2):
                signUp()
            elif (menu == 3):
                quit = True
            else:
                print("Masukkan angka valid !!")
                print()

            while (loggedIn):
                show_menu()
                try:
                    menu_user = int(input("Pilih Opsi: "))
                    print()

                    if(menu_user==1):
                        pat = str(input("Masukkan pertanyaan: "))
                        jwb = str(input("Masukkan jawaban: "))
                        input_question(pat,jwb)

                    elif(menu_user==2):
                        pat = str(input("Masukkan pertanyaan: ")).lower()
                        similar_sentences = check_string(1,pat)
                        if(similar_sentences!=[] and len(similar_sentences)<=2):
                            list_pertanyaan = read_question()
                            temp_pertanyaan = list(list_pertanyaan)
                            index = closest(pat,similar_sentences)
                            for row in temp_pertanyaan:
                                if (kmp_search((similar_sentences[index]).lower(), (row[0]).lower()) != -1):
                                    row[0] = ''
                                    row[1] = ''
                                    temp_pertanyaan.append((row[0],row[1]))
                            list_pertanyaan = tuple(temp_pertanyaan)
                            write_question(list_pertanyaan)
                        else:
                            similar_sentences = check_string(2,pat)
                            if(similar_sentences!=[]):
                                print("Mungkin maksud anda:")
                                if(len(similar_sentences)<=3):
                                        y = len(similar_sentences)
                                else:
                                        y = 3
                                for i in range(y):
                                    temp_kasus2[i] = similar_sentences[i]
                                    print(f"{i+1}. {temp_kasus2[i]}")
                                question_user = int(input("Pilih Opsi: "))
                                list_pertanyaan = read_question()
                                for row in list_pertanyaan:
                                    if (kmp_search(similar_sentences[question_user-1], row[0]) != -1):
                                        row[0] = ''
                                        row[1]= ''
                                        list_pertanyaan.append((row[0],row[1]))
                                write_question(list_pertanyaan)
                            else:
                                print("Pertanyaan tidak ditemukan")
                                print()    

                    elif(menu_user==3):
                        pat = str(input("Masukkan pertanyaan: ")).lower()
                        with open('Daftar Pertanyaan.csv', newline='') as csvfile:
                            matches = []
                            reader = csv.DictReader(csvfile)
                            similar_sentences = check_string(1,pat)
                            if(similar_sentences!=[] and len(similar_sentences)<=2):
                                index = closest(pat,similar_sentences)
                                for row in reader:
                                    if (kmp_search(similar_sentences[index], row['Pertanyaan'].lower()) != -1):
                                        if(row['Jawaban']!=''):
                                            matches.append(row['Jawaban'])

                            else:
                                similar_sentences = check_string(2,pat)
                                temp_kasus2 = [None]*3
                                if(similar_sentences!=[]):
                                    print("Mungkin maksud anda:")
                                    if(len(similar_sentences)<=3):
                                        y = len(similar_sentences)
                                    else:
                                        y = 3
                                    for i in range (y):
                                        temp_kasus2[i] = similar_sentences[i]
                                        print(f"{i+1}. {temp_kasus2[i]}")
                                    question_user = int(input("Pilih Opsi: "))
                                    for row in reader:
                                        if (kmp_search(similar_sentences[question_user-1], row['Pertanyaan'].lower()) != -1):
                                            if(row['Jawaban']!=''):
                                                matches.append(row['Jawaban'])
                                else:
                                    print("Pertanyaan tidak ditemukan")
                                    print()

                            if (len(matches) > 0):
                                for match in matches:
                                    print(match)
                                    print()
                                matches = []

                    elif (menu_user==4):
                        loggedIn = False

                except ValueError:
                    print("Masukan angka!")

        except ValueError:
            print("Masukan angka!")

    print("Terima kasih telah menggunakan ChatBot ini !!")

if __name__ == '__main__':
    main()