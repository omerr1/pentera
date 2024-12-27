Requirements:
- Python 3.10+
- pip install -r requirements.txt

To run the project we use the devbox. Just run the following command in the terminal:
```
python dev_box.py --minions 10
```

* Itll create 10 minions and a master server.
- The master server will be running on port 5000.
- The minions will be running on ports 5001 to 5010.

To use the API we can use that curl command:
```
curl --location 'http://localhost:5000/crack' \
--header 'Content-Type: application/json' \
--data '{"hashes": ["884da840d90406ec7ce0ef5da231353c", "662ec13a6ff8f7e5b1dd27298e7dddf9"]}'
```
which will return - 
```
{
    "passwords": {
        "662ec13a6ff8f7e5b1dd27298e7dddf9": "056-1906033",
        "884da840d90406ec7ce0ef5da231353c": "050-4000033"
    }
}
```

In general we store requests in a queue and process them in a worker thread.
I thought about implementing multiprocess in the minion servers as well but couldnt really make it work on my machine due to resource constraints.
overall it takes around a minute to crack a list of passwords.

Future Improvements:
    - Minion Multi-Process
    - Master detection of Minion crashes (Currently, with this architecture, I can detect it but cant really do anything about it)
    - Better understanding of the domain and password cracking - compare the results to actual softwares such as hashcat.
