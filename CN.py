import streamlit as st
import json
import base64
from io import BytesIO

# --- (1) DATA INITIALIZATION ---
# This is the "database" of your app.
# It's populated with all the rich content from the CST 303 syllabus.

def get_initial_data():
    """
    Initializes the session state with all syllabus modules, topics,
    definitions, tips, and PYQs for CST 303 Computer Networks.
    This is the master data structure.
    """
    return {
        "modules": {
            "Module 1: Intro & Physical Layer": {
                "OSI vs. TCP/IP Reference Models": {
                    "definition": """
                    **Reference Models** are conceptual frameworks that standardize the functions of a communication system into a series of layers.

                    **OSI Reference Model (Open Systems Interconnection):**
                    A 7-layer model (Physical, Data Link, Network, Transport, Session, Presentation, Application). It's a comprehensive, theoretical model.
                    [Image of the OSI Reference Model layers]

                    **TCP/IP Reference Model:**
                    A 4-layer or 5-layer model (Link, Internet, Transport, Application) that is the practical basis for the modern Internet.
                    [Image of the TCP/IP model layers]

                    **Comparison:**
                    * OSI is prescriptive (defines what *should* be done), TCP/IP is descriptive (describes what the Internet *does*).
                    * OSI has 7 layers, TCP/IP has 4 or 5 (e.g., OSI's Session/Presentation are part of TCP/IP's Application layer).
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Compare TCP/IP and OSI reference model.'\n* 'With a neat diagram, explain Open Systems Interconnection (OSI) Reference Model.'",
                    "strategy": "Do not just list the layers. For a 14-mark question, you must explain the *function* of each layer in both models and then provide a detailed comparison. Create a table: Layer Name (OSI), Layer Name (TCP/IP), and Key Functions/Protocols. This is a high-yield topic to memorize.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Physical Layer Topologies & Modes": {
                    "definition": """
                    **Physical Topology:** The layout of the network (how nodes are connected).
                    * **Bus:** All nodes share a single cable. (Old)
                    * **Star:** All nodes connect to a central hub or switch. (Most common LAN topology)
                    * **Ring:** Nodes are connected in a circle.
                    * **Mesh:** Every node is connected to every other node (or many other nodes).

                    **Communication Modes:**
                    * **Simplex:** One-way communication (e.g., Radio, TV broadcast).
                    * **Half-Duplex:** Two-way communication, but *not at the same time* (e.g., Walkie-talkie).
                    * **Full-Duplex:** Two-way communication, simultaneously (e.g., Telephone call, modern Ethernet).
                    """,
                    "pyq_focus": "Explain the various physical topologies with neat sketches.\n* 'Define simplex, half-duplex, and full-duplex transmission modes. Give one example for each.'",
                    "strategy": "These are common 3-mark (Part A) questions. Be able to draw the 4 main topologies and give a 1-sentence definition and one pro/con for each. The communication modes are also a classic definition question.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Signal Encoding": {
                    "definition": """
                    How data (bits) is converted into a physical signal (voltage) to be sent over a wire.
                    * **NRZ (Non-Return to Zero):** 1 = high voltage, 0 = low voltage. Simple, but has problems with long strings of 0s or 1s (clock synchronization).
                    * **Manchester Encoding:** Transmits the clock and data combined. 0 = high-to-low transition, 1 = low-to-high transition (or vice-versa).
                    * **Differential Manchester:** 0 = transition at the start of the bit period, 1 = no transition at the start. (Always has a transition in the middle).
                    """,
                    "pyq_focus": "'Sketch the waveform in Manchester and Differential Manchester Encoding for the bitstream 11000110010.'",
                    "strategy": "This is a 'practice-by-hand' question. Get a bitstream from the textbook and draw the waveforms for Manchester and Differential Manchester. Pay close attention to the *transitions* in the middle of the bit period. This is a very common numerical-style question.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Transmission Media": {
                    "definition": """
                    The physical path between transmitter and receiver.
                    * **Guided Media (Wired):**
                        * **Twisted Pair:** Copper wires (e.g., Ethernet cables, CAT5/CAT6). Inexpensive, common.
                        * **Coaxial Cable:** Single copper core with shielding (e.g., Cable TV). Better shielding than twisted pair.
                        * **Optical Fiber:** Transmits light pulses. Very high bandwidth, immune to EMI, long distance.
                    * **Unguided Media (Wireless):** Radio waves, Microwaves, Infrared.
                    """,
                    "pyq_focus": "'Compare Twisted Pair, Coaxial Cable and Optical Fibre guided transmission media.'\n* 'Write the physical and transmission characteristics of Optical Fibre Cable.'",
                    "strategy": "Create a comparison table: Media Type, Cost, Bandwidth, Max Distance, EMI Immunity. Fiber Optics is the 'best' on all technical specs but cost/installation is a factor.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Performance Indicators": {
                    "definition": """
                     **Bandwidth:** The *theoretical* maximum data transfer rate (e.g., 100 Mbps).
                    * **Throughput:** The *actual* measured data transfer rate. (Always less than or equal to bandwidth).
                    * **Latency (Delay):** The time it takes for a single bit to travel from sender to receiver.
                        * `Latency = Propagation Time + Transmission Time + Queuing Time + Processing Time`
                    * **Propagation Time:** `Distance / Propagation Speed` (Time for a bit to travel the wire)
                    * **Transmission Time:** `Packet Size / Bandwidth` (Time to push all bits of the packet onto the wire)
                    * **Bandwidth-Delay Product:** `Bandwidth × Latency`. Represents the number of bits "in flight" in the network.
                    """,
                    "pyq_focus": "Calculate Transmission Time for a packet. (e.g., 1 million bytes on 200 Kbps channel).\n* Calculate Propagation Delay. (e.g., 12,000 km at 2.4x10^8 m/s).\n* Define Bandwidth-Delay product.",
                    "strategy": """**Pay attention to units!** This is the #1 place to make a mistake.\n* `1 KB = 1000 bytes` (in networking), `1 MB = 1,000,000 bytes`.
                    * `1 Kbps = 1000 bits per second`.
                    * `1 byte = 8 bits`.
                    * Before you divide, convert everything to common units (e.g., bits and seconds).
                    * `Transmission Time = (1,000,000 bytes * 8 bits/byte) / (200 * 1000 bits/sec)`
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 2: Data Link Layer": {
                "Error Detection and Correction": {
                    "definition": """
                    Techniques to detect and/or fix bits that flip during transmission.
                    * **Parity Check:** A single bit added to make the total number of 1s even or odd. Detects single-bit errors.
                    * **Cyclic Redundancy Check (CRC):** (Polynomial code) The sender divides the data by a generator polynomial and appends the *remainder* as a checksum. The receiver divides the (data + remainder) by the same polynomial. If the result is 0, the data is likely correct. Very powerful at detecting burst errors.
                    * **Hamming Code:** A code that can *detect and correct* bit errors. It uses multiple parity bits placed at powers-of-2 positions.
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'A bit stream 10011101 is transmitted using the standard CRC method. The generator polynomial is x³ + 1. Show the actual bit string transmitted.'\n* 'An 8-bit byte... is to be encoded using an even-parity Hamming code. What is the binary value after encoding?'",
                    "strategy": "You *must* practice these calculations by hand.\n* **CRC:** This is binary polynomial long division (using XOR). Remember to append `k-1` zeros (where `k` is the length of the generator) to your data *before* dividing.\n* **Hamming:** Memorize the steps: (1) Find `p` (number of parity bits) using `2^p ≥ m + p + 1`. (2) Place parity bits at positions 1, 2, 4, 8... (3) Determine the value of each parity bit by checking the data bits it's responsible for (e.g., P1 checks bits 3, 5, 7, 9, 11...; P2 checks 3, 6, 7, 10, 11...).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Sliding Window Protocols": {
                    "definition": """
                    Protocols for reliable and efficient data transfer over an unreliable link.
                    * **Go-Back-N (GBN):** Allows a sender to transmit multiple (`N`) packets without waiting for an ACK. If a packet is lost, the receiver *discards all subsequent packets*. The sender must retransmit the lost packet and *all* packets that came after it.
                    * **Selective Repeat (SR):** Also allows a sender window. If a packet is lost, the receiver buffers all subsequent *correct* packets. It only asks the sender to retransmit the *one* lost packet. More efficient but more complex.
                    """,
                    "pyq_focus": "'Explain the concept of Sliding window protocols. Differentiate between... Go-back-N and Selective repeat.'",
                    "strategy": "Draw the diagrams! The best way to explain is to show a timeline diagram: Sender sends 1, 2, 3, 4, 5. Packet 3 is lost. Show what happens in GBN (Receiver ACKs 1, 2, then discards 4, 5. Sender times out, re-sends 3, 4, 5). Then show what happens in SR (Receiver ACKs 1, 2, buffers 4, 5, sends NAK for 3. Sender re-sends *only* 3. Receiver delivers 3, 4, 5 to application).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Multiple Access Protocols (MAC)": {
                    "definition": """
                    How multiple stations share a single broadcast channel (like Ethernet or WiFi).
                    * **ALOHA:** Just send. If it collides, wait a random time and retry.
                    * **CSMA (Carrier Sense):** Listen before transmitting. If channel is busy, wait.
                    * **CSMA/CD (Collision Detection):** (Used in wired Ethernet) Listen *while* transmitting. If a collision is detected, stop immediately, send a jam signal, wait a *binary exponential backoff* time, and retry.
                    * **CSMA/CA (Collision Avoidance):** (Used in WiFi) Can't detect collisions in the air. So, it tries to *avoid* them by using "Request to Send" (RTS) and "Clear to Send" (CTS) packets.
                    """,
                    "pyq_focus": "'Give the differences between CSMA/CD and CSMA/CA protocol.'\n* 'What is Binary exponential backoff algorithm? Explain its working.'",
                    "strategy": "The key difference: CSMA/CD is *post-collision* (it reacts), CSMA/CA is *pre-collision* (it tries to prevent). Why? In wireless, you have the 'hidden terminal problem' - you can't hear everyone who can hear the access point, so you can't be sure the channel is clear.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Ethernet (IEEE 802.3)": {
                    "definition": """
                    The dominant wired LAN technology. Uses CSMA/CD (on older hubs) or full-duplex (on modern switches).
                    **Ethernet Frame:**
                    [Image of the Ethernet frame format]
                    `[Preamble | SFD | Dest MAC | Source MAC | Length/Type | Data (Payload) | FCS (CRC)]`
                    * **Preamble/SFD:** Used for clock synchronization.
                    * **MAC Addresses:** 6-byte (48-bit) globally unique "hardware" addresses.
                    * **Data:** The IP packet (or other payload). Must be at least 46 bytes.
                    * **FCS:** Frame Check Sequence (a 32-bit CRC) for error detection.
                    """,
                    "pyq_focus": "'Draw and explain the frame format for Ethernet.'\n* 'Ethernet frames must be at least 64 bytes long... Fast Ethernet... How is it possible to maintain the same minimum frame size?'",
                    "strategy": "Memorize the frame format and the size of each field (in bytes). The 'minimum frame size' question is a classic. The 64-byte minimum (Slot Time) is to ensure a station can detect a collision before it finishes sending. In Fast Ethernet (10x faster), the *time* to send 64 bytes is 10x shorter. To fix this, they either (a) kept the network diameter 10x smaller or (b) (the real answer) pushed for *switched, full-duplex* Ethernet, where collisions don't happen at all.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Bridges & Switches": {
                    "definition": """
                    Devices that connect network segments at the **Data Link Layer (Layer 2)**.
                    * **Repeater/Hub (Layer 1):** A "dumb" device. A bit comes in one port, it's regenerated and sent out *all other ports*. Creates a single, large *collision domain*.
                    * **Bridge/Switch (Layer 2):** A "smart" device. It reads the *MAC addresses* in a frame. It learns which MAC address lives on which port and builds a *MAC address table*. It then *forwards* the frame *only* to the port where the destination MAC lives.
                    * **Key function:** Switches *break up collision domains*. Each port on a switch is its own collision domain.
                    """,
                    "pyq_focus": "'Distinguish between Bridges and Switches.'\n* 'Differentiate between bridges and switches.'\n* 'Repeaters, Hubs, Bridges, Switches, Routers and Gateways.' (Explain each)",
                    "strategy": "The key difference: Bridge = old term, 2 ports. Switch = modern term, many ports. They do the same job. The *real* comparison is Hub vs. Switch. Hub = Layer 1, dumb, one collision domain. Switch = Layer 2, smart (uses MACs), multiple collision domains. A Router is a Layer 3 device (uses IP addresses).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 3: Network Layer (Routing & Congestion)": {
                "Distance Vector Routing": {
                    "definition": "A decentralized routing algorithm. Each router maintains a 'vector' (table) of (Destination, Cost, NextHop). Routers *only* know their direct neighbors. They periodically send their *entire* routing table to their neighbors. Neighbors use this info (and the Bellman-Ford algorithm) to update their own tables.",
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Consider the given subnet... distance vector routing is used... vectors just come in to router C... What is C’s new routing table?'\n* 'Explain the Count-to-Infinity problem in distance vector routing.'",
                    "strategy": """**Practice the table update problem:**\n1.  C's new cost to a destination `X` *via* neighbor `B` is: `Cost(C,B) + Cost(B,X)`.
                    2.  `Cost(C,B)` is the measured delay (given as 6).
                    3.  `Cost(B,X)` is the value from `B`'s vector.
                    4.  Calculate this for *every* neighbor (`B`, `D`, `E`).
                    5.  `C`'s *new* cost to `X` is the `min()` of all these calculated paths. The `NextHop` is the neighbor that *gave* you that minimum cost.
                    * **Count-to-Infinity:** The classic problem where "good news" (a link is down) travels slowly. Solved with 'split horizon' or 'poison reverse'""",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Link State Routing": {
                    "definition": """A centralized routing algorithm (e.g., OSPF). Each router *independently* builds a *complete map* of the entire network.
                    1.  Routers send "Link State Advertisements" (LSAs) to *all* other routers (flooding) - "Hi, I'm A, and I'm connected to B (cost 5) and C (cost 3)."
                    2.  Each router collects all LSAs and builds an identical graph of the network.
                    3.  Each router runs **Dijkstra's Algorithm** (Shortest Path First) on this graph to find the shortest path from itself to all other destinations.""",
                    "pyq_focus": "'Explain how routing is performed using link state algorithm. Illustrate with an example.'\n* 'Compare the features of link state routing with distance vector routing.'",
                    "strategy": "The key comparison: **DV (RIP)**: 'Tells neighbors about the world.' Slow convergence, count-to-infinity. **LS (OSPF)**: 'Tells the world about its neighbors.' Fast convergence, complex, more computation (Dijkstra).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Congestion Control": {
                    "definition": """What happens when too many packets are in the network, causing routers to drop them.
                    * **Leaky Bucket:** A simple algorithm to regulate the *rate* of traffic. A "bucket" holds packets and "leaks" them out at a constant rate, smoothing out bursts.
                    * **Token Bucket:** More flexible. A "bucket" collects "tokens" at a constant rate. To send a packet, you must consume a token. This *allows* bursts (up to the bucket size) but limits the *average* rate.
                    * **RED (Random Early Detection):** A "proactive" congestion *avoidance* technique. As a router's queue *starts* to get full, it *randomly* drops a few packets *before* it's completely full. This signals to TCP senders to slow down, preventing total gridlock.""",
                    "pyq_focus": "'Illustrate the leaky bucket congestion control technique.'\n* 'A computer... is regulated by a token bucket... How long can the computer transmit at the full 6 Mbps?'\n* 'Describe two major differences between the warning bit method and the Random Early Detection (RED) method.'",
                    "strategy": """Practice the Token Bucket math problem. It's about rates.\n* `Bucket Capacity = 8 Mb`
                    * `Fill Rate = 1 Mbps`
                    * `Drain Rate = 6 Mbps`
                    * `Net Drain Rate = 6 - 1 = 5 Mbps`
                    * `Time to empty = Bucket Capacity / Net Drain Rate = 8 Mb / 5 Mbps = 1.6 seconds`.""",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 4: Network Layer (Internet)": {
                "IP Protocol and IPv4": {
                    "definition": """
                    The **Internet Protocol (IP)** is the core protocol of the Network Layer. It is a **connectionless** (unreliable) protocol responsible for *host-to-host addressing and routing* of packets (datagrams).
                    
                    **IPv4 Header:**
                    
                    Key fields:
                    * **Version:** (4)
                    * **IHL:** Header Length (in 32-bit words).
                    * **Total Length:** Packet length (header + data).
                    * **TTL (Time to Live):** A hop counter. Decremented by each router. When it hits 0, packet is dropped (prevents loops).
                    * **Protocol:** Which Transport layer protocol is inside? (6 = TCP, 17 = UDP).
                    * **Header Checksum:** Error check *only for the header*.
                    * **Source IP Address:** 32-bit address.
                    * **Destination IP Address:** 32-bit address.
                    """,
                    "pyq_focus": "'Draw and explain the wide-form of the IPv4 packets.'\n* 'In IP, the checksum covers only the header and not the data. Identify the reason.' (Ans: Header changes at each router (TTL), data doesn't. And Transport layer (TCP) already checks the data, so it's redundant).",
                    "strategy": "You don't need to memorize every field, but you *must* know: Version, TTL, Protocol, Checksum, Source IP, Dest IP. Understand *why* it's 'unreliable' - there's no ACK, no retransmission. That's TCP's job.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "IP Addressing and Subnetting": {
                    "definition": """
                    **IP Address:** A 32-bit logical address (e.g., `192.168.1.10`).
                    **Subnet Mask:** A 32-bit mask (e.g., `255.255.255.0`) that splits the IP into two parts:
                    1.  **Network ID:** (The part where the mask is `255`s or `1`s).
                    2.  **Host ID:** (The part where the mask is `0`s).
                    
                    **Subnetting:** The process of "borrowing" bits from the Host ID portion to create more Network IDs (subnets). This allows a large block of addresses (like a Class B) to be broken into smaller, manageable networks.
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'How do you subnet the Class C IP address 195.1.1.0 so as to have 10 subnets...'\n* 'A network on the Internet has a subnet mask of 255.255.240.0. What is the maximum number of hosts it can handle?'",
                    "strategy": """**This is the #1 problem to practice.**
                    **Problem 1: 'Max hosts for mask 255.255.240.0?'**
                    1.  `255.255.240.0` in binary: `11111111.11111111.11110000.00000000`
                    2.  Count the `0`s (host bits). There are `4 + 8 = 12` host bits.
                    3.  `Number of Hosts = 2^(host bits) - 2`
                    4.  `2^12 - 2 = 4096 - 2 = 4094` hosts. (You subtract 2 for the Network Address and Broadcast Address).

                    **Problem 2: 'Subnet 195.1.1.0 (Class C) for 10 subnets?'**
                    1.  It's Class C, so default mask is `255.255.255.0`. You have 8 host bits to work with.
                    2.  You need 10 subnets. How many bits do you need to *borrow*?
                        * `2^3 = 8` (Not enough).
                        * `2^4 = 16` (Enough). So, you must borrow **4 bits** from the host part.
                    3.  New subnet mask: Old mask was `...00000000`. New mask is `...11110000` (borrowed 4 bits).
                    4.  `...11110000` in decimal is `240`.
                    5.  New mask is `255.255.255.240`.""",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "ARP, RARP, DHCP": {
                    "definition": """
                    * **Problem:** IP works with IP addresses (Layer 3), but Ethernet works with MAC addresses (Layer 2). How does a router find the MAC address for a given IP?
                    * **ARP (Address Resolution Protocol):** Solves this. A host broadcasts a query: "Who has IP `192.168.1.5`? Tell me your MAC." The computer with that IP replies: "I do. My MAC is `AA:BB:CC:11:22:33`."
                    * **RARP (Reverse ARP):** (Old) A diskless workstation broadcasts: "My MAC is `...`. Can someone please tell me my IP address?"
                    * **DHCP (Dynamic Host Configuration Protocol):** The modern, powerful version of RARP. A computer boots up and broadcasts a "DHCP Discover" message. A DHCP server replies, *leasing* it an IP address, subnet mask, default gateway, and DNS server for a limited time.
                    """,
                    "pyq_focus": "'Explain the address resolution problem using Address Resolution Protocol (ARP) and Reverse Address ResolutionProtocol (RARP) with an example network.'\n* 'Draw and explain BOOTP/DHCP message format.'",
                    "strategy": "Understand the core problem: mapping Layer 3 (IP) to Layer 2 (MAC). ARP = 'IP -> MAC'. RARP/DHCP = 'MAC -> IP'.'",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Routing Protocols (OSPF, BGP)": {
                    "definition": """
                    The actual protocols that implement routing algorithms.
                    * **OSPF (Open Shortest Path First):** An *intra-domain* (within one company/AS) routing protocol. It's a **Link State** protocol. Each router builds a full map of its area and runs Dijkstra's algorithm.
                    * **BGP (Border Gateway Protocol):** The *inter-domain* routing protocol for the entire Internet. It's a **Path Vector** protocol (an enhanced Distance Vector). BGP doesn't just care about the *shortest* path; it cares about *policy*. (e.g., "Don't send traffic from AT&T through Sprint's network").
                    """,
                    "pyq_focus": "'Describe how does OSPF perform routing...'\n* 'Describe the features of BGP. How does BGP avoid count to infinity problem?'\n* 'What is meant by exterior gateway routing protocol? Explain the working of BGP?'",
                    "strategy": "Remember the key distinction: **OSPF is for routing *inside* one network (like a university campus). BGP is for routing *between* networks (like connecting the university to its ISP).** OSPF uses Link State (Dijkstra). BGP uses Path Vector (policy).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "IPv6": {
                    "definition": """
                    The successor to IPv4, created because the 32-bit IPv4 address space ran out.
                    * **128-bit addresses** (vs 32-bit). `2^128` addresses is an astronomical number.
                    * Addresses written in hexadecimal (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`).
                    * **Simplified Header:** No checksum, no fragmentation fields. Designed to be faster for routers.
                    
                    * **New Features:** Built-in support for security (IPsec) and multicasting.
                    """,
                    "pyq_focus": "'Draw IPv6 Datagram format and explain its features.'\n* 'How many octets does the smallest possible IPv6 datagram contain?'\n* 'The Protocol field used in the IPv4 header is not present in the fixed IPv6 header. Why?' (Ans: It's replaced by the 'Next Header' field, which is more flexible).",
                    "strategy": "Focus on the *differences* with IPv4. Why was it created? (Address space). How is the header different? (Simpler, 128-bit addresses, no checksum).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 5: Transport & Application": {
                "Transport Layer Services (TCP vs. UDP)": {
                    "definition": """
                    The Transport Layer provides **process-to-process** communication (using port numbers).
                    
                    **UDP (User Datagram Protocol):**
                    * **Connectionless** ("fire and forget").
                    * **Unreliable:** No ACKs, no retransmission, no flow control.
                    * **Minimal Header:** (Source Port, Dest Port, Length, Checksum).
                    * **Use Case:** Fast, low-overhead. Good for DNS, DHCP, streaming video, online gaming.
                    
                    **TCP (Transmission Control Protocol):**
                    * **Connection-Oriented:** A 3-way handshake is required to set up a connection.
                    * **Reliable:** Uses sequence numbers and ACKs to guarantee every segment is delivered in order, without errors. Lost segments are retransmitted.
                    * **Flow Control:** Prevents a fast sender from overwhelming a slow receiver (using a "receive window").
                    * **Congestion Control:** Tries to prevent the *network* itself from being overwhelmed.
                    * **Use Case:** Reliable. Good for WWW (HTTP), Email (SMTP), File Transfer (FTP).
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* 'Distinguish the header formats of Transmission Control protocol (TCP) and User Datagram Protocol (UDP).'\n* 'Why is Transport layer called true End to End layer?'\n* 'Can TCP be used directly over a network (e.g. an Ethernet) without using IP? Justify.' (Ans: No. TCP handles process-to-process, IP handles host-to-host. TCP relies on IP to route its segments).",
                    "strategy": "This is the most important comparison in the module. Create a 2-column table: TCP vs. UDP. Compare them on: Connection-oriented, Reliability, Header size, Flow control, Congestion control, and Use cases. This is a classic 6-8 mark question.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "TCP Connection & Congestion Control": {
                    "definition": """
                    **TCP Segment Header:**
                    
                    * **Source/Dest Port:** (16 bits each)
                    * **Sequence Number:** (32 bits) Byte number of the *first* byte in this segment.
                    * **Acknowledgement Number:** (32 bits) The sequence number of the *next* byte the receiver expects.
                    * **Flags:** (e.g., `SYN` - synchronize, `FIN` - finish, `ACK` - acknowledgment, `RST` - reset).
                    * **Window Size:** Flow control. How many bytes the receiver is willing to accept.
                    
                    **Connection Establishment (3-Way Handshake):**
                    
                    1.  **Client -> Server:** `SYN` (Seq=x)
                    2.  **Server -> Client:** `SYN` + `ACK` (Seq=y, Ack=x+1)
                    3.  **Client -> Server:** `ACK` (Seq=x+1, Ack=y+1)
                    
                    **TCP Congestion Control:**
                    The algorithm (e.g., "Slow Start," "Congestion Avoidance") that TCP uses to manage its sending rate to avoid collapsing the network. It "probes" for available bandwidth by slowly increasing its rate, and then "backs off" (e.g., cuts its rate in half) when it detects packet loss.
                    """,
                    "pyq_focus": "'Draw and explain TCP segment header. Explain TCP connection establishment process.'\n* 'Describe the TCP congestion control approaches...'\n* 'Three-way handshake... is used... rather than two-way handshake. Justify.' (Ans: To prevent old duplicate `SYN` packets from creating 'half-open' connections).",
                    "strategy": "Memorize the 3-way handshake diagram. It's a guaranteed question. Also memorize the key fields of the TCP header (Ports, Seq/Ack numbers, Flags, Window). You don't need to know every single flag, but `SYN`, `ACK`, and `FIN` are essential.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Application Layer Protocols": {
                    "definition": """
                    Protocols that provide services directly to the user/application.
                    * **DNS (Domain Name System):** (Port 53, UDP) Translates human-readable domain names (e.g., `google.com`) into machine-readable IP addresses (e.g., `172.217.14.228`).
                    * **FTP (File Transfer Protocol):** (Port 20, 21) A stateful protocol for transferring files. Uses *two* connections: a "control" connection (port 21) and a "data" connection (port 20).
                    * **SMTP (Simple Mail Transfer Protocol):** (Port 25) Used for *pushing* email from a client to a server, and from server to server.
                    * **WWW (World Wide Web):** Architecture is client-server (browser-web server). The protocol is **HTTP** (Hypertext Transfer Protocol) on port 80 (or 443 for HTTPS).
                    * **SNMP (Simple Network Management Protocol):** Used by network administrators to monitor and manage network devices (routers, switches).
                    """,
                    "pyq_focus": "'What is DNS? Explain... working.'\n* 'What is the role of Simple Mail Transfer Protocol (SMTP) in E-mail?'\n* 'How does FTP handle file transfer operation?'\n* 'Explain the working of World Wide Web (WWW).'",
                    "strategy": "This module is mostly 'Explain what X is.' You need to know the *purpose* of each protocol, its *port number* (for the main ones like HTTP, FTP, DNS), and its *basic mechanism* (e.g., DNS is hierarchical, FTP uses two connections, SMTP is for 'pushing' mail).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            }
        },
        "pyqs": {
            "Module 1: Intro & Physical Layer": [
                {"q": "Compare TCP/IP and OSI reference model.", "my_text": "", "my_files": []},
                {"q": "Sketch the waveform in Manchester and Differential Manchester Encoding for the bitstream 11000110010.", "my_text": "", "my_files": []},
                {"q": "What is the transmission time of a packet sent by a station if the length of the packet is 1 million bytes and the bandwidth of the channel is 200 Kbps?", "my_text": "", "my_files": []},
                {"q": "Explain the various physical topologies with neat sketches.", "my_text": "", "my_files": []}
            ],
            "Module 2: Data Link Layer": [
                {"q": "A bit stream 10011101 is transmitted using the standard CRC method. The generator polynomial is x³ + 1. Show the actual bit string transmitted. Suppose the third bit from the left is inverted... Show that this error is detected.", "my_text": "", "my_files": []},
                {"q": "Give the differences between CSMA/CD and CSMA/CA protocol.", "my_text": "", "my_files": []},
                {"q": "Draw and explain the frame format for Ethernet.", "my_text": "", "my_files": []},
                {"q": "Differentiate between the working of One-bit sliding window, Selective repeat and Go-back-N.", "my_text": "", "my_files": []}
            ],
            "Module 3: Network Layer (Routing & Congestion)": [
                {"q": "Distance vector routing is used... vectors have just come in to router C: from B: (5, 0, 8, 12, 6, 2); from D: (16, 12, 6, 0, 9, 10); and from E: (7, 6, 3, 9, 0, 4). The measured delays to B, D, and E, are 6, 3, and 5, respectively. What is C’s new routing table?", "my_text": "", "my_files": []},
                {"q": "Explain the Count-to-Infinity problem in distance vector routing. Describe two techniques to solve it.", "my_text": "", "my_files": []},
                {"q": "Illustrate the leaky bucket congestion control technique.", "my_text": "", "my_files": []},
                {"q": "Compare the features of link state routing with distance vector routing.", "my_text": "", "my_files": []}
            ],
            "Module 4: Network Layer (Internet)": [
                {"q": "How do you subnet the Class C IP address 195.1.1.0 so as to have 10 subnets with a maximum of 12 hosts in each subnet.", "my_text": "", "my_files": []},
                {"q": "A network on the Internet has a subnet mask of 255.255.240.0. What is the maximum number of hosts it can handle?", "my_text": "", "my_files": []},
                {"q": "Draw IPv6 Datagram format and explain its features.", "my_text": "", "my_files": []},
                {"q": "Explain the purposes of using ARP and RARP in the network layer. Also describe the working of each.", "my_text": "", "my_files": []}
            ],
            "Module 5: Transport & Application": [
                {"q": "Distinguish the header formats of Transmission Control protocol (TCP) and User Datagram Protocol (UDP).", "my_text": "", "my_files": []},
                {"q": "Draw and explain TCP segment header. Explain TCP connection establishment process (3-way handshake).", "my_text": "", "my_files": []},
                {"q": "What is DNS? Explain its working with resource records and name servers.", "my_text": "", "my_files": []},
                {"q": "With the help of a basic model, explain the working of World Wide Web (WWW).", "my_text": "", "my_files": []}
            ]
        }
    }

# --- (2) HELPER FUNCTIONS ---
# These handle file/data conversions

def get_state_as_json():
    """Converts the entire session state to a JSON string for downloading."""
    return json.dumps(st.session_state.study_data, indent=2)

def create_download_link(json_string, filename="cst303_progress.json"):
    """Generates a base64-encoded download link for the JSON data."""
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}" style="background-color: #0068c9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Save My Progress</a>'
    return href

def file_to_b64(file):
    """Converts an UploadedFile object to a base64 string."""
    file_bytes = file.getvalue()
    b64_string = base64.b64encode(file_bytes).decode()
    return b64_string

def display_b64_file(b64_string, file_name):
    """Displays a base64 file (image or PDF) in Streamlit."""
    try:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            st.image(base64.b64decode(b64_string), caption=file_name, use_column_width=True)
        elif file_name.lower().endswith('.pdf'):
            # This is a common workaround to embed PDFs
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_string}" width="700" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.warning(f"Can't preview file type: {file_name}")
    except Exception as e:
        st.error(f"Error displaying file {file_name}: {e}")

# --- (3) MAIN APP LOGIC ---

# Set wide mode and a title
st.set_page_config(layout="wide", page_title="CST 303 Study Tracker")

# Initialize session state
if 'study_data' not in st.session_state:
    st.session_state.study_data = get_initial_data()

# Get the master data object
study_data = st.session_state.study_data

# --- Sidebar Navigation ---
st.sidebar.title("🚀 CST 303 Computer Networks")
st.sidebar.header("Navigation")

# Calculate progress for the sidebar
total_topics = 0
completed_topics = 0
for mod, topics in study_data["modules"].items():
    total_topics += len(topics)
    for topic_name, topic_data in topics.items():
        if topic_data["done"]:
            completed_topics += 1

if total_topics > 0:
    progress_percent = completed_topics / total_topics
    st.sidebar.progress(progress_percent)
    st.sidebar.caption(f"{completed_topics} / {total_topics} Topics Completed")
else:
    st.sidebar.progress(0)
    st.sidebar.caption("0 / 0 Topics Completed")

view_options = ["📈 Dashboard"] + list(study_data["modules"].keys()) + ["✍️ PYQ Practice"]
view = st.sidebar.radio("Go to:", view_options)

st.sidebar.divider()
st.sidebar.warning("Your progress is saved in this browser session. **Use the 'Save My Progress' button on the Dashboard to download a file** you can load later.")


# --- View 1: Progress Dashboard ---
if view == "📈 Dashboard":
    st.title("📈 CST 303 Progress Dashboard")
    st.markdown("Welcome to your study tracker! Use the sidebar to navigate to a module or practice PYQs.")

    col1, col2 = st.columns(2)
    with col1:
        st.header("Overall Progress")
        if total_topics > 0:
            st.progress(progress_percent)
            st.metric(label="Topics Completed", value=f"{completed_topics} / {total_topics}")
        else:
            st.info("No topics found.")

    with col2:
        st.header("Self-Assessment")
        confidence_counts = {"Not Confident": 0, "Somewhat Confident": 0, "Very Confident": 0}
        for mod, topics in study_data["modules"].items():
            for topic_name, topic_data in topics.items():
                if topic_data["done"] and topic_data["survey"]:
                    if topic_data["survey"].startswith("Not Confident"):
                        confidence_counts["Not Confident"] += 1
                    elif topic_data["survey"].startswith("Somewhat Confident"):
                        confidence_counts["Somewhat Confident"] += 1
                    elif topic_data["survey"].startswith("Very Confident"):
                        confidence_counts["Very Confident"] += 1
        
        st.bar_chart(confidence_counts)


    st.divider()

    # --- Save/Load Section ---
    st.header("Save & Load Your Progress")
    st.warning("🚨 **IMPORTANT:** This app does not have a database. Your progress is lost when you close this tab. **Save your progress by downloading the JSON file** and load it when you return.")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Save Progress")
        json_data = get_state_as_json()
        st.markdown(create_download_link(json_data, "cst303_progress.json"), unsafe_allow_html=True)
        st.info("Click the button above to save a JSON file of all your notes, links, and progress.")

    with col2:
        st.subheader("Load Progress")
        uploaded_file = st.file_uploader("Upload your `cst303_progress.json` file", type="json")
        if uploaded_file is not None:
            try:
                loaded_data = json.load(uploaded_file)
                # Basic validation
                if "modules" in loaded_data and "pyqs" in loaded_data:
                    # Overwrite the session state with the loaded data
                    st.session_state.study_data = loaded_data
                    st.success("Progress loaded successfully!")
                    st.info("The page will now reload to reflect your data.")
                    st.rerun() 
                else:
                    st.error("This does not appear to be a valid progress file.")
            except Exception as e:
                st.error(f"Error loading file: {e}")

# --- View 2: Module Study View ---
elif view in study_data["modules"].keys():
    module_key = view
    module_data = study_data["modules"][module_key]
    st.title(f"📚 {module_key}")

    # Topic selection
    topic_name = st.selectbox("Select a topic to study:", module_data.keys())
    
    # Get the data for the selected topic
    topic_data = module_data[topic_name]
    
    st.divider()
    
    # --- Checkbox to mark as done ---
    is_done = st.checkbox(
        "Mark as Done", 
        value=topic_data["done"], 
        key=f"{module_key}_{topic_name}_done"
    )
    st.session_state.study_data["modules"][module_key][topic_name]["done"] = is_done
    
    # --- Pre-filled Content ---
    st.header("🎓 Core Content")
    tab_def, tab_pyq, tab_strat = st.tabs(["📜 Definition", "🎯 PYQ Focus", "💡 Strategy"])
    with tab_def:
        st.markdown(topic_data["definition"], unsafe_allow_html=True)
    with tab_pyq:
        st.info(topic_data["pyq_focus"])
    with tab_strat:
        st.success(topic_data["strategy"])

    # --- User's Study Hub ---
    st.divider()
    st.header("My Study Hub")
    tab_notes, tab_links, tab_media = st.tabs(["My Notes", "My Links", "My Media (Photos/Diagrams)"])

    with tab_notes:
        notes = st.text_area(
            "Add your personal notes, summaries, and questions here...", 
            value=topic_data["my_notes"], 
            height=300, 
            key=f"{module_key}_{topic_name}_notes"
        )
        st.session_state.study_data["modules"][module_key][topic_name]["my_notes"] = notes

    with tab_links:
        st.markdown("Add links to useful YouTube videos, articles, or tutorials.")
        new_link = st.text_input("Paste a URL:", key=f"{module_key}_{topic_name}_link_input")
        
        if st.button("Add Link", key=f"{module_key}_{topic_name}_link_btn"):
            if new_link and new_link.startswith("http"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_links"].append(new_link)
                st.rerun() # Refresh to clear input and show new link
            else:
                st.warning("Please enter a valid URL (starting with http).")
        
        st.subheader("My Saved Links:")
        for i, link in enumerate(topic_data["my_links"]):
            col1, col2 = st.columns([0.9, 0.1])
            col1.markdown(f"- [{link}]({link})")
            if col2.button("X", key=f"{module_key}_{topic_name}_link_del_{i}", help="Delete this link"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_links"].pop(i)
                st.rerun()

    with tab_media:
        st.markdown("Upload your own diagrams, mind maps, or photos of handwritten notes.")
        
        # File uploader for adding new media
        uploaded_files = st.file_uploader(
            "Upload files (PNG, JPG, PDF)", 
            accept_multiple_files=True, 
            type=["png", "jpg", "jpeg", "pdf"],
            key=f"{module_key}_{topic_name}_photos_uploader"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                file_b64 = file_to_b64(file)
                st.session_state.study_data["modules"][module_key][topic_name]["my_photos_bytes"].append({
                    "name": file.name,
                    "b64": file_b64
                })
            # We must rerun to clear the file uploader and show the new files
            st.rerun()

        st.subheader("My Saved Media:")
        if not topic_data["my_photos_bytes"]:
            st.info("No media uploaded for this topic yet.")
        
        # Display saved media with delete buttons
        for i, file_data in enumerate(topic_data["my_photos_bytes"]):
            st.markdown(f"**{file_data['name']}**")
            display_b64_file(file_data['b64'], file_data['name'])
            
            if st.button(f"Delete {file_data['name']}", key=f"{module_key}_{topic_name}_media_del_{i}"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_photos_bytes"].pop(i)
                st.rerun()
            st.divider()

            
    # --- Survey (as requested) ---
    if is_done:
        st.divider()
        st.header("🧠 Self-Assessment")
        st.write("Now that you've marked this topic as done, how confident do you feel?")
        
        survey_options = ["---", "Not Confident (Need Review)", "Somewhat Confident", "Very Confident (Ready for Exam)"]
        
        # Find index for radio button
        current_survey_val = topic_data.get("survey") # Use .get for safety
        if current_survey_val in survey_options:
            survey_index = survey_options.index(current_survey_val)
        else:
            survey_index = 0

        response = st.radio(
            "Confidence Level:", 
            survey_options, 
            index=survey_index, 
            key=f"{module_key}_{topic_name}_survey"
        )
        
        if response != "---":
            st.session_state.study_data["modules"][module_key][topic_name]["survey"] = response
        else:
            st.session_state.study_data["modules"][module_key][topic_name]["survey"] = None


# --- View 3: PYQ Practice ---
elif view == "✍️ PYQ Practice":
    st.title("✍️ PYQ Practice Portal")
    st.info("Test your knowledge with questions from previous years. Your answers are saved with your progress file.")
    
    pyq_module = st.selectbox("Select Module:", study_data["pyqs"].keys())
    
    st.divider()
    
    questions = study_data["pyqs"][pyq_module]
    
    for i, q_data in enumerate(questions):
        st.header(f"Question {i+1}")
        st.markdown(f"**{q_data['q']}**")
        
        with st.expander(f"Show/Hide My Answer for Q{i+1}"):
            # Text Answer
            answer_text = st.text_area(
                "Type your answer, notes, or solution plan:", 
                value=q_data["my_text"], 
                key=f"{pyq_module}_q{i}_text"
            )
            st.session_state.study_data["pyqs"][pyq_module][i]["my_text"] = answer_text
            
            # File Answer
            st.subheader("My Solution Files")
            
            # File uploader for adding new files
            uploaded_solution = st.file_uploader(
                "Upload your handwritten solution (PDF, PNG, JPG)", 
                type=["pdf", "png", "jpg", "jpeg"], 
                key=f"{pyq_module}_q{i}_file_uploader"
            )
            
            if uploaded_solution:
                file_b64 = file_to_b64(uploaded_solution)
                st.session_state.study_data["pyqs"][pyq_module][i]["my_files"].append({
                    "name": uploaded_solution.name,
                    "b64": file_b64
                })
                st.rerun()

            # Display saved files
            if not q_data["my_files"]:
                st.info("No solution files uploaded for this question yet.")

            for file_index, file_data in enumerate(q_data["my_files"]):
                st.markdown(f"**{file_data['name']}**")
                display_b64_file(file_data['b64'], file_data['name'])
                
                if st.button(f"Delete {file_data['name']}", key=f"{pyq_module}_q{i}_file_del_{file_index}"):
                    st.session_state.study_data["pyqs"][pyq_module][i]["my_files"].pop(file_index)
                    st.rerun()
                st.divider()