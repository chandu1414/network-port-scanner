from flask import Flask, render_template, request, Response
import socket
import threading
import queue
import time
import json

app = Flask(__name__)

# Queue to hold the scan results to be streamed to the client
scan_queue = queue.Queue()
is_scanning = False

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            scan_queue.put({'port': port, 'status': 'open'})
        sock.close()
    except Exception as e:
        pass

def run_scan(ip, start_port=1, end_port=1024):
    global is_scanning
    is_scanning = True
    threads = []
    
    scan_queue.put({'message': f"Starting scan on target: {ip}"})
    scan_queue.put({'message': f"Scanning ports {start_port} to {end_port}...\n"})
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()
        
        # Slight delay to avoid too many threads at once and make the terminal effect visible
        if port % 50 == 0:
            time.sleep(0.1)

    for thread in threads:
        thread.join()
        
    scan_queue.put({'message': "\nScan completed."})
    is_scanning = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream_scan')
def stream_scan():
    ip = request.args.get('ip', '127.0.0.1')
    
    global is_scanning
    if is_scanning:
        return "Scan already running", 400
        
    # Start the scan in a separate thread
    threading.Thread(target=run_scan, args=(ip, 1, 1024)).start()
    
    def generate():
        global is_scanning
        while is_scanning or not scan_queue.empty():
            try:
                # Wait for up to 1 second for a new item
                data = scan_queue.get(timeout=1.0)
                yield f"data: {json.dumps(data)}\n\n"
            except queue.Empty:
                pass
                
        # Send a final event to close the connection
        yield f"data: {json.dumps({'status': 'done'})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
