# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu
import os,glob,copy
from astropy.io import fits
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .background import Background
from .grismapcorr import GrismApCorr

class Extract:
    def __init__(self,grismfile,bkgfile,flatfile,tracefile,sensefile,halfdy,
                 objname='None',
                 savefolder='EXTRACT',overwrite=False,
                 padyup=5,padylow=5,
                 padxleft=15,padxright=15
                ):
        # remove/create savefolder
        if overwrite:
            os.system('rm -r {0}'.format(savefolder))
            print('Remove {0}'.format(savefolder))
        else:
            tmp = os.getcwd()
            try:
                os.chdir(savefolder)
                os.chdir(tmp)
                print('Stop: Savefolder {0} already exists, overwrite = {1}'.format(savefolder,overwrite))
                return
            except:
                pass
        tmp = os.getcwd()
        for i in savefolder.split('/'):
            os.system('mkdir {0}'.format(i))
            os.chdir(i)
        os.chdir(tmp)            
        print('Set savefolder {0}'.format(savefolder))
        # start instantiation
        self.data = {'objname':objname,
                     'grismfile':grismfile,
                     'bkgfile':bkgfile,
                     'flatfile':flatfile,
                     'tracefile':tracefile,
                     'sensefile':sensefile,
                     'halfdy':halfdy,
                     'savefolder':savefolder,
                     'padyup':padyup,
                     'padylow':padylow,
                     'padxleft':padxleft,
                     'padxright':padxright
                    }
        self.data['ROOTNAME'] = self._rootname() 
        self.grism = Background(objname=objname,gfile=grismfile[0],tfile=tracefile,
                                extnum=grismfile[1],savefolder='tmp_',overwrite=True,
                                padyup=padyup,padylow=padylow,
                                halfdyup=halfdy,halfdylow=halfdy,
                                padxleft=padxleft,padxright=padxright
                               )
        self.bkg = Background(objname=objname,gfile=bkgfile[0],tfile=tracefile,
                                extnum=bkgfile[1],savefolder='tmp_',overwrite=True,
                                padyup=padyup,padylow=padylow,
                                halfdyup=halfdy,halfdylow=halfdy,
                                padxleft=padxleft,padxright=padxright
                               )
        self.flatfield = Background(objname=objname,gfile=flatfile[0],tfile=tracefile,
                                extnum=flatfile[1],savefolder='tmp_',overwrite=True,
                                padyup=padyup,padylow=padylow,
                                halfdyup=halfdy,halfdylow=halfdy,
                                padxleft=padxleft,padxright=padxright
                               )
        self.sensitivity = self._get_sensitivity(sensefile)
    def _get_sensitivity(self,sensefile):
        tmp = fits.open(sensefile)
        return pd.DataFrame(tmp[1].data)
    def _rootname(self):
        grismfile = self.data['grismfile']
        tmp = fits.open(grismfile[0])[0].header['ROOTNAME']
        return tmp
    ##########
    ##########
    ##########
    def compute(self,do_bkgsub=True,do_flat=True,do_apcorr=True,instrument=None,do_flam=True):
        data = self.grism.bkg.data['Y']
        bkg = self.bkg.bkg.data['Y']
        flat = self.flatfield.bkg.data['Y']
        mask = self.grism.bkg.data['MASK']
        trace = self.grism.trace
        bbox = self.grism.bbox
        ww = bbox['bbox']['WW']
        xg = bbox['bbox']['XG']
        # we need
        # flam = cps / (apcorr * sensitivity * ww_per_pix)
        ##### cps
        if do_bkgsub:
            data = data - bkg
        if do_flat:
            data = data / flat
        cps = (data * mask.astype(float)).sum(axis=0)
        ##### ww_per_pix
        ww_per_pix = self._compute_wwperpix(ww,xg)
        ##### apcorr
        if do_apcorr:
            if instrument is None:
                string = 'instrument must be specified for do_apcorr = {0}'.format(do_apcorr)
                string += '\navailable instrument = {0}'.format(GrismApCorr().available_instrument)
                raise ValueError(string)
            apsize = mask.astype(float).sum(axis=0)
            grismapcorr = GrismApCorr(instrument=instrument,apsize=apsize,wave=ww,
                                      aptype='diameter',apunit='pix',waveunit='A'
                                     )  
            grismapcorr.compute()
            apcorr = grismapcorr.data['apcorr'].diagonal()
        else:
            apcorr = np.full_like(ww,1.,dtype=float)
        ##### sensitivity
        if do_flam:
            sensitivity_model = interp1d(self.sensitivity.WAVELENGTH,self.sensitivity.SENSITIVITY,kind='linear',bounds_error=False,fill_value=None)
            sensitivity = sensitivity_model(ww)
            sensitivity[~np.isfinite(sensitivity)] = 1. # replace nan with 1.
            flam = cps / (apcorr * sensitivity * ww_per_pix)
        else:
            sensitivity = np.full_like(ww,1.,dtype=float)
            flam = None
        ##### output
        self.extract = {'image':data,
                        'mask':mask,
                        'trace':trace,
                        'bbox':bbox,
                        'do_bkgsub':do_bkgsub,
                        'do_flat':do_flat,
                        'do_apcorr':do_apcorr,
                        'instrument':instrument,
                        'do_flam':do_flam,
                        '1d':{'cps':cps,'ww':ww,'xg':xg,
                              'apcorr':apcorr,'sensitivity':sensitivity,'ww_per_pix':ww_per_pix,
                              'flam':flam
                             }
                       }
    def _compute_wwperpix(self,ww,xg):
        wwdiff = np.diff(ww)
        wwdiff = np.append(wwdiff,wwdiff[-1])
        xgdiff = np.diff(xg)
        xgdiff = np.append(xgdiff,xgdiff[-1])
        return wwdiff/xgdiff
    ##########
    ##########
    ##########
    def show(self,save=False,savename_prefix=None,saveformat='pdf',
             params={'figsize':(10,10),
                     'color':'red',
                     'ls':':',
                     'lw':4,
                     'marker':'x',
                     'alpha':0.2,
                     'fontsize':12,
                     'minmax_im':(5.,99.),
                     'xpertick_im':100,
                     'xpertick_1d':50,
                     'cmap_im':'viridis',
                     'cmap_mask':'Greys',
                     'annotate_level':0.,
                     'sensitivity_level':0.1e16,
                     'adjust_minmax_flam':(0.9,1.1)
             }
            ):
        adjust_minmax_flam = params['adjust_minmax_flam']
        minmax_im = params['minmax_im']
        xpertick_im = params['xpertick_im']
        xpertick_1d = params['xpertick_1d']
        color = params['color']
        ls = params['ls']
        alpha = params['alpha']
        lw = params['lw']
        marker = params['marker']
        fontsize = params['fontsize']
        figsize = params['figsize']
        cmap_im = params['cmap_im']
        cmap_mask = params['cmap_mask']
        annotate_level = params['annotate_level']
        sensitivity_level = params['sensitivity_level']
        image = self.extract['image']
        mask = self.extract['mask']
        xref = self.extract['trace']['XREF']
        yref = self.extract['trace']['YREF']
        trace_xg = self.extract['trace']['XG']
        trace_yg = self.extract['trace']['YG']
        trace_ww = self.extract['trace']['WW']
        bbox_bbx = self.extract['bbox']['bbox']['BBX']
        bbox_bby = self.extract['bbox']['bbox']['BBY']
        bbox_xg = self.extract['bbox']['bbox']['XG']
        bbox_ww = self.extract['bbox']['bbox']['WW']
        do_flam = self.extract['do_flam']
        cps = self.extract['1d']['cps']
        flam = self.extract['1d']['flam']
        sensitivity = self.extract['1d']['sensitivity']

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(4,1,1)
        vmin,vmax = np.percentile(image,minmax_im[0]),np.percentile(image,minmax_im[1])
        ax.imshow(image,origin='lower',cmap=cmap_im,vmin=vmin,vmax=vmax)
        tmpx,tmpy = trace_xg,trace_yg
        bbx0,bby0 = bbox_bbx[0],bbox_bby[0]
        tmpx,tmpy = tmpx-bbx0,tmpy-bby0
        ww = trace_ww
        ax.plot(tmpx,tmpy,color=color,ls=ls,lw=lw,alpha=alpha)
        for i,ii in enumerate(tmpx):
            if (i in {0,len(tmpx)-1}) or (np.mod(i,xpertick_im)==0):
                label = '{0}A'.format(int(ww[i]))
                ax.plot(tmpx[i],tmpy[i],color=color,marker=marker)
                ax.annotate(label,(tmpx[i],tmpy[i]),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=fontsize,
                             rotation=0.,
                             color=color
                            )
        tmpmask = mask.astype(float)
        tmpmask[tmpmask==1.] = np.nan
        ax.imshow(tmpmask,origin='lower',cmap=cmap_mask,vmin=0.,alpha=alpha)
        string = '{0} {1} \ndo_bkgsub={2} do_flat={3}'.format(self.data['objname'],self.data['ROOTNAME'],
                                                              self.extract['do_bkgsub'],self.extract['do_flat']
                                                             )
        ax.set_title(string,fontsize=fontsize)
        string = 'pixY - {0}'.format(yref)
        ax.set_ylabel(string,fontsize=fontsize)

        ax = fig.add_subplot(4,1,2,sharex=ax)
        tmpy = cps.copy()
        tmpx = bbox_xg.copy()
        bbx0 = bbox_bbx[0]
        tmpx = tmpx-bbx0
        ax.plot(tmpx,tmpy)
        ax.plot(tmpx,np.full_like(tmpx,annotate_level,dtype=float),color=color,ls=ls,lw=lw)
        tmpx2 = trace_xg - bbx0
        tmpy2 = np.full_like(tmpx2,annotate_level,dtype=float)
        ww = trace_ww
        for i,ii in enumerate(tmpx2):
            if (i in {0,len(tmpx2)-1}) or (np.mod(i,xpertick_1d)==0):
                label = '{0}A'.format(int(ww[i]))
                ax.plot(tmpx2[i],annotate_level,color=color,marker=marker)
                ax.annotate(label,(tmpx2[i],annotate_level),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=fontsize,
                             rotation=90.,
                             color=color
                            )
        ax.set_ylabel('cps',fontsize=fontsize)
        ax.grid()
        
        if do_flam:
            ax = fig.add_subplot(4,1,3,sharex=ax)
            tmpx = bbox_xg-bbx0
            tmpy = flam.copy()
            ax.plot(tmpx,tmpy)
            m = np.argwhere(sensitivity >= sensitivity_level).flatten()
            tmpx_good,tmpy_good,ww_good = tmpx[m],tmpy[m],bbox_ww[m]
            for i,ii in enumerate(tmpx_good):
                if (i in {0,len(tmpx_good)-1}) or (np.mod(i,xpertick_1d)==0):
                    label = '{0}A'.format(int(ww_good[i]))
                    ax.plot(tmpx_good[i],tmpy_good[i],color=color,marker=marker)
                    ax.annotate(label,(tmpx_good[i],tmpy_good[i]),
                                 textcoords='offset points',
                                 xytext=(5,-5),
                                 ha='left',
                                 fontsize=fontsize,
                                 rotation=0.,
                                 color=color
                                )
            ax.set_ylim(tmpy_good.min()*adjust_minmax_flam[0],tmpy_good.max()*adjust_minmax_flam[1])
            ax.set_ylabel('flam',fontsize=fontsize)
            ax.grid()

            ax = fig.add_subplot(4,1,4,sharex=ax)
            ax.plot(tmpx,sensitivity)
            ax.plot(tmpx,np.full_like(tmpx,sensitivity_level),ls=ls,label='sensitivity_level = {0:.2E}'.format(sensitivity_level))
            ax.set_ylabel('sensitivity',fontsize=fontsize)
            ax.legend()
            ax.grid()
        else:
            pass

        string = 'pixX - {0}'.format(xref)
        ax.set_xlabel(string,fontsize=fontsize)

        fig.tight_layout()
        if save:
            string = '{0}_spc1d.{1}'.format(self.data['objname'],saveformat) if savename_prefix is None else '{0}_spc1d.{1}'.format(savename_prefix,saveformat)
            string = './{0}/'.format(self.data['savefolder'] + string
            fig.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
