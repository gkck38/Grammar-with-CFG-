import os
from graphviz import Digraph

def ciz_agaci(agac_sozlugu, dosya_adi="parse_tree"):
    # ağaç grafiğini başlat (Yukarıdan aşağıya doğru: TB - Top to Bottom)
    dot = Digraph(comment='Parse Tree')
    dot.attr(rankdir='TB') 

    # düğümlerin birbirine karışmaması için benzersiz bir ID sayacı tutuyoruz
    sayac = [0] 

    def dallari_ekle(parent_id, alt_dugum):
        if isinstance(alt_dugum, dict):
            # eğer bu bir kural ise (Non-terminal), elips şeklinde çizilir
            for kural, deger in alt_dugum.items():
                sayac[0] += 1
                guncel_id = str(sayac[0])
                
                dot.node(guncel_id, str(kural))
                if parent_id:
                    dot.edge(parent_id, guncel_id)
                
                # içine girmeye devam et (Recursion)
                dallari_ekle(guncel_id, deger)
                
        elif isinstance(alt_dugum, list):
            # grammar2'deki gibi yan yana kurallar geldiyse tek tek dolaş
            for eleman in alt_dugum:
                dallari_ekle(parent_id, eleman)
                
        else:
            # eğer bu bir kelime ise (Terminal), hocanın istediği gibi MAVİ KUTU şeklinde çiz
            sayac[0] += 1
            guncel_id = str(sayac[0])
            dot.node(guncel_id, str(alt_dugum), shape='box', style='filled', fillcolor='#5b9bd5', fontcolor='white')
            if parent_id:
                dot.edge(parent_id, guncel_id)

    # ağacın en tepesini (Kök düğümü) yakala
    baslangic_kurali = list(agac_sozlugu.keys())[0]
    sayac[0] += 1
    kok_id = str(sayac[0])
    dot.node(kok_id, str(baslangic_kurali))
    
    # kökten başlayarak dallanmayı ateşle
    dallari_ekle(kok_id, agac_sozlugu[baslangic_kurali])

    cikis_klasoru = "MiniParserProject/trees" # src klasöründen bir üste çıkıp trees klasörüne gir
    
    # Eğer trees adında bir klasör yoksa, Python otomatik olarak oluştursun
    os.makedirs(cikis_klasoru, exist_ok=True)

    dot.render(dosya_adi, directory=cikis_klasoru, format='png', view=False, cleanup=True)
    print(f"[BAŞARILI] Ağaç görseli '{cikis_klasoru}/{dosya_adi}.png' olarak kaydedildi!")