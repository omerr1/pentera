import argparse
import subprocess
import time

class DevBox:
    def __init__(self, minion_count, base_minion_port=5001):
        self.minion_count = minion_count
        self.base_minion_port = base_minion_port
        self.minion_processes = []

    def start_minions(self):
        print(f"Starting {self.minion_count} Minion servers...")
        for i in range(self.minion_count):
            port = self.base_minion_port + i
            process = subprocess.Popen(['python', 'minion_server.py', '--port', str(port)])
            self.minion_processes.append((port, process))
            print(f"Minion started on port {port}")

    def start_master(self):
        minion_urls = [f"http://localhost:{port}" for port, _ in self.minion_processes]
        print(f"Starting Master server with Minion URLs: {minion_urls}")
        subprocess.Popen(['python', 'master_server.py', '--minions', ','.join(minion_urls)])
        print(f"Master started on port 5000")

    def run(self):
        try:
            self.start_minions()
            time.sleep(2)  # Allow Minions to initialize
            self.start_master()
        except Exception as e:
            print(f"Error initializing servers: {e}")
            self.stop_all()

    def stop_all(self):
        print("Shutting down all servers...")
        for _, process in self.minion_processes:
            process.terminate()
        print("All Minions stopped.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialize Master and Minion servers.")
    parser.add_argument('--minions', type=int, default=1, help="Number of Minion servers to start")
    args = parser.parse_args()

    dev_box = DevBox(minion_count=args.minions)
    dev_box.run()
