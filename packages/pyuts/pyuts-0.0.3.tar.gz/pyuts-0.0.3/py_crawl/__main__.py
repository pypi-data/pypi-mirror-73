# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 09:23:15) 
# [Clang 10.0.1 (clang-1001.0.46.3)]
# Embedded file name: /Users/jack/WorkSpace/testCrawl/pyutils/py_crawl/__main__.py
# Compiled at: 2020-05-13 16:20:28
# Size of source mod 2**32: 1132 bytes


def initScrapyProject(projectName):
    from pyutils.py_mix.cmdU import CmdU
    copyName = projectName
    if '/' in projectName:
        names = projectName.split('/')
        projectName = names[-1]
    CmdU.produce('scrapy').run(f"scrapy startproject {projectName}")
    from py_file.fileU import FileU
    fileU = FileU()
    settingStr = fileU.read_str('pyutils/py_crawl/scrapySettings.py_')
    settingStr = settingStr.replace('scrapyprojectname', projectName)
    settingStr = settingStr.replace('Scrapyprojectname', f"{projectName[:1].upper()}{projectName[1:]}")
    fileU.write_str(f"{projectName}/{projectName}/settings.py", settingStr)
    fileU.write_str(f"{projectName}/{projectName}/commands/__init__.py", '# -*- coding: UTF-8 -*-')
    fileU.write_str(f"{projectName}/{projectName}/__init__.py", '# -*- coding: UTF-8 -*-\nimport sys\nsys.path.append("../") ')
    if copyName != projectName:
        fileU.move(projectName,copyName)


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 2:
        print('example: python -m pyutils.py_crawl scrapy_init test')
        exit()
    else:
        action = sys.argv[1]
        if action == 'scrapy_init':
            projectName = sys.argv[2]
            initScrapyProject(projectName)
        else:
            print('example: python -m pyutils.py_crawl scrapy_init test')
# okay decompiling __main__.cpython-37.pyc
