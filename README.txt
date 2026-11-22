COMP H2702 - Network Exposure Project Dataset

This package is designed for SAFE, LOCAL-ONLY network testing.

Target:
127.0.0.1 (localhost only)

Ports:
18080 - local HTTP test service
19090 - local banner service
20001 - local generic TCP service
20002 - intentionally not opened by the supplied test script

How to use:
1. Open Terminal 1.
2. Run: python local_test_services.py
3. Leave Terminal 1 running.
4. In Terminal 2, run your own network-exposure script.
5. Read targets.txt and ports.txt from your program.
6. Report which ports are OPEN or CLOSED.
7. Optional: perform a banner read on 19090 or 20001.
8. Optional: send a normal HTTP GET request to http://127.0.0.1:18080/

Scope:
- Use ONLY 127.0.0.1 and the supplied ports.
- Do not expand the project to scan external networks.
- Do not scan university, home-router, cloud or public IP ranges.

Note:
Port 20002 is expected to be CLOSED, but on rare systems another local application may already use that port.
