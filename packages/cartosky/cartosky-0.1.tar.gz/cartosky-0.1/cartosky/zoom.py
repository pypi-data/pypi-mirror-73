#!/usr/bin/env python
"""
Using AxisArtist to zoom on specific surveys.
"""
import os

import numpy as np
import pylab as plt
import pandas as pd
from collections import OrderedDict as odict

from mpl_toolkits.axisartist.grid_helper_curvelinear import GridHelperCurveLinear
from mpl_toolkits.axisartist import Subplot
import mpl_toolkits.axisartist as axisartist
import  mpl_toolkits.axisartist.angle_helper as angle_helper

from cartosky.utils import setdefaults,get_datadir,hpx_gal2cel
from cartosky.core import Skymap,McBrydeSkymap,OrthoSkymap
from cartosky.survey import SurveySkymap,SurveyMcBryde,SurveyOrtho

# Original DES Formatter
# ADW: Why doesn't ZoomFormatter180 work?
class ZoomFormatterDES(angle_helper.FormatterDMS):

    def __call__(self, direction, factor, values):
        values = np.asarray(values)
        ss = np.where(values>=0, 1, -1)
        values = np.mod(np.abs(values),360)
        values -= 360*(values > 180)
        return [self.fmt_d % (s*int(v),) for (s, v) in zip(ss, values)]

class ZoomFormatter(angle_helper.FormatterDMS):
    def _wrap_angle(self, angle):
        return angle

    def __call__(self, direction, factor, values):
        values = np.asarray(values)
        values = self._wrap_angle(values)
        ticks = [self.fmt_d % (int(v),) for v in values]
        return ticks

class ZoomFormatter360(ZoomFormatter):
    def _wrap_angle(self, angle):
        """Ticks go from 0 to 360"""
        angle = np.mod(angle,360)
        return angle

class ZoomFormatter180(ZoomFormatter):
    def _wrap_angle(self, angle):
        """Ticks go from -180 to 180"""
        angle = np.mod(np.abs(angle),360)
        angle -= 360*(angle > 180)
        return angle

class SurveyZoom(SurveyMcBryde):
    FRAME = [[-50,-50,90,90],[10,-75,10,-75]]
    EXTENT = [90,-50,-75,10]
    FIGSIZE=(8,5)

    def __init__(self, rect=None, *args, **kwargs):
        defaults = dict(gridlines=False,celestial=True)
        setdefaults(kwargs,defaults)
        do_celestial = kwargs['celestial']
        super(SurveyZoom,self).__init__(*args, **kwargs)

        self.set_axes_limits()
        self.create_axes(rect)
        self.set_axes_limits()

        self.ax.set_frame_on(False)
        self.aa.grid(True,linestyle=':',color='k',lw=0.5)

        if do_celestial: self.invert_xaxis()

    @classmethod
    def figure(cls,**kwargs):
        """ Create a figure of proper size """
        defaults=dict(figsize=cls.FIGSIZE)
        setdefaults(kwargs,defaults)
        return plt.figure(**kwargs)

    def draw_parallels(*args, **kwargs): return
    def draw_meridians(*args, **kwargs): return

    def invert_xaxis(self):
        self.ax.invert_xaxis()
        self.aa.invert_xaxis()

    def set_axes_limits(self):
        extent = [min(self.FRAME[0]),max(self.FRAME[0]),
                  min(self.FRAME[1]),max(self.FRAME[1])]

        self.ax.set_extent(self.EXTENT)

        # AxisArtist
        if hasattr(self,'aa'):
            self.aa.set_xlim(self.ax.get_xlim())
            self.aa.set_ylim(self.ax.get_ylim())

        return self.ax.get_xlim(),self.ax.get_ylim()

    def create_tick_formatter(self):
        return ZoomFormatter()

    def create_axes(self,rect=111):
        """
        Create a special AxisArtist to overlay grid coordinates.

        Much of this taken from the examples here:
        http://matplotlib.org/mpl_toolkits/axes_grid/users/axisartist.html
        """
        # from curved coordinate to rectlinear coordinate.
        def tr(x, y):
            return self(x,y)

        # from rectlinear coordinate to curved coordinate.
        def inv_tr(x,y):
            return self(x,y,inverse=True)

        # Cycle the coordinates
        extreme_finder = angle_helper.ExtremeFinderCycle(20, 20)

        # Find a grid values appropriate for the coordinate.
        # The argument is a approximate number of grid lines.
        grid_locator1 = angle_helper.LocatorD(9,include_last=False)
        #grid_locator1 = angle_helper.LocatorD(8,include_last=False)
        grid_locator2 = angle_helper.LocatorD(6,include_last=False)

        # Format the values of the grid
        tick_formatter1 = self.create_tick_formatter()
        tick_formatter2 = angle_helper.FormatterDMS()

        grid_helper = GridHelperCurveLinear((tr, inv_tr),
                                            extreme_finder=extreme_finder,
                                            grid_locator1=grid_locator1,
                                            grid_locator2=grid_locator2,
                                            tick_formatter1=tick_formatter1,
                                            tick_formatter2=tick_formatter2,
        )

        fig = plt.gcf()
        rect = self.ax.get_position()
        ax = axisartist.Axes(fig,rect,grid_helper=grid_helper,frameon=False)
        fig.add_axes(ax)

        ## Coordinate formatter
        def format_coord(x, y):
            return 'lon=%1.4f, lat=%1.4f'%inv_tr(x,y)
        ax.format_coord = format_coord
        ax.axis['left'].major_ticklabels.set_visible(True)
        ax.axis['right'].major_ticklabels.set_visible(False)
        ax.axis['bottom'].major_ticklabels.set_visible(True)
        ax.axis['top'].major_ticklabels.set_visible(True)

        ax.axis['bottom'].label.set(text="Right Ascension",size=18)
        ax.axis['left'].label.set(text="Declination",size=18)
        self.aa = ax

        # Set the current axis back to the SkyAxes
        fig.sca(self.ax)

        return fig,ax

class DESSkymapMcBryde(SurveyZoom):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[-50,-50,90,90],[10,-75,10,-75]]
    EXTENT = [90,-50,-75,10]
    FIGSIZE=(8,5)

    def __init__(self, *args, **kwargs):
        defaults = dict(lon_0=0,celestial=True)
        setdefaults(kwargs,defaults)
        #super(DESSkymapMcBryde,self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def create_tick_formatter(self):
        return ZoomFormatterDES()
        #return ZoomFormatter180()

DESSkymap = DESSkymapMcBryde

### These should be moved into streamlib

class DESSkymapQ1(DESSkymapMcBryde):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[10,-46],[-68,-38]]

    def draw_inset_colorbar(self, *args, **kwargs):
        defaults = dict(loc=4,height="6%",width="20%",bbox_to_anchor=(0,0.05,1,1))
        setdefaults(kwargs,defaults)
        super(DESSkymapMcBryde,self).draw_inset_colorbar(*args,**kwargs)

class DESSkymapQ2(DESSkymapMcBryde):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[60,0],[8,-45]]

    def draw_inset_colorbar(self, *args, **kwargs):
        defaults = dict(loc=2,width="30%",height="4%",bbox_to_anchor=(0,-0.1,1,1))
        setdefaults(kwargs,defaults)
        super(DESSkymapMcBryde,self).draw_inset_colorbar(*args,**kwargs)

class DESSkymapQ3(DESSkymapMcBryde):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[5,60],[-68,-38]]

    def draw_inset_colorbar(self, *args, **kwargs):
        defaults = dict(loc=3,height="7%",bbox_to_anchor=(0,0.05,1,1))
        setdefaults(kwargs,defaults)
        super(DESSkymapMcBryde,self).draw_inset_colorbar(*args,**kwargs)

class DESSkymapQ4(DESSkymapMcBryde):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[90,70],[-15,-55]]

    def draw_inset_colorbar(self, *args, **kwargs):
        defaults = dict(loc=3,width="30%",height="4%",bbox_to_anchor=(0,0.05,1,1))
        setdefaults(kwargs,defaults)
        super(DESSkymapMcBryde,self).draw_inset_colorbar(*args,**kwargs)

class DESSkymapCart(SurveyZoom):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[-60,-60,100,100],[10,-75,10,-75]]
    FIGSIZE=(8,5)

    def __init__(self, *args, **kwargs):
        defaults = dict(projection='cyl',celestial=True)
        setdefaults(kwargs,defaults)
        super(DESSkymapCart,self).__init__(*args, **kwargs)

    def create_tick_formatter(self):
        return ZoomFormatterDES()
        #return ZoomFormatter180()


class DESLambert(SurveySkymap):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FIGSIZE=(8,5)

    def __init__(self, *args, **kwargs):
        defaults = dict(projection='laea',lon_0=120,lat_0=-90,
                        llcrnrlon=-110,llcrnrlat=8,
                        urcrnrlon=60,urcrnrlat=-15,
                        round=False,celestial=False)

        setdefaults(kwargs,defaults)
        super(SurveySkymap,self).__init__(*args, **kwargs)


    def draw_meridians(self,*args,**kwargs):

        def lon2str(deg):
            # This is a function just to remove some weird string formatting
            deg -= 360. * (deg >= 180)
            if (np.abs(deg) == 0):
                return r"$%d{}^{\circ}$"%(deg)
            elif (np.abs(deg) == 180):
                return r"$%+d{}^{\circ}$"%(np.abs(deg))
            else:
                return r"$%+d{}^{\circ}$"%(deg)

        #defaults = dict(labels=[1,1,1,1],labelstyle='+/-',
        #                fontsize=14,fmt=lon2str)
        defaults = dict(fmt=lon2str,labels=[1,1,1,1],fontsize=14)
        if not args:
            defaults.update(meridians=np.arange(0,360,60))
        setdefaults(kwargs,defaults)

        #return self.drawmeridians(*args,**kwargs)
        return super(DESLambert,self).draw_meridians(*args,**kwargs)

    def draw_parallels(self,*args,**kwargs):
        defaults = dict(labels=[0,0,0,0])
        setdefaults(kwargs,defaults)
        ret =  super(DESLambert,self).draw_parallels(*args,**kwargs)

        ax = plt.gca()
        for l in ret.keys():
            ax.annotate(r"$%+d{}^{\circ}$"%(l), self(0,l),xycoords='data',
                        xytext=(+5,+5),textcoords='offset points',
                        va='top',ha='left',fontsize=12)
        return ret

    def draw_inset_colorbar(self,*args,**kwargs):
        defaults = dict(bbox_to_anchor=(-0.01,0.07,1,1))
        setdefaults(kwargs,defaults)
        return super(DESLambert,self).draw_inset_colorbar(*args,**kwargs)


class DESPolarLambert(DESLambert):
    """Class for plotting a zoom on DES. This is relatively inflexible."""
    # RA, DEC frame limits
    FIGSIZE=(8,8)

    def __init__(self, *args, **kwargs):
        defaults = dict(projection='splaea',lon_0=60,boundinglat=-20,
                        round=True,celestial=True,parallels=True)
        setdefaults(kwargs,defaults)
        super(SurveySkymap,self).__init__(*args, **kwargs)



class BlissSkymap(SurveyZoom):
    """Class for plotting a zoom on BLISS. This is relatively inflexible."""
    # RA, DEC frame limits
    FRAME = [[130,130,0,0],[-5,-55,-5,-55]]
    FIGSIZE = (12,3)
    defaults = dict(lon_0=-100)
    wrap_angle = 60

    def __init__(self, *args, **kwargs):
        setdefaults(kwargs,self.defaults)
        super(BlissSkymap,self).__init__(*args, **kwargs)

    def create_tick_formatter(self):
        return ZoomFormatter360()

class MaglitesSkymap(SurveyOrtho):
    defaults = dict(SurveyOrtho.defaults,lat_0=-90,celestial=True)

    def draw_meridians(self,*args,**kwargs):
        defaults = dict(labels=[1,1,1,1],fontsize=14,labelstyle='+/-')
        setdefaults(kwargs,defaults)
        cardinal = kwargs.pop('cardinal',False)
        meridict = super(OrthoSkymap,self).draw_meridians(*args,**kwargs)
        # We've switched to celestial, need to update meridian text
        for k,v in meridict.items():
            text = v[1][0].get_text()
            if text.startswith('-'):   text = text.replace('-','+')
            elif text.startswith('+'): text = text.replace('+','-')
            v[1][0].set_text(text)
        return meridict
