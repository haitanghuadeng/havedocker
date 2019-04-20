# -*- coding:utf-8 -*-


class DockerInitRunError(Exception):
    """
        # 定义DockerInitRunError异常，当前主机没有docker.server。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerRunImageError(Exception):
    """
        # 定义DockerRunImageError异常，实例化未知镜像错误。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerRunImageTypeError(Exception):
    """
        # 定义DockerRunImageTypeError异常，实例化未知镜像错误。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerHistoryArgsError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerHistoryTypeError(Exception):
    """
        # 定义DockerHistoryTypeError异常，层级树类型错误。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerfileError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerfileLocationError(Exception):
    """
        # 定义DockerfileLocationError异常，指令集位置错误。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerStatusError(Exception):
    """
        # 定义DockerStatusError异常，容器已启动。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerPushError(Exception):
    """
        # 定义DockerPushError异常，容器已启动。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerPullError(Exception):
    """
        # 定义DockerPushError异常，容器已启动。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerNetWorkError(Exception):
    """
        # 定义DockerNetWorkError异常，错误指令。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerPortError(Exception):
    """
        # 定义DockerPortError异常，不存在的ID或名称。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerTagError(Exception):
    """
        # 定义DockerTagError异常，不存在的ID或名称。
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerNewNetworkError(Exception):
    """
        # 定义DockerNewNetworkError异常
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerQueryNetworkError(Exception):
    """
        # 定义DockerQueryNetworkError异常
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerRmNetworkError(Exception):
    """
        # 定义DockerRmNetworkError异常
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerConnectNetworkError(Exception):
    """
        # 定义DockerConnectNetworkError异常
    """

    def __init__(self, Errorinfo):
        super(Exception, self).__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo
