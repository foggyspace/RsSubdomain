import argparse
import threading
import sys

from queue import Queue


__AUTHOR__ = "seaung"

__VERSION__ = "0.0.1"


def loader_file(path):
    """
    加载文件
    :param path: 文件路径
    :return list: 返回一个list
    """
    lines = []
    with open(path) as fs:
        for line in fs.readlines():
            lines.append(line.strip())
    return lines


def _set_commandline_options():
    """
    设置命令行参数
    """
    add_commandline_options = argparse.ArgumentParser("\r\n
                                                      一个非常简单的子域名查询工具\r\n")
    add_commandline_options.add_argument("--domain", dest="domain",
                                         action="store", help="目标站点主域名.",
                                        type=str)
    add_commandline_options.add_argument("--filename", dest="filename",
                                         action="store", help="域名字典文件.",
                                         type=str)
    add_commandline_options.add_argument("--number", dest="number",
                                         action="store", help="线程数量",
                                         type=int, default=3)
    return add_commandline_options.parse_args(), add_commandline_options


def print_usage_text():
    usage_text = """
root@home~> python3 RsSubdomain.py --domain baidu.com
root@home~> python3 RsSubdomain.py --filename ./domain.txt
    """


class RsSubDomain(object):
    def __init__(self, domain=None, filename=None, thread_number=5):
        self.filename = filename
        self.domain = domain
        self.thread_number = thread_number
        self.queue = Queue()

    def run(self):
        if domain is None:
            loader_queue = loader_file(self.filename)
            for queue_item in loader_queue:
                self.queue.put(queue_item)
        else:
            self.queue.put(self.domain)

        total = self.queue.qsize()
        threads = []

        for number in range(self.thread_number):
            threads.append(self.RsSubDomainThreading(self.queue, self.total))

        for th in threads:
            th.start()

        for th in threads:
            th.join()

    class RsSubDomainThreading(threading.Thread):
        def __init__(self, queue, total):
            super().__init__()
            self.queue = queue
            self.total = total

        def run(self):
            while not self.queue.empty():
                queue_element = self.queue.get_nowait()

                self.progress_message()


        def progress(self):
            done = float(self.total - self.queue.qsize())
            count = float(self.total)
            progress_message = "[+] Last {} | complete progress {:.2f}".format(self.queue.qsize(), (done/count)*100)
            sys.stdout.write("\r" + progress_message)
            sys.stdout.flush()


def main():
    parser, options = _set_commandline_options()

    if (options.filename or options.domain) is None:
        parser.print_help()
        parser.print_usage()
        print_usage_text()
        exit(0)


def print_logo_text():
    logo_text = f"""
        {__AUTHOR__}

        {__VERSION__}
     ____        ____        _         _                       _
    |  _ \ ___  / ___| _   _| |__   __| | ___  _ __ ___   __ _(_)_ __
    | |_) / __| \___ \| | | | '_ \ / _` |/ _ \| '_ ` _ \ / _` | | '_
    |  _ <\__ \  ___) | |_| | |_) | (_| | (_) | | | | | | (_| | | | | |
    |_| \_\___/ |____/ \__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_|

    """
    print(logo_text)


if __name__ == "__main__":
    print_logo_text()
    main()

