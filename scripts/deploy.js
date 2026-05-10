import pkg from "hardhat";
import fs from "fs";
import path from "path";

const { ethers } = pkg;

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying HoneypotAdvanced from:", deployer.address);

  const HoneypotFactory = await ethers.getContractFactory("HoneypotAdvanced");
  const honeypot = await HoneypotFactory.deploy({ value: ethers.parseEther("1.0") });
  await honeypot.waitForDeployment();

  const address = await honeypot.getAddress();
  console.log("HoneypotAdvanced deployed at:", address);

  const sharedDir = process.env.SHARED_DIR || ".";
  fs.mkdirSync(sharedDir, { recursive: true });
  const addrFile = path.join(sharedDir, "contract_address.txt");
  fs.writeFileSync(addrFile, address);
  console.log("Contract address written to:", addrFile);
}

main().catch((err) => { console.error(err); process.exit(1); });