#   Copyright 2022 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from flask import Flask, request, abort, jsonify, render_template
from datetime import datetime
import inspect
import os
import json
import tempfile
import subprocess
import time
import re
from urllib.parse import urlparse
import base64
import requests
from requests.auth import HTTPBasicAuth
import traceback
from datetime import timedelta, timezone

import yaml
from jinja2 import Template

# User Imports
import globals
import common
import api_keycloak_call

# 設定ファイル読み込み・globals初期化
app = Flask(__name__)
app.config.from_envvar('CONFIG_API_AUTHC_INFRA_PATH')
globals.init(app)


def client_role_users_get(realm, client_id, role_name):
    """ロール毎のユーザ情報リスト取得 get user info list for each role

    Args:
        realm (str): realm
        client_id (str): client id
        role_name (str): role_name

    Returns:
        [type]: [description]
    """
    try:
        globals.logger.debug('#' * 50)
        globals.logger.debug('CALL {}:realm[{}] client_id[{}] role_name[{}]'.format(inspect.currentframe().f_code.co_name, realm, client_id, role_name))
        globals.logger.debug('#' * 50)

        token_user = os.environ["EXASTRO_KEYCLOAK_USER"]
        token_password = os.environ["EXASTRO_KEYCLOAK_PASSWORD"]
        token_realm_name = os.environ["EXASTRO_KEYCLOAK_MASTER_REALM"]

        # ロール毎のユーザ情報リスト取得 get user info list for each role
        role_users_info = api_keycloak_call.keycloak_role_uesrs_get(realm, client_id, role_name, token_user, token_password, token_realm_name)

        rows = []
        for user_info in role_users_info:
            row = {
                "user_id": user_info["id"],
                "user_name": user_info["username"],
                "first_name": user_info["firstName"],
                "last_name": user_info["lastName"],
                "email": user_info["email"]
            }
            rows.append(row)

        return jsonify({"result": "200", "rows": rows }), 200

    except Exception as e:
        return common.serverError(e)
