# pandas-zmq

Communicate [Pandas](https://pypi.org/project/pandas/) DataFrame over [ZeroMQ](https://pypi.org/project/pyzmq/) connection

## API

```
send_dataframe(socket, dataframe, flags=0)
```

```
recv_dataframe(socket, flags=0)
```

### Server

```
import pandas_zmq

# ...
pandas_zmq.send_dataframe(socket, df)
```


### Client

```
import pandas_zmq

# ...
df = pandas_zmq.recv_dataframe(socket)
```
