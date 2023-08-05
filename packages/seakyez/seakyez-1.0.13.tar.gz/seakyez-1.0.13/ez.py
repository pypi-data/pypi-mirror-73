import time, datetime
import urllib.request, urllib.parse
import os, threading, subprocess, zipfile, ntpath, shutil, platform, sys
import random, csv, re, html
from json import loads, dumps
from atexit import register
from collections.abc import Iterable
from collections import Counter
from functools import reduce
from types import GeneratorType
from itertools import chain, combinations
try:
    import pandas as pd
except ModuleNotFoundError:
    pass

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') + ('\\' if sys.platform.startswith('win') else '/')
DataTypeError = TypeError('Unsupported data type.')

def csv2xlsx(filename: str, sheet_name = 'Sheet1') -> str:
    '''
    Convert a csv file to xlsx file.
    @returns:
        Path of the xlsx file.
    '''
    ext = '.csv' # extension
    if not filename.endswith(ext):
        filename += ext
    filename = os.path.abspath(filename)
    basename = os.path.basename(filename).split(ext)[0] + '.xlsx'
    ret = os.path.join(os.path.dirname(filename), basename)
    df = pd.read_csv(filename).to_excel(ret, sheet_name)
    return ret

def xlsx2csv(filename: str, sheet_name = 0) -> str:
    '''
    Convert an xlsx file to csv file.
    @returns:
        Path of the csv file.
    '''
    ext = '.xlsx' # extension
    if not filename.endswith(ext):
        filename += ext
    filename = os.path.abspath(filename)
    basename = os.path.basename(filename).split(ext)[0] + '.csv'
    ret = os.path.join(os.path.dirname(filename), basename)
    pd.read_excel(filename, sheet_name).to_csv(ret)
    return ret       

def getSourceCode(url: str) -> str:
    '''
    Retrieve the decoded content behind the url.
    '''
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    request = urllib.request.Request(url,  headers=headers)
    return urllib.request.urlopen(request).read().decode()

def random_pop(sequence):
    '''
    Randomly remove and pop an item from the sequence.
    '''
    return sequence.pop(random.randrange(0, len(sequence)))

def rpassword(length: tuple = (8, 20), capital: bool = True, numbers: bool = True, punctuations: bool = False) -> str:
    '''
    Randomly generate a password. Full clexicon is list(map(chr, range(32, 126))).
    @params:
        length: a tuple of with the format of (minLength, maxLength),
                or an integer that specifies the length.
                Default: (8, 20).
        capital: a bool that specifies the inclusion of capital letters.
                Default: True.
        numbers: a bool that specifies the inclusion of numbers.
                Default: True.
        punctuations: a bool that specifies the inclusion of punctuations, which will be selected from [` -=[]\;',./~!@#$%^&*()_+{}|:"<>?].
                Default: False.
    @return:
        password: a string. If no argument is set to True, a lower-case string will be returned.
    '''
    lexicon = list(map(chr, range(32, 126)))
    if not capital:
        lexicon = filter(lambda x: not x.isupper(), lexicon)
    if not numbers:
        lexicon = filter(lambda x: not x.isdigit(), lexicon)
    if not punctuations:
        lexicon = filter(lambda x: x.isalnum(), lexicon)
    lexicon = list(lexicon)
    if isinstance(length, (tuple, list)):
        assert len(length) == 2, 'length object must have exactly 2 elements!'
        mi, ma = length
        iterations = random.randint(mi, ma)
    else:
        iterations = length
    password = ''.join([ random.choice(lexicon) for _ in range(iterations) ])
    return password

def replacePattern(pattern: str, string: str, substr: str = '') -> str:
    '''
    Replace the substring that follows a pattern from a string.
    @params:
        pattern: a Regex string or a re.Pattern object.
        string: the target string.
        substr: default is empty, which removes the pattern.
    @return:
        new: the final result string
    '''
    if type(pattern) == str:
        pattern = re.compile(pattern)
    if type(pattern) != re.Pattern:
        raise DataTypeError
    new = string
    while True:
        match = re.search(pattern, new)
        if not match:
            return new
        target = match.group()
        new = new.replace(target, substr)

def prchoice(obj):
    '''
    Probabilistic random choice. (Random choice with probability)
    Obj should be a two's iterable.
    '''
    targets = []
    probs = []
    for target, prob in obj:
        targets.append(target)
        probs.append(prob)
    probability = random.uniform(0, 1)
    index = 0
    while sum(probs[:index + 1]) < probability:
        index += 1
    return targets[index]

cd = os.chdir
ls = os.listdir
pwd = os.getcwd
rm = os.remove
rm_rf = shutil.rmtree

def cdlnk(path: str):
    '''cd lnk path'''
    os.chdir(getlnk(path))

def getlnk(path: str):
    '''Get lnk path'''
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    return shortcut.Targetpath

def rpop(sequence: list):
    '''Randomly remove and return an item from the sequence'''
    index = random.randrange(0, len(sequence))
    return sequence.pop(index)

def dupFolder(path: str, copies: int, pattern: str = '?', start: int = 1):
    '''Duplicate a folder into some copies with names following a pattern.
    pattern: Use ? for number. Pattern is the suffix.
    Sample pattern: "folder (?)" -> "folder (1)"
    start: if not specified, number starts from 1.
    Raise AssertionError if '?' is not in pattern.'''
    assert '?' in pattern, 'Invalid Pattern'
    for i in range(start, start + copies):
        os.makedirs(os.path.join(path, pattern.replace('?', str(i))))

def dupFile(name: str, copies: int, pattern: str = '?', start: int = 1):
    '''Duplicate a file into some copies with names following a pattern.
    pattern: Use ? for number. Pattern is the suffix.
    Sample pattern: " (?)" -> "filename (1)"
    start: if not specified, number starts from 1.
    Raise AssertionError if '?' is not in pattern.
    Raise FileNotFoundError if file not found.'''
    assert '?' in pattern, 'Invalid Pattern'
    path = os.path.dirname(name)
    filename = os.path.basename(name)
    dotNotFound = '.' not in filename
    if dotNotFound:
        for f in os.listdir(path):
            if filename in f :
                filename = f
                break
        else:
            raise FileNotFoundError(f'No such file or directory: {name}')
    dot = find(filename).last('.')
    suffix = filename[dot:]
    filename = filename[:dot]
    if dotNotFound:
        name += suffix
    for i in range(start, start + copies):
        shutil.copy(name, os.path.join(path, pattern.replace('?', str(i)) + suffix))

def summation(iterable):
    '''Add all the elements of an iterable together.
    Call the __add__ or update function of the element of the iterable.'''
    if isinstance(iterable, GeneratorType):
        iterable = list(iterable)
    typ = type(iterable[0])
    if hasattr(typ, '__add__'):
        return reduce(typ.__add__, iterable)
    if hasattr(typ, 'update'):
        def update(a, b):
            a.update(b)
            return a
        return reduce(update, iterable)
    raise DataTypeError

def countLines(path: str, filetype: str):
    '''Count the lines of all the files with the specified type in the path.'''
    count = 0
    for item in os.listdir(path):
        directory = os.path.join(path, item)
        if os.path.isdir(directory):
            for script in os.listdir(directory):
                if script.endswith(filetype):
                    count += fread(os.path.join(directory, script), False).count('\n')
        elif os.path.isfile(item) and item.endswith(filetype):
            count += fread(directory, False).count('\n')
    return count

class Settings:
    '''Settings is for remembering user settings using a dict.
    It saves the settings automatically on program exit.
    Recommend passing __file__ to path for simplicity.'''
    suffix = '.json'
    def __init__(self, path: str, settingsName: str = 'settings.json'):
        self.path = os.path.dirname(path)
        if '.' in settingsName:
            assert Settings.suffix in settingsName
        self.settingsName = settingsName if settingsName.endswith(Settings.suffix) else settingsName + Settings.suffix
        self.settingsFile = os.path.join(self.path, self.settingsName)
        self.load()
        register(self.save)

    def setdefault(self, key, value):
        return self.settings.setdefault(key, value)

    def set(self, key, value):
        self.__setitem__(key, value)

    def setSettingOptions(self, settingOptions):
        for key in self.settings.copy():
            if key not in settingOptions:
                del self.settings[key]

    def get(self, key, default):
        return self.settings.get(key, default)

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __str__(self):
        return str(self.settings)

    def __repr__(self):
        return repr(self.settings)

    def __contains__(self, key):
        return key in self.settings

    def pop(self, key) -> bool:
        hasKey = key in self.settings
        if hasKey:
            self.settings.pop(key)
        return hasKey

    def load(self):
        try:
            self.settings: dict = loads(fread(self.settingsFile, False))
        except (FileNotFoundError, TypeError):
            self.settings = {}

    def save(self):
        fwrite(self.settingsFile, dumps(self.settings))

def Eval(string: str):
    '''Use eval() without dealing with exceptions.'''
    try: return eval(string)
    except: return string

def translate(string: str, to_l: str = 'zh', from_l: str = 'en') -> str:
    '''Translate string from from_l language to to_l language'''
    if not string: return ''
    header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    query = urllib.parse.quote(string, encoding = 'utf-8')
    url = f'https://translate.google.cn/m?hl={to_l}&sl={from_l}&q={query}'
    request = urllib.request.Request(url, headers = header)
    page = urllib.request.urlopen(request).read().decode('utf-8')
    print(page)
    target = find(page).between('class="t0">', '</div>', 1, 1)
    return html.unescape(target)

def __handlepy(directory, func, reminder = False):
    ''' Do something, meaning that func(directory), to a py file or a folder of py files.
        func must has exactly one argument filename.
        '''
    if os.path.isfile(directory):
        if directory.endswith('.py'):
            if reminder:
                print('File detected')
            func(directory)
    elif os.path.isdir(directory):
        if reminder:
            print('Folder detected')
        for file in os.listdir(directory):
            if file.endswith('.py'):
                if reminder:
                    print(file)
                func(os.path.join(directory, file))
    else:
        raise Exception('Invalid directory!')

def exportpy(directory: str, withConsole: bool, zipFile: bool = True, reminder: bool = False):
    '''Exports a GUI python app.'''
    ## Add '-noconfirm' ?
    path = os.path.dirname(directory)
    args = ['pyinstaller', '--onefile', '--distpath', path, '--workpath', path, '--specpath', path, '--noconsole']
    if withConsole:
        args.pop()
    def export(filename):
        subprocess.run(args + [filename])
        if not zipFile: return
        currDir = os.getcwd()
        path, file = ntpath.split(filename)
        os.chdir(path)
        prefix = find(file).before('.py')
        zipname = prefix + '.zip'
        with zipfile.ZipFile(zipname, 'w') as zipFile:
            for f in [prefix + '.exe', prefix + '.spec']:
                zipFile.write(f)
                os.remove(f)
            for f in os.listdir(prefix):
                zipFile.write(os.path.join(prefix, f))
            shutil.rmtree(prefix)
        os.chdir(currDir)
    threading.Thread(target = lambda directory, func, reminder: __handlepy(directory, func, reminder), \
                     args = (directory, export, reminder)).start()

def py2pyw(directory: str, pywname: str = '', reminder: bool = False):
    ''' Converts a py file or a folder of py files to pyw files.
        pywname is the name of a pyw file and is only available when converting a file.
        If pywname is empty, it will be set to pyw filename wil be set to the name of py file.'''
    suffix = '.pyw'
    if pywname and not pywname.endswith(suffix):
        pywname += suffix
    threading.Thread(target = lambda directory, func, reminder: __handlepy(directory, func, reminder), \
                     args = (directory, lambda filename: fwrite(pywname or filename + 'w', fread(filename, False)), reminder)).start()

def rmlnk(path: str = desktop):
    ''' Remove "- 快捷方式" from a path.'''
    for folder in os.listdir(path):
        folder = os.path.join(path, folder)
        if folder.endswith('.lnk'):
            os.rename(folder, folder.replace(' - 快捷方式', ''))

cd = os.chdir

def cddt():
    '''Change current Directory to DeskTop'''
    os.chdir(desktop)

def copyToClipboard(text):
    ''' Copy text to clipboard. I don't care about Linux.'''
    text = str(text)
    system = platform.system()
    if system == 'Windows':
        try:
            from win32 import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except ModuleNotFoundError:
            # Solution: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python/
            from tkinter import Tk
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(text)
            r.update() # now it stays on the clipboard after the window is closed
            r.destroy()
    elif system == 'Darwin':
        process = subprocess.Popen('pbcopy', env = {'LANG': 'en_US.UTF-8'}, stdin = subprocess.PIPE)
        process.communicate(text.encode('utf-8'))

## abbreviation
cpc = copyToClipboard

def pasteFromClipboard():
    system = platform.system()
    if system == 'Windows':
        try:
            from win32 import win32clipboard
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return data
        except:
            return ''
    elif system == 'Darwin':
        return ''

def checkfolders(folder1: str, folder2: str) -> bool:
    '''Check whether folder1 is exactly the same as folder2'''
    l1 = os.listdir(folder1)
    l2 = os.listdir(folder2)
    if l1 != l2:
        return False
    for f in l1:
        p1 = os.path.join(folder1, f)
        if os.path.isdir(p1):
            p2 = os.path.join(folder2, f)
            if not checkfolders(p1, p2):
                return False
    return True

def find_item(path: str, target: str, findAll: bool = False) -> str:
    '''
    Recursively find the path of an item in your computer whose name contains the target.
    If findAll is False, it will stop immediately after first match.
    @params:
        path: directory to find
        target: the name of target file
        findAll: bool
    '''
    try:
        files = os.listdir(path)
    except PermissionError:
        return ''
    for item in files:
        full_path = os.path.join(path, item)
        if target in item:
            if not full_path:
                return full_path
        elif os.path.isdir(item):
            if find_item(target, full_path) and findAll:
                return full_path
    return ''

def timeof(func, args: tuple = ()):
##    from functools import partial
##    partial(func, args)
    return timer(func, 1, args)

def timer(func, iterations: int = 1000, args: tuple = ()):
    '''If func has arguments, put them into args.'''
    t = time.perf_counter()
    for i in range(iterations):
        func(*args)
    return time.perf_counter() - t

def fread(filename: str, evaluate: bool = True, coding: str = 'utf8'):
    '''Read the file that has the filename.
       Set evaluate to true to evaluate the content.
       Default coding: utf8.'''
    with open(filename, encoding = coding) as file:
        content = file.read()
        if evaluate:
            content = Eval(content)
        return content

def fwrite(filename: str, content, mode: str = 'w', coding: str = 'utf8'):
    ''' Write the file that has the filename with content.
        Default mode: "w"
        Default coding: utf8.'''
    with open(filename, mode, encoding = coding) as file:
        if type(content) != str:
            content = repr(content)
        file.write(content)

def fcopy(src: str, dst: str, coding: str = 'utf8'):
    '''Copy a file.
       Requires source directory(src) and destination directory(dst).
       Default coding: utf8.'''
    filename = src[:find(src).last('\\')]
    fwrite(dst if dst.endswith(filename) else os.path.join(dst, filename), fread(src, coding), coding = coding)

def write_csv(filename: str, content: list):
    ''''A simple csv writer.
        Write each element of the content list into a row.'''
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, 'w', newline = '') as f:
        writer = csv.writer(f)
        for data in content:
            writer.writerow(data)

def advancedSplit(obj: str, *seperators) -> list:
    '''Can have multiple seperators.'''
    if seperators == () or len(seperators) == 1:
        return obj.split(*seperators)
    word = ''
    lst = []
    for ch in obj:
        word += ch
        for sep in seperators:
            if word.endswith(sep):
                word = find(word).before(sep)
                if word:
                    lst.append(word)
                    word = ''
    if word:
        lst.append(word)
    return lst
##abbreviation
asplit = advancedSplit

def similar(obj1, obj2, capital = True):
    '''
    Determine the how similar two strings are.
    Set capital to False to ignore upper case.
    '''
    def grade(o1, o2):
        ## Let o1 >= o2
        if o1 == o2:
            return 1
        if o1 == '' or o2 == '':
            return 0
        len_o1 = len(o1)
        len_o2 = len(o2)
        score = len_o2 / len_o1
        if score == 1:
            result = sum((i == j) + (i != j) * (i.lower() == j.lower()) * 0.9 for i, j in zip(o1, o2)) / len_o1
            return eval(format(result, '.4f'))
        if len_o2 <= 15 and score > 0.6:
            substrings = [ o2[i: j] for i in range(len_o2) for j in reversed(range(i + 1, len_o2)) ]
            maxLen = 0
            for i, sub in enumerate(substrings):
                subLen = len(sub)
                if sub in o1 and maxLen < subLen:
                    maxLen = subLen
                try:
                    if i < 2 ** len(o2) - 2 and maxLen > len(substrings[i + 1]):
                        break
                except IndexError:
                    break
            else:
                return 0
            score = maxLen / len_o1
        if o2.lower() in o1.lower():
            if o2 in o1:
                if o1.startswith(o2):
                    score *= 1.5
                else:
                    pass
            else:
                score *= 0.9
        else:
            d1, d2 = find(o1).count(), find(o2).count()
            sd = set(d2.keys()).difference(set(d1.keys()))
            if len(sd) == len(d2):  ##完全不一样
                return 0
            for key in d1:
                if key in d2:
##                    score *= (d2[key] / d1[key]) ** ((d1[key] >= d2[key]) * 2 - 1)
                    if d1[key] > d2[key]:
                        score *= d2[key]/d1[key]
                    else:
                        score *= d1[key]/d2[key]
            score *= 1 - sum([d2.get(item) for item in sd ]) / len_o2
##            不乘0.8的话similar('12345678', '23')跟similar('12345678', '24')都是0.25
##          可以用距离
            score *= 0.8
        return eval(format(score, '.4f'))

    if type(obj1) != str or type(obj2) != str:
        raise DataTypeError
    if not capital:
        obj1 = obj1.lower()
        obj2 = obj2.lower()
    if len(obj1) >= len(obj2):
        return grade(obj1, obj2)
    else:
        return grade(obj2, obj1)

def __levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i, c2 in enumerate(s2):
        lst = [i + 1]
        for j, c1 in enumerate(s1):
            if c1 == c2:
                lst.append(distances[j])
            else:
                lst.append(1 + min(distances[j], distances[j + 1], lst[-1]))
        distances = lst
    return distances[-1]

def similar2(obj1, obj2, capital = True):
    '''
    Check the how similar string obj1 to obj2 is using Levenshtein Distance.
    Set capital to False to ignore capital.
    '''
    if capital:
        obj1 = obj1.lower()
        obj2 = obj2.lower()
    ld = __levenshteinDistance(obj1, obj2)
    return 1 - ld / len(obj2)

def predir():
    '''Go back to the parent folder (not root).'''
    path = os.getcwd()
    os.chdir(path[:find(path).last('\\')])

def isMultiple(obj1, obj2) -> bool:
    '''Check whether obj1 is a multiple of obj2'''
    type1 = type(obj1)
    assert type1 == type(obj2), 'Inconsistent data type'
    if type1 == int: return obj1 % obj2 == 0
    length1 = len(obj1)
    length2 = len(obj2)
    if length1 % length2:
        return False
    return all(obj1[i:i + length2] == obj2 for i in range(0, length1, length2))

def contains(obj, *args) -> bool:
    '''Check whether obj contains any of the args.'''
    return any(arg in obj for arg in args)

class find:
    '''A helper class which finds something in the object.
       An empty object will result in undefined behaviors.'''
    def __init__(self, obj):
        self.type = type(obj)
        self.empty = self.type()
        self.obj = obj
        if not isinstance(obj, Iterable):
            print('Unsupported data is converted to str by default.')
            self.obj = repr(obj)
            self.type = str

    def __iter(self, target):
        try:
            if self.type == str:
                for i in range(len(self.obj)):
                    if self.obj[i:i + len(target)] == target:
                        yield i
            else:
                for i, n in enumerate(self.obj):
                    if n == target:
                        yield i
        except Exception as e:
            print(e)
            raise DataTypeError

    def before(self, target, nth = 1):
        '''Return the obj before the target.'''
        for i, n in enumerate(self.__iter(target)):
            if i == nth - 1:
                return self.obj[:n]
        return self.empty

    def after(self, target, nth = 1):
        '''Return the obj after the target.'''
        for i, n in enumerate(self.__iter(target)):
            if i == nth - 1:
                return self.obj[n + (self.type != str or len(target)):]
        return self.empty

    def nth(self, target, nth = 1):
        '''Return the nth index.'''
        count = nth - 1 if nth >= 0 else nth % sum(1 for _ in self.__iter(target))
        for i, n in enumerate(self.__iter(target)):
            if i == count:
                return n
        return -1

    def all(self, target):
        '''Find all the occurring indices in an obj.'''
        return tuple(self.__iter(target))

    def between(self, left, right, ln = 1, rn = -1):
        '''
        Return the obj between left and right (both are exclusive).
        Start after nth(ln) ocurrence of left.
        End before nth(rn) ocurrence of right.
        If ln or rn is 0, then left or right becomes inclusive.
        '''
        start = 0 if ln == 0 else self.nth(left, ln) + len(left)
        end = None if rn == 0 else start + find(self.obj[start:]).nth(right, rn)
        return self.obj[start:end]

    def consecutive(self) -> int:
        '''Count the longest consecutive targets.'''
        if self.type == dict:
            raise DataTypeError
        maxStreak = streak = 1
        for i, n in enumerate(self.obj):
            if i == 0: continue
            if n == self.obj[i - 1]:
                streak += 1
            else:
                if streak >= maxStreak:
                    maxStreak = streak
                streak = 1
        return maxStreak

    def distance(self, left, right, ln = 1, rn = -1) -> int:
        '''
        Find the distance between left and right.
        Start after nth(ln) ocurrence of left.
        End before nth(rn) ocurrence of right.
        '''
        return len(self.between(obj1, obj2))

    def keys(self, value) -> tuple:
        '''Find a tuple of all the keys with the value.'''
        if self.type != dict:
            raise DataTypeError
        return tuple(k for k, v in self.obj.items() if v == value)

    def key(self, value):
        '''Find the unique key that corresponds to the value.'''
        if self.type != dict:
            raise DataTypeError
        return next((k for k, v in self.obj.items() if v == value), None)

    def last(self, target):
        '''Find the last index in obj. Return -1 if not found'''
        try:
            if self.type == str:
                for i, item in enumerate(reversed(self.obj)):
                    index = len(self.obj) - i - 1
                    if self.obj[index:index + len(target)] == target:
                        return index
            else:
                for i, item in enumerate(reversed(self.obj)):
                    if item == target:
                        return len(self.obj) - i - 1
            return -1
        except:
            raise DataTypeError

    def powerSet(self):
        '''
        Find all the subs of obj except the empty sub and itself.
        This fuction returns a list because set is not ordered.
        '''
        return list(chain.from_iterable(combinations(self.obj, r) for r in range(len(self.obj) + 1)))
    #    res = [[]]
    #    for n in self.obj:
    #        for lst in res:
    #            res.append(lst + [n])
    #    return res

    def count(self):
        '''Calls collections.Counter'''
        return dict(Counter(self.obj))

    def switch(self, obj1, obj2):
        ''''Switch obj1 and obj2 in obj. (Assume obj1 and obj2 occur once)'''
        obj = self.obj[:]
        if obj1 != obj2:
            index1 = self.nth(obj1)
            if index1 == -1:
                raise ValueError(f"{obj1} not found.")
            index2 = self.nth(obj2)
            if index2 == -1:
                raise ValueError(f"{obj1} not found.")
            if self.type == str:
                if type(obj1) != str or type(obj2) != str:
                    raise DataTypeError
                if index1 > index2:
                    obj1, obj2 = obj2, obj1
                    index1, index2 = index2, index1
                obj = obj[:index1] + obj2 + obj[index1 + len(obj1):index2] + obj1 + obj[index2 + len(obj2):]
            else:
                obj[index1], obj[index2] = obj2, obj1
        return obj

##flatten = lambda x:[y for l in x for y in flatten(l)] if isinstance(x, list) else [x]
def flatten(sequence, ignore_types = (str, bytes)):
    '''Flattens an iterable if not ignored.'''
    typ = type(sequence)
    def generator(sequence):
        for item in sequence:
            if isinstance(item, typ):
                yield from flatten(item)
            else:
                yield item
    return sequence if isinstance(sequence, ignore_types) else typ(generator(sequence))

def rmdup(obj):
    '''Return a list without duplicates.'''
    new = []
    for i in obj:
        if i not in new:
            new.append(i)
    return type(obj)(new)

def without(obj, *args):
    '''Return an obj without elements of args.'''
    typ = type(obj)
    generator = (i for i in obj if i not in args)
    if typ in [list, tuple]:
        return type(obj)(generator)
    if typ == str:
        for arg in args:
            obj = obj.replace(arg, '')
        return obj
    if typ == dict:
        return { k: obj[k] for k in obj if k not in args }
    if typ in [set, frozenset]:
        return obj.difference(args)
    raise DataTypeError

def replaceWith(obj, withObj, *args):
    '''Replace the occurence of args in obj with withObj.'''
    argList = []
    for arg in args: argList += [arg, withObj]
    return sub(obj, *argList)

def substitute(obj, *args):
    '''obj supported data type: str, tuple, list, set.
       Usage: substitute([1, 2, 3, 4], 1, 2, 2, 3) // Returns [3, 3, 3, 4]
       Abbreviation: sub'''
    num = len(args)
    if num == 0:
        return
    if num % 2:
        raise Exception('Incorrect number of words')
    typ = type(obj)
    if typ == str:
        new = obj
        for i in range(0, num, 2):
            new = new.replace(str(args[i]), str(args[i + 1]))
    else:
        if typ in [tuple, list]:
            new = typ()
        else:
            raise DataTypeError
        for item in obj:
            for i in range(0, num, 2):
                if item == args[i]:
                    item = args[i + 1]
            if typ == set:
                new.add(item)
            else:
                new = new.__add__(typ([item]))
    return new

##abbreviation
sub = substitute

def formatted():
    '''请叫我套路生成器'''
    fmt = input('Please input your format sentence with variables replaced by {}.\n>>> ')
    while fmt.find('{}') == -1:
        fmt = input('Please type in at least 1 pair of {}!\n>>> ')
    else:
        fmtlst = fmt.split('{}')
        printlst = []
        while True:
            printstr = ''
            var = input('Please input your variables seperated with only 1 space or comma below. No input will stop this function.\n>>> ')
            varlst = advancedSplit(var)
            if not var:
                break
            if len(varlst) == 1:
                varlst *= fmt.count('{}')
            elif len(varlst) != fmt.count('{}'):
                print('Incorrect number of variables!')
                continue
            for i in range(len(varlst)):
                printstr += fmtlst[i]+varlst[i]
            if len(fmtlst) == len(varlst)+1:
                printstr += fmtlst[-1]
            printlst.append(printstr)
        seperation = input('Input Sentence Seperator. Default: \'\\n\'.\n>>> ') or '\n'
        print('\nResult:\n\n' + seperation.join(printlst) + '\n\n')

#abbreviation
fmt = formatted

def intToDatetime(date: int):
    return datetime.datetime(date // 10000, (date % 10000) // 100, date % 100)

def delta_days(date1: int, date2: int = None):
    '''Return the days difference between two dates.
       Date must be in the format of YYYYMMDD.
       If date2 is None, then it will be regarded as today.'''
    start = intToDatetime(date1)
    end = intToDatetime(date2) if date2 else datetime.datetime.today()
    delta = abs((end - start).days + 1)
    return delta

def days_ago(nDays: int, date: int = None):
    '''Return the date n days ago.
       If date is None, then it will be regarded as today.'''
    start = intToDatetime(date) if date else datetime.datetime.today()
    d = start - datetime.timedelta(days = nDays)
    return int(d.strftime('%Y%m%d'))

def days_later(nDays: int, date: int = None):
    '''Return the date n days after someday.
       If date is None, then it will be regarded as today.'''
    start = intToDatetime(date) if date else datetime.datetime.today()
    d = start + datetime.timedelta(days = nDays)
    return int(d.strftime('%Y%m%d'))