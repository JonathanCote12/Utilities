#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Serge Dmitrieff
# www.biophysics.fr
#
# Based on Python Pyx
from pyx import *
from numpy import *
from pyx.graph import axis
from import_tools import *



"""
# SYNOPSIS

   splot is a shorthand command-line tool draw graphs using PyX. PyX is good.

# DESCRIPTION

   splot plots a graph from a text file (should I add excel support ?)
   it is meant to be fast and dirty (but uses PyX to be beautiful)

# SYNTAX

   python splot.py TEXT_FILE [OPTIONS] [ADDITIONAL_TEXT_FILES] [ADDITIONAL_OPTIONS]

# OPTIONS

    splot has two kinds of options : global (for the whole figure) and local (for a particular file)
    All options should be written as option_name=option_value

    Global options :
        xlabel        : label of x axis
        ylabel        : label of y axis
        width         : width of figure
        height        : height of figure
        xmin          : min x value
        xmax          : max x value
        ymin          : min y value
        ymax          : max y value
        key           : position of figure legend
        out           : name of output file
        -ylog         : y axis is logarithmic
        -xlog         : x axis is logarithmic
        -keep         : keep options for subsequent plots, until -discard
        -discard      : discard options for next plot

    Local options :
        x        : index of column or row to be used as x axis values (e.g. x=0 for the first column)
                        also can specify an operation : x=A[:,0]*A[:,1]
        y        : index of column or row to be used as y axis values (e.g. x=0 for the first column)
                        also can specify an operation : y=A[:,1]*A[:,2]/A[:,3]
        dy       : index of column or row to be used as dy values (e.g. x=0 for the first column)
                        also can specify an operation : dy=A[:,2]/sqrt(A[:,3])
        mode     : h for horizontal (rows), v for vertical (column) (default)

        color    : color of lines or symbol ; can be either red, green, blue, dark, medium, light, black
                        or color.cmyk.*  or color.rgb.*
                        or an operation, e.g. color=A[:,2]

        style    : style of plot : - or _ for a line, -- for dashed, .- for dashdotted
                                    o for circles  x , * for crosses  + for plus   > , <     for triangles
        if       : condition to keep the rows or columns

        range    : range of rows / columns to plot

        size     : size of symbol used

        line     : thickness of line, from 0 to 5

        title (or legend) : title of the graph

# EXAMPLES :

            splot.py file.txt
                        plots the second column of file.txt as a function of the first column
            splot.py file.txt x=3 y=7
                        plots the 4th (3+1) column of file.txt as a function of the eigth column (7+1)
            splot.py file.txt x=3 y=7 and x=3 y=10
                        plots the 4th (3+1) column of file.txt as a function of the eigth column (7+1),
                        and another plot of 4th column as a function of 11th column
            splot.py file.txt color=red file2.txt out=plot.pdf
                        plots in red the second column of file.txt as a function of the first column
                        plots the second column of file2.txt as a function of the first column in the same graph
            splot.py file.txt 'y=sqrt(A[:,1]^2+A[:,2]^2)' dy=3 color=1 grad=gray xlabel='$t$ in minutes' ylabel='$\bar{z}$'
                        A[:,1] and A[:,2] are the second and third columns of file.txt
                        the deviation is set from the fourth column of file.txt
                        the color is set from the second column of file.txt, based on a gray-level gradient
                        labels and titles use the Latex interpreter
            splot.py file.txt if='A[:,0]>1'
                        plots the second column as a function of the first if elements of the first are greater than 1
            splot.py file.txt mode='h' if='A[0,:]>1' -xlog
                        plots the second row as a function of the first row if elements of the first row are greater than 1
                        the x axis is logarithmic
            splot.py file.txt mode='h' if='A[0,:]>1' andif='A[0,:]<=1'
                        plots the second row as a function of the first row if elements of the first row are greater than 1
                        and (with a different style) if the elements of the first row are smaller than 1
            splot.py range=3 -keep data_0*.txt
                        plots data from only the third line of the files data_0*.txt
            splot.py data.txt x=1 y=2 and y=3
                        plots the third and fourth column as a function of the second
"""

# Basic set of colours
colours=[color.gray(0.0),color.gray(0.5),color.rgb.red,color.rgb.blue]
symbols=[graph.style.symbol.plus,graph.style.symbol.circle,graph.style.symbol.cross,graph.style.symbol.triangle]
linests=[style.linestyle.solid,style.linestyle.dashed,style.linestyle.dashdotted,style.linestyle.dotted]

# Dictionaries
col_dict= {
    'red' : color.rgb.red,
    'blue' : color.rgb.blue,
    'green' : color.rgb.green,
    'black' : color.gray(0.0),
    'dark' : color.gray(0.25),
    'medium' : color.gray(0.5),
    'light' : color.gray(0.75)
    }

linst_dict={
    '_' : style.linestyle.solid,
    '-' : style.linestyle.solid,
    '.' : style.linestyle.dotted,
    '.-' : style.linestyle.dashdotted,
    '-.' : style.linestyle.dashdotted,
    '--' : style.linestyle.dashed
    }

symst_dict={
    'x' : graph.style.symbol.cross,
    '*' : graph.style.symbol.cross,
    '+' : graph.style.symbol.plus,
    'o' : graph.style.symbol.circle,
    '>' : graph.style.symbol.triangle,
    '<' : graph.style.symbol.triangle
    }

linw_dict={
    '1' :     style.linewidth.thin,
    '2' :     style.linewidth.thick,
    '3' :     style.linewidth.Thick,
    '4' :     style.linewidth.THIck,
    '5' :     style.linewidth.THICK
    }

grad_dict={
    'rainbow'    :     color.gradient.Rainbow,
    'whitered'    :     color.gradient.WhiteRed,
    'wr'        :     color.gradient.WhiteRed,
    'redwhite'    :     color.gradient.RedWhite,
    'rw'        :     color.gradient.RedWhite,
    'gray'        :     color.gradient.Gray,
    'grey'        :     color.gradient.Gray,
    'gr'        :     color.gradient.Gray,
    'jet'        :     color.gradient.Jet,
    }

__SPLIT_MARK__ = '--split_mark--'

class Toplot:
    # Toplot is a class containing the options for plotting
    #   it also contains a method to split into two
    def __init__(self, fname, args):
        self.file_name=fname
        self.args=[arg for arg in args]
    def check_split(self):
        na=len(self.args)
        do_split=0
        for i,arg in enumerate(self.args):
            if arg==__SPLIT_MARK__:
                do_split=1
                n_split=i
        if do_split:
            future_args=self.args
            self.args=self.args[0:n_split]
            future_args.pop(n_split)
            return [1,Toplot(self.file_name,future_args)]
        else:
            return [0,1]


class Glob:
    # Glob is the global plotter class
    # It mostly sorts arguments and prepares global plot options
    def __init__(self, args):
        narg=len(args)
        if nargs<2:
            self.usage()
        self.out='plot'
        self.xlabel=None
        self.ylabel=None
        self.xmin=None
        self.xmax=None
        self.ymin=None
        self.ymax=None
        self.key=None
        self.width=8
        self.height=5
        self.kdist=0.1
        self.xlog=0
        self.ylog=0

        keyz=''
        future_plots=[]
        current_args=[]
        keep=0
        has_name=0

        # we iterate through arguments and assign them to global or local options
        for arg in args:
            # Global options
            if arg.startswith('out='):
                self.out=arg[4:]
            elif arg.startswith('xlabel='):
                self.xlabel=arg[7:]
            elif arg.startswith('ylabel='):
                self.ylabel=arg[7:]
            elif arg.startswith('width='):
                self.width=float(arg[6:])
            elif arg.startswith('height='):
                self.height=float(arg[7:])
            elif arg.startswith('xmin='):
                self.xmin=float(arg[5:])
            elif arg.startswith('ymin='):
                self.ymin=float(arg[5:])
            elif arg.startswith('xmax='):
                self.xmax=float(arg[5:])
            elif arg.startswith('ymax='):
                self.ymax=float(arg[5:])
            elif arg.startswith('key='):
                keyz=arg[4:]
            elif arg.startswith('kdist='):
                self.kdist=arg[6:]
            elif arg.startswith('legend=') or arg.startswith('title'):
                self.key=graph.key.key(pos="tl", dist=self.kdist)
            elif arg.startswith('--help'):
                self.usage()
            elif arg.startswith('-xlog'):
                self.xlog=1
            elif arg.startswith('-ylog'):
                self.ylog=1
            # Local / semi-local options
            elif arg.startswith('andif'):
                if has_name==0:
                    raise ValueError('Error : cannot use andif= before the first declared file')
                else:
                    #future_plots.append(Toplot(fname,current_args))
                    current_args.append(__SPLIT_MARK__)
                    current_args.append(arg)

            elif arg.startswith('-keep'):
                keep=1
            elif arg.startswith('-discard'):
                keep=0
            elif arg.startswith('-') or arg.find('=')>=0:
                current_args.append(arg)
            # If it's not an option, it's definitey a filename
            elif arg=='and':
                current_args.append(__SPLIT_MARK__)
            else:
                # If there is already a name for a future plot
                if has_name:
                    future_plots.append(Toplot(fname,current_args))
                    if keep==0:
                        current_args=[]
                else:
                    has_name=1
                fname=arg

        # We still need add the last file to futureèplots
        if has_name:
            future_plots.append(Toplot(fname,current_args))
            has_name=0

        # we check if the plots must be split by and / andif
        for toplot in future_plots:
            [is_split,new_plot]=toplot.check_split()
            if is_split:
                future_plots.append(new_plot)

        # we deal with global plot properties
        if self.xlabel:
            try:
                self.xlabel=r"%s" %(self.xlabel)
            except:
                self.xlabel=None

        if self.ylabel:
            try:
                self.ylabel=r"%s" %(self.ylabel)
            except:
                self.ylabel=None

        try:
            self.key=graph.key.key(pos="%s" %(keyz), dist=float(self.kdist))
        except:
            if keyz=='None':
                self.key=None

        if self.xlog:
            xaxis=axis.log(title=self.xlabel,min=self.xmin,max=self.xmax);
        else:
            xaxis=axis.linear(title=self.xlabel,min=self.xmin,max=self.xmax)
        if self.ylog:
            yaxis=axis.log(title=self.ylabel,min=self.ymin,max=self.ymax)
        else:
            yaxis=axis.linear(title=self.ylabel,min=self.ymin,max=self.ymax)

        self.graph=graph.graphxy(width=self.width,height=self.height,key=self.key,
                x=xaxis,
                y=yaxis )

        # We create the graphs
        self.graphs=[Graph(toplot) for toplot in future_plots]

    def make_plot(self):
        for graf in self.graphs:
            self.plot(graf)

    def plot(self,graf):
        self.graph.plot([graph.data.points([(x,graf.Y[i],graf.dX[i],graf.dY[i],graf.S[i],graf.C[i]) for i, x in enumerate(graf.X[:])], x=1, y=2,dx=3,dy=4,size=5,color=6,title=graf.legend)],graf.style)

    def save_plot(self):
        if self.graphs:
            if self.out.endswith('.eps'):
                self.graph.writeEPSfile(self.out)
            elif self.out.endswith('.svg'):
                self.graph.writeSVGfile(self.out)
            else:
                self.graph.writePDFfile(self.out)


    def usage(self):
        disp('splot is a simple command line plotting tool based on PyX (PyX is awesome !)')
        disp('---------------------------- Warning : you should use PyX for more options')
        disp('Examples :')
        disp('splot.py file.txt')
        disp('splot.py file.txt color=red file2.txt out=plot.pdf')
        disp('splot.py file.txt y=A[:,1]^2+A[:,2]^2 dy=3 color=1')
        quit

class Graph(Glob):
    # Graph is a class containing a single line/set of points and their style, created from class Toplot
    numr=-1
    def __init__(self, toplot):
        args=toplot.args
        self.file=toplot.file_name
        Graph.numr+=1
        self.x=0
        self.y=1
        self.mode='v'
        self.legend="file %s" %Graph.numr
        self.data=[]
        self.dX=[]
        self.dY=[]
        self.S=[]
        self.C=[]
        self.dx=[]
        self.dy=[]
        #self.col=[]
        col=''
        siz=''
        self.cond=[]
        self.range=[]
        (A,a,b)=getdata(self.file)
        labels=splitheader(self.file)

        # Dirty tricks for maximum compatibility
        if min(a,b)==1:
            self.x='auto'
            self.y=0
        if a==1:
            self.mode='h'

        # using local options
        for arg in args:
            if arg.startswith('legend=') or arg.startswith('title='):
                if arg.startswith('legend='):
                    legend=arg[7:]
                else:
                    legend=arg[6:]
                if legend=='None' or legend=='none':
                    self.legend=None
                else:
                    self.legend=r"%s" %legend
            elif arg.startswith('x='):
                self.x=(arg[2:])
            elif arg.startswith('y='):
                self.y=(arg[2:])
            elif arg.startswith('mode='):
                self.mode=arg[5:]
            elif arg.startswith('dx='):
                self.dx=(arg[3:])
            elif arg.startswith('dy='):
                self.dy=(arg[3:])
            elif arg.startswith('if='):
                self.cond=(arg[3:])
            elif arg.startswith('andif='):
                self.cond=(arg[6:])
            elif arg.startswith('range='):
                self.range=(arg[6:])
            elif arg.startswith('color='):
                col=arg[6:]
            elif arg.startswith('size='):
                siz=arg[5:]



        #if (len(self.range) or len(self.cond)):
        if len(self.range):
            A=self.set_A_range(A)

        # We perform a first extraction of X and Y to be able to evalyate conditions on X,Y
        self.X=self.set_from_input(A,self.x,'x')
        self.Y=self.set_from_input(A,self.y,'y')
        self.dX=self.set_from_input(A,self.dx,'dx')
        self.dY=self.set_from_input(A,self.dy,'dy')

        #if (len(self.range) or len(self.cond)):
        if len(self.cond):
            A=self.set_A_condition(A)

        # Now we perfeorm the definitive extraction of X,Y once A has bne filtered
        self.X=self.set_from_input(A,self.x,'x')
        self.Y=self.set_from_input(A,self.y,'y')
        self.dX=self.set_from_input(A,self.dx,'dx')
        self.dY=self.set_from_input(A,self.dy,'dy')

        # Now we assign colors and size if need be
        if siz.isdigit() or siz.find('A[')>=0:
            self.S=self.set_from_input(A,siz,'size')
        if col.isdigit() or col.find('A[')>=0:
            self.C=self.set_from_input(A,col,'color')

        if not len(self.C):
            self.C=self.X
        if not len(self.S):
            self.S=self.X

        # We check size
        lX=len(self.X)
        lY=len(self.Y)
        if lX>lY:
            self.X=self.X[0:lY]
            lX=lY
        elif lY>lX:
            self.Y=self.Y[0:lX]
            lY=lX
        if not len(self.dY):
            self.dY=zeros((lX,1))
        if not len(self.dX):
            self.dX=zeros((lX,1))

        # we scale the color scale
        self.C=(self.C-min(self.C))/(max(self.C)-min(self.C))

        # we make sure no size is non-positive
        if min(self.S)<=0:
            self.S=(self.S-min(self.S))+0.001

        # and now we can make the style !
        self.style=Style(args).style

    def set_from_input(self,A,input,coord):
        # We first check if axis defined by a row/column number
        try :
            i=int(input)
            if self.mode=='h':
                return A[i,:]
            else:
                return A[:,i]
        except:
            if input:
                # Automatic axis value : 1 to length of array
                if input.startswith('aut'):
                    if self.mode=='h':
                        return array(range(len(A[0,:])))
                    else:
                        return array(range(len(A[:,0])))
                # Interpreting axis value
                try:
                    return eval(input)
                except:
                    print('We could note evaluate %s from %s' %(coord,input))
                return []
            else:
                return []

    def set_A_range(self,A):
        # first we need to make data horizontal for the range operation
        if self.mode=='h':
            B=A.transpose()
        else:
            B=A.copy()
        if len(self.range)>0:
            srange=self.range.split(":")
            lr=len(srange)
            try :
                iii=array([int(s) for s in srange])
                if lr==1:
                    B=array([B[iii[0]]])
                elif lr==2:
                    B=B[iii[0]:iii[1]]
                elif lr==3:
                    B=B[iii[0]:iii[2]:iii[1]]
                else:
                    print('Range must be of the format begin:end or begin:range')
                    raise ValueError('Range must be of the format begin:end or begin:step:end')
            except:
                raise ValueError('Cannot convert Range to adequate format (note : range must be of the format begin:end or begin:step:end)')
        if self.mode=='h':
            A=B.transpose()
        else:
            A=B.copy()

        return A


    def set_A_condition(self,A):
        if self.mode=='h':
            B=A.transpose()
        else:
            B=A.copy()

        if len(self.cond)>0:
            X=self.X
            Y=self.Y
            try:
                kept=eval(self.cond)
                if self.mode=='h':
                    B=B[kept]
                    A=B.transpose()
                else:
                    A=A[kept]
            except:
                raise ValueError('Cannot understand condition. Hint use : if=\'A[:,2]>0.5\' ')

        return A

class Style(Graph):
    # A class containing the style to make a graph
    def __init__(self, args):
        count=Graph.numr
        self.style=[]
        self.dxy=[]
        self.goodstyle=goodstyle(args,count)

        for arg in args:
            if arg.startswith('dy=') or arg.startswith('dx='):
                if self.goodstyle.setcolor:
                    self.dxy=[self.goodstyle.linew,self.goodstyle.setcolor]
                else:
                    self.dxy=[self.goodstyle.linew,colours[0]]

        if self.goodstyle.kind=='symbol':
            if not len(self.dxy):
                self.style=[changesymbol(**vars(self.goodstyle)),graph.style.errorbar(False)]
            else:
                self.style=[changesymbol(**vars(self.goodstyle)),graph.style.errorbar(errorbarattrs=self.dxy)]

        elif self.goodstyle.kind=='line':
            if not len(self.dxy):
                self.style=[graph.style.line([self.goodstyle.linest,self.goodstyle.linew,self.goodstyle.setcolor]),graph.style.errorbar(False)]
            else:
                self.style=[graph.style.line([self.goodstyle.linest,self.goodstyle.linew,self.goodstyle.setcolor]),graph.style.errorbar(errorbarattrs=self.dxy)]

class goodstyle(Style):
    # A class containing the style attributes to pass to python PyX
    def __init__(self,args,count):
        self.kind='symbol'
        self.setcolor=colours[int(ceil(count/4)) %4]
        self.symbol=symbols[count %4]
        self.setsize=0.5
        self.linew=style.linewidth.thin
        self.linest=linests[count %4]
        self.gradient=color.gradient.Rainbow;

        for arg in args:
            if arg.startswith('color='):
                col=arg[6:]
                try :
                    # We first try to set it from the dictionary
                    self.setcolor=col_dict[col]
                except :
                    if col.isdigit() or col.find('A[')>=0:
                        # Color should be set from the data
                        self.setcolor=False
                    else:
                        # color might have been passed as a proper color
                        if not col.startswith('color.'):
                            # shorthand notation is tolerated
                            col='color.%s' %(col)
                        try:
                            # trying if color is a defined PyX color
                            self.setcolor=eval(col)
                        except:
                            print('Warning : could not understand color from %s' %col)

            if arg.startswith('gradient=') or arg.startswith('grad='):
                grad=arg.split('=')[1]
                try :
                    # We first try to set it from the dictionary
                    self.gradient=grad_dict[grad]
                except :
                    if not grad.startswith('color.gradient'):
                        # shorthand notation is tolerated
                        if grad.startswith('gradient'):
                            grad='color.%s' %(grad)
                        else:
                            grad='color.gradient.%s' %(grad)
                    try:
                        # trying if color is a defined PyX color
                        self.gradient=eval(grad)
                    except:
                        print('Warning : could not understand gradient from %s' %grad)

            elif arg.startswith('size='):
                siz=arg[5:]
                if siz.find('A[')>=0:
                    # Size depends on data
                    self.setsize=-1
                else:
                    try:
                        sizi=float(siz)
                        if siz.find('.')<0:
                            # size is a data column
                            self.setsize=-1
                        else:
                            # size is a numerical value
                            self.setsize=sizi
                    except:
                        print('Warning : could not understand size from %s' %siz)

            elif arg.startswith('line='):
                self.kind='line'
                lin=arg[5:]
                try:
                    self.linew=linw_dict[lin]
                except:
                    print('Warning : could not understand line width from %s' %lin)

            elif arg.startswith('style='):
                stil=arg[6:]
                try:
                    self.linest=linst_dict[stil]
                    self.kind='line'
                except:
                    try:
                        self.symbol=symst_dict[stil]
                        self.kind='symbol'
                    except:
                        print('Warning : could not understand style from %s' %stil)

        if self.kind=='line':
            # For now splot does not support gradient line coloring
            if not self.setcolor:
                self.setcolor=colours[int(ceil(count/4)) %4]



class changesymbol(graph.style.symbol):
    # A flexible symbol class derived from PyX's very own changesymbol class
    def __init__(self, sizecolumnname="size", colorcolumnname="color",
                       gradient=color.gradient.Rainbow,
                       symbol=graph.style.symbol.triangle,
                       symbolattrs=[deco.filled, deco.stroked],
                       setsize=0.5,kind='symbol',linew=False,linest=False,
                       setcolor=color.gray(0.0),
                       **kwargs):
        # add some configuration parameters and modify some other
        self.sizecolumnname = sizecolumnname
        self.colorcolumnname = colorcolumnname
        self.gradient = gradient
        self.setsize = setsize
        self.setcolor = setcolor
        if self.setcolor:
            symbolattrs=[deco.filled([self.setcolor]), deco.stroked([self.setcolor])]
        graph.style.symbol.__init__(self, symbol=symbol, symbolattrs=symbolattrs, **kwargs)

    def columnnames(self, privatedata, sharedata, agraph, columnnames, dataaxisnames):
        # register the new column names
        if self.sizecolumnname not in columnnames:
            raise ValueError("column '%s' missing" % self.sizecolumnname)
        if self.colorcolumnname not in columnnames:
            raise ValueError("column '%s' missing" % self.colorcolumnname)
        return ([self.sizecolumnname, self.colorcolumnname] +
                graph.style.symbol.columnnames(self, privatedata, sharedata, agraph,
                                               columnnames, dataaxisnames))

    def drawpoint(self, privatedata, sharedata, graph, point):
        # replace the original drawpoint method by a slightly revised one
        if sharedata.vposvalid and privatedata.symbolattrs is not None:
            x_pt, y_pt = graph.vpos_pt(*sharedata.vpos)
            if self.setsize<0:
                siz=privatedata.size_pt*point[self.sizecolumnname]
            else :
                siz=privatedata.size_pt*self.setsize
            if     self.setcolor:
                color= self.setcolor
            else:
                color = self.gradient.getcolor(point[self.colorcolumnname])
            col =privatedata.symbolattrs + [color]
            privatedata.symbol(privatedata.symbolcanvas, x_pt, y_pt, siz, col)


if __name__ == "__main__":
    nargs=len(sys.argv);
    args=sys.argv[1:];

    glob=Glob(args)
    glob.make_plot()
    glob.save_plot()
