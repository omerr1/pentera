import argparse
import requests
from flask import Flask, request, jsonify
import threading

class MasterServer:
    def __init__(self, minion_urls):
        self.app = Flask(__name__)
        self.minion_urls = minion_urls
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/crack', methods=['POST'])
        def crack():
            data = request.json
            return self._handle_crack_request(data)

    def _handle_crack_request(self, data):
        hashes_to_crack = data['hashes']
        found_passwords = {h: None for h in hashes_to_crack}
        stop_event = threading.Event()

        threads = self._spawn_minion_threads(hashes_to_crack, found_passwords, stop_event)
        self._wait_for_completion(threads, stop_event)

        return jsonify({'passwords': found_passwords})

    def _spawn_minion_threads(self, hashes_to_crack, found_passwords, stop_event):
        step = 100_000_000 // len(self.minion_urls)
        threads = []
        
        for i, url in enumerate(self.minion_urls):
            start, end = i * step, (i + 1) * step - 1
            thread = threading.Thread(
                target=self._request_minion,
                args=(url, start, end, hashes_to_crack, found_passwords, stop_event)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        return threads

    def _request_minion(self, url, start, end, hashes_to_crack, found_passwords, stop_event):
        try:
            response = requests.post(
                url + '/crack-phone-number-md5', 
                json={'hashes': hashes_to_crack, 'start': start, 'end': end}
            )
            if response.status_code == 200:
                results = response.json().get('passwords', {})
                if any(results.values()):
                    for hash_val, password in results.items():
                        if password:
                            found_passwords[hash_val] = password
                    if all(found_passwords.values()):
                        stop_event.set()
        except requests.exceptions.RequestException:
            pass

    def _wait_for_completion(self, threads, stop_event):
        while not stop_event.is_set() and any(t.is_alive() for t in threads):
            stop_event.wait(0.1)

    def run(self):
        self.app.run(host='localhost', port=5000)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Master server.")
    parser.add_argument('--minions', type=str, required=True, help="Comma-separated list of Minion URLs")
    args = parser.parse_args()

    minion_urls = args.minions.split(',')
    server = MasterServer(minion_urls=minion_urls)
    server.run()
