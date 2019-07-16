# -*- coding:utf-8 -*-
from flask import Blueprint

test_bp = Blueprint('test_bp', __name__)


@test_bp.route('/', methods=['GET', 'POST'])
def test_index():
    # app.logger.info('hello,world')
    # logging.info('hello,world')
    return ('hello,world!!!')



