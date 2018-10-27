# -*- coding: utf-8 -*-
"""
Python 操作HDFS

@Author YH YR
@Time 2018/10/25 14:22
"""
from hdfs import Client, HdfsError


class HDFSUtil:
    def __init__(self, url):
        self._client = Client(url)

    def make_dir(self, hdfs_path):
        """
        支持递归创建多级目录
        :param hdfs_path:
        :return:
        """
        self._client.makedirs(hdfs_path)

    def delete_hdfs_file(self, hdfs_path):
        """
        删除HDFS文件

        如果是目录, 必须为空
        :param hdfs_path:
        :return:
        """
        self._client.delete(hdfs_path)

    def delete_hdfs_dir(self, hdfs_dir):
        """
        删除HDFS文件/目录

        如果目录不为空, 递归删除
        :param hdfs_dir:
        :return:
        """
        dir_list = self.hdfs_dir_list(hdfs_dir)
        if dir_list is None or len(dir_list) == 0:
            print('Delete File: {0}'.format(hdfs_dir))
            self._client.delete(hdfs_dir)
        else:
            for file_name in dir_list:
                self.delete_hdfs_dir(hdfs_dir + '/' + file_name)
            print('Delete Dir: {0}'.format(hdfs_dir))
            self._client.delete(hdfs_dir)

    def upload_to_hdfs(self, local_path, hdfs_path):
        """
        将本地文件/目录上传到HDFS上

        如果目录不存在, 会自动创建
        :param local_path:
        :param hdfs_path:
        :return:
        """
        self._client.upload(hdfs_path, local_path, cleanup=True)

    def download_from_hdfs(self, hdfs_path, local_path):
        """
        将HDFS上的文件/目录下载到本地
        :param hdfs_path:
        :param local_path:
        :return:
        """
        self._client.download(hdfs_path, local_path, overwrite=True)

    def write_to_hdfs(self, hdfs_path, data, overwrite=False, append=True):
        """
        追加: overwrite=false, append=true => Default
        复写: overwrite=true, append=false

        overwrite和append逻辑必须互斥
        :param hdfs_path:
        :param data:
        :param overwrite: Boolean 是否复写
        :param append: Boolean 是否追加
        :return:
        """
        if not self._client.content(hdfs_path, strict=False):
            print('File Not exist in HDFS')
        self._client.write(hdfs_path, data, overwrite=overwrite, append=append)

    def move_or_rename(self, hdfs_src_path, hdfs_dst_path):
        """
        文件移动/重命名
        :param hdfs_src_path:
        :param hdfs_dst_path:
        :return:
        """
        self._client.rename(hdfs_src_path, hdfs_dst_path)

    def hdfs_dir_list(self, hdfs_path):
        """
        获取指定目录下的文件
        当hdfs_path不是目录, 捕获异常并返回None
        :param hdfs_path:
        :return: List[filename] or None
        """
        try:
            return self._client.list(hdfs_path, status=False)
        except HdfsError:
            return None
