import json
import time
from grammar_loader import load_grammar
from recursive_parser import parse_sentence
from visualizer import ciz_agaci

def main():
    baslangic_zamani = time.time()
    grammar_file = r"MiniParserProject/data/grammar3.txt"
    sentences_file = r"MiniParserProject/data/sentences3.txt"

    print(f"--- Gramer Yükleniyor: {grammar_file} ---")
    try:
        grammar = load_grammar(grammar_file)
    except FileNotFoundError:
        print("HATA: grammar dosyası bulunamadı!")
        return

    print(f"--- Cümleler Test Ediliyor: {sentences_file} ---\n")
    
    try:
        with open(sentences_file, 'r', encoding='utf-8') as f:
            for line in f:
                cumle = line.strip()
                if not cumle:
                    continue
                
                print(f"Input: {cumle}")
                
                # 1. parser'dan gelen raporu al
                sonuc = parse_sentence(cumle, grammar)
                
                # 2. rapor Valid ise JSON bas ve AĞACI ÇİZ!
                if sonuc["valid"]:
                    print("Valid")
                    print("JSON:")
                    # en dışa "sentence" sarmalayıcısı ekliyoruz
                    final_json = {"<sentence>": sonuc["tree"]["<sentence>"]} if "<sentence>" in sonuc["tree"] else sonuc["tree"]
                    print(json.dumps(final_json, indent=4, ensure_ascii=False))
                    dosya_ismi = f"agac_{cumle.replace(' ', '_')}"
                    ciz_agaci(final_json, dosya_ismi)
                # 3. rapor Invalid ise o 15 Puanlık hatayı bas!
                else:
                    print("Invalid")
                    print("Error:")
                    print(f"  • Where the error occurs: at token {sonuc['error_index']} (\"{sonuc['error_token']}\")")
                    print(f"  • What was expected: {sonuc['expected']}")
                    print(f"  • Why the sentence is invalid: the sentence encountered \"{sonuc['error_token']}\", but grammar requires {sonuc['expected']} to proceed.")
                
                print("\n" + "=" * 50 + "\n")
                
    except FileNotFoundError:
        print("HATA: sentences.txt dosyası bulunamadı!")

    bitis_zamani = time.time()
    gecen_sure = bitis_zamani - baslangic_zamani
    print(f"Toplam Geçen Süre: {gecen_sure:.2f} saniye")

if __name__ == "__main__":
    main()