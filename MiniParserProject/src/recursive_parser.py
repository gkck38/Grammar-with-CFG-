from grammar_loader import load_grammar
import json


grammar = load_grammar(r"MiniParserProject\data\grammar1.txt")  #bu kısım main.py'de olucak deneme için buraya bıraktım

cumle = "the man saw a dog"
tokens = cumle.split()
guncel_endeks = 0

def parse(kural_adi):
    global guncel_endeks 
    
    # --- GÖREV 1: KELİME (TERMINAL) KONTROLÜ ---
    if kural_adi not in grammar:
        
        # 1. İstisna: Epsilon (ε)
        if kural_adi == "ε":
            return {"ε": "ε"}

        # 2. Sınır: Cümle bitti mi?
        elif guncel_endeks >= len(tokens):
            return False

        # 3. Eşleşme: Kelime tutuyor mu?
        elif tokens[guncel_endeks] == kural_adi:
            eslesen_kelime = tokens[guncel_endeks]
            guncel_endeks += 1
            # Sözlük yerine direkt kelimenin kendisini dönüyoruz yoksa hata aldım
            return eslesen_kelime 

        # 4. Eşleşmeme
        else:
            return False

    # --- GÖREV 2: KURAL KONTROLÜ (BACKTRACKING) ---
    for alternatif in grammar[kural_adi]:
        temp_endeks = guncel_endeks
        parse_sonucu = {}

        for alt_kural in alternatif:
            sonuc = parse(alt_kural)

            if sonuc is False:
                break

            # Hatamın düzeltmesi : Gelen şey sözlük mü, düz kelime mi?
            if isinstance(sonuc, dict):
                parse_sonucu.update(sonuc)
            else:
                parse_sonucu = sonuc

        # break çalışmadıysa, yani tüm alt kurallar başarılıysa
        else:
            return {kural_adi: parse_sonucu}

        # Başarısız olursa geri sar (Backtracking)
        guncel_endeks = temp_endeks
        
    return False

# Test 
sonuc_agaci = parse("<sentence>")

if sonuc_agaci:
    print("Valid")
    print(json.dumps(sonuc_agaci, indent=4))
else:
    print("Invalid")