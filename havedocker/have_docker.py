# -*- coding:utf-8 -*-


import os
import inspect
import getpass
import platform
import subprocess


class DockerInitRunError(Exception):
    """
        # 定义DockerInitRunError异常，__main__主机没有docker.server。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerRunImageError(Exception):
    """
        # 定义DockerRunImageError异常，实例化未知镜像错误。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerRunImageTypeError(Exception):
    """
        # 定义DockerRunImageError异常，实例化未知镜像错误。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerHistoryArgsError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerHistoryTypeError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerfileError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerfileLocationError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class DockerStatusError(Exception):
    """
        # 定义DockerStatusError异常，容器已启动。
    """

    def __init__(self, Errorinfo):
        super().__init__(self)
        self.errorinfo = Errorinfo

    def __str__(self):
        return self.errorinfo


class Agility_Docker(object):
    def __init__(self, debug=False, help=False):
        """
        :param debug: 仅测试下，debug=True，将忽略docker是否存在。这将导致部分功能无法使用。
        :param help: 默认False， 声明：需要方法提示时，help=True即可。
        :param return: 在__init__中，并不设定return的存在，以exit()作为闭包。
        """
        if help:
            print("""{} From help:
            :param debug: 仅测试下，debug=True，将忽略docker是否存在。这将导致部分功能无法使用。
            :param help: 默认False， 声明：需要方法提示时，help=True即可。""".format(self.__class__.__name__))
            exit()
        if not debug:
            cmd = subprocess.Popen(
                'docker --help',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            self.cmd_status = cmd.wait()
            if self.cmd_status == 1:
                raise DockerInitRunError('__main__.主机没有docker.server')
            elif self.cmd_status == 127:
                raise DockerInitRunError(
                    '__main__.主机并不存在docker指令集 status={}'.format(
                        cmd.wait()))
            elif self.cmd_status == 128:
                raise DockerInitRunError(
                    '__main__.效验docker无效， status={}'.format(
                        cmd.wait()))

    @staticmethod
    def get__function_name():
        return inspect.stack()[1][3]

    def cmd_query(self, debug=False, self_object='vessel', help=False):
        """
            # 用来查看所有在后台运行的docker实例化对象
            :param self_object: ('vessel' / 'images') 默认为'vessel'，只接收所有实例化容器信息。
            为'images'时，将收集本地docker中所存在images。
            :param debug: 默认为False。不为True时，只返回实例化vessel对象组的dict或images对象组的dict。
            为True时，不做修改将直接返回str
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果docker存在后台运行容器，返回容器ID字典，dict_key为vessel的ID，值为除ID之外所有查询到的结果。
            反之，只返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param self_object: ('vessel' / 'images') 默认为'vessel'，只接收所有实例化容器信息。
            为'images'时，将收集本地docker中所存在images。
            :param debug: 默认为False。不为True时，只返回实例化vessel对象组的dict或images对象组的dict。
            为True时，不做修改将直接返回str
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果docker存在后台运行容器，返回容器ID字典，dict_key为vessel的ID，值为除ID之外所有查询到的结果。
            反之，只返回False。当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        if self_object == 'vessel':
            cmd = subprocess.Popen('docker ps -a', stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if debug:
                return cmd
            if cmd.count('\n') > 1:
                vessel_list = cmd.split('\n')
                vessel = {}
                vessel_type = vessel_list[0]

                vessel_id = [
                    vessel_type.index('CONTAINER ID'),
                    vessel_type.index('IMAGE')]
                vessel_image = [
                    vessel_type.index('IMAGE'),
                    vessel_type.index('COMMAND')]
                vessel_command = [
                    vessel_type.index('COMMAND'),
                    vessel_type.index('CREATED')]
                vessel_created = [
                    vessel_type.index('CREATED'),
                    vessel_type.index('STATUS')]
                vessel_status = [
                    vessel_type.index('STATUS'),
                    vessel_type.index('PORTS')]
                vessel_ports = [
                    vessel_type.index('PORTS'),
                    vessel_type.index('NAMES')]
                vessel_names = [vessel_type.index('NAMES'), len(vessel_type)]
                vessel_body = vessel_list[1:-1]

                for selfvesssel in vessel_body:
                    vessel['{}'.format(selfvesssel[vessel_id[0]:vessel_id[1]])] = {
                        'image': selfvesssel[vessel_image[0]:vessel_image[1]],
                        'command': selfvesssel[vessel_command[0]:vessel_command[1]],
                        'created': selfvesssel[vessel_created[0]:vessel_created[1]],
                        'status': selfvesssel[vessel_status[0]:vessel_status[1]],
                        'ports': selfvesssel[vessel_ports[0]:vessel_ports[1]],
                        'names': selfvesssel[vessel_names[0]:vessel_names[1]]
                    }
                return vessel
            else:
                return False
        elif self_object == 'images':
            cmd = subprocess.Popen('docker images', stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if debug:
                return cmd
            if cmd.count('\n') > 1:
                images_list = cmd.split('\n')
                images = {}
                images_type = images_list[0]
                images_repository = [
                    images_type.index('REPOSITORY'),
                    images_type.index('TAG')]
                images_tag = [
                    images_type.index('TAG'),
                    images_type.index('IMAGE ID')]
                images_image_id = [
                    images_type.index('IMAGE ID'),
                    images_type.index('CREATED')]
                images_created = [
                    images_type.index('CREATED'),
                    images_type.index('SIZE')]
                images_size = [images_type.index('SIZE'), len(images_type)]
                images_body = images_list[1:-1]
                for selfimage in images_body:
                    images['{}'.format(selfimage[images_repository[0]:images_repository[1]])] = {
                        'tag': selfimage[images_tag[0]:images_tag[1]],
                        'image_id': selfimage[images_image_id[0]:images_image_id[1]],
                        'created': selfimage[images_created[0]:images_created[1]],
                        'size': selfimage[images_size[0]:images_size[1]]
                    }
                return images
            else:
                return False

    def cmd_pull_images(self, images_name=None, help=False):
        """
            # 拉取镜像
            :param images_name: 提供的镜像名，以作拉取对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果被拉取的镜像不存在，程序执行完成之后将会返回True。
            若不提供images_name，将返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param images_name: 提供的镜像名，以作拉取对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果被拉取的镜像不存在，程序执行完成之后将会返回True。
            若不提供images_name，将返回False。当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        if not images_name:
            return False
        commend = os.popen('docker pull {}'.format(images_name)).read()
        print(commend)
        return True

    def cmd_run_vessel(self, images_name=None,
                       run_cmd='/bin/bash',
                       vessel_name=None,
                       cpu_shares=None,
                       cpuset_cpus=None,
                       blkio_weight=None,
                       help=False
                       ):
        """
            # 实例化容器对象，并返回实例化对象的唯一HASH64中前12位，因为这是容器ID
            :param images_name: 默认为None
            :param run_cmd: 默认实例化运行镜像时，将会以'/bin/bash'
            :param vessel_name: str
            :param cpu_shares: int ~= int8 -128~127 -128~65535
            :param cpuset_cpus: int [0, 1, 2]
            :param blkio_weight: int 10~1000
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: HASH64[:12]，当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param images_name: 默认为None
            :param run_cmd: 默认实例化运行镜像时，将会以'/bin/bash'
            :param vessel_name: str
            :param cpu_shares: int ~= int8 -128~127 -128~65535
            :param cpuset_cpus: int [0, 1, 2]
            :param blkio_weight: int 10~1000
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: HASH64[:12]，当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        self_commend = 'docker run -itd'
        if not images_name:
            raise DockerRunImageError('{}镜像不存在，无法实例化。'.format(images_name))
        if run_cmd is None:
            raise DockerRunImageTypeError('{} Error'.format(run_cmd))
        if vessel_name is not None:
            if not isinstance(vessel_name, str):
                raise DockerRunImageTypeError('{} Namespace Error')
            else:
                vessel_name = '--name %s' % vessel_name
        else:
            vessel_name = ''
        if cpu_shares is not None:
            if not (0 <= cpu_shares <= 65535):
                raise DockerRunImageTypeError(
                    '{} Type is int, -128<= cpu_shares <=127, number error'.format(cpu_shares))
            else:
                cpu_shares = '--cpu-shares {}'.format(cpu_shares)
        else:
            cpu_shares = ''
        if cpuset_cpus is not None:
            if cpuset_cpus not in [0, 1, 2]:
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< cpuset_cpus <=127, number error'.format(cpuset_cpus))
            else:
                cpuset_cpus = '--cpus {}'.format(cpuset_cpus)
        else:
            cpuset_cpus = ''
        if blkio_weight is not None:
            if not (10 < blkio_weight <= 1000):
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< blkio_weight <=65535, number error'.format(blkio_weight))
            else:
                blkio_weight = '--blkio-weight {}'.format(blkio_weight)
        else:
            blkio_weight = ''
        self_commend = '{} {} {} {} {} {} {} '.format(self_commend,
                                                      vessel_name,
                                                      cpu_shares,
                                                      cpuset_cpus,
                                                      blkio_weight,
                                                      images_name,
                                                      run_cmd)
        commend = os.popen(self_commend).read()
        if commend.count('\n') > 1:
            images_id = commend.split('\n')[-1][:12]
        else:
            images_id = commend[:12]
        return images_id

    def docker_rm_object(self, Exclude=None, self_object='vessel', help=False):
        """
            # docker_rm_object 用来删除实例化容器
            :param Exclude: 默认为None。添加排除项，除Exclude之外删除
            :param self_object: 默认对象为实例化容器 ('vessel' / 'images')
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None。如果docker后台运行的容器介被删除，将以True作为尾值闭包。
            如果cmd_ps_a()并没有给出正确值，那么将返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param Exclude: 默认为None。添加排除项，除Exclude之外删除
            :param self_object: 默认对象为实例化容器 ('vessel' / 'images')
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None。如果docker后台运行的容器介被删除，将以True作为尾值闭包。
            如果cmd_ps_a()并没有给出正确值，那么将返回False。当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        vessel_id = self.cmd_query()
        images_id = self.cmd_query(self_object='images')
        if self_object == 'vessel':
            if vessel_id:
                if Exclude:
                    for e in Exclude:
                        if e in vessel_id.keys():
                            del vessel_id[e]
                        else:
                            pass
                    for j in vessel_id:
                        os.popen('docker rm -f {}'.format(j))
                else:
                    for j in vessel_id:
                        os.popen('docker rm -f {}'.format(j))
                return True
            else:
                return False
        elif self_object == 'images':
            if images_id:
                if Exclude:
                    for e in Exclude:
                        if e in images_id.keys():
                            del images_id[e]
                        else:
                            pass
                    for j in images_id.keys():
                        os.popen(
                            'docker rmi -f {}'.format(images_id[j]['image_id']))
                else:
                    for j in images_id:
                        os.popen(
                            'docker rmi -f {}'.format(images_id[j]['image_id']))
                return True
            else:
                return False

    def docker_cp(self, goods=None, vessel=None, path=':/', help=False):
        """
            # cmd_cp_into 用于就文件、文件夹复制移动到实例化容器指定路径上
            :param goods: 被复制对象(file/dir)
            :param vessel: 实例化容器
            :param path: 实例化容器中的指定路径
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: goods和vessel同时存在(True), 将返回True。不满条件，返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param goods: 被复制对象(file/dir)
            :param vessel: 实例化容器
            :param path: 实例化容器中的指定路径
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: goods和vessel同时存在(True), 将返回True。不满条件，返回False。当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        if goods and vessel:
            os.popen('docker cp {} {}{}'.format(goods, vessel, path))
            return True
        else:
            return False

    def docker_history(self, argument=None, all=False, help=False):
        """
            # docker_history 将对镜像进行分层树
            :param argument: 镜像repository
            :param all: 默认为False， all=False时，argument需要提供参数。
                    all=True时, argument不需要参数支持将返回所有镜像的history
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: *args为单值时，返回command。*args为list时，返回key-value。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param argument: 镜像repository
            :param all: 默认为False， all=False时，argument需要提供参数。
                    all=True时, argument不需要参数支持将返回所有镜像的history
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: *args为单值时，返回command。*args为list时，返回key-value。当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        if not all:
            try:
                assert argument
            except AssertionError:
                raise DockerHistoryArgsError(
                    '{}缺少参数，argument=False'.format(argument))
            if isinstance(argument, str):
                command = subprocess.Popen(
                    'docker history {}'.format(argument),
                    stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            elif isinstance(argument, list):
                history = {}
                for sh in argument:
                    command = subprocess.Popen(
                        'docker history {}'.format(argument),
                        stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    history[sh] = command
                return history
            else:
                raise DockerHistoryTypeError(
                    '{} unknown Type()'.format(argument))
        else:
            cmd = self.cmd_query(self_object='images')
            history = {}
            for sh in cmd.keys():
                if 'none' in sh:
                    continue
                elif 'daocloud.io/library/nginx' in sh:
                    continue
                else:
                    command = subprocess.Popen(
                        'docker history {}'.format(sh),
                        stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    history[sh] = command
            return history

    def dockerfile(self,
                   FROM='centos',
                   MAINTAINER=platform.system(),
                   RUN=None,
                   CMD=None,
                   COPY=None,
                   ADD=None,
                   EXPOSE=None,
                   WORKDIR=None,
                   ENTRYPOINT=None,
                   ENV=None,
                   VOLUME=None, help=False):
        """
            # existing problem
            - 关于dockerfile文件中，MAINTAINER作者项暂时以兼容方式获取username
            - 关于dockerfile-body中，暂时采用dict方式进行存储。
            - 暂未编写VOLUME，
            :param FROM: 镜像源
            :param MAINTAINER : 默认为系统名称，支持自定义
            :param RUN: 例子 RUN=['pip3 install tornado', 'apt update']，type=str/list
            :param CMD: 例子 CMD=['apt install httpd', 'yum install tree'], type=str/list
            :param COPY: 例子 COPY=[['EPC_test', '/'], [3]] type=str/list
                    COPY位置摆放逻辑：并不以下标为准，以存在的元素数量。如果有七条命令，那么指定的位置将为第几条命令。不存在0
            :param ADD: 例子 ADD=[['nginx.1.14.2.tar', '/'], [4]] type=str/list
            :param EXPOSE: 例子 EXPOSE=[80, 8080, 443], type=int/list 始终位于dockerfile最底层
            :param WORKDIR: 例子 WORKDIR=[[['/root'], ['/bin']], [2, 3]], type=str/list
            :param ENTRYPOINT: 例子 ENTRYPOINT=[[['/bin/echo'], ['Hello World']], [2, 3]]
            :param ENV: 例子 type=str/list
                    ENV=[
                         [['WELCOME "You are in my container, welcome!"'],
                          ['name Cloud Man ENTRYPOINT echo "Hello, $name"']],
                         [2, 3]
                        ]
            :param VOLUME: 例子 VOLUME=["/data1", "/data2"]，位于FROM、MAINTAINER之后 type=str/list
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None， 当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param FROM: 镜像源
            :param MAINTAINER : 默认为系统名称，支持自定义
            :param RUN: 例子 RUN=['pip3 install tornado', 'apt update']，type=str/list
            :param CMD: 例子 CMD=['apt install httpd', 'yum install tree'], type=str/list
            :param COPY: 例子 COPY=[['EPC_test', '/'], [3]] type=str/list
                    COPY位置摆放逻辑：并不以下标为准，以存在的元素数量。如果有七条命令，那么指定的位置将为第几条命令。不存在0
            :param ADD: 例子 ADD=[['nginx.1.14.2.tar', '/'], [4]] type=str/list
            :param EXPOSE: 例子 EXPOSE=[80, 8080, 443], type=int/list 始终位于dockerfile最底层
            :param WORKDIR: 例子 WORKDIR=[[['/root'], ['/bin']], [2, 3]], type=str/list
            :param ENTRYPOINT: 例子 ENTRYPOINT=[[['/bin/echo'], ['Hello World']], [2, 3]]
            :param ENV: 例子 type=str/list
                    ENV=[
                         [['WELCOME "You are in my container, welcome!"'],
                          ['name Cloud Man ENTRYPOINT echo "Hello, $name"']],
                         [2, 3]
                        ]
            :param VOLUME: 例子 VOLUME=["/data1", "/data2"]，位于FROM、MAINTAINER之后 type=str/list
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None， 当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        dockerfile = []
        os_name = MAINTAINER

        dockerfile.append('FROM {}'.format(FROM))

        if os_name == 'LINUX':
            username = getpass.getuser()
            dockerfile.append('MAINTAINER {} {}'.format(os_name, username))
        elif os_name == 'Windows':
            username = os.environ['USERNAME']
            dockerfile.append('MAINTAINER {} {}'.format(os_name, username))
        else:
            if MAINTAINER is str:
                dockerfile.append('MAINTAINER {}'.format(MAINTAINER))
            else:
                os_name = 'None'
                username = 'None'
                dockerfile.append('MAINTAINER {} {}'.format(os_name, username))

        type_volume = type(VOLUME)
        if type_volume is list:
            for volume in VOLUME:
                dockerfile.append('VOLUME {}'.format(volume))
        elif type_volume is 'NoneType':
            pass

        type_run = type(RUN)
        if type_run is list:
            for run in RUN:
                dockerfile.append('RUN {}'.format(run))
        elif type_run is 'NoneType':
            pass

        type_command = type(CMD)
        if type_command is list:
            for command in CMD:
                dockerfile.append('CMD {}'.format(command))
        elif type_command is 'NoneType':
            pass

        def location(object, head_cmd=None):
            type_copy = type(object)
            if type_copy is list:
                if len(object) > 1:
                    if len(object[0]) == len(object[1]):
                        if type_run is 'NoneType':
                            for cmd in object[0]:
                                dockerfile.append(
                                    '{} {}'.format(head_cmd, cmd))
                        else:
                            for body in object[0]:
                                dockerfile.append(
                                    '{} {}'.format(head_cmd, body))
                            for num in object[1]:
                                dockerfile.remove('{} {}'.format(
                                    head_cmd, object[0][object[1].index(num)]))
                                dockerfile.insert(
                                    num - 1, '{} {}'.format(head_cmd, object[0][object[1].index(num)]))
                    else:
                        raise DockerfileError(
                            '{} 提供了{} body参数， 提供了{} 位置参数'.format(
                                head_cmd, len(
                                    object[0]), len(
                                    object[1])))
                elif len(object):
                    for cmd in object[0]:
                        dockerfile.append('{} {}'.format(head_cmd, cmd))
                else:
                    pass
            elif type_copy is str:
                dockerfile.append('{} {}'.format(head_cmd, object))
            elif type_copy is 'NoneType':
                pass

        location(object=COPY, head_cmd='COPY')
        location(object=ADD, head_cmd='ADD')
        location(object=WORKDIR, head_cmd='WORKDIR')
        location(object=ENTRYPOINT, head_cmd='ENTRYPOINT')
        location(object=ENV, head_cmd='ENV')

        type_port = type(EXPOSE)
        if type_port is list:
            for port in EXPOSE:
                dockerfile.append('EXPOSE {}'.format(port))
        elif type_port is 'NoneType':
            pass
        elif type_port is int:
            dockerfile.append('EXPOSE {}'.format(EXPOSE))

        if 'FROM' in dockerfile[0]:
            pass
        else:
            raise DockerfileLocationError(
                "Your dockerfile first line is {}, Is should be 'FROM ...'!".format(
                    (dockerfile[0].split(' '))[0]))

        for element in dockerfile:
            print(element)

    def vessel_status(self, argument='unpause', vessel_id=None, help=False):
        """
            vessel_status 方法，暂停或继续运行容器。区别于cmd_run_vessel()方法，提供针对容器管理的方案。
            :param argument: 默认'unpause'， 可选参数 ['unpause' / 'pause']
            :param vessel_id: 实例化容器ID，
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None， 当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From Help:
            vessel_status 方法，暂停或继续运行容器。区别于cmd_run_vessel()方法，提供针对容器管理的方案。
            :param argument: 默认'unpause'， 可选参数 ['unpause' / 'pause']
            :param vessel_id: 实例化容器ID，
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None， 当help=True时，将返回'help'""".format(self.__class__.__name__, self.get__function_name()))
            return 'help'
        if vessel_id is None:
            raise DockerStatusError('vessel_status需要vessel_id参数， 而非None')
        vessel_list = self.cmd_query()
        if argument == 'unpause':
            if vessel_id in vessel_list.keys():
                if '(Paused)' in vessel_list.get(vessel_id)['status']:
                    subprocess.Popen(
                        'docker {} {}'.format(argument, vessel_id),
                        stdout=subprocess.PIPE)
                else:
                    raise DockerStatusError(
                        '{}容器状态并非...(Paused)，unpause失效'.format(vessel_id))
            else:
                raise DockerStatusError('{}容器未存在， unpause失效'.format(vessel_id))
        elif argument == 'pause':
            if vessel_id in vessel_list.keys():
                subprocess.Popen(
                    'docker {} {}'.format(argument, vessel_id),
                    stdout=subprocess.PIPE)
            else:
                raise DockerStatusError('{}容器未存在， pause失效'.format(vessel_id))
        else:
            raise DockerStatusError('argument={}，未知指令'.format(argument))
