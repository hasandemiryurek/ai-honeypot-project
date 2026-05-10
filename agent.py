import joblib
import json
import time
from web3 import Web3

# 1. AYARLAR (Senin aldığın adresi buraya sabitledik)
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3" 
RPC_URL = "http://127.0.0.1:8545"

# 2. BLOKZİNCİR BAĞLANTISI
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if web3.is_connected():
    print(f"✅ Blokzincire bağlanıldı! İzlenen adres: {CONTRACT_ADDRESS}")
else:
    print("❌ Hata: Blokzincire bağlanılamadı. npx hardhat node açık mı?")
    exit()

# 3. AI BEYNİNİ YÜKLE (Az önce eğittiğimiz model)
try:
    model = joblib.load('honeypot_ai_model.pkl')
    print("🧠 AI Modeli başarıyla yüklendi.")
except:
    print("❌ Hata: 'honeypot_ai_model.pkl' bulunamadı!")
    exit()

# 4. SÖZLEŞME BİLGİLERİNİ (ABI) OKU
# Hardhat derleme yapınca bu dosyayı otomatik oluşturur
with open('artifacts/contracts/Honeypot.sol/Honeypot.json') as f:
    artifact_data = json.load(f)
    abi = artifact_data['abi']

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# 5. SALDIRI ANALİZ FONKSİYONU (AI BURADA DEVREYE GİRER)
def analyze_attacker(attacker_address):
    # Saldırganın makine kodunu (bytecode) çekiyoruz
    bytecode = web3.eth.get_code(attacker_address).hex()
    
    # Eğitimde kullandığımız özelliklerin aynısını çıkarıyoruz
    # (Uzunluk ve 'f' karakteri sayısı)
    features = [[len(bytecode), bytecode.count('f')]]
    
    # AI'ya soruyoruz: "Bu kod sence nedir?"
    prediction = model.predict(features)
    
    if prediction[0] == 1:
        return "🚨 TEHLİKELİ (Zafiyetli/Saldırgan Kod Tespit Edildi)"
    else:
        return "✅ GÜVENLİ (Normal Kullanıcı)"

# 6. OLAYLARI DİNLEME DÖNGÜSÜ
print("🕵️ Gözcü nöbette... Birinin tuzağa düşmesi bekleniyor...")

# Tuzağımızdaki 'AttackDetected' olayını filtreliyoruz
event_filter = contract.events.AttackDetected.create_filter(from_block='latest')

while True:
    try:
        # Yeni bir olay var mı diye kontrol et
        for event in event_filter.get_new_entries():
            attacker = event.args.attacker
            print(f"\n🔔 Yeni Olay: {attacker} adresi tuzağa dokundu!")
            
            # AI Analizini başlat
            teshis = analyze_attacker(attacker)
            print(f"🔍 AI Teşhisi: {teshis}")
            
        time.sleep(2) # İşlemciyi yormamak için kısa bir mola
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        time.sleep(5)