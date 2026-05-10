import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("HoneypotModule", (m) => {
  const honeypot = m.contract("Honeypot"); // contracts/Honeypot.sol'u bulur

  return { honeypot };
});