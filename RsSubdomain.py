import argparse
import threading
import sys
import dns.resolver

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
    add_commandline_options = argparse.ArgumentParser("\n\r一个非常简单的子域名查询工具\n\r")
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
root@home~> python3 RsSubdomain.py --filename ./domain.txt --domain baidu.com
    """


class RsSubDomain(object):
    def __init__(self, domain=None, filename=None, thread_number=5):
        self.filename = filename
        self.domain = domain
        self.thread_number = thread_number
        self.queue = Queue()
        self.result = []

    def run(self):
        #if self.domain is None:
        loader_queue = loader_file(self.filename)
        for queue_item in loader_queue:
            self.queue.put(queue_item + "." + self.domain)
        #else:
            #self.queue.put(self.domain)

        total = self.queue.qsize()
        threads = []

        for number in range(self.thread_number):
            threads.append(self.RsSubDomainThreading(self.queue, self.result, total))

        for th in threads:
            th.start()

        for th in threads:
            th.join()

        return list(set(self.result))

    class RsSubDomainThreading(threading.Thread):
        def __init__(self, queue, result, total):
            #super(RsSubDomainThreading, self).__init__(queue, result, total)
            threading.Thread.__init__(self)
            self.queue = queue
            self.total = total
            self.result = result

        def run(self):
            while not self.queue.empty():
                queue_element = self.queue.get_nowait()
                try:
                    self.progress()
                    result = dns.resolver.query(queue_element, 'A')
                    if result.response.answer:
                        self.result.append(queue_element)
                except Exception as e:
                    pass


        def progress(self):
            done = float(self.total - self.queue.qsize())
            count = float(self.total)
            found_count = len(self.result)
            progress_message = "[+] Last {} | complete progress {:.2f} | Found {}".format(self.queue.qsize(), (done/count)*100, found_count)
            sys.stdout.write("\r" + progress_message)
            sys.stdout.flush()


def main():
    parser, options = _set_commandline_options()

    if (parser.filename and parser.domain) is None:
        options.print_help()
        options.print_usage()
        print_usage_text()
        exit(0)

    result = RsSubDomain(domain=parser.domain, filename=parser.filename).run()


    print()

    for item in result:
        print("[*] DNS Record : " + item)


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

