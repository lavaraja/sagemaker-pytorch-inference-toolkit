# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

import os
import subprocess
from subprocess import CalledProcessError

from retrying import retry
from sagemaker_pytorch_serving_container import torchserve
from sagemaker_pytorch_serving_container import handler_service

HANDLER_SERVICE = handler_service.__file__

def configure_logging():
    log_levels = {
        '0': 'off',
        '10': 'fatal',
        '20': 'error',
        '30': 'warn',
        '40': 'info',
        '50': 'debug',
        '60': 'trace'
    }

    ts_loglevel = os.environ.get('TS_LOGLEVEL')

    if ts_loglevel is not None:
        if ts_loglevel in log_levels:
            try:
                log_level = log_levels[ts_loglevel]
                subprocess.run(['sed', '-i', f's/info/{log_level}/g', 'etc/log4j2.xml'], check=True)
                print(f"Logging level set to {log_level}")
            except subprocess.CalledProcessError:
                print("Error configuring the logging", file=sys.stderr)
        else:
            print(f"Invalid TS_LOGLEVEL value: {ts_loglevel}. No changes made to logging configuration.", file=sys.stderr)
    else:
        print("TS_LOGLEVEL not set. Using default logging configuration.")

def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError)

@retry(stop_max_delay=1000 * 30,
       retry_on_exception=_retry_if_error)
def _start_torchserve():
    # there's a race condition that causes the model server command to
    # sometimes fail with 'bad address'. more investigation needed
    # retry starting mms until it's ready
    torchserve.start_torchserve(handler_service=HANDLER_SERVICE)

def main():
    configure_logging()
    _start_torchserve()

if __name__ == '__main__':
    main()
