# -*- coding: utf-8 -*-

__all__ = ["BaseException", "TestException", "TargetDirException", "IncorrectInputException", "TargetOptionException",
           "ParamTypeException", "ProtobufSourceNotExist", "ParamLenException"]


class BaseException(Exception):
    def __init__(self, msg=None, detail_msg=None):
        self.msg = msg
        self.detail_msg = detail_msg

    def __str__(self):
        exception_msg = "Message:"
        if self.msg:
            exception_msg = f"{exception_msg} {self.msg}"
        else:
            exception_msg = f"{exception_msg} 暂无"
        if self.detail_msg:
            exception_msg = f"{exception_msg}\n  {self.detail_msg}"
        return exception_msg


"""基础异常"""


class TestException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "程序测试调试异常")


class TargetDirException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "暂时不支持此路径")


class TargetOptionException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "暂时不支持此选项")


class IncorrectInputException(BaseException):
    def __init__(self, detail_msg=None):
        BaseException.__init__(self, "输入值错误", detail_msg)


class ParamTypeException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "参数类型错误")


class ParamLenException(BaseException):
    def __init__(self):
        BaseException.__init__(self, "参数长度不一致错误")


class OvertopRangeException(BaseException):
    pass


"""protobuf相关异常"""


class ProtobufSourceNotExist(BaseException):
    def __init__(self):
        BaseException.__init__(self, "Proto源文件不存在或为空")



