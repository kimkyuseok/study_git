# 2024 04 19 로그 log
# 로그를 표시할수 있게 한다.
# 외주업체에서 에러가 나면 로그를 보고 판단한다.
# 스크립트 작성은 PEP8 기준으로 작성한다.
# 비브 파이프라인 글로벌 로그 부분 이해를 못한 관계로 빼고 진행

import os
import logging
# 설치된 파이썬 기본 라이브러리에 파일있음 확인
# print(logging.__file__)
# 로깅 레벨을 변경해보자.


class LogLevel:
    INFO = 'info'
    DEBUG = 'debug'
    CRITICAL = 'critical'
    ERROR = 'error'


def set_log_level(logger,log_level):
    # 준비한 로그가 아니면 패스
    if log_level not in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.CRITICAL, LogLevel.ERROR]:
        return
    if log_level == LogLevel.INFO:
        logger.setLevel(logging.INFO)
    elif log_level == LogLevel.DEBUG:
        logger.setLevel(logging.DEBUG)
    elif log_level == LogLevel.CRITICAL:
        logger.setLevel(logging.CRITICAL)
    elif log_level == LogLevel.ERROR:
        logger.setLevel(logging.ERROR)


def get_logger(name,log_level=None,filename=None):
    # 로거에 정의할 이름. 주로 해당 클래스나 모듈이름이 들어간다고함 - 경훈td -
    logger = logging.getLogger(name)

    # 핸들러 준비
    logger.handlers = []

    # 포메터 정의
    formatter = logging.Formatter('%(asctime)s %(levelname)7s [%(name)s:%(lineno)5d] %(message)s')

    # 콘솔 핸들러 정의
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 파일 핸들러 정의
    if filename:
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # 마야 로거에 확산 막는다.
    logger.propagate = 0

    if log_level:
        set_log_level(logger, log_level)
    return logger
