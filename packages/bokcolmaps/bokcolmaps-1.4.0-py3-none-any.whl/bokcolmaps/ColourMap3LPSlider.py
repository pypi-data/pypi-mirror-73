"""
ColourMap3LPSlider class definition
"""

from bokeh.models.widgets import Slider
from bokeh.models.layouts import Column

from bokeh.core.properties import Instance

from bokcolmaps.ColourMap3LP import ColourMap3LP

from bokcolmaps.get_common_kwargs import get_common_kwargs


class ColourMap3LPSlider(Column):

    """
    A ColourMap3LP with a slider linked to the z coordinate
    (i.e. the 2D slice being displayed).
    """

    __view_model__ = 'Column'
    __subtype__ = 'ColourMap3LPSlider'

    __view_module__ = 'bokeh'

    cmaplp = Instance(ColourMap3LP)
    zslider = Instance(Slider)

    def __init__(self, x, y, z, dm, **kwargs):

        """
        All init arguments same as for ColourMap3LP.
        """

        palette, cfile, revcols, xlab, ylab, zlab,\
            dmlab, rmin, rmax, xran, yran = get_common_kwargs(**kwargs)

        cmheight = kwargs.get('cmheight', 575)
        cmwidth = kwargs.get('cmwidth', 500)
        lpheight = kwargs.get('lpheight', 500)
        lpwidth = kwargs.get('lpwidth', 300)
        revz = kwargs.get('revz', False)
        hoverdisp = kwargs.get('hoverdisp', True)
        scbutton = kwargs.get('scbutton', False)

        super().__init__()

        self.height = cmheight
        self.width = int((cmwidth + lpwidth) * 1.1)

        self.cmaplp = ColourMap3LP(x, y, z, dm,
                                   palette=palette, cfile=cfile, revcols=revcols,
                                   xlab=xlab, ylab=ylab, zlab=zlab, dmlab=dmlab,
                                   cmheight=cmheight, cmwidth=cmwidth,
                                   lpheight=lpheight, lpwidth=lpwidth,
                                   rmin=rmin, rmax=rmax, xran=xran, yran=yran,
                                   revz=revz, hoverdisp=hoverdisp, scbutton=scbutton)

        self.zslider = Slider(title=zlab + ' index', start=0, end=z.size - 1,
                              step=1, value=0, orientation='horizontal')

        self.zslider.js_on_change('value', self.cmaplp.cmplot.cjs_slider)

        self.children.append(Column(self.zslider, width=self.width))
        self.children.append(self.cmaplp)
