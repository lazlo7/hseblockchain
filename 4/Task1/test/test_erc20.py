import pytest
from web3 import Web3
import json
import os


@pytest.fixture(scope="module")
def deploy_contract():
    # We use fixture to reuse the same state for all tests.
    # We already got the contract compiled, so we simply read the abi and bytecode
    with open("./Task1/artifacts/contracts/MyToken.sol/MyToken.json", "r") as mytoken_json:
        mytoken_json = json.load(mytoken_json)
        abi = mytoken_json["abi"]
        bytecode = mytoken_json["bytecode"]

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    chain_id = 31337

    # We get this from npx hardhat node output, just like before.
    sender_privkey    = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  
    receiver1_privkey = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
    receiver2_privkey = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"

    sender_account    = w3.eth.account.from_key(sender_privkey)
    receiver1_account = w3.eth.account.from_key(receiver1_privkey)
    receiver2_account = w3.eth.account.from_key(receiver2_privkey)

    sender_address    = sender_account.address
    receiver1_address = receiver1_account.address
    receiver2_address = receiver2_account.address

    # Deploy the contract and mint tokens.
    MyToken = w3.eth.contract(abi=abi, bytecode=bytecode)
    initial_supply = w3.to_wei(10_000, "ether")

    construct_txn = MyToken.constructor(
        "LolToken",
        "LOL",
        initial_supply
    ).build_transaction(
        {
            "from": sender_address,
            "nonce": w3.eth.get_transaction_count(sender_address),
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
        }
    )
    signed_txn = sender_account.sign_transaction(construct_txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

    return {
        "w3": w3,
        "chain_id": chain_id,
        "contract": contract,
        "sender_account": sender_account,
        "receiver1_account": receiver1_account,
        "receiver2_account": receiver2_account,
        "sender_address": sender_address,
        "receiver1_address": receiver1_address,
        "receiver2_address": receiver2_address,
    }


def test_transfer_to_receiver1(deploy_contract):
    """
    Testing:
        1) Sender has 10,000 tokens initially.
        2) Transfers 100 tokens to Receiver_1.
        3) Checks that Receiver_1 has 100, and Sender has 9,900.
    """
    info       = deploy_contract
    w3         = info["w3"]
    contract   = info["contract"]
    sender_acc = info["sender_account"]
    sender_adr = info["sender_address"]
    r1_adr     = info["receiver1_address"]
    chain_id   = info["chain_id"]

    transfer_amount = w3.to_wei(100, "ether")

    # Build & sign the transfer tx
    transfer_tx = contract.functions.transfer(r1_adr, transfer_amount).build_transaction(
        {
            "from": sender_adr,
            "nonce": w3.eth.get_transaction_count(sender_adr),
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
        }
    )
    signed_transfer_tx = sender_acc.sign_transaction(transfer_tx)
    tx_hash = w3.eth.send_raw_transaction(signed_transfer_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Verify balances
    sender_balance   = contract.functions.balanceOf(sender_adr).call()
    receiver1_balance = contract.functions.balanceOf(r1_adr).call()

    assert sender_balance == w3.to_wei(9_900, "ether"), "Sender balance should be 9900 tokens"
    assert receiver1_balance == w3.to_wei(100, "ether"), "Receiver_1 balance should be 100 tokens"


def test_transfer_to_receiver2(deploy_contract):
    """
    Testing:
        1) At this point, the Sender should have 9,900 tokens (after the first test).
        2) Transfer 300 tokens to Receiver_2.
        3) Checks that Receiver_2 now has 300, and Sender has 9,600.
           (Because they've already transferred 100 in the previous test.)
    """
    info       = deploy_contract
    w3         = info["w3"]
    contract   = info["contract"]
    sender_acc = info["sender_account"]
    sender_adr = info["sender_address"]
    r2_adr     = info["receiver2_address"]
    chain_id   = info["chain_id"]

    transfer_amount = w3.to_wei(300, "ether")

    # Build & sign the transfer tx
    transfer_tx = contract.functions.transfer(r2_adr, transfer_amount).build_transaction(
        {
            "from": sender_adr,
            "nonce": w3.eth.get_transaction_count(sender_adr),
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
        }
    )
    signed_transfer_tx = sender_acc.sign_transaction(transfer_tx)
    tx_hash = w3.eth.send_raw_transaction(signed_transfer_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    # Verify balances
    sender_balance   = contract.functions.balanceOf(sender_adr).call()
    receiver2_balance = contract.functions.balanceOf(r2_adr).call()

    assert sender_balance == w3.to_wei(9_600, "ether"), "Sender balance should be 9,600 tokens"
    assert receiver2_balance == w3.to_wei(300, "ether"), "Receiver_2 balance should be 300 tokens"
