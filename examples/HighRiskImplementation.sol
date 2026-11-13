// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Repository fixture used by automated scanner tests. Not intended for deployment.
contract HighRiskImplementation {
    mapping(address => uint256) public balances;
    address public owner;

    function withdraw() external {
        (bool sent,) = msg.sender.call{value: balances[msg.sender]}("");
        balances[msg.sender] = 0;
    }

    function setOwner(address next) external { owner = next; }
    function originAuth() external view returns (bool) { return tx.origin == owner; }
    function execute(address target, bytes calldata data) external { target.delegatecall(data); }
}
