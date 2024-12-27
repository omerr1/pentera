import hashlib


class HashCracker:
    @staticmethod
    def compare_md5(hash_to_crack, input_data):
        return hashlib.md5(input_data.encode()).hexdigest() == hash_to_crack

    # Other hash types for future use
    @staticmethod
    def compare_sha256(hash_to_crack, input_data):
        return hashlib.sha256(input_data.encode()).hexdigest() == hash_to_crack

    @staticmethod
    def compare_sha512(hash_to_crack, input_data):
        return hashlib.sha512(input_data.encode()).hexdigest() == hash_to_crack
