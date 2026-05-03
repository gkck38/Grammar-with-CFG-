def load_grammar(file_path):
    grammar = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or "::=" not in line:
                continue
                
            lhs, rhs = line.split("::=")
            lhs = lhs.strip()
            
            alternatives = rhs.split("|")
            parsed_alternatives = []
            
            for alt in alternatives:
                tokens = alt.strip().split() #kelimeleri ayırmak için split kullanıyoruz
                parsed_alternatives.append(tokens)
            parsed_alternatives.sort(key=len, reverse=True) #kısa olan alternatifler önce gelmesin diye sıralama  yoksa hata
            grammar[lhs] = parsed_alternatives
            
    return grammar