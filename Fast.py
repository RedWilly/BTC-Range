import os
import time
import hashlib
from ecdsa import SigningKey, SECP256k1
from base58 import b58encode_check
from multiprocessing import Pool, cpu_count, Manager, Process

TARGET_ADDRESS = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
FOUND_FILE = "foundit.txt"
LOG_INTERVAL = 5  # seconds

def sha256(data):
    return hashlib.sha256(data).digest()

def ripemd160(data):
    return hashlib.new("ripemd160", data).digest()

def get_public_key(private_key, compressed=True):
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    x, y = vk.pubkey.point.x(), vk.pubkey.point.y()
    if compressed:
        return (b'\x02' if y % 2 == 0 else b'\x03') + x.to_bytes(32, 'big')
    else:
        return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

def generate_bitcoin_address(public_key):
    extended_key = b'\x00' + ripemd160(sha256(public_key))
    return b58encode_check(extended_key)

def check_key(private_key_hex, found_flag, counter):
    private_key = bytes.fromhex(private_key_hex)
    public_key_compressed = get_public_key(private_key, compressed=True)
    address_compressed = generate_bitcoin_address(public_key_compressed).decode('utf-8')

    counter.value += 1
    if address_compressed == TARGET_ADDRESS:
        with open(FOUND_FILE, "a") as f:
            f.write(f"Private key: {private_key_hex}\nAddress: {TARGET_ADDRESS}\n")
        found_flag.value = 1
        return True
    return False

def worker(start, end, found_flag, counter):
    current_int = start
    while current_int < end and not found_flag.value:
        private_key_hex = hex(current_int)[2:].zfill(64)
        if check_key(private_key_hex, found_flag, counter):
            print(f"Match found with key: {private_key_hex}")
            break
        current_int += 1

def log_counters(counters):
    while True:
        total = sum(counter.value for counter in counters)
        print(f"Total Keys Scanned: {total}", end="\r")
        time.sleep(LOG_INTERVAL)

def main():
    start_hex = "0000000000000000000000000000000000000000000000020000000000000000"
    end_hex = "000000000000000000000000000000000000000000000003ffffffffffffffff"

    start_int = int(start_hex, 16)
    end_int = int(end_hex, 16)
    range_size = (end_int - start_int) // cpu_count()

    with Manager() as manager:
        found_flag = manager.Value('i', 0)
        counters = [manager.Value('i', 0) for _ in range(cpu_count())]

        with Pool(cpu_count()) as pool:
            pool.starmap_async(worker, [(start_int + i * range_size, start_int + (i + 1) * range_size, found_flag, counters[i]) for i in range(cpu_count())])

            log_process = Process(target=log_counters, args=(counters,))
            log_process.start()

            pool.close()
            pool.join()

        log_process.terminate()

if __name__ == "__main__":
    main()
