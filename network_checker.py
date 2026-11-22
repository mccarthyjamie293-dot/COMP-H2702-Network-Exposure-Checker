import socket
import http.client

def load_data(filename):
    data = []

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if line !="":
                    data.append(line)

    except FileNotFoundError:
        print("Error: Could not find", filename)

    return data

def validate_input(ip, port):
    if ip != "127.0.0.1":
        print("Error: Only localhost is allowed")
        return False

    try:
        port = int(port)

        if port not in [18080, 19090, 20001, 20002]:
            print("Error: Port is not approved")
            return False

        return True

    except ValueError:
        print("Error: Invalid port number")
        return False

def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, int(port)))

            if result == 0:
                return "OPEN"
            else:
                return "CLOSED"

    except (ValueError, OSError):
        return "ERROR"


def get_banner(ip, port):
    if not validate_input(ip, port):
        return "Invalid target or port"
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode("utf-8").strip()
            return banner

    except (OSError, UnicodeError):
        return "Could not read banner"

def check_http(ip, port):
    if not validate_input(ip, port):
        return "ERROR", "Invalid target or port"
    
    connection = None

    try:
        connection = http.client.HTTPConnection(ip, port, timeout=2)
        connection.request("GET", "/")

        response = connection.getresponse()

        status = response.status
        content_type = response.getheader("Content-Type")

        return status, content_type
    
    except (OSError, http.client.HTTPException):
        return "ERROR", "Unavailable"

    finally:
        if connection is not None:
            connection.close()


def save_report(results, open_count, closed_count):
    try:
        with open("network_report.txt", "w") as file:
            file.write("--- Network Exposure Report ---\n")

            for result in results:
                file.write(result + "\n")

            file.write("\n--- Port Summary ---\n")
            file.write("Open ports: " + str(open_count) + "\n")
            file.write("Closed ports: " + str(closed_count) + "\n")

        print("Report saved successfully")

    except OSError:
        print("Error saving report")



targets = load_data("targets.txt")
ports = load_data("ports.txt")
if not targets or not ports:
    print("Error: Required input files are missing or empty")
    exit()

print("Targets:", targets)
print("Ports:", ports)



open_count = 0
closed_count = 0
results = []

for port in ports:
    if not validate_input(targets[0], port):
        print("Skipping invalid input:", port)
        continue

    status = check_port(targets[0], port)
    print("Port", port, ":", status)
    results.append("Port " + port + " : " + status)

    if status == "OPEN":
        open_count += 1
    elif status == "CLOSED":
        closed_count += 1

print("\n--- Port Summary ---")
print("Open ports:", open_count)
print("Closed ports:", closed_count)

save_report(results, open_count, closed_count)

print("\n--- Service Banner ---")
banner = get_banner(targets[0], 19090)
print("Port 19090 banner:", banner)


try:
    with open("network_report.txt", "a") as file:
        file.write("\n--- Service Banner ---\n")
        file.write("Port 19090 banner: " + banner + "\n")

except OSError:
    print("Error: Could not save banner")


print("\n--- HTTP Service ---")

http_status, content_type = check_http(targets[0], 18080)

print("HTTP status:", http_status)
print("Content type:", content_type)

try:
    with open("network_report.txt", "a") as file:
        file.write("\n--- HTTP Service ---\n")
        file.write("HTTP status: " + str(http_status) + "\n")
        file.write("Content type: " + str(content_type) + "\n")

except OSError:
    print("Error: Could not save HTTP results")


print("\n--- Generic TCP Service ---")

generic_banner = get_banner(targets[0], 20001)

print("Port 20001 banner:", generic_banner)

try:
    with open("network_report.txt", "a") as file:
        file.write("\n--- Generic TCP Service ---\n")
        file.write("Port 20001 banner: " + generic_banner + "\n")

except OSError:
    print("Error: Could not save generic TCP results")

print("\n--- Security Analysis ---")

if http_status == 200:
    finding1 = "Port 18080 returned HTTP 200, showing the local HTTP service responded successfully."
else:
    finding1 = "The local HTTP service did not return a successful HTTP 200 response."

if open_count > 0:
    finding2 = str(open_count) + " open ports were detected. These services may require further security investigation."
else:
    finding2 = "No open ports were detected during this check."

finding3 = "An open port does not automatically mean a vulnerability exists. Further investigation is needed."


print(finding1)
print(finding2)
print(finding3)

try:
    with open("network_report.txt", "a") as file:
        file.write("\n--- Security Analysis ---\n")
        file.write(finding1 + "\n")
        file.write(finding2 + "\n")
        file.write(finding3 + "\n")

except OSError:
    print("Error: Could not save security analysis")
