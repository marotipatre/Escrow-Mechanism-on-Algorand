# Algorand Escrow Contract

Welcome to the **Algorand Escrow Contract**! This smart contract is designed to facilitate secure and trustless transactions in a decentralized marketplace using the Algorand blockchain. It incorporates an **escrow mechanism** and **dispute resolution system** to ensure fair and transparent transactions between buyers, sellers, and arbitrators.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Contract Functions](#contract-functions)
   - [Creating the Escrow](#creating-the-escrow)
   - [Depositing Funds](#depositing-funds)
   - [Releasing Funds](#releasing-funds)
   - [Refunding Funds](#refunding-funds)
   - [Raising a Dispute](#raising-a-dispute)
   - [Resolving a Dispute](#resolving-a-dispute)
   - [Expiring the Escrow](#expiring-the-escrow)
   - [Deleting the Contract](#deleting-the-contract)
4. [Workflow](#workflow)
5. [Use Cases](#use-cases)
6. [License](#license)

---

## Overview

The **Algorand Escrow Marketplace Contract** is a smart contract that enables secure transactions between buyers and sellers in a decentralized marketplace. It uses an escrow mechanism to hold funds until the transaction is completed or a dispute is resolved. The contract also includes a dispute resolution system, where a third-party arbitrator can intervene to resolve conflicts.

This contract is ideal for marketplaces where trust between buyers and sellers is limited, and a secure, transparent, and automated system is required to handle transactions.

---

## Key Features

- **Escrow Mechanism**: Funds are held securely in escrow until the transaction is completed or a dispute is resolved.
- **Dispute Resolution**: A third-party arbitrator can resolve disputes by releasing funds to the seller or refunding the buyer.
- **Time-Locks**: Funds are automatically refunded to the buyer if no action is taken within a specified time frame.
- **Multi-Signature Transactions**: Funds can only be released or refunded with the approval of the buyer, seller, or arbitrator.
- **Transparency**: All transactions are recorded on the Algorand blockchain, ensuring transparency and immutability.

---

## Contract Functions

### Creating the Escrow

- **`create_application`**: Initializes the escrow contract with the asset ID, price, seller, buyer, arbitrator, and escrow duration.
  - **Parameters**:
    - `value`: The price of the asset in microALGO.
    - `seller`: The account address of the seller.
    - `buyer`: The account address of the buyer.
    - `arbitrator`: The account address of the arbitrator.
    - `escrow_duration`: The duration (in seconds) for which the escrow will remain active.

---

### Depositing Funds

- **`deposit_funds`**: Allows the buyer to deposit funds into the escrow account.
  - **Parameters**:
    - `payment`: A payment transaction from the buyer to the escrow account.
  - **Checks**:
    - Only the buyer can deposit funds.
    - The payment must match the asset price.
    - The transaction must not already be settled.

---

### Releasing Funds

- **`release_funds_to_seller`**: Releases funds from the escrow to the seller.
  - **Checks**:
    - Only the buyer or arbitrator can call this function.
    - The transaction must not already be settled.

---

### Refunding Funds

- **`refund_funds_to_buyer`**: Refunds funds from the escrow to the buyer.
  - **Checks**:
    - Only the seller or arbitrator can call this function.
    - The transaction must not already be settled.

---

### Raising a Dispute

- **`raise_dispute`**: Allows the buyer or seller to raise a dispute.
  - **Checks**:
    - Only the buyer or seller can raise a dispute.
    - No dispute should already be raised.
    - The transaction must not already be settled.

---

### Resolving a Dispute

- **`resolve_dispute`**: Allows the arbitrator to resolve a dispute by releasing funds to the seller or refunding the buyer.
  - **Parameters**:
    - `decision`: A string indicating the resolution (`"release_to_seller"` or `"refund_to_buyer"`).
  - **Checks**:
    - Only the arbitrator can resolve disputes.
    - A dispute must be raised.
    - The transaction must not already be settled.

---

### Expiring the Escrow

- **`expire_escrow`**: Automatically refunds the buyer if the escrow expires without any action.
  - **Checks**:
    - The escrow duration must have passed.
    - The transaction must not already be settled.

---

### Deleting the Contract

- **`delete_application`**: Deletes the contract after the transaction is settled.
  - **Checks**:
    - Only the contract creator can delete the application.
    - The transaction must be settled.

---

## Workflow

1. **Setup**:
   - The seller creates the escrow contract with the asset details, price, and arbitrator.
   - The buyer deposits funds into the escrow.

2. **Transaction**:
   - If the transaction is successful, the buyer or arbitrator releases funds to the seller.
   - If the transaction fails, the seller or arbitrator refunds the buyer.

3. **Dispute**:
   - If a dispute arises, the arbitrator resolves it by releasing funds to the seller or refunding the buyer.

4. **Expiry**:
   - If no action is taken before the escrow expires, the funds are automatically refunded to the buyer.

---

## Use Cases

1. **Digital Asset Marketplace**:
   - Sellers can list digital assets (e.g., NFTs) with a fixed price.
   - Buyers can securely purchase assets using the escrow mechanism.

2. **Freelance Services**:
   - Clients can hold payments in escrow until the freelancer delivers the work.
   - Disputes can be resolved by a trusted arbitrator.

3. **Peer-to-Peer Trading**:
   - Buyers and sellers can trade assets without trusting each other, relying on the escrow and dispute resolution system.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---