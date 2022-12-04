import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from nft_image_query import get_nft_image

# load variables from .env
load_dotenv()

# setup we3 instance
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
nft_meta_json = os.getenv("NFT_IPFS_META_JSON")
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('./contracts/nft_handler.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("NFT_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )
    return contract

# load contract
contract = load_contract()

# streamlit frontend
# The user is be able to select an account for the contract owner from a list of accounts. 
# And, the user is be able to enter a URI that links to a piece of digital artwork
st.title("Register for a Certificate of membership token")
accounts = w3.eth.accounts
address = st.selectbox("Select account for membership", options=accounts)
artwork_uri = st.text_input("The URI to the artwork")



if st.button("Purchase a Certificate of Membership Token"):
    tx_hash = contract.functions.awardItem(address, nft_meta_json).transact({
        "from": address,
        "gas": 1000000,
        "value": Web3.toWei(1, "ether")
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write(contract.functions.getRecentTokenURI().call())

st.markdown("---")

################################################################################
# # Display a Token
# ################################################################################
st.markdown("## Display Certificate")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Artwork Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(get_nft_image(token_uri))

