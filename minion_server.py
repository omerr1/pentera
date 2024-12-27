import argparse
from flask import Flask, request, jsonify
from multiprocessing import Pool
from hash_cracker import HashCracker


class MinionServer:
    def __init__(self, port):
        self.app = Flask(__name__)
        self.port = port
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/crack-phone-number-md5", methods=["POST"])
        def crack_phone_number_md5():
            data = request.json
            return self._handle_crack_request(data)

    def _handle_crack_request(self, data):
        hashes_to_crack = data["hashes"]
        start = data["start"]
        end = data["end"]

        print(f"Cracking {len(hashes_to_crack)} hashes from {start} to {end}")
        results = self._crack_hashes(hashes_to_crack, start, end)
        return jsonify({"passwords": results})

    def _crack_hashes(self, hashes_to_crack, start, end):
        results = {h: None for h in hashes_to_crack}

        for num in range(start, end + 1):
            filled_number = str(num).zfill(8)
            phone_number = f"05{filled_number[0]}-{filled_number[1:]}"

            # Try this phone number against all remaining uncracked hashes
            for hash_val in [h for h, p in results.items() if p is None]:
                if self.try_password(hash_val, phone_number):
                    results[hash_val] = phone_number

            # If all hashes are cracked, we can stop early
            if all(results.values()):
                break

        return results

    @staticmethod
    def try_password(hash_to_crack, password):
        return password if HashCracker.compare_md5(hash_to_crack, password) else None

    def run(self):
        self.app.run(host="localhost", port=self.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Minion server.")
    parser.add_argument(
        "--port", type=int, required=True, help="Port to run the Minion server"
    )
    args = parser.parse_args()

    server = MinionServer(port=args.port)
    server.run()
