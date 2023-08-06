import os,glob

def organize(rootpath=None,outfolder=None,overwrite=False):
    if rootpath is None:
        rootpath = '.'
    if outfolder is None:
        outfolder = 'output'
    # setup outfolder
    if not overwrite:
        tmp = glob.glob('*')
        if outfolder in tmp:
            raise ValueError('outfolder = {0} already exists. Set overwrite = True to overwrite'.format(outfolder))
    if overwrite:
        os.system('rm -r ./{0}'.format(outfolder))
    os.system('mkdir {0}'.format(outfolder))
    # moving files
    tmp = glob.glob('{0}/*'.format(rootpath))
    for i in tmp:
        if i.split('.')[-1]=='ipynb':
            continue
        if i.split('/')[-1]==outfolder:
            continue
        os.system('cp -r {0} ./{1}/.'.format(i,outfolder))
        os.system('rm -r {0}'.format(i))
        