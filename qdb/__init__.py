#
# Copyright 2014 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import gevent.monkey
gevent.monkey.patch_all()

import sys

from qdb.tracer import Qdb

# Populate the namespace with command managers for the user.
from qdb.comm import (  # NOQA
    RemoteCommandManager,
    ServerLocalCommandManager,
)

# Populate the namespace with potentially user facing errors. This allows the
# user to more easily import them to catch.
from qdb.errors import (  # NOQA
    QdbAuthenticationError,
    QdbError,
    QdbQuit,
    QdbFailedToConnect,
    QdbCommunicationError,
)

_version = '0.1.0'


def set_trace(host='localhost',
              port=8001,
              auth_msg='',
              default_file=None,
              eval_fn=None,
              exception_serializer=None,
              skip_fn=None,
              pause_signal=None,
              redirect_output=True,
              retry_attepts=10,
              uuid=None,
              cmd_manager=None,
              stop=True):
    """
    Begins tracing from this point.
    All arguments except for stackframe are passed to the constructor of the
    internal Qdb object.
    This function will continue to act on the same Qdb object until disable()
    is called.
    """
    Qdb(
        host=host,
        port=port,
        eval_fn=eval_fn,
        exception_serializer=exception_serializer,
        skip_fn=skip_fn,
        pause_signal=pause_signal,
        redirect_output=redirect_output,
        retry_attepts=retry_attepts,
        uuid=uuid,
        cmd_manager=cmd_manager,
    ).set_trace(sys._getframe().f_back, stop=stop)
    # We use f_back so that we start in the caller of this function.


def disable(mode='soft'):
    """
    Disables the internal Qdb object. If mode == 'soft', It will stop the
    command manager (releasing its resources) and continue execution without
    tracing. If mode == 'hard', it will raise a QdbQuit exception.
    Any other value for mode will raise a ValueError.
    """
    Qdb().disable(mode)