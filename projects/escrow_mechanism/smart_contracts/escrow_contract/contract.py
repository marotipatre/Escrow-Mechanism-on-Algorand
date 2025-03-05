from algopy import *
from algopy.arc4 import abimethod


class EscrowMarketplace(ARC4Contract):
    # State variables
    seller: Account
    buyer: Account
    arbitrator: Account # third-party
    amount: UInt64
    escrow_expiry: UInt64  
    is_disputed: bool
    is_settled: bool



    @abimethod(allow_actions=["NoOp"], create="require")
    def create_application(
        self,
        value: UInt64,
        seller: Account,
        buyer: Account,
        arbitrator: Account,
        escrow_duration: UInt64,  # Duration in seconds
    ) -> None:
        self.value = value
        self.seller = seller
        self.buyer = buyer
        self.arbitrator = arbitrator
        self.escrow_expiry = Global.latest_timestamp + escrow_duration
        self.is_disputed = False
        self.is_settled = False

    # Deposit funds into escrow (called by buyer)
    @abimethod()
    def deposit_funds(self, payment: gtxn.PaymentTransaction) -> None:
        assert Txn.sender == self.buyer, "Only the buyer can deposit funds"
        assert payment.receiver == Global.current_application_address, "Payment must be sent to the escrow"
        assert payment.amount == self.value, "Payment must match the asset price"
        assert not self.is_settled, "Transaction is already settled"

    # Release funds to seller (called by buyer or arbitrator)
    @abimethod()
    def release_funds_to_seller(self) -> None:
        assert Txn.sender in (self.buyer, self.arbitrator), "Only buyer or arbitrator can release funds"
        assert not self.is_settled, "Transaction is already settled"

        # Transfer funds to seller
        itxn.Payment(
            receiver=self.seller,
            amount=self.value,
            fee=1_000,
        ).submit()

        # Mark as settled
        self.is_settled = True

    # Refund funds to buyer (called by seller or arbitrator)
    @abimethod()
    def refund_funds_to_buyer(self) -> None:
        assert Txn.sender in (self.seller, self.arbitrator), "Only seller or arbitrator can refund funds"
        assert not self.is_settled, "Transaction is already settled"

        # Transfer funds back to buyer
        itxn.Payment(
            receiver=self.buyer,
            amount=self.value,
            fee=1_000,
        ).submit()

        # Mark as settled
        self.is_settled = True

    # Raise a dispute (called by buyer or seller)
    @abimethod()
    def raise_dispute(self) -> None:
        assert Txn.sender in (self.buyer, self.seller), "Only buyer or seller can raise a dispute"
        assert not self.is_disputed, "Dispute already raised"
        assert not self.is_settled, "Transaction is already settled"

        self.is_disputed = True

    # Resolve dispute (called by arbitrator)
    @abimethod()
    def resolve_dispute(self, decision: String) -> None:
        assert Txn.sender == self.arbitrator, "Only the arbitrator can resolve disputes"
        assert self.is_disputed, "No dispute to resolve"
        assert not self.is_settled, "Transaction is already settled"

        if decision == "release_to_seller":
            self.release_funds_to_seller()
        elif decision == "refund_to_buyer":
            self.refund_funds_to_buyer()
        else:
            assert False, "Invalid decision"

        # Mark as settled
        self.is_settled = True

    # Time-lock: Automatically refund buyer if escrow expires
    @abimethod()
    def expire_escrow(self) -> None:
        assert Global.latest_timestamp >= self.escrow_expiry, "Escrow has not expired yet"
        assert not self.is_settled, "Transaction is already settled"

        # Refund buyer
        self.refund_funds_to_buyer()

    # Delete the application (only after settlement)
    @abimethod(allow_actions=["DeleteApplication"])
    def delete_application(self) -> None:
        assert self.is_settled, "Transaction must be settled before deleting"
        assert Txn.sender == Global.creator_address, "Only the creator can delete the application"