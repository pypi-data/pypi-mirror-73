# Copyright 2020 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Helper functions that depend on the DataFrame class."""

import json

import getml.communication as comm

from .data_frame import DataFrame

# --------------------------------------------------------------------

def list_data_frames():
    """Lists all available data frames of the project.

    Examples:

        .. code-block:: python

            d, _ = getml.datasets.make_numerical()
            getml.data.list_data_frames()
            d.save()
            getml.data.list_data_frames()

    Raises:
        IOError:

            If an error in the communication with the getML engine
            occurred.

    Returns:
        dict:

            Dict containing lists of strings representing the names of
            the data frames objects

            * 'in_memory'
                held in memory (RAM).
            * 'in_project_folder'
                stored on disk.

    Note:

        All data listed in 'in_memory' will be lost when switching
        the project using :func:`~getml.engine.set_project` or
        restarting the getML engine whereas those in
        'in_project_folder' is persistent.

    """

    cmd = dict()
    cmd["type_"] = "list_data_frames"
    cmd["name_"] = ""

    sock = comm.send_and_receive_socket(cmd)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    json_str = comm.recv_string(sock)

    sock.close()

    return json.loads(json_str)

# --------------------------------------------------------------------

def load_data_frame(name):
    """Retrieves a :class:`~getml.data.DataFrame` handler of data in the
    getML engine.

    A data frame object can be loaded regardless if it is held in
    memory (accessible through the 'Data Frames' tab in the getML
    monitor) or not. It only has to be present in the current project
    and thus listed in the output of
    :func:`~getml.data.list_data_frames`.

    Args:
        name (str):
            Name of the data frame object present in the getML engine.

    Examples:

        .. code-block:: python

            d, _ = getml.datasets.make_numerical(population_name = 'test')
            d2 = getml.data.load_data_frame('test')


    Raises:
        TypeError: If any of the input arguments is of wrong type.

        ValueError:

            If `name` does not corresponding to a data frame on the
            engine.

    Returns:
        :class:`~getml.data.DataFrame`:
            Handle the underlying data frame in the getML engine.

    Note:

        The getML engine knows to different states of a data frame
        object. Firstly, the current instance in memory (RAM) that
        holds the most recent changes applied via the Python API
        (listed under the 'in_memory' key of
        :func:`~getml.data.list_data_frames`) and, secondly, the
        version stored to disk by calling the
        :meth:`~getml.data.DataFrame.save` method (listed under the
        'in_project_folder' key). If a data frame object corresponding
        to `name` is present in both of them, the most recent version
        held in memory is loaded. To load the one from memory instead,
        you use the :meth:`~getml.data.DataFrame.load` method.

        In order to load a data frame object from a different project,
        you have to switch projects first. Caution: any changes
        applied after the last call to
        :meth:`~getml.data.DataFrame.save` will be lost. See
        :func:`~getml.engine.set_project` and
        :class:`~getml.data.DataFrame` for more details about the
        lifecycles of the models.

    """

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    data_frames_available = list_data_frames()

    # First, attempt to load a data frame held in memory.
    if name in data_frames_available['in_memory']:
        return DataFrame(name).refresh()

    if name in data_frames_available['in_project_folder']:
        return DataFrame(name).load()

    raise ValueError("No data frame holding the name '"+name+"' present on the getML engine")

# --------------------------------------------------------------------

