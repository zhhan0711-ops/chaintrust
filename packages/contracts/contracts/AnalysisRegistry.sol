// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
/// @notice Testnet-only registry of analysis references; no reports or source code are stored.
contract AnalysisRegistry {
    struct AnalysisRecord { bytes32 sourceRef; bytes32 reportHash; uint256 timestamp; address analyst; }
    mapping(bytes32 => AnalysisRecord[]) private recordsBySource;
    event AnalysisRecorded(bytes32 indexed sourceRef, bytes32 indexed reportHash, uint256 timestamp, address analyst);
    function recordAnalysis(bytes32 sourceRef, bytes32 reportHash) external {
        require(sourceRef != bytes32(0) && reportHash != bytes32(0), "hash required");
        AnalysisRecord memory record = AnalysisRecord(sourceRef, reportHash, block.timestamp, msg.sender);
        recordsBySource[sourceRef].push(record);
        emit AnalysisRecorded(sourceRef, reportHash, block.timestamp, msg.sender);
    }
    function getRecords(bytes32 sourceRef) external view returns (AnalysisRecord[] memory) { return recordsBySource[sourceRef]; }
}
