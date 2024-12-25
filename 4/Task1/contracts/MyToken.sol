// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply
    ) ERC20(_name, _symbol) {
        // Mint initial supply to the contract deployer
        _mint(msg.sender, _initialSupply);
    }
    // Allows to additionally mint tokens, if needed
    function mint(address _to, uint256 _amount) external {
        _mint(_to, _amount);
    }
}
