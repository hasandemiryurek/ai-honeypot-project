import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. VERİ SETİNİ YÜKLE
# Bu dosyanın içinde 'bytecode' ve 'label' (0 veya 1) sütunları olmalı
try:
    df = pd.read_csv('mini_dataset.csv')
    print("✅ Veri seti yüklendi.")
except FileNotFoundError:
    print("❌ Hata: 'mini_dataset.csv' bulunamadı!")
    exit()

# 2. ÖZELLİK ÇIKARIMI (Feature Extraction)
# AI'nın bytecode'un içindeki hangi detaylara bakacağını belirliyoruz.
def extract_features(bytecode):
    # '0x' kısmını temizleyip sadece kod kısmına odaklanıyoruz
    clean_code = bytecode.replace('0x', '')
    
    # Özellik 1: Kodun uzunluğu (Karmaşık sözleşmeler genelde daha uzundur)
    length = len(clean_code)
    
    # Özellik 2: İçindeki 'f' karakteri sayısı 
    # (Örn: Kritik opcodeların byte karşılıklarını saymak gibi basit bir mantık)
    f_count = clean_code.count('f')
    
    return [length, f_count]

# Tüm satırlar için bu özellikleri hesapla ve X listesine koy
X = [extract_features(b) for b in df['bytecode']]
# Hedef sonuçları (saldırı mı değil mi?) y listesine koy
y = df['label']

# 3. MODELİ OLUŞTUR VE EĞİT
# 'Random Forest' (Rastgele Orman) algoritması bir sürü karar ağacı kurarak öğrenir.
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("⏳ Eğitim başlıyor...")
model.fit(X, y)
print("✅ Eğitim tamamlandı!")

# 4. MODELİ DONDUR VE KAYDET
# Artık bu 'model' nesnesini her seferinde eğitmemek için dosyaya yazıyoruz.
joblib.dump(model, 'honeypot_ai_model.pkl')
print("💾 'honeypot_ai_model.pkl' başarıyla oluşturuldu.")