import { ethers } from 'hardhat';
async function main(){const registry=await ethers.deployContract('AnalysisRegistry');await registry.waitForDeployment();console.log('AnalysisRegistry:',await registry.getAddress());}
main().catch((e)=>{console.error(e);process.exitCode=1});
