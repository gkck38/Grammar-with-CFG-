def parse_sentence(cumle, grammar):
    #  grammar'deki terminallere göre cümleyi tokenlara ayırıyoruz
    terminaller = set() #terminalleri bir kümede toplama işlemi yapıyoruz. 
    for alternatifler in grammar.values():
        for alt in alternatifler:
            for kelime in alt:
                if kelime not in grammar and kelime != "ε":
                    terminaller.add(kelime)
    #uzunluğu 1 olanlar karakter , fazla olanlar kelime 
    karakter_bazli_mi = all(len(t) == 1 for t in terminaller) if terminaller else False 

    if cumle.strip() == "ε" or cumle.strip().lower() == "boş string":
        tokens = []
    elif karakter_bazli_mi: #karakter bazlıysa ona göre tokenlara ayırıyoruz
        tokens = list(cumle.replace(" ", "")) 
    else:
        tokens = cumle.split() 
    # ----------------------------------------------

    guncel_endeks = 0

    en_uzak_endeks = 0 #çökmeden max nereye kadar gidebildiğimizi tutacak
    beklenen_kurallar = set() #en uzak noktada hangi kuralların beklendiğini tutacak

    def parse(kural_adi):
        nonlocal guncel_endeks, en_uzak_endeks, beklenen_kurallar #onları fonksiyon içinde değiştirebilmek için nonlocal ile tanımlıyoruz
        
        # terminal veya ε kontrolü : 
        if kural_adi not in grammar:
            
            if kural_adi == "ε":
                return {"ε": "ε"}

            # Cümle Bitti Kontrolü
            elif guncel_endeks >= len(tokens): #eğer cümlenin sonuna gelmişsek ve hala kural arıyorsak, bu da bir hatadır
                if guncel_endeks > en_uzak_endeks:
                    en_uzak_endeks = guncel_endeks
                    beklenen_kurallar = {kural_adi}
                elif guncel_endeks == en_uzak_endeks:
                    beklenen_kurallar.add(kural_adi)
                return False

            # başarılı eşleşme: terminal kural mevcut token ile eşleşiyor
            elif tokens[guncel_endeks] == kural_adi:
                eslesen_kelime = tokens[guncel_endeks]
                guncel_endeks += 1
                return eslesen_kelime 

            # Hatalı Kelime
            else:
                #hata  alınan yer en uzak noktaysa, beklenen kelimeyi kaydet
                if guncel_endeks > en_uzak_endeks:
                    en_uzak_endeks = guncel_endeks
                    beklenen_kurallar = {kural_adi}
                elif guncel_endeks == en_uzak_endeks:
                    beklenen_kurallar.add(kural_adi)
                return False

        # Backtracking ile alternatifleri dene 
        for alternatif in grammar[kural_adi]:
            temp_endeks = guncel_endeks #alternatif cümleye uymazsa geri dönebilmek için temp endeks
            parse_sonucu = {}
            basarili_mi = True

            for alt_kural in alternatif: #recursive olarak her alt kuralı dene
                sonuc = parse(alt_kural) #fonksiyonun kendisini çağırarak alt kuralları çözmeye çalışıyoruz
                if sonuc is False:
                    basarili_mi = False
                    break  #herhangi biri yanlış olursa direkt false 

                # --- BURASI GÜNCELLENDİ: Ağacı birleştirme zekası ---
                if not parse_sonucu: 
                    parse_sonucu = sonuc # Kutu boşsa, gelen ilk parçayı direkt koy
                else:
                    if not isinstance(parse_sonucu, list):
                        # gelen sözlükse yani alternatif birden fazla kural içeriyorsa, parse_sonucu'na ekle (Grammar1 mantığı)
                        if isinstance(parse_sonucu, dict) and isinstance(sonuc, dict):
                            parse_sonucu.update(sonuc)
                        else:
                            # Biri harf (str) diğeri sözlükse, onları bir Liste yap (Grammar2'deki AttributeError çözümü)
                            parse_sonucu = [parse_sonucu]
                            parse_sonucu.append(sonuc)
                    else:
                        parse_sonucu.append(sonuc)

            if basarili_mi:
                return {kural_adi: parse_sonucu} #json formatında ağaç oluşturmak için sözlük döndürüyoruz

            guncel_endeks = temp_endeks #alternatif başarısız olduysa endeksi geri alarak diğer alternatifleri dene
            
        return False

    # farklı grammarler olabileceği için başlangıç kuralını otomatik olarak belirliyoruz
    baslangic_kurali = list(grammar.keys())[0]
    agac = parse(baslangic_kurali)

    # eğer durum başarılıysa, ağacı ve valid bilgisini içeren bir sözlük döndür
    if agac and guncel_endeks == len(tokens):
        return {"valid": True, "tree": agac}
    
    # başarısız durumda, en uzak noktada beklenen kuralları ve hatayı içeren bir sözlük döndür
    else:
        hata_kelimesi = tokens[en_uzak_endeks] if en_uzak_endeks < len(tokens) else "EOF (Cümle Sonu)" #eğer en uzak endeks cümlenin sonunu aşmışsa, hatayı "EOF" olarak gösteriyoruz   
        beklenenler = " or ".join(beklenen_kurallar)  
        
        return {
            "valid": False,
            "error_index": en_uzak_endeks + 1,  # 0. indeks yerine 1'den başlat
            "error_token": hata_kelimesi,
            "expected": beklenenler
        }