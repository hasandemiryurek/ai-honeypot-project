// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Honeypot {
    mapping(address => uint256) public balances;
    event AttackDetected(address indexed attacker, uint256 amount);

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Bu fonksiyon, sözleşmeye düz para (Ether) gönderildiğinde çalışır
    receive() external payable {
        // AI ajanının duyması için bu eventi (olayı) tetikliyoruz
        emit AttackDetected(msg.sender, msg.value);
        
        // Paran burada kalıyor, geri vermiyoruz (Tuzak!)
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 bal = balances[msg.sender];
        require(bal > 0, "Yetersiz bakiye");

        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Para gonderilemedi");

        balances[msg.sender] = 0;
    }
}