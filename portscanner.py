# -*- coding: utf-8 -*-
# ============================================================
#  PortScanner — CLI v1.0
#  A terminal-based port scanner
#  Concepts: sockets, threading, try/except, file writing
# ============================================================

import socket
import threading
import datetime
import sys
import os

# ── GLOBALS ───────────────────────────────────────────────
# A list to store all open ports found during the scan
open_ports = []

# A lock prevents multiple threads writing to the list at the same time
# Without this, threads would overwrite each other's results
lock = threading.Lock()

# Well-known port names — maps port numbers to service names
PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}


# ============================================================
#  CORE SCANNER
# ============================================================

def scan_port(ip, port, timeout):
    """
    Tries to connect to a single port.
    If successful, the port is open — add it to the list.
    
    try/except handles errors gracefully instead of crashing.
    """
    try:
        # Create a TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)  # Don't wait longer than timeout seconds

        # connect_ex() returns 0 if connection succeeded (port open)
        # Any other number means the port is closed or filtered
        result = s.connect_ex((ip, port))

        if result == 0:
            # Lock the list before writing to it (thread safety)
            with lock:
                open_ports.append(port)

        s.close()  # Always close the socket when done

    except socket.error:
        pass  # Silently ignore connection errors


def scan_range(ip, ports, timeout):
    """
    Scans a range of ports using multiple threads.
    Threading lets us scan many ports simultaneously — much faster.
    """
    threads = []

    for port in ports:
        # Create a thread for each port
        # target = the function to run
        # args = the arguments to pass to that function
        t = threading.Thread(target=scan_port, args=(ip, port, timeout))
        threads.append(t)
        t.start()  # Start the thread immediately

    # Wait for ALL threads to finish before continuing
    for t in threads:
        t.join()


# ============================================================
#  DISPLAY & REPORTING
# ============================================================

def print_banner():
    print("\n" + "=" * 55)
    print("          PORTSCANNER — CLI v1.0")
    print("          Network Reconnaissance Tool")
    print("=" * 55)


def print_results(ip, start_port, end_port, duration):
    """Displays scan results in a clean table."""

    print(f"\n  Scan complete in {duration:.2f} seconds")
    print(f"  Target : {ip}")
    print(f"  Range  : {start_port} - {end_port}")
    print(f"  Found  : {len(open_ports)} open port(s)\n")

    if not open_ports:
        print("  No open ports found.\n")
        return

    print("  " + "-" * 40)
    print(f"  {'PORT':<10} {'SERVICE':<15} {'STATUS'}")
    print("  " + "-" * 40)

    # Sort ports numerically before displaying
    for port in sorted(open_ports):
        # .get() looks up the port in PORT_NAMES
        # If not found, returns "Unknown" as default
        service = PORT_NAMES.get(port, "Unknown")
        print(f"  {port:<10} {service:<15} OPEN")

    print("  " + "-" * 40 + "\n")


def save_report(ip, start_port, end_port, duration):
    """Saves scan results to a .txt file."""

    # datetime.now() gets the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename  = f"scan_{ip}_{timestamp}.txt"

    # 'w' means write mode — creates the file if it doesn't exist
    with open(filename, 'w') as f:
        f.write("=" * 55 + "\n")
        f.write("  PORTSCANNER REPORT\n")
        f.write("=" * 55 + "\n")
        f.write(f"  Target    : {ip}\n")
        f.write(f"  Range     : {start_port} - {end_port}\n")
        f.write(f"  Duration  : {duration:.2f} seconds\n")
        f.write(f"  Timestamp : {timestamp}\n")
        f.write(f"  Open ports: {len(open_ports)}\n\n")

        if open_ports:
            f.write(f"  {'PORT':<10} {'SERVICE':<15} STATUS\n")
            f.write("  " + "-" * 35 + "\n")
            for port in sorted(open_ports):
                service = PORT_NAMES.get(port, "Unknown")
                f.write(f"  {port:<10} {service:<15} OPEN\n")
        else:
            f.write("  No open ports found.\n")

    print(f"  Report saved to: {filename}\n")


# ============================================================
#  INPUT VALIDATION
# ============================================================

def validate_ip(ip):
    """Checks if the IP address format is valid."""
    try:
        socket.inet_aton(ip)  # Throws an error if IP is invalid
        return True
    except socket.error:
        return False


def get_input():
    """Collects and validates user input."""

    print("\n  Target IP (e.g. 127.0.0.1 to scan yourself):")
    ip = input("  > ").strip()

    if not validate_ip(ip):
        print("  Invalid IP address.")
        return None, None, None, None

    print("\n  Start port (1-65535):")
    start = input("  > ").strip()

    print("  End port (1-65535):")
    end = input("  > ").strip()

    # int() converts string to integer
    # We wrap in try/except in case the user types letters instead of numbers
    try:
        start = int(start)
        end   = int(end)
    except ValueError:
        print("  Ports must be numbers.")
        return None, None, None, None

    if not (1 <= start <= 65535 and 1 <= end <= 65535 and start <= end):
        print("  Invalid port range.")
        return None, None, None, None

    print("\n  Timeout per port in seconds (default 0.5):")
    timeout_input = input("  > ").strip()
    timeout = float(timeout_input) if timeout_input else 0.5

    return ip, start, end, timeout


# ============================================================
#  MAIN
# ============================================================

def main():
    # sys.stdout.reconfigure fixes Windows encoding for special characters
    sys.stdout.reconfigure(encoding='utf-8')

    print_banner()

    print("""
  WARNING: Only scan systems you own or have explicit
  permission to scan. Unauthorized scanning is illegal.
    """)

    while True:
        print("  [1]  Start Scan")
        print("  [2]  Exit")
        print("-" * 55)

        choice = input("  Choose: ").strip()

        if choice == "1":
            ip, start, end, timeout = get_input()

            if ip is None:
                continue

            # Clear previous results before a new scan
            open_ports.clear()

            print(f"\n  Scanning {ip} ports {start}-{end} ...")
            print("  Please wait...\n")

            # Record start time to calculate duration
            start_time = datetime.datetime.now()

            # Split port range into chunks of 100 for threading
            # range() generates a sequence of numbers
            chunk_size = 100
            for i in range(start, end + 1, chunk_size):
                # min() makes sure we don't go past the end port
                chunk = range(i, min(i + chunk_size, end + 1))
                scan_range(ip, chunk, timeout)

            # Calculate how long the scan took
            duration = (datetime.datetime.now() - start_time).total_seconds()

            print_results(ip, start, end, duration)

            save = input("  Save report to file? (y/n): ").strip().lower()
            if save == 'y':
                save_report(ip, start, end, duration)

        elif choice == "2":
            print("\n  Goodbye.\n")
            break

        else:
            print("\n  Enter 1 or 2.\n")


if __name__ == "__main__":
    main()