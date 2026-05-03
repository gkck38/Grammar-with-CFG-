def parse_sentence(cumle, grammar):
    tokens = cumle.split()
    guncel_endeks = 0

    # --- HATA TAKİP AJANI DEĞİŞKENLERİ ---
    en_uzak_endeks = 0
    beklenen_kurallar = set()

    def parse(kural_adi):
        nonlocal guncel_endeks, en_uzak_endeks, beklenen_kurallar 
        
        # --- GÖREV 1: KELİME (TERMINAL) KONTROLÜ ---
        if kural_adi not in grammar:
            
            if kural_adi == "ε":
                return {"ε": "ε"}

            # Cümle Bitti Kontrolü
            elif guncel_endeks >= len(tokens):
                # AJAN DEVREDE: Eğer bu en uzak noktaysa, aranan kuralı not et
                if guncel_endeks > en_uzak_endeks:
                    en_uzak_endeks = guncel_endeks
                    beklenen_kurallar = {kural_adi}
                elif guncel_endeks == en_uzak_endeks:
                    beklenen_kurallar.add(kural_adi)
                return False

            # Başarılı Eşleşme
            elif tokens[guncel_endeks] == kural_adi:
                eslesen_kelime = tokens[guncel_endeks]
                guncel_endeks += 1
                return eslesen_kelime 

            # Hatalı Kelime
            else:
                # AJAN DEVREDE: Hata alınan yer en uzak noktaysa, beklenen kelimeyi kaydet
                if guncel_endeks > en_uzak_endeks:
                    en_uzak_endeks = guncel_endeks
                    beklenen_kurallar = {kural_adi}
                elif guncel_endeks == en_uzak_endeks:
                    beklenen_kurallar.add(kural_adi)
                return False

        # --- GÖREV 2: KURAL KONTROLÜ (BACKTRACKING) ---
        for alternatif in grammar[kural_adi]:
            temp_endeks = guncel_endeks
            parse_sonucu = {}
            basarili_mi = True

            for alt_kural in alternatif:
                sonuc = parse(alt_kural)
                if sonuc is False:
                    basarili_mi = False
                    break

                if isinstance(sonuc, dict):
                    parse_sonucu.update(sonuc)
                else:
                    parse_sonucu = sonuc

            if basarili_mi:
                return {kural_adi: parse_sonucu}

            guncel_endeks = temp_endeks
            
        return False

    # --- ANA ÇALIŞTIRMA VE ÇIKTI KONTROLÜ ---
    baslangic_kurali = list(grammar.keys())[0]
    agac = parse(baslangic_kurali)

    # BAŞARILI DURUM: Ağaç oluştu ve cümlenin tamamı okunduysa
    if agac and guncel_endeks == len(tokens):
        return {"valid": True, "tree": agac}
    
    # BAŞARISIZ DURUM: Hata raporunu paketle ve main.py'ye gönder!
    else:
        hata_kelimesi = tokens[en_uzak_endeks] if en_uzak_endeks < len(tokens) else "EOF (Cümle Sonu)"
        beklenenler = " or ".join(beklenen_kurallar)
        
        return {
            "valid": False,
            "error_index": en_uzak_endeks + 1,  # 0. indeks yerine insanlar için 1'den başlat
            "error_token": hata_kelimesi,
            "expected": beklenenler
        }