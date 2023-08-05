#merge ts files
from pathlib import Path 
import sys 
import os
import shutil
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
import time
import click
import hashlib
import subprocess
from urllib.parse import urlparse
import requests
global_set = {'use_wget':False,'downloaded':0,'not_printed':False}
def down_content(url,outfile,downloader,rate = 0):
    try:
        if outfile.exists():
            if outfile.stat().st_size > 1:
                if not global_set['not_printed']:
                    print('Exists','{:.3f}%'.format(rate*100), outfile)
                return
        global_set['downloaded'] += 1 
        print('{:.3f}%'.format(rate*100),url,outfile.name)
        temp_file = outfile.with_suffix('.temp_download')
        if global_set['use_wget']:
            t = subprocess.call('wget -e robots=off --no-check-certificate -q -O "{}" {}'.format(temp_file,url),shell=True) 
            assert t == 0
        else:
            content = downloader.get(url, stream=True)
            with open(temp_file, "wb") as fp:
                for chunk in content.iter_content(chunk_size=512):
                    fp.write(chunk)
        os.rename(temp_file,outfile)
    except Exception as e:
        print(e)
def join_url(purl,url):
    purl = urlparse(purl)
    pp     = Path(purl.path)
    fs = purl.scheme+'://'+purl.netloc+'{}'
    if url.startswith('http'):
        url_result = url 
    elif url.startswith('/'):
        url_result = fs.format(url)
    else:
        url_result = fs.format(pp.parent / Path(url))
    return url_result
def _deal(s,fp):
    result = None
    if not s.startswith('#'):
        new_line = Path(s).name
        result = s.strip()
    else:
        start = s.find('URI=')
        new_line = s
        if start != -1:
            keyf = s[start+4:].strip().replace('"','')
            new_line = s.replace(keyf,Path(keyf).name)
            result = keyf.strip()
    fp.write(new_line)
    return result


def download_m3u8_requeset(url,out_name,delete_m3u8,suffix,multi_requests,force_aac,fast_flag):
    
  
    print('download',url,out_name)
    m3u8_dir = out_name.parent / (out_name.name + '_dir')
    if not m3u8_dir.exists():
        os.makedirs(m3u8_dir)
    m3u8_file = m3u8_dir / 'index.m3u8'

    session = requests.session()

    down_content(url,m3u8_file,session)

    files = []
    ultra_m3u8 = m3u8_dir / 'index_ultra.m3u8'
    fp = open(ultra_m3u8,'w')
    for i in open(m3u8_file):
        s = _deal(i,fp)
        if s:
            files.append(s)
    fp.close()
    pool = ThreadPoolExecutor(multi_requests)

    n_files = len(files)
    
    for it in range(10):
        global_set['downloaded'] = 0
        if it > 0:
            global_set['not_printed'] = True

        all_tasks = [pool.submit(down_content,join_url(url, i),m3u8_dir / Path(i).name,session,(n+1)/n_files) for n,i in enumerate(files)]
        wait(all_tasks,return_when=ALL_COMPLETED)
        time.sleep(0.5)
        if global_set['downloaded'] == 0:
            break
    if not force_aac:
        ffmpeg_command = f'ffmpeg -y -allowed_extensions ALL -i "{ultra_m3u8}" -c:v copy -c:a copy {fast_flag} "{out_name}"'
        print("ffmpeg exec:",ffmpeg_command)
        t = subprocess.call(ffmpeg_command,shell=True)
        print('ffmpeg return:',t)
    else: 
        t = 1
    if t != 0:
        ffmpeg_command = f'ffmpeg -y -allowed_extensions ALL -i "{ultra_m3u8}" -c:v copy -c:a aac {fast_flag} "{out_name}"'
        print("ffmpeg exec:",ffmpeg_command)
        t = subprocess.call(ffmpeg_command,shell=True)
        print('second trying ffmpeg return:',t)
    time.sleep(1)
    n_exists_files = len(list(m3u8_dir.glob('*')))
    if delete_m3u8 and n_exists_files>n_files and out_name.exists():
        shutil.rmtree(m3u8_dir)


def download_m3u8_ffmpeg(url,out_name,delete_m3u8,suffix,multi_requests,force_aac,fast_flag):

    if out_name.exists():
        print(url,out_name,"文件已存在")
        return
    else:
        print('download',url,out_name)
    m3u8_dir = out_name.parent / (out_name.name + '_dir')
    if not m3u8_dir.exists():
        os.makedirs(m3u8_dir)
    m3u8_name = m3u8_dir / ('temp.m3u8')
    subprocess.call(f'ffmpeg -y -i {url} -c copy  {m3u8_name}',shell=True)
    time.sleep(0.5)
    fs = list(m3u8_dir.glob('*.ts'))
    outfile = merge_file(fs,m3u8_dir/'m3u8.txt')
    subprocess.call(f'ffmpeg -y -allowed_extensions ALL -i "{outfile}" -c copy {fast_flag} "{out_name}"',shell=True)
    if delete_m3u8:
        shutil.rmtree(m3u8_dir)
def merge_file(files,outfile='out.txt',key_file = None):
    file_list = [Path(i).absolute() for i in files]
    stem = file_list[0].stem
    ipos = 0
    for i in range(1,len(stem)+1):
        print(stem[-i])
        if not stem[-i].isdigit():
            ipos = len(stem) - (i-1)
            break
    print(ipos,'ipos')
    file_list.sort(key = lambda x:int(x.stem[ipos:]))
    fp = open(outfile,'w')
    fp.write('#EXTM3U\n#EXT-X-TARGETDURATION:400\n')
    sf = '#EXTINF:400,\n{}\n'
    if key_file is not None:
        fp.write('#EXT-X-KEY:METHOD=AES-128,URI="{}"\n'.format(key_file))
    
    for f in file_list:
        fp.write(sf.format(f))
    fp.write('#EXT-X-ENDLIST')
    fp.close()
    return outfile 
def deal_dir(dirname,format='*.ts',walk=True,out_dir=None,key_f = '*.key',used_dirs = [],fast_flag=''):
    p = Path(dirname)
    if str(p) in used_dirs:
        return
    try:
        fs = list(p.glob(format))
    except:
        return
    key_file = list(p.glob(key_f))
    if key_file:
        key_file = key_file[0]
    else:
        key_file = None
    if fs:
        used_dirs.append(str(p))
        if out_dir is None:
            out_dir = p
        else: 
            out_dir = Path(out_dir)
        outfile = out_dir / (p.stem+'_out.m3u8')
        merge_file(fs,outfile,key_file=key_file)

        out_mp4 = out_dir / outfile.with_suffix('.mp4').name
        print(out_mp4)
        if not out_mp4.exists() or True:

            subprocess.call(f'ffmpeg -y -allowed_extensions ALL -i "{outfile}" -c copy {fast_flag} "{out_mp4}"',shell=True)
        if out_mp4.is_file():
            os.remove(outfile)
    else:
        m3u8_files = list(p.glob('*.m3u8'))
        if m3u8_files:
            for i in m3u8_files:
                outfile,m3u8_dir = merge_m3u8_file(i)
                if m3u8_dir:
                    used_dirs.append(str(m3u8_dir))
                    if out_dir is None:
                        out_dir = p
                    else: 
                        out_dir = Path(out_dir)
                    out_mp4 = out_dir / outfile.with_suffix('.mp4').name
                    if not out_mp4.exists() or True:
                        subprocess.call(f'ffmpeg -y -allowed_extensions ALL -i "{outfile}" -c copy {fast_flag} "{out_mp4}"',shell=True)
                    if out_mp4.is_file():
                        os.remove(outfile)
    if walk:
        for i in p.glob('*'):
            if i.is_dir():
                deal_dir(i,format,walk,out_dir)
def merge_m3u8_file(m3u8_name):
    m3u8_parent = Path(m3u8_name).parent
    fp = open(m3u8_name)
    ts_path = None
    for i in fp:
        if not i.startswith('#'):
            try:
                ts_path = Path(i)
            except:
                continue
            break 
    fp.seek(0,0)
    ts_dir = None
    if ts_path is None:
        return None,None
    for i in range(100):
        name = ts_path.name
        ts_path = ts_path.parent 
        if (m3u8_parent / name).exists():
            ts_dir = (m3u8_parent/name).absolute()
            break
    else:
        print('no ts file was found.')
        return None,None
    out_m3u8 = None
    if ts_dir:
        out_m3u8 = ts_dir/(ts_dir.name+'.m3u8')
        ofp = open(out_m3u8,'w')
        for i in fp:
            if i.startswith('#'):
                start = i.find('URI=')
                if start != -1:
                    keyf = i[start+4:].strip().replace('"','')
                    m = Path(keyf)
                    keyn = ts_dir / m.name 
                    i = '{}"file://{}"\n'.format(i[:start+4],keyn)
                ofp.write(str(i))
            else:
                ofp.write(str(ts_dir/Path(i).name))
        ofp.close()
    return out_m3u8,ts_dir
def is_existed(filepath):
    index_set = set()
    for pf in filepath.parent.parent.glob('*'):
        if pf.is_dir:
            index_set.update({j for i in pf.glob('*') if i.is_file() for j in i.stem.split('.')})
    name_list = filepath.stem.split('.')
    for i in name_list:
        if i != 'fast':
            if i in index_set:
                return True,i 
    return False,None


@click.command()
@click.argument('uri',nargs=-1)
@click.option('--dirname','-d',  default=None,help="需要合并的m3u8文件所在的文件夹")
@click.option('--suffix','-s',   default='.ts',help='视频文件后缀')
@click.option('--url','-u',               help='需要下载的m3u8链接,如果url采用多行的形式则认为是多个url，如果单个url采用空格分割，则分别认定为url output')
@click.option('--output','-o',            help='输出文件,%d作为格式化文件名输出。m3u8文件合并时，该参数为文件夹路径')
@click.option('--delete','-D',   default=True,type=click.BOOL,help='是否删除源文件,针对url下载项使用')
@click.option('--downloader',    default='requests',type=click.Choice(['requests','ffmpeg','wget']),help='m3u8 下载器选择(默认requests)')
@click.option('--multi_requests',default=2,help='requests 下载单个url的线程数')
@click.option('--md5_suffix',    default=True,help="文件名中是否加入md5后缀，默认加入")
@click.option('--faststart',     default=False,help="加入ffmpeg的faststart处理",is_flag = True)
@click.option('--force_aac','-f',default=False,help="ffmpeg强制转码aac 默认False",is_flag=True)
@click.option('--yes_answer','-y',default=False,help="对出现的分歧采用yes回答",is_flag=True)
def main(uri = None,dirname=None,url=None,suffix='.ts',output=None,delete=False,downloader='requests',multi_requests=1,md5_suffix=True,faststart=False,
         force_aac=True,yes_answer=False):
    set_input = False
    if not faststart:
        fast_flag = ''
    else:
        fast_flag = '-movflags faststart'
    if not dirname and not url:
        if uri:
            set_input = True
            if uri[0].startswith('http'):
                url = uri[0]
            else:
                dirname = uri[0]
    if not output:
        if set_input:
            if len(uri) == 2:
                output = uri[1]
        else:
            if len(uri) == 1:
                output = uri[0]

    suffix = '*'+suffix
    if url:
        if downloader == 'ffmpeg':
            download_m3u8 = download_m3u8_ffmpeg 
        elif downloader == 'wget':
            download_m3u8 = download_m3u8_requeset
            global_set['use_wget'] = True
        else:
            download_m3u8 = download_m3u8_requeset
        print('downloader :',downloader)
        # for i,s in enumerate(url.strip().split('\n')):
        #     st = s.split()
        #     url = st[0]
        md5_name = str(hashlib.md5(url.encode('utf8')).hexdigest())
        
        if output:
            pof = Path(output)
            oname_split = pof.name.split('.')
            if md5_suffix:
                oname_split.insert(1,md5_name)
            out_name = pof.with_name('.'.join(oname_split))
        else:
            out_name = '{}.mp4'
            out_name = Path(out_name.format(md5_name))
        out_name = out_name.absolute()
        exists,feature = is_existed(out_name)
        if exists:
            if not yes_answer:
                ans = input('file "{}" already existed, continue to cover it?[Y/N]N'.format(feature))
                if ans.lower() == 'y':
                    could_download = True 
                else: 
                    could_download = False
            else:
                could_download = True
        else:
            could_download = True
        if could_download:

            print('outfilename :',out_name.name)
            download_m3u8(url,out_name,delete,suffix,multi_requests,force_aac,fast_flag)
            print('write_file:',out_name.name)

    if dirname:
        deal_dir(dirname,format=suffix,out_dir=output,fast_flag= fast_flag)
if __name__=='__main__':
    main()