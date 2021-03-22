pragma solidity ^0.6.6;

contract Bank {
    
    using SafeMath for uint256;
    
    mapping(address => uint256) balances;   //Balances of addresses
    mapping(address => bool) isEnrolled;    //Is address already enrolled
    
    address public owner;   //Owner of the smart contract
    uint256 totalSupply_;   //Total supply of Omnies
    
    // Events
    event logFile(address indexed accountAddress, string linkToOGF, string fileName, string fileHash, int totalSize);
    event logChunk(address indexed accountAddress, string indexed linkToOGF, string senderGUID, string receiverGUID, string chunkHash, int chunkNb);
    event logDeletion(address indexed accountAddress, string indexed linkToOGF);
    
    // @notice Create the bank with an initial amount of stashies
    constructor(uint256 total) public {
        totalSupply_ = total;
        balances[msg.sender] = totalSupply_;
        owner = msg.sender;
    }


    /// @notice Enroll a customer with the bank, giving them an initial amount of Omnies
    /// @return The balance of the user after enrolling
    function enroll() public returns (uint256) {
        require(isEnrolled[msg.sender] == false);
        balances[msg.sender] = 5000;
        isEnrolled[msg.sender] = true;
        return balances[msg.sender];
    }

    /// @notice Give Omnies
    /// @return Balance after the deposit is made
    function giveOmnies() public returns (uint256) {
        balances[msg.sender] = balances[msg.sender].add(10);
        return balances[msg.sender];
    }

    /// @notice Read balance of the account
    /// @return The balance of the user
    function myBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    function totalSupply() public view returns (uint256) {
        return totalSupply_;
    }
    
    
    /// @notice Log file upload and deduct Omnies
    function uploadFile(string memory linkToOGF, string memory fileName, string memory fileHash, int totalSize) public {
        emit logFile(msg.sender, linkToOGF, fileName, fileHash, totalSize);
        balances[msg.sender] = balances[msg.sender].sub(50);
    }
    
    /// @notice Log Chunk upload
    function uploadChunk(string memory linkToOGF, string memory senderGUID, string memory receiverGUID, string memory chunkHash, int chunkNb) public {
        emit logChunk(msg.sender, linkToOGF, senderGUID, receiverGUID, chunkHash, chunkNb);
    }
    
    /// @notice Log file deletion
    function deleteFile(string memory linkToOGF) public {
        emit logDeletion(msg.sender, linkToOGF);
    }
}

library SafeMath {
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
      assert(b <= a);
      return a - b;
    }
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
      uint256 c = a + b;
      assert(c >= a);
      return c;
    }
}