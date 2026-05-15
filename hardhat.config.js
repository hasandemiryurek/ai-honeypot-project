import "@nomicfoundation/hardhat-toolbox";

export default {
  solidity: "0.8.24",
  networks: {
    hardhat: {
      chainId: 1337,
      mining: { auto: true, interval: 2000 },
    },
    localhost: {
  url: process.env.RPC_URL || "http://127.0.0.1:8545",
  chainId: 1337,
},
  },
};