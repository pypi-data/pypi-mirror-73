# Kyanit API
# Copyright (C) 2020 Zsolt Nagy
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>.

"""
# Kyanit API

Kyanit API is a Python API for interfacing and interacting with Kyanit.

For a command-line utility, see Kyanit CTL at https://kyanit.eu/docs/kyanit-ctl.

Install the latest released version of Kyanit API from PyPI with:

```
pip install kyanitapi
```

Then import the module with:

```python
import kyanitapi
```

The module publishes the `Kyanit` class to connect to Kyanit boards. Import the class
directly with:

```python
from kyanitapi import Kyanit
```

Kyanit provides an addressing mechanism called the "Color ID," which mapps to the IP
address of the Kyanit board. The Color ID consists of 3 colors from the **R**ed,
**G**reen, **B**lue, **C**yan, **M**agenta, **Y**ellow and **W**hite pallette. If you
don't know how to find out the Color ID of a Kyanit board, head to Kyanit's
documentation at: https://kyanit.eu/docs/kyanit

Addressing using the Color ID works on home networks with a subnet mask of
255.255.255.0, which is what most home and small business routers create. Assuming you
know the Color ID of the board, and the network address to which it's connected, you can
instantiate the `Kyanit` class with:

```python
my_kyanit = Kyanit('BCG', '192.168.1.0')
```

Where 'BCG' is the Color ID of the board and '192.168.1.0' is the network address.

On non-255.255.255.0 networks, it is possible to connect to the Kyanit board providing
only it's IP address:

```python
my_kyanit = Kyanit(ip_addr='192.168.1.6')
```

Once instantiated, you can perform all sorts of actions on your Kyanit board. You can
ping the board with `Kyanit.ping`, get its status with `Kyanit.get_status`, and perform
file operations like listing the files on the board with `Kyanit.get_file_list` or
downloading and uploading files with `Kyanit.get_file` and `Kyanit.put_file`
respectively. Other file actions, like delete and rename are also possible.

System-level operations are provided as well, these being the `Kyanit.reboot`, which
re-initializes the board, `Kyanit.stop` and `Kyanit.start` which stop and start the user
code.

Kyanit also provides a notion of a "network variable" called the Netvar, which can be
accessed with the `Kyanit.netvar` method.

Here's an example in the REPL to demonstrate some of these actions:

```python
>>> from kyanitapi import Kyanit
>>> my_kyanit = Kyanit('BCG', '192.168.1.0')
>>> my_kyanit.ping()
True
>>> my_kyanit.get_status()
{'free_flash': 3514368, 'free_memory': 18768, 'run_state': 'CODE.PY MAIN', ...}
>>> my_kyanit.get_file_list()
['wlan.json', 'code.py']
>>> my_kyanit.put_file('some_file.txt', 'some text')
'OK'
>>> my_kyanit.get_file_list()
['wlan.json', 'code.py', 'some_file.txt']
>>> my_kyanit.get_file('some_file.txt')
b'some text'
>>> my_kyanit.delete_file('some_file.txt')
'OK'
>>> my_kyanit.get_file_list()
['wlan.json', 'code.py']
>>> my_kyanit.stop()
'OK'
>>> my_kyanit.get_status()
{'free_flash': 3514368, 'free_memory': 20288, 'run_state': 'STOPPED', ...}
>>> my_kyanit.start()
'OK'
>>> my_kyanit.get_status()
{'free_flash': 3514368, 'free_memory': 17744, 'run_state': 'CODE.PY MAIN', ...}
```

See the `Kyanit` class and module function documentations to see what the class and this
module can do.

# License Notice

Copyright (C) 2020 Zsolt Nagy

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, version
3 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this
program. If not, see <https://www.gnu.org/licenses/>.
"""


import json
import ipaddress
from functools import wraps

import psutil
import requests
import pythonping

try:
    from ._version import __version__  # noqa
except ImportError:
    pass


VALID_ID_COLORS = ["B", "C", "G", "M", "R", "W", "Y"]


def get_networks():
    """
    Return a list with networks that have a netmask of 255.255.255.0 in the current
    system. Only such networks are supported for connecting to a Kyanit using the Color
    ID.

    Return an empty list, if no such networks are found.

    List items will be tuples in the form of `('Interface Name', '<ip_address>')`, such
    as `('eth0', '192.168.1.0')` or `('Local Area Connection', '192.168.3.0')` depending
    on the operating system.
    """

    all_interfaces = psutil.net_if_addrs()
    networks = []
    for if_name in all_interfaces:
        for nic_address in all_interfaces[if_name]:
            if nic_address.netmask == "255.255.255.0":
                networks.append(
                    (
                        if_name,
                        # store network address
                        str(
                            ipaddress.IPv4Network(
                                "{}/24".format(nic_address.address), strict=False
                            ).network_address
                        ),
                    )
                )  # noqa
    return networks


def cid_is_valid(color_id):
    """
    Return `True` if `color_id` is a valid Color ID string, and `False` otherwise.

    'BBB' (an address of 0) is not considered to be valid, and neither is any ID
    representing an address above 254.
    """

    if not isinstance(color_id, str):
        return False
    if len(color_id) != 3:
        return False
    color_id = color_id.upper()
    for symbol in color_id:
        if symbol not in VALID_ID_COLORS:
            return False
    # Color ID must result in an IP octet between 1 and 254
    num = 0
    for symbol in enumerate(color_id[::-1]):
        num += len(VALID_ID_COLORS) ** symbol[0] * VALID_ID_COLORS.index(symbol[1])
    if num < 1 or num > 254:
        return False
    return True


def ip_is_valid(ip_addr):
    """
    Return `True` if `ip_addr` is a valid IP address string, and `False` otherwise.
    """

    try:
        ipaddress.IPv4Network(ip_addr)
    except ipaddress.AddressValueError:
        return False
    else:
        return True


def netmask_is_valid(netmask):
    """
    Return `True` if `netmask` is a valid netmask string, and `False` otherwise.
    """

    try:
        ipaddress.IPv4Network("0.0.0.0/{}".format(netmask))
    except ipaddress.NetmaskValueError:
        return False
    else:
        return True


def ip_to_cid(ip_addr):
    """
    Convert an IP address string to a Color ID. It is assumed that the IP address is
    from a network with a netmask of 255.255.255.0.

    If the passed IP address is not valid, `ValueError: IP invalid` will be raised.

    Returned value is the Color ID string.
    """

    if not ip_is_valid(ip_addr):
        raise ValueError("IP invalid")
    num = int(ip_addr.split(".")[3])
    max_addr = len(VALID_ID_COLORS) ** 3 - 1
    if num < 0 or num > max_addr:
        # this should never be raised if VALID_ID_COLORS has at least 7 symbols.
        raise ValueError()
    base = len(VALID_ID_COLORS)
    symbols = VALID_ID_COLORS
    digits = []
    while num:
        digits.append(symbols[int(num % base)])
        num = int(num / base)
    digits.reverse()
    result = "".join(digits)
    return (symbols[0] * (3 - len(result))) + result


def cid_to_ip(color_id, network_addr):
    """
    Convert a Color ID to an IP address within the network given in `network_addr`.

    If `color_id` is not a valid Color ID, `ValueError: Color ID invalid` will be
    raised. Consequently if `network_addr` is not a valid address,`ValueError: Network
    invalid` will be raised. The last octet of `network_addr` must be zero, and a subnet
    mask of 255.255.255.0 is assumed.

    Returned value is an IP address string.
    """

    if not cid_is_valid(color_id):
        raise ValueError("Color ID invalid")
    if not ip_is_valid(network_addr):
        raise ValueError("Network invalid")
    if ipaddress.IPv4Address(network_addr).packed[3] != 0:
        raise ValueError("Network invalid")
    num = 0
    for symbol in enumerate(color_id[::-1]):
        num += len(VALID_ID_COLORS) ** symbol[0] * VALID_ID_COLORS.index(symbol[1])
    ip = network_addr.split(".")
    ip[3] = str(num)
    return ".".join(ip)


class KyanitConnectionError(Exception):
    """
    Raised when connecting to Kyanit fails or results in a timeout. No arguments are
    passed to this exception.

    Handle it as follows:

    ```python
    try:
        # some Kyanit operation
        ...
    except KyanitConnectionError:
        # do something on connection error
    ```
    """

    pass


class KyanitRequestError(Exception):
    """
    Raised when Kyanit responds with a status code other than 200 OK. The first argument
    passed to this exception will be the response status code, the second will be the
    response body.

    Handle it as follows:

    ```python
    try:
        # some Kyanit operation
        ...
    except KyanitRequestError as error:
        status_code = error.args[0]
        response_body = error.args[1]

        if status_code == 404:
            # do something on 404 Not Found
            ...

        # handle the rest, if desired
        ...
    ```
    """

    pass


def _request_handler(rtype=None):
    # returns a decorator, rtype can be 'json', 'text' or None, which determines the
    # format in which the response body will be returned
    def decorated(func):
        # decorator to handle requests and request errors
        @wraps(func)
        def handle_request(*args, **kwargs):
            conn_error = False
            try:
                response = func(*args, **kwargs)
            except (requests.exceptions.Timeout, OSError):
                # discard the chain, it's a connection error
                conn_error = True
            if conn_error:
                raise KyanitConnectionError
            if response.status_code != 200:
                raise KyanitRequestError(
                    response.status_code,
                    response.json()["error"] if "error" in response.json() else None,
                )
            else:
                if rtype == "json":
                    return response.json()
                elif rtype == "text":
                    return response.text
                return response.content

        return handle_request

    return decorated


class Kyanit:
    """
    Class for a Kyanit connection instance. No connection attempt is made on
    instantiation.

    Provide either a Color ID with a Network address OR an IP address. These can not be
    changed after instantiation. Timeout is in seconds.

    If both Color ID and IP address are provided, `ValueError: bad connection method`
    will be raised. If neither is provided, `ValueError: no connection method` will be
    raised.

    All methods that perform a request towards Kyanit will be blocking until a response
    is received or the request is timed out.
    """

    def __init__(self, color_id=None, network_addr=None, ip_addr=None, timeout=3):
        if color_id is not None and ip_addr is not None:
            raise ValueError("bad connection method")
        elif color_id is None and ip_addr is None:
            raise ValueError("no connection method")

        if color_id is not None:
            self._ip_addr = cid_to_ip(color_id, network_addr=network_addr)
            self._color_id = color_id

        elif ip_addr is not None:
            self._color_id = ip_to_cid(ip_addr)
            self._ip_addr = ip_addr

        self._network_addr = network_addr
        self.set_timeout(timeout)

    def info(self):
        """
        Return connection info.

        Return value is a dict with the following schema:

        ```python
        {
            'color_id': str,
            'network_addr': str,
            'ip_addr': str
        }
        ```
        """

        return {
            "color_id": self._color_id,
            "network_addr": self._network_addr,
            "ip_addr": self._ip_addr,
        }

    def set_timeout(self, seconds):
        """
        Set connection timeout in seconds.
        """

        self._timeout = seconds

    def ping(self, count=3, timeout=1, verbose=False):
        """
        Ping Kyanit.

        You may provide ping count and timeout in seconds. If verbose is `True`, results
        will be printed.

        Return value is `True` is ping was successful, `False` otherwise
        """

        return pythonping.ping(
            self._ip_addr, count=count, timeout=timeout, verbose=verbose
        ).success()

    def get_status(self, tries=1):
        """
        Get status of Kyanit. Getting status will be attempted a number of times defined
        in `tries`. Each try may time out, therefore getting status may take `tries *
        self.timeout` amount of time. (Useful after some longer operation, ex. directly
        after reboot.)

        Returned value will be a dict with the following schema:

        ```python
        {
            'firmware_version': str,  # version number in the format major.minor.patch
            'color_id': str,  # current Color ID of the Kyanit
            'free_memory': int,  # free heap RAM in bytes
            'free_flash': int,  # amount of bytes free in the filesystem
            'run_state': str,  # see note below
            'error_traceback': [
                str
            ] # key is present if run_state is ERROR, and contains the traceback lines
        }
        ```

        Note: for possible run states see
        https://github.com/kyanit-project/kyanit#run-states
        """

        num_tries = 0
        while True:
            try:
                data = requests.get(
                    "http://{}:3300/sys/state".format(self._ip_addr),
                    timeout=self._timeout,
                )
            except Exception:
                num_tries += 1
                if num_tries >= tries:
                    break
            else:
                return data.json()
        raise KyanitConnectionError

    @_request_handler("json")
    def stop(self, force=False):
        """
        Stop runner, stopping all tasks. New run state will be 'STOPPED'.

        A kyanit.StoppedError will be passed to code.cleanup on Kyanit.

        Return value is the string `OK` if successful.
        """

        return requests.post(
            "http://{}:3300/sys/stop{}".format(
                self._ip_addr, "/force" if force else ""
            ),
            timeout=self._timeout,
        )

    @_request_handler("json")
    def start(self):
        """
        Start runner. Kyanit will attempt to import 'code.py' and call main.

        Return value is the string `OK` if successful.
        """

        return requests.post(
            "http://{}:3300/sys/start".format(self._ip_addr), timeout=self._timeout
        )

    # @_request_handler('json')
    # def reset(self, soft=False):
    #     """
    #     Perform a soft reset on the Kyanit. The system will restart, but the wlan
    #     connection will
    #     be preserved, if unchanged.

    #     kyanit.ResetError will be passed to code.cleanup on Kyanit before the reset
    #     procedure.

    #     Might take some time before Kyanit will respond to further requests. It's a
    #     good practice
    #     to `get_status` with a number of tries larger than 1 (ex. 5) after reboot or
    #     reset.

    #     Return value is the string `OK` if successful.
    #     """

    #     return requests.post('http://{}:3300/sys/reboot/soft'.format(self._ip_addr),
    #                          timeout=self._timeout)

    @_request_handler("json")
    def reboot(self):
        """
        Perform a hard reset on the Kyanit. The system will fully restart, wlan
        connection will be performed again.

        kyanit.RebootError will be passed to code.cleanup on Kyanit before the reboot
        procedure.

        Might take some time before Kyanit will respond to further requests. It's a good
        practice to `get_status` with a number of tries larger than 1 (ex. 5) after
        reboot or reset.

        Return value is the string `OK` if successful.
        """

        return requests.post(
            "http://{}:3300/sys/reboot".format(self._ip_addr), timeout=self._timeout
        )

    @_request_handler("json")
    def get_file_list(self):
        """
        Return a list with all of the file names present on Kyanit.
        """

        return requests.get(
            "http://{}:3300/files".format(self._ip_addr), timeout=self._timeout
        )

    @_request_handler()
    def get_file(self, filename):
        """
        Get the contents of the file with the name passed to `filename` from Kyanit.

        `KyanitRequestError` with status code 404 will be raised if file is not found.

        Directories are not supported, if the filename contains a '/'
        `KyanitRequestError` will be raised with a status code 500. The same error will
        be raised if trying to get `main.py`, `boot.py` or `_boot.py` as these files are
        protected and internal to Kyanit.

        Return type is bytes (the contents of the file).
        """

        return requests.get(
            "http://{}:3300/files/{}".format(self._ip_addr, filename),
            timeout=self._timeout,
        )

    @_request_handler("json")
    def put_file(self, filename, content):
        """
        Create or replace a file with the name passed to `filename` on the Kyanit, and
        upload contents passed to `content`, which may be bytes or string.

        Directories are not supported, if the filename contains a '/'
        `KyanitRequestError` will be raised with a status code 500. The same error will
        be raised if trying to put `main.py`, `boot.py` or `_boot.py` as these files are
        protected and internal to Kyanit.

        Return value is the string `OK` if successful.
        """

        return requests.put(
            "http://{}:3300/files/{}".format(self._ip_addr, filename),
            content,
            timeout=self._timeout,
        )

    @_request_handler("json")
    def delete_file(self, filename):
        """
        Delete a file with the name passed to `filename` on the Kyanit.

        `KyanitRequestError` with status code 404 will be raised if file is not found.

        Directories are not supported, if the filename contains a '/'
        `KyanitRequestError` will be raised with a status code 500. The same error will
        be raised if trying to delete `main.py`, `boot.py` or `_boot.py` as these files
        are protected and internal to Kyanit.

        Return value is the string `OK` if successful.
        """

        return requests.delete(
            "http://{}:3300/files/{}".format(self._ip_addr, filename),
            timeout=self._timeout,
        )

    @_request_handler("json")
    def rename_file(self, filename, newname):
        """
        Rename a file with the name passed to `filename` to `newname` on the Kyanit.

        `KyanitRequestError` with status code 404 will be raised if file is not found.

        Directories are not supported, if the filename contains a '/'
        `KyanitRequestError` will be raised with a status code 500. The same error will
        be raised if trying to rename `main.py`, `boot.py` or `_boot.py` as these files
        are protected and internal to Kyanit.
        """

        return requests.put(
            "http://{}:3300/files/{}?rename={}".format(
                self._ip_addr, filename, newname
            ),
            timeout=self._timeout,
        )

    @_request_handler("json")
    def netvar(self, obj=None, clear=False):
        """
        Read or write the Netvar on Kyanit.

        If `obj` is `None`, return the value of Netvar.outbound() from Kyanit.

        If `obj` is other than `None`, set the value of Netvar.inbound() on the Kyanit.
        In that case return value is the string 'OK' if successful. Otherwise
        `TypeError` will be raised if `obj` is not JSON serializable.

        If `clear` is `True`, `obj` is disregarded and Netvar.inbound() will be set to
        `None` on the Kyanit.

        Examples:

        Get Netvar.inbound() with:

        ```python
        Kyanit.netvar()
        ```

        Set Netvar.outbound() with:

        ```python
        Kyanit.netvar('new_value')
        ```

        `'new_value'` could be can be any Python object that's JSON serializable.

        Clear Netvar.outbound() with:

        ```python
        Kyanit.netvar(clear=True)
        ```

        See https://github.com/kyanit-project/kyanit#the-netvar for more on Netvar.
        """

        if clear:
            return requests.post(
                "http://{}:3300/netvar".format(self._ip_addr),
                json.dumps(None),
                timeout=self._timeout,
            )

        if obj is None:
            return requests.get(
                "http://{}:3300/netvar".format(self._ip_addr), timeout=self._timeout
            )
        else:
            return requests.post(
                "http://{}:3300/netvar".format(self._ip_addr),
                json.dumps(obj),
                timeout=self._timeout,
            )
