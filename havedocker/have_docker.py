# -*- coding:utf-8 -*-


import os
import inspect
import getpass
import platform
import subprocess
from havedocker.DockerError import *


class Agility_Docker(object):
    def __init__(self, help=False):
        """
        :param help: 默认False， 声明：需要方法提示时，help=True即可。
        :param return: 在__init__中，并不设定return的存在，以exit()作为闭包。
        """
        if help:
            print("""{} From help:
            :param debug: 仅测试下，debug=True，将忽略docker是否存在。这将导致部分功能无法使用。
            :param help: 默认False， 声明：需要方法提示时，help=True即可。""".format(self.__class__.__name__))
        self.DockerHelp = subprocess.Popen(
            'docker --help',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        self.DockerVersion = subprocess.Popen(
            'docker -v',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()[0].decode()
        self.DockerStatus = self.DockerHelp.wait()
        if self.DockerStatus == 1:
            raise DockerInitRunError('当前主机没有docker.server')
        elif self.DockerStatus == 127:
            raise DockerInitRunError(
                '当前主机并不存在docker指令集 status={}'.format(
                    self.DockerHelp.wait()))
        elif self.DockerStatus == 128:
            raise DockerInitRunError(
                '效验docker无效， status={}'.format(
                    self.DockerHelp.wait()))

    @staticmethod
    def __get__function_name():
        return inspect.stack()[1][3]

    def DockerQuery(self, formatting=False, self_object='vessel', help=False):
        """
            # DockerQuery方法，用来查看所有在后台运行的docker实例化对象
            :param self_object: ['vessel' / 'images'] 默认为'vessel'，只接收所有实例化容器信息。
            为'images'时，将收集本地docker中所存在images。
            :param formatting: 默认为False。不为True时，只返回实例化vessel对象组的dict或images对象组的dict。
            为True时，不做修改将直接返回str
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果docker存在后台运行容器，返回容器ID字典，dict_key为vessel的ID，值为除ID之外所有查询到的结果。
            反之，只返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param self_object: ['vessel' / 'images'] 默认为'vessel'，只接收所有实例化容器信息。
            为'images'时，将收集本地docker中所存在images。
            :param debug: 默认为False。不为True时，只返回实例化vessel对象组的dict或images对象组的dict。
            为True时，不做修改将直接返回str
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果docker存在后台运行容器，返回容器ID字典，dict_key为vessel的ID，值为除ID之外所有查询到的结果。
            反之，只返回False。当help=True时，将返回'help'""".format(self.__class__.__name__, self.__get__function_name()))
            return 'help'
        if self_object == 'vessel':
            cmd = subprocess.Popen('docker ps -a', stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if formatting:
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
                vessel_names = [
                    vessel_type.index('NAMES'),
                    len(vessel_type) + 1]
                vessel_body = vessel_list[1:-1]

                for selfvessel in vessel_body:
                    vessel['{}'.format((selfvessel[vessel_id[0]:vessel_id[1]]).rstrip())] = {
                        'image': (selfvessel[vessel_image[0]:vessel_image[1]]).rstrip(),
                        'command': (selfvessel[vessel_command[0]:vessel_command[1]]).rstrip(),
                        'created': (selfvessel[vessel_created[0]:vessel_created[1]]).rstrip(),
                        'status': (selfvessel[vessel_status[0]:vessel_status[1]]).rstrip(),
                        'ports': (selfvessel[vessel_ports[0]:vessel_ports[1]]).rstrip(),
                        'names': (selfvessel[vessel_names[0]:vessel_names[1]]).rstrip()
                    }
                return vessel
            else:
                return False
        elif self_object == 'images':
            cmd = subprocess.Popen('docker images', stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if formatting:
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
                images_size = [images_type.index('SIZE'), len(images_type) + 1]
                images_body = images_list[1:-1]
                for selfimage in images_body:
                    images['{}'.format((selfimage[images_repository[0]:images_repository[1]]).rstrip())] = {
                        'tag': (selfimage[images_tag[0]:images_tag[1]]).rstrip(),
                        'image_id': (selfimage[images_image_id[0]:images_image_id[1]]).rstrip(),
                        'created': (selfimage[images_created[0]:images_created[1]]).rstrip(),
                        'size': (selfimage[images_size[0]:images_size[1]]).rstrip()
                    }
                return images
            else:
                return False

    def DockerPull(self, images_name=None, help=False):
        """
            # DockerPull方法，拉取镜像
            :param images_name: 提供的镜像名，以作拉取对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回执行命令结果，如果未提供拉取镜像名称，抛出异常。
        """
        if help:
            print(
                """{}.{} From help:
            :param images_name: 提供的镜像名，以作拉取对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回执行命令结果，如果未提供拉取镜像名称，抛出异常。'""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
            return 'help'
        if images_name:
            commend = os.popen('docker pull {}'.format(images_name)).read()
            return commend
        else:
            raise DockerPullError(
                "images_name:'{}'is None, 需要提供一个镜像名参数".format(images_name))

    def DockerRun(self, images_name=None,
                  run_cmd='/bin/bash',
                  vessel_name=None,
                  network=None,
                  ip=None,
                  cpu_shares=None,
                  cpuset_cpus=None,
                  blkio_weight=None,
                  help=False
                  ):
        """
            # existing problem
                memory: int 100
                memory_swap: int memory+swap
                暂未设定memory、BlockIO相关参数
            # 实例化容器对象，并返回实例化对象的唯一HASH64中前12位，因为这是容器ID
            :param images_name: 默认为None
            :param run_cmd: 默认实例化运行镜像时，将会以'/bin/bash'
            :param vessel_name: str
            :param network: 指定虚拟网卡类型, 可指定自定义网卡类型 str
            :param ip: 指定IP地址 str
            :param cpu_shares: int 0~65535
            :param cpuset_cpus: int [0, 1, 2]
            :param blkio_weight: int 10~1000
            :param help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 返回HASH64[:12]，以及命令执行结果
        """
        if help:
            print(
                """{}.{} From help:
            :param images_name: 默认为None
            :param run_cmd: 默认实例化运行镜像时，将会以'/bin/bash'
            :param vessel_name: str
            :param network: 指定虚拟网卡类型, 可指定自定义网卡类型 str
            :param ip: 指定IP地址 str
            :param cpu_shares: int 0~65535
            :param cpuset_cpus: int [0, 1, 2]
            :param blkio_weight: int 10~1000
            :param help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 返回HASH64[:12]，以及命令执行结果""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
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
                vessel_name = ' --name %s' % vessel_name
        else:
            vessel_name = ''
        if cpu_shares is not None:
            if not (0 <= cpu_shares <= 65535):
                raise DockerRunImageTypeError(
                    '{} Type is int, -128<= cpu_shares <=127, number error'.format(cpu_shares))
            else:
                cpu_shares = ' --cpu-shares {}'.format(cpu_shares)
        else:
            cpu_shares = ''
        if cpuset_cpus is not None:
            if cpuset_cpus not in [0, 1, 2]:
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< cpuset_cpus <=127, number error'.format(cpuset_cpus))
            else:
                cpuset_cpus = ' --cpus {}'.format(cpuset_cpus)
        else:
            cpuset_cpus = ''
        if blkio_weight is not None:
            if not (10 < blkio_weight <= 1000):
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< blkio_weight <=65535, number error'.format(blkio_weight))
            else:
                blkio_weight = ' --blkio-weight {}'.format(blkio_weight)
        else:
            blkio_weight = ''
        if network:
            if isinstance(network, str):
                network_str = self.DockerQueryNetwork(formatting=True)
                if network in network_str:
                    network = ' --network {}'.format(network)
                else:
                    raise DockerRunImageError(
                        "network:{}, 提供了错误的虚拟网卡名称".format(network))
            else:
                raise DockerRunImageError(
                    "network:{}, 提供了错误格式的虚拟网卡".format(type(network)))
        else:
            network = ''
        if ip:
            if isinstance(type(ip), str):
                network = ' --ip {}'.format(ip)
            else:
                raise DockerRunImageError(
                    "ip:{], 提供了错误格式的虚拟网卡".format(type(ip)))
        else:
            ip = ''
        self_commend = '{}{}{}{}{}{}{} {} {}'.format(self_commend,
                                                     vessel_name,
                                                     cpu_shares,
                                                     cpuset_cpus,
                                                     blkio_weight,
                                                     network,
                                                     ip,
                                                     images_name,
                                                     run_cmd)
        commend = os.popen(self_commend).read()
        if commend.count('\n') > 1:
            images_id = commend.split('\n')[-1][:12]
        else:
            images_id = commend[:12]
        return [images_id, commend]

    def DockerRmObject(self, Exclude=None, self_object='vessel', help=False):
        """
            # DockerRmObject 用来删除实例化容器
            :param Exclude: 默认为None。添加排除项，除Exclude之外删除
            :param self_object: 默认对象为实例化容器 ['vessel' / 'images']
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None。如果docker后台运行的容器介被删除，将以True作为尾值闭包。
            如果cmd_ps_a()并没有给出正确值，那么将返回False。当help=True时，将返回'help'
        """
        if help:
            print("""{}.{} From help:
            :param Exclude: 默认为None。添加排除项，除Exclude之外删除
            :param self_object: 默认对象为实例化容器 ['vessel' / 'images']
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None。如果docker后台运行的容器介被删除，将以True作为尾值闭包。
            如果cmd_ps_a()并没有给出正确值，那么将返回False。
                    当help=True时，将返回'help'""".format(self.__class__.__name__, self.__get__function_name()))
            return 'help'
        vessel_id = self.DockerQuery()
        images_id = self.DockerQuery(self_object='images')
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
                    for E in Exclude:
                        if E in images_id.keys():
                            del images_id[E]
                        else:
                            pass
                    for idk in images_id.keys():
                        os.popen(
                            'docker rmi -f {}'.format(images_id[idk]['image_id']))
                else:
                    for id in images_id:
                        os.popen(
                            'docker rmi -f {}'.format(images_id[id]['image_id']))
                return True
            else:
                return False

    def DockerCp(self, goods=None, vessel=None, path=':/', help=False):
        """
            # DockerCp 用于就文件、文件夹复制移动到实例化容器指定路径上
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
            :return: goods和vessel同时存在(True), 将返回True。不满条件，返回False。当help=True时，将返回'help'""".format(
                self.__class__.__name__, self.__get__function_name()))
            return 'help'
        if goods and vessel:
            os.popen('docker cp {} {}{}'.format(goods, vessel, path))
            return True
        else:
            return False

    def DockerHistory(self, argument=None, all=False, help=False):
        """
            # DockerHistory 将对镜像进行分层树
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
            :return: *args为单值时，返回command。*args为list时，返回key-value。
                    当help=True时，将返回'help'""".format(
                self.__class__.__name__, self.__get__function_name()))
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
            cmd = self.DockerQuery(self_object='images')
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

    def DockerFile(self,
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
            print(
                """{}.{} From help:
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
            :return: 默认返回None， 当help=True时，将返回'help'""".format(
                    self.__class__.__name__, self.__get__function_name()))
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

    def DockerVesselStatus(self,
                           argument='unpause',
                           vessel_id=None,
                           help=False):
        """
            DockerVesselStatus 方法，暂停或继续运行容器。区别于cmd_run_vessel()方法，提供针对容器管理的方案。
            :param argument: 默认'unpause'， 可选参数 ['unpause' / 'pause']
            :param vessel_id: 实例化容器ID，
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 默认返回None， 当help=True时，将返回'help'
        """
        if help:
            print(
                """{}.{} From Help:
                            vessel_status 方法，暂停或继续运行容器。区别于cmd_run_vessel()方法，提供针对容器管理的方案。
                            :param argument: 默认'unpause'， 可选参数 ['unpause' / 'pause']
                            :param vessel_id: 实例化容器ID，
                            :param help: 默认False， 声明：需要方法提示时，help=True即可。
                            :return: 默认返回None， 当help=True时，将返回'help'""".format(
                    self.__class__.__name__, self.__get__function_name()))
            return 'help'
        if vessel_id is None:
            raise DockerStatusError('vessel_status需要vessel_id参数， 而非None')
        vessel_list = self.DockerQuery()
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

    def DockerPush(self, images_name=None, help=False):
        """
            # DockerPush方法，推送镜像
            :param images_name: 提供的镜像名，以作推送对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果被推送的镜像存在，程序执行完成之后将会返回True。
            :param help: 当help=True时，将返回'help'
        """
        if help:
            print(
                """{}.{} From help:
            :param images_name: 提供的镜像名，以作拉取对象
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 如果被拉取的镜像不存在，程序执行完成之后将会返回True。
            当help=True时，将返回'help'""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
            return 'help'
        if not images_name:
            raise DockerPushError(
                "images_name:'{}'is None, 需要提供一个镜像名参数".format(images_name))
        commend = os.popen('docker push {}'.format(images_name)).read()
        print(commend)
        return True

    def DockerNewNetwork(
            self,
            create=True,
            driver='bridge',
            subnet=None,
            gateway=None,
            NetWorkName=None,
            help=False):
        """
            # DockerNewNetwork方法，
            :param create: 默认True， create=True时，意为创建虚拟网卡  bool值
            :param driver: 默认None'，指定虚拟网卡类型 ['bridge' / 'overlay' / 'macvlan'] 'host'和'null'无法成为有效命令
            :param subnet: 默认None，提供网段信息 [127.0.0.1/24] str类型
            :param gateway: 默认None，提供网关信息 [192.168.1.1] str类型
            :param NetWorkName: 默认为None，新建虚拟网卡的名称。如果query=False，NetWorkName若为None将抛出异常
            :param help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 默认返回成功执行的命令结果，同样包含错误命令。
        """
        if help:
            print("""{}.{}
                    :param create: 默认True， create=True时，意为创建虚拟网卡  bool值
                    :param driver: 默认None'，指定虚拟网卡类型 ['bridge' / 'overlay' / 'macvlan'] 'host'和'null'无法成为有效命令
                    :param subnet: 默认None，提供网段信息 [127.0.0.1/24] str类型
                    :param gateway: 默认None，提供网关信息 [192.168.1.1] str类型
                    :param NetWorkName: 默认为None，新建虚拟网卡的名称。如果query=False，NetWorkName若为None将抛出异常
                    :param help: 默认False， 声明：需要方法提示时，help=True即可
                    :return: 默认返回成功执行的命令结果，同样包含错误命令。""".format(
                self.__class__.__name__,
                self.__get__function_name()))
            return 'help'
        if not create:
            raise DockerNetWorkError("关键参数错误：create必须为True")
        if not NetWorkName:
            raise DockerNetWorkError(
                "NetWorkName:{} not is None，需要提供参数".format(NetWorkName))
        if type(NetWorkName) not in [str, None]:
            raise DockerNetWorkError("create=True时，必须提供NetWorkName参数")
        if driver not in ['bridge', 'overlay', 'macvlan']:
            raise DockerNetWorkError(
                "--driver {}提供的参数错误，查询help".format(driver))
        if not subnet and not gateway and NetWorkName:
            commend = os.popen(
                'docker network create {}'.format(NetWorkName)).read()
            return commend
        if subnet and not gateway and NetWorkName:
            raise DockerNetWorkError("--gateway 需要提供参数")
        elif not subnet and gateway and NetWorkName:
            raise DockerNetWorkError("--subnet 需要提供参数")
        elif not subnet and not gateway and driver and NetWorkName:
            commend = os.popen('docker network create --driver {} {}'.format(
                driver, NetWorkName)).read()
            return commend
        else:
            if isinstance(
                subnet,
                str) and isinstance(
                gateway,
                str) and isinstance(
                driver,
                    str):
                if '/' in subnet:
                    commend = os.popen(
                        'docker network create --driver {} --subnet {} --subnet {} {}'.format(
                            driver, subnet, subnet, NetWorkName)).read()
                    return commend
                else:
                    raise DockerNetWorkError(
                        "--subnet 需要标准IP地址格式，当前类型不符，查询help")
            else:
                raise DockerNetWorkError(
                    "subnet | gateway | driver 需要str类型，当前类型不符")

    def DockerQueryNetwork(self, formatting=False, Inspect=False, NetworkName=None, help=False):
        """
            # DockerQueryNetwork方法，用于查询docker中的虚拟网卡
            :param formatting: 默认False， 不做处理直接返回执行结果。formatting=True，将返回字典
            :param Inspect: 默认False，Inspect=True时，必须提供NetworkName值
            :param NetworkName: 默认None，需要时，传入str值
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 返回结果
        """
        if help:
            print("""{}.{}            
            :param formatting: 默认False， 不做处理直接返回执行结果。formatting=True，将返回字典(但对inspect无效)
            :param Inspect: 默认False，Inspect=True时，必须提供NetworkName值
            :param NetworkName: 默认None，需要时，传入str值
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 返回结果""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
            return 'help'
        if Inspect:
            if isinstance(NetworkName, str):
                if NetworkName in self.DockerQueryNetwork():
                    command = subprocess.Popen('docker network inspect {}'.format(NetworkName), stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    return command
                else:
                    raise DockerQueryNetworkError("NetworkName:{}错误传参".format(NetworkName))
            else:
                raise DockerQueryNetworkError("NetworkName:{},{}错误类型或未传参".format(type(NetworkName), NetworkName))
        else:
            if isinstance(NetworkName, str):
                raise DockerQueryNetworkError("只查询时，无需NetworkName参数")
            command = subprocess.Popen('docker network ls', stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            if formatting:
                network_list = command.split('\n')
                network = {}
                vessel_type = network_list[0]

                network_id = [
                    vessel_type.index('NETWORK ID'),
                    vessel_type.index('NAME')]
                network_name = [
                    vessel_type.index('NAME'),
                    vessel_type.index('DRIVER')]
                network_driver = [
                    vessel_type.index('DRIVER'),
                    vessel_type.index('SCOPE')]
                vessel_scope = [
                    vessel_type.index('SCOPE'),
                    len(vessel_type) + 1]
                vessel_body = network_list[1:-1]

                for selfvessel in vessel_body:
                    network['{}'.format((selfvessel[network_id[0]:network_id[1]]).rstrip())] = {
                        'name': (selfvessel[network_name[0]:network_name[1]]).rstrip(),
                        'driver': (selfvessel[network_driver[0]:network_driver[1]]).rstrip(),
                        'scope': (selfvessel[vessel_scope[0]:vessel_scope[1]]).rstrip()
                    }
                return network
            else:
                return command

    def DockerRmNetwork(self, Exclude=None, RmNetworkName=None, help=False):
        """
            # DockerRmNetwork方法，用于删除指定的虚拟网卡
            :param Exclude: 默认为None，添加排除项 str / list
            :param RmNetworkName: 选择删除指定的虚拟网卡名称
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 返回执行结果
        """
        if help:
            print("""{}.{}
            :param Exclude: 默认为None，添加排除项
            :param RmNetworkName: 选择删除指定的虚拟网卡名称
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return: 返回执行结果""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
            return 'help'
        if RmNetworkName is None:
            if isinstance(Exclude, str):
                network_list = [i for i in self.DockerQueryNetwork(formatting=True)]
                if Exclude in network_list:
                    network_list.remove(Exclude)
                    for name in network_list:
                        subprocess.Popen('docker network rm {}'.format(name), stdout=subprocess.PIPE)
                return True
            elif isinstance(Exclude, list):
                network_list = [i for i in self.DockerQueryNetwork(formatting=True)]
                if Exclude in network_list:
                    for exclude in network_list:
                        network_list.remove(exclude)
                    if network_list is []:
                        return True
                    for name in network_list:
                        subprocess.Popen('docker network rm {}'.format(name), stdout=subprocess.PIPE)
                return True
            else:
                raise DockerRmNetworkError("Exclude:{} 参数需要提供".format(Exclude))
        elif isinstance(RmNetworkName, str):
            subprocess.Popen('docker network rm {}'.format(RmNetworkName), stdout=subprocess.PIPE)
            return True
        elif isinstance(RmNetworkName, list):
            commend = 'docker network rm'
            for name in RmNetworkName:
                commend = commend + ' ' + name
            subprocess.Popen('docker network rm {}'.format(commend), stdout=subprocess.PIPE)
            return True
        else:
            raise DockerRmNetworkError("DockerRmNetwork:{}未知类型".format(type(RmNetworkName)))

    def DockerConnectNetwork(self, Network=None, VesselName=None, help=False):
        """
            # DockerConnectNetwork方法，用于对指定容器添加虚拟网卡
            :param Network: 默认None，指定虚拟网卡名称
            :param VesselName: 默认None，指定容器ID
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return:默认返回执行结果
        """
        if help:
            print("""{}.{}            
            :param Network: 默认None，指定虚拟网卡名称
            :param VesselName: 默认None，指定容器ID
            :param help: 默认False， 声明：需要方法提示时，help=True即可。
            :return:默认返回执行结果""".format(
                    self.__class__.__name__,
                    self.__get__function_name()))
            return 'help'
        if isinstance(Network, str) and isinstance(VesselName, str):
            vessel_name = [self.DockerQuery()[i]['names'] for i in self.DockerQuery()]
            if VesselName in self.DockerQuery():
                if Network in self.DockerQueryNetwork(formatting=True):
                    subprocess.Popen('docker network connect {} {}'.format(Network, VesselName), stdout=subprocess.PIPE)
                    return True
                else:
                    raise DockerConnectNetworkError("Network:{}未知参数".format(Network))
            if VesselName in vessel_name:
                if Network in self.DockerQueryNetwork(formatting=True):
                    subprocess.Popen('docker network connect {} {}'.format(Network, VesselName), stdout=subprocess.PIPE)
                    print('docker network connect {} {}'.format(Network, vessel_name))
                    return True
                else:
                    raise DockerConnectNetworkError("Network:{}未知参数".format(Network))
            else:
                raise DockerConnectNetworkError("VesselName:{}未知参数".format(VesselName))
        elif isinstance(Network, str) and not VesselName:
            raise DockerConnectNetworkError("VesselName:{}未传递参数".format(VesselName))
        elif isinstance(VesselName, str) and not Network:
            raise DockerConnectNetworkError("Network:{}未传递参数".format(Network))
        else:
            raise DockerConnectNetworkError("DockerConnectNetworkError:未传递任何参数!")

    def DockerPort(self, vessel_name=None, help=False):
        """
            # DockerPort方法，用于查询指定容器下，所有端口信息
            :param vessel_name: 提供指定容器的ID或名称 [vesselID / vesselName]
            :param help: help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 默认返回执行命令的结果
        """
        if help:
            print("""{}.{} From help:
                    :param vessel_name: 提供指定容器的ID或名称 [vesselID / vesselName]
                    :param help: help: 默认False， 声明：需要方法提示时，help=True即可""".format(
                self.__class__.__name__,
                self.__get__function_name()))
            return 'help'
        if isinstance(vessel_name, str):
            vessel_list = self.DockerQuery()
            names = []
            if vessel_name in vessel_list.keys():
                cmd = subprocess.Popen('docker port {}'.format(vessel_name),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1)
                return cmd.communicate()[0].decode()
            else:
                for vessel_name_value in vessel_list:
                    names.append(vessel_list.get(vessel_name_value)['names'])
                if vessel_name in names:
                    cmd = subprocess.Popen(
                        'docker port {}'.format(vessel_name),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=1)
                    return cmd.communicate()[0].decode()
                else:
                    raise DockerPortError(
                        "Vessel_name:{}，不存在于docker实例化容器列表中".format(vessel_name))

        else:
            raise DockerPortError(
                "Vessel_name:{}，错误的vessel_name类型".format(
                    type(vessel_name)))

    def DockerTag(self, oldName=None, newName=None, help=False):
        """
            # DockerTag方法，用来修改镜像标签
            :param oldName: 原镜像名称 str
            :param newName: 新镜像名称 str
            :param help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 返回命令执行状态
        """
        if help:
            print("""{}.{} From help:
            :param oldName: 原镜像名称 str
            :param newName: 新镜像名称 str
            :param help: 默认False， 声明：需要方法提示时，help=True即可
            :return: 返回命令执行状态""".format(
                self.__class__.__name__,
                self.__get__function_name()))
            return 'help'
        docker_images = self.DockerQuery(self_object='images')
        if isinstance(oldName, str):
            if isinstance(newName, str):
                images_list = []
                for name in docker_images:
                    images_list.append(docker_images[name]['image_id'])
                if oldName in docker_images or oldName in images_list:
                    cmd = subprocess.Popen(
                        'docker tag {} {}'.format(oldName, newName),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=1)
                    return cmd.communicate()[0].decode()
            elif not newName:
                raise DockerTagError("newName:{}未知参数，可查询帮助".format(newName))
            else:
                raise DockerTagError(
                    "newName:{}提供了错误类型，可查询帮助".format(
                        type(newName)))
        else:
            raise DockerTagError(
                "oldName:{}提供了错误类型，可查询帮助".format(
                    type(oldName)))


if __name__ == '__main__':
    docker = Agility_Docker()
    aa = docker.DockerVersion
    print(aa)
    pass
"""
    docker = Agility_Docker()
    print(docker.DockerQueryNetwork(Inspect=True, NetworkName='fad41f9a44e9'))
    # 查询指定虚拟网卡的详细信息
"""
"""
    docker = Agility_Docker()
    print(
        docker.DockerNewNetwork(
            create=True,
            NetWorkName='test1'))
    # 新建虚拟网卡'test1'，默认类型
"""
"""
    docker = Agility_Docker()
    docker.DockerConnectNetwork(Network='fad41f9a44e9', VesselName='123')
    # 由于实例化容器名并不存在，所以抛出DockerConnectNetworkError:未知参数
"""
"""
    docker = Agility_Docker()
    docker.DockerRmNetwork(RmNetworkName=['fad41f9a44e9', '690455df4dbd', 'aea5b4a1ba89'])
"""
"""
    docker = Agility_Docker()
    docker.DockerTag(oldName='fce289e99eb9', newName='test1')
"""
"""
    docker = Agility_Docker()
    print(
        docker.DockerRun(
            vessel_name='test2',
            network='mynet1',
            images_name='daocloud.io/library/registry:2.6.1',
            run_cmd='/bin/sh'))
    # 实例化运行容器
"""
"""
    docker = Agility_Docker()
    print(docker.DockerPort(vessel_name='nginx1'))
    # 查询容器名为'nginx1'的端口信息
"""
"""
    docker = Agility_Docker()
    docker.DockerNetwork(rm=True)
    # 删除默认虚拟网卡以外的网卡
"""
"""
    docker = Agility_Docker()
    print(
        docker.DockerNewNetwork(
            create=True,
            subnet='192.168.0.0/24',
            gateway='192.168.0.1',
            NetWorkName='test1'))
    # 创建一个虚拟网卡，网段为192.168.0.0/24，网关指向192.168.0.1，名称为test1
"""
"""
    docker = Agility_Docker()
    docker_network = docker.DockerNetwork(query=True)
    docker_network = docker_network.split('\n')
    docker_name = []
    for i in docker_network[1:-1]:
        docker_name.append(i[:12])
    print(docker_name)
    print(docker.DockerNetwork(query=True, Inspect=True, NetWorkEthName=docker_name[1]))
    # 查询所有NetWork的详细信息
"""
