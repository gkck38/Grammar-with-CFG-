import json
from grammar_loader import load_grammar
from recursive_parser import parse_sentence

def main():
    grammar_file = r"MiniParserProject\data\grammar1.txt"
    sentences_file = r"MiniParserProject\data\sentences.txt"

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
                
                # 1. Parser'dan gelen raporu al
                sonuc = parse_sentence(cumle, grammar)
                
                # 2. Rapor Valid ise JSON bas
                if sonuc["valid"]:
                    print("Valid")
                    print("JSON:")
                    # En dışa "sentence" sarmalayıcısı ekliyoruz
                    final_json = {"sentence": sonuc["tree"]["<sentence>"]} if "<sentence>" in sonuc["tree"] else sonuc["tree"]
                    print(json.dumps(final_json, indent=4))
                    
                # 3. Rapor Invalid ise o 15 Puanlık hatayı bas!
                else:
                    print("Invalid")
                    print("Error:")
                    print(f"  • Where the error occurs: at token {sonuc['error_index']} (\"{sonuc['error_token']}\")")
                    print(f"  • What was expected: {sonuc['expected']}")
                    print(f"  • Why the sentence is invalid: the sentence encountered \"{sonuc['error_token']}\", but grammar requires {sonuc['expected']} to proceed.")
                
                print("\n" + "=" * 50 + "\n")
                
    except FileNotFoundError:
        print("HATA: sentences.txt dosyası bulunamadı!")

if __name__ == "__main__":
    main()