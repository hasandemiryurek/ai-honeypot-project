import pkg from "hardhat";
const { ethers } = pkg;

async function main() {
  // Hardhat'in verdiği hazır hesaplardan saldırganı alalım
  const [owner, attacker] = await ethers.getSigners();
  
  // Senin oluşturduğun Honeypot adresi
  const honeypotAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  console.log("🚀 Saldırı simülasyonu başlatılıyor...");
  console.log(`Saldırgan adresi: ${attacker.address}`);

  // Tuzağa 1 ETH gönderiyoruz
  const tx = await attacker.sendTransaction({
    to: honeypotAddress,
    value: ethers.parseEther("1.0")
  });

  console.log("⏳ İşlem ağa gönderildi, onaylanıyor...");
  await tx.wait();
  
  console.log("✅ Tuzağa para başarıyla gönderildi!");
  console.log("Şimdi Python (Agent) terminaline bak, alarm çalmış olmalı!");
}

main().catch((error) => {
  console.error("Hata oluştu:", error);
  process.exit(1);
});