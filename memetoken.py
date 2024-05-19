import json
from solana.keypair import Keypair
from solana.rpc import Client
from spl.token.instructions import TokenInstruction
from spl.token import Account, Token
import spl.protocol.token as token_pb2

# Ganti nilai berikut sesuai keinginan Anda:
LOLLY_IMAGE_URL = "https://example.com/lolly.png"  # URL gambar meme Lolly Anda
LOLLY_NAME = "Lolly Token"  # Nama token Anda
LOLLY_SYMBOL = "LOL"  # Simbol token Anda
DECIMALS = 9  # Jumlah desimal token Anda (Solana menggunakan desimal 9)
TOTAL_SUPPLY = 100000000  # Total supply token Anda

# Ganti dengan wallet address dan private key Solana Anda (**JANGAN DIBAGIKAN!**):
YOUR_WALLET_ADDRESS = "your_wallet_address"
YOUR_PRIVATE_KEY = "your_private_key"

# Ganti dengan URL endpoint Solana node (sesuaikan dengan node yang Anda gunakan)
SOLANA_RPC_URL = "https://api.devnet.solana.com"


def deploy_lolly_token():
    # Inisialisasi client Solana
    client = Client(SOLANA_RPC_URL)

    # Buat wallet dari private key
    wallet = Keypair.from_secret_key(bytes.fromhex(YOUR_PRIVATE_KEY))

    # Buat token mint account
    mint_account = Keypair()
    mint_account_address = mint_account.public_key

    # Buat token account untuk wallet Anda
    token_account = Keypair()
    token_account_address = token_account.public_key

    # Buat instruksi create token account
    create_token_account_ix = TokenInstruction.create_account(
        mint_account_address,
        token_account_address,
        wallet.public_key
    )

    # Buat instruksi initialize mint
    initialize_mint_ix = TokenInstruction.initialize_mint(
        mint_account_address,
        DECIMALS,
        wallet.public_key
    )

    # Buat instruksi mint token
    mint_to_ix = TokenInstruction.mint_to(
        mint_account_address,
        token_account_address,
        wallet.public_key,
        TOTAL_SUPPLY
    )

    # Buat instruksi metadata program
    metadata_program_id = "metadatix.solana.com"
    metadata_account = Keypair()
    metadata_account_address = metadata_account.public_key

    # Buat instruksi create metadata account
    create_metadata_account_ix = spl.token.instructions.CreateMetadataAccountInstruction(
        metadata_program_id,
        metadata_account_address,
        mint_account_address,
        wallet.public_key,
        LOLLY_NAME,
        LOLLY_SYMBOL,
        LOLLY_IMAGE_URL,
        []
    )

    # Buat instruksi update metadata account
    update_metadata_account_ix = spl.token.instructions.UpdateMetadataAccountInstruction(
        metadata_program_id,
        metadata_account_address,
        [],
        [],
        [],
        [],
        wallet.public_key
    )

    # Buat transaction
    transaction = client.transaction()
    transaction.add_instruction(create_token_account_ix)
    transaction.add_instruction(initialize_mint_ix)
    transaction.add_instruction(mint_to_ix)
    transaction.add_instruction(create_metadata_account_ix)
    transaction.add_instruction(update_metadata_account_ix)

    # Sign transaction
    transaction.sign(wallet)

    # Submit transaction
    tx_hash = client.send_transaction(transaction)
    print(f"Lolly Token deployed to address: {mint_account_address}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    deploy_lolly_token()
