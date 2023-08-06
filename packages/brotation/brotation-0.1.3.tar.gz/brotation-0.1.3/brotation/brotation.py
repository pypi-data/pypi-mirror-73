"""Main module.

Rotation Policy
================
Rotation policy is also supported:

- 7-daily (mon-sun) :       e.g. flowmonitor.git.d6.7z
- 1-per-week of the month:  e.g. flowmonitor.git.w0.7z
- 1 per month:              e.g. flowmonitor.git.m9.7z
- 1 per year:               e.g. flowmonitor.git.y17.7z

So we need 7 + 5 + 12 = 24 files to cover a whole year.

In each backup the dairy backup is generated and then is cloned
modifying the rotation names, so the compressed file only is sent once
and hence all files correspond with the last update.

As soon a new day comes, some of the previous backups files will be left
behind creating the rotation sequence.

'womanly_speech.d2.xz',
'womanly_speech.d5.xz',
'womanly_speech.m01.xz',
'womanly_speech.m11.7z',
'womanly_speech.m11.xz',
'womanly_speech.m12.7z',
'womanly_speech.m12.xz',
'womanly_speech.m3.7z',
'womanly_speech.m5.7z',
'womanly_speech.m6.xz',
'womanly_speech.m8.xz',
'womanly_speech.w0.xz',
'womanly_speech.w13.xz',
'womanly_speech.w17.7z',
'womanly_speech.w17.xz',
'womanly_speech.w2.7z',
'womanly_speech.w26.7z',
'womanly_speech.w39.7z',
'womanly_speech.w9.7z',
'womanly_speech.y11.7z',
'womanly_speech.y13.xz',
'womanly_speech.y14.7z',
'womanly_speech.y15.xz',
'womanly_speech.y17.7z',
'womanly_speech.y20.xz'

# rules:

1. get day, week, month numbers
2. if month goes to 1, then last month became last year.
3. if week goes back to 0, then last week became last month.
4. if days goes back to 0, then last day became last week.

# steps:

1. create the dictionary of existing rotate files.
2. compte the current day.
3. chech above rules in order.
4. try to get the last


d{n} --> d{}

"""
#import wingdbstub
import re
import os
import time
import tarfile

from shutil import copyfile
from subprocess import Popen, PIPE
from datetime import datetime

from gutools.tools import expandpath, soft_update, fileiter, load_config
from gutools.ushift import Rotator, FQItem

# --------------------------------------------------
# logger
# --------------------------------------------------
from gutools.loggers import logger, \
    trace, exception, debug, info, warn, error
log = logger(__name__)


rotate_match = re.compile(r'(?P<key>.+?)\.(?P<rot>(d[0-6]|w[0-9]|w[0-4][0-9]|w5[1-3]|\d|m[0-9]|m1[0-2]?|m0[0-9]|y\d{2}))\.(?P<ext>7z|xz)$', re.DOTALL).match


def extract_info(path):
    """*Extract rotate info from path.*
    """
    m = rotate_match(path)
    if m:
        return FQItem(m.groupdict())


class BackupRotator(Rotator):
    RANGES = [
        ('d', 0, 6),
        ('w', 0, 4),
        ('m', 1, 12),
        ('y', 10, None),
    ]

    CMD = {
        # xz -9 -c - > foo.tar.xz
        'zz': ['xz', '-c', '--threads=0'],
        'xz': ['cJvf', ],
    }

    COMPRESSOR = {
        'xz': 'xz',
        'gz': 'gzip',
    }
    """A class ...

    """
    @classmethod
    def today(cls):
        t = datetime.today()
        wrange = cls.RANGES[1][-1] - cls.RANGES[1][-2] + 1
        w = int(t.strftime("%j")) % wrange
        return FQItem(rot='d', d=t.weekday(), w=w, m=t.month, y=f'{t.year}'[:2])

    def __init__(self, where, folders=None, cpu=None, config=None, config_file=None, *args, **kw):
        super().__init__(self.RANGES)
        self.where = None,
        self.folders = None
        self.cpu = cpu
        self.config = config
        self._config(where, folders, cpu, config_file)

        debug(f"where: {self.where}")
        debug(f"folders: {self.folders}")
        debug(f"config: {self.config}")

    def _config(self, where, folders, cpu, config_file, **kw):
        self.config_file = config_file  # or '~/.config/backups.conf'
        if self.config is None:
            self.config = load_config(self.config_file)
            where = where or self.config.get('where')
            folders = folders or self.config.get('folders')
            cpu = cpu or self.config.get('cpu')

        self.folders = folders if isinstance(folders, list) else [folders]
        self.where = where
        self.cpu = cpu

    def _parse(self, element):
        item = extract_info(element)
        if item:
            item['rot'], value = item['rot'][0], int(item['rot'][1:])
            item[item['rot']] = value
            return item

    def _rebuild(self, item):
        """*Reconstruct an element from parsed data.*"""
        return "{key}.{rot}{value}.{ext}".format(**item)
        # return f"{item['rot']}{item[item['rot']]}" + "[{d}.{w}.{m}.{y}]".format(**item)

    def apply(self, items, where=None, cpu=None):
        """*xxx*

        - load config if not already downloaded.
        - xax


        """
        where = where or self.where
        cpu = cpu or self.cpu
        for root in self.folders:
            if not root:
                continue

            firstone = None
            root = expandpath(root)
            for fqitem in items:
                fqitem['ext'] = self.config.get('compression', 'xz')
                fqitem['key'] = os.path.basename(root)
                name = repr(fqitem)
                if firstone:
                    target = os.path.join(os.path.dirname(firstone), name)
                    copyfile(firstone, target)
                else:
                    output = os.path.join(where, name)
                    firstone = self.compress(output, root, cpu)
                    foo = 1
        foo = 1

    def compress(self, output, root, cpu=100):
        """*Compress folder using tar and xz utitlities.*
        - 'output': the compressed tar file name.
        - 'root': folder to compress.
        - 'cwd' is a relative path from where the files would be included

        The approach is to use system call directly for faster execution.
        Using tarfile library implies python intervention, that will be
        slower than system call, specially running in a raspberry.
        """
        ext = os.path.splitext(output)[-1][1:]
        # with tarfile.open(output, f"w:{ext}") as tar:
            # tar.add(root, arcname=os.path.basename(root))

        cwd, name = os.path.split(root)

        #  tar -cf - foo/ | xz --lzma2=dict=1536Mi,nice=273 -c - > foo.tar.xz
        # cmd = ['tar', '-cf', '-', name, '|']
        # cmd.extend(self.CMD[ext])
        # tarfolder, tarname = os.path.split(output)
        # tarname = os.path.join(tarfolder, cwd[1:], tarname)
        # os.makedirs(os.path.dirname(tarname), exist_ok=True)
        # cmd.extend(['>', tarname])
        cmd = []

        cmd.extend(['nice', 'tar', ])
        cmd.extend(self.CMD[ext])
        tarfolder, tarname = os.path.split(output)
        tarname = os.path.join(tarfolder, cwd[1:], tarname)
        os.makedirs(os.path.dirname(tarname), exist_ok=True)
        cmd.extend([tarname, name])

        print(' '.join(cmd))
        # print(f">> cpu: {cpu}")
        context = dict(stdout=PIPE, cwd=cwd, text=True)
        with Popen(cmd, **context) as proc:
            if cpu:
                compressor = self.COMPRESSOR.get(ext, 'xz')
                limit = ['cpulimit', '--limit', f"{cpu}", '--lazy', '--exe', compressor, ]  # f'--pid={proc.pid}']
                print(' '.join(limit))
                time.sleep(10)  # give some time to create all childs
                lim = Popen(limit, **context)

            for line in proc.stdout.readlines():
                # print(line)
                pass
            foo = 1
        if cpu:
            print("Killing cpulimit")
            lim.kill()

        return tarname

    def load_config(self, config):
        """
        *TBD*
        """
        foo = 1


