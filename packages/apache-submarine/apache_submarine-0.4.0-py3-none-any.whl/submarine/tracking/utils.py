# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from submarine.store import DEFAULT_SUBMARINE_JDBC_URL
from submarine.store.sqlalchemy_store import SqlAlchemyStore
from submarine.utils import env

_TRACKING_URI_ENV_VAR = "SUBMARINE_TRACKING_URI"
_JOB_NAME_ENV_VAR = "SUBMARINE_JOB_NAME"

# Extra environment variables which take precedence for setting the basic/bearer
# auth on http requests.
_TRACKING_USERNAME_ENV_VAR = "SUBMARINE_TRACKING_USERNAME"
_TRACKING_PASSWORD_ENV_VAR = "SUBMARINE_TRACKING_PASSWORD"
_TRACKING_TOKEN_ENV_VAR = "SUBMARINE_TRACKING_TOKEN"
_TRACKING_INSECURE_TLS_ENV_VAR = "SUBMARINE_TRACKING_INSECURE_TLS"

_tracking_uri = None


def is_tracking_uri_set():
    """Returns True if the tracking URI has been set, False otherwise."""
    if _tracking_uri or env.get_env(_TRACKING_URI_ENV_VAR):
        return True
    return False


def set_tracking_uri(uri):
    """
    Set the tracking server URI. This does not affect the
    currently active run (if one exists), but takes effect for successive runs.
    """
    global _tracking_uri
    _tracking_uri = uri


def get_tracking_uri():
    """
    Get the current tracking URI. This may not correspond to the tracking URI of
    the currently active run, since the tracking URI can be updated via ``set_tracking_uri``.
    :return: The tracking URI.
    """
    # TODO get database url from submarine-site.xml
    global _tracking_uri
    if _tracking_uri is not None:
        return _tracking_uri
    elif env.get_env(_TRACKING_URI_ENV_VAR) is not None:
        return env.get_env(_TRACKING_URI_ENV_VAR)
    else:
        return DEFAULT_SUBMARINE_JDBC_URL


def get_job_name():
    """
    Get the current job name.
    :return The job name:
    """
    if env.get_env(_JOB_NAME_ENV_VAR) is not None:
        return env.get_env(_JOB_NAME_ENV_VAR)


def get_sqlalchemy_store(store_uri):
    return SqlAlchemyStore(store_uri)
