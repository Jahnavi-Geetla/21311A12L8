from flask import Flask, jsonify, request
import requests
import threading
import time

app = Flask(_name_)
window_size = 10
number_window = []
lock = threading.Lock()

def fetch_numbers_from_test_server(number_id):
    url = f"https://testserver.com/numbers/{number_id}"  # Replace with actual test server URL
    try:
        response = requests.get(url, timeout=0.5)  # Set timeout to 500 ms
        if response.status_code == 200:
            numbers = response.json().get("numbers", [])
            return numbers
    except requests.exceptions.RequestException:
        return []
    return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    numbers = fetch_numbers_from_test_server(number_id)
    with lock:
        prev_state = number_window.copy()
        for number in numbers:
            if number not in number_window:
                if len(number_window) >= window_size:
                    number_window.pop(0)  # Remove the oldest number
                number_window.append(number)
        curr_state = number_window.copy()
        avg = sum(curr_state) / len(curr_state) if curr_state else 0

    response = {
        "numbers": numbers,
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "avg": round(avg, 2)
    }
    return jsonify(response)

if _name_ == '_main_':
    app.run(debug=True)