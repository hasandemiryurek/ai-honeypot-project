import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";
import { parseEther } from "ethers";

export default buildModule("HoneypotAdvanced", (m) => {
  const honeypot = m.contract("HoneypotAdvanced", [], { value: parseEther("1.0") });
  return { honeypot };
});