Customized vertica connector 
==========

The Python Wrapper to vertica_python lib for reconnectiong across server nodes

Credentials
-------------
```sh
vertica_configs - json variable in ENV
connection_info = {"host": <VERTICA_HOST>,
                   "port": <VERTICA_PORT>,
                   "backup_server_node": [<SERVER_NODE_1>, <SERVER_NODE_2>, <SERVER_NODE_3>}


user = os.getenv("VERTICA_USER"),
password = os.getenv("VERTICA_PASSWORD")
database = "DWH"
vertica_configs = json.loads(os.getenv("VERTICA_CONFIGS"))
```

Usage
```sh
pip3 install vertica-connector-talenttech
```

```python
import os
import json
from vconnector.vertica_connector import VerticaConnector
with VerticaConnector(user, password, vertica_configs) as cnx:
      cur = cnx.cursor()
      sql = "SELECT 1"
      cur.execute(sql)
