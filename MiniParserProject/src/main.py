from grammar_loader import load_grammar
from recursive_parser import parse

# Önce grameri yükle
kural_sozlugu = load_grammar("../data/grammar1.txt")

# Sonra cümleleri okuyup parse fonksiyonuna gönder...