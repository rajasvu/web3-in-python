import requests

def get_nft_image(nft_uri):
    meta_data = requests.get(nft_uri)
    return meta_data.json()["image"]

if __name__== "__main__":
    get_nft_image("nft-meta-file-url-on-ipfs")