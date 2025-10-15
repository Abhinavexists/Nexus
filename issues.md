## **MongoDB SSL Connection Debug (Issue 1)**

### **Problem**

My MongoDB Atlas connection using PyMongo failed with:

```bash
[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1010)
```

despite valid certificates and updated libraries.

### **Root Cause**

The issue was **not SSL-related** but caused by **MongoDB Atlas rejecting the client before handshake** because my **public IP was not whitelisted** in the Atlas Network Access settings.
Atlas returns a TLS internal error in such cases, which caused the confusion.

---

## **Step-by-Step Fixes Implemented**

1. **URI Escaping Fix**

   * Initially, the error was:

     ```bash
     pymongo.errors.InvalidURI: Username and password must be escaped according to RFC 3986
     ```

   * Fixed by properly URL-encoding the username and password in the connection URI.

2. **DNS and Network Checks**

   * Verified DNS resolution:

     ```bash
     dig _mongodb._tcp.cluster0.o1y0czn.mongodb.net SRV
     ```

     → Confirmed SRV records for all three MongoDB shard nodes.
   * Tested connectivity:

     ```bash
     ncat -vz ac-rhtkdtb-shard-00-00.o1y0czn.mongodb.net 27017
     ```

     → Confirmed port 27017 reachable (no local firewall issues).

3. **Certificate Validation**

   * Verified CA certificates were correctly installed:

     ```bash
     pacman -Qs ca-certificates
     ls -lh /etc/ssl/certs/ca-certificates.crt
     ```

     → Confirmed valid sym link and trusted Mozilla bundle.
   * Also ran:

     ```bash
     sudo trust extract-compat
     ```

     to refresh the CA trust store.

4. **Checked OpenSSL and Python SSL Compatibility**

   * Ensured up-to-date OpenSSL:

     ```bash
     openssl version
     ```

     → `OpenSSL 3.6.0`
   * Verified Python SSL integration:

     ```bash
     python -m ssl
     ```

     → Working fine.

5. **Atlas Network Access Fix**

   * Found the root cause: client’s IP was **not whitelisted** in Atlas.
   * Added current public IP from:

     ```bash
     curl ifconfig.me
     ```

     → Added that IP to Atlas **Network Access > IP Whitelist**.
   * Connection succeeded immediately after that.

---

## **Final Working Code**

```python
import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URL')

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where(),
    tlsAllowInvalidCertificates=False,
    server_api=ServerApi('1'),
    serverSelectionTimeoutMS=10000
)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
```

---

## **Key Takeaways**

* **Always whitelist your current public IP** in Atlas before connecting.
* **TLS handshake failures can mask network access errors** from Atlas.
* Use **`certifi`** to ensure trusted root certificates.
* Store credentials securely in `.env` files, not hardcoded in code.
* Verify connectivity using `dig` and `ncat` to isolate DNS vs SSL issues.

---

Would you like me to format this into a short Markdown README section (like “MongoDB SSL Debug Log” for your project repo)?
