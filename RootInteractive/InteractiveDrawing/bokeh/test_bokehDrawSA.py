from RootInteractive.InteractiveDrawing.bokeh.bokehDrawSA import *
import RootInteractive.Tools.aliTreePlayer
from ROOT import TFile, TStatToolkit, gSystem, AliTreePlayer
from bokeh.io import curdoc

output_file("test_bokehDrawSA.html")
# import logging

gSystem.Load("$ALICE_ROOT/lib/libSTAT.so")

TFile.SetCacheFileDir("../../data/")
tree = AliTreePlayer.LoadTrees("echo http://rootinteractive.web.cern.ch/RootInteractive/data/tutorial/bokehDraw/treeABCD.root", ".*", ".*ABCD.*", ".*", "", "")
RootInteractive.Tools.aliTreePlayer.AddMetadata(tree, "A.AxisTitle","A (cm)")
RootInteractive.Tools.aliTreePlayer.AddMetadata(tree, "B.AxisTitle","B (cm/s)")
RootInteractive.Tools.aliTreePlayer.AddMetadata(tree, "C.AxisTitle","B (s)")
RootInteractive.Tools.aliTreePlayer.AddMetadata(tree, "D.AxisTitle","D (a.u.)")

df = pd.DataFrame(np.random.random_sample(size=(2000, 6)), columns=list('ABCDEF'))
initMetadata(df)
df.eval("Bool=A>0.5", inplace=True)
df["AA"]=(df.A*10).round(0)/10.
df["CC"]=(df.C*5).round(0)
df["DD"]=(df.D*2).round(0)
df.head(10)
df.meta.metaData = {'A.AxisTitle': "A (cm)", 'B.AxisTitle': "B (cm/s)", 'C.AxisTitle': "C (s)", 'D.AxisTitle': "D (a.u.)", 'Bool.AxisTitle': "A>half", 'E.AxisTitle': "Category"}



figureArray = [
#   ['A'], ['C-A'], {"color": "red", "size": 7, "colorZvar":"C", "filter": "A<0.5"}],
    [['A'], ['C-A'], {"color": "red", "size": 7, "colorZvar":"C"}],
    [['A'], ['C+A', 'C-A']],
    [['B'], ['C+B', 'C-B'],{"color": "red", "size": 7, "colorZvar":"C"}],
    [['D'], ['(A+B+C)*D'], {"size": 10}],
]
widgets="slider.A(0,1,0.05,0,1), slider.B(0,1,0.05,0,1), slider.C(0,1,0.01,0.1,1), slider.D(0,1,0.01,0,1), checkbox.Bool(1), multiselect.E(0,1,2,3,4)"
#widgets="slider.A(0,1,0.05,0,1), slider.B(0,1,0.05,0,1), slider.C(0,1,0.01,0.1,1), slider.D(0,1,0.01,0,1), checkbox.Bool(1), dropdown.E(0,1,2,3,4)"
figureLayout: str = '((0,1,2, plot_height=300),(3, x_visible=1),commonX=1,plot_height=300,plot_width=1200)'
tooltips = [("VarA", "(@A)"), ("VarB", "(@B)"), ("VarC", "(@C)"), ("VarD", "(@D)")]

widgetParams=[
    ['range', ['A']],
    ['range', ['B',0,1,0.1,0,1]],
    ['range', ['C'], {'type':'minmax'}],
    ['range', ['D'], {'type':'sigma', 'bins':10, 'sigma':3}],
    ['range', ['E'], {'type':'sigmaMed', 'bins':10, 'sigma':3}],
    ['slider', ['AA'],{'bins':10}],
    ['multiSelect',["DD"]],
    ['select',["CC",0,1,2,3]],
    #['slider','F', ['@min()','@max()','@med','@min()','@median()+3*#tlm()']], # to be implmneted
]
widgetLayoutDesc=[ [0,1,2], [3,4,5], [6,7], {'sizing_mode':'scale_width'} ]

figureLayoutDesc=[
    [0,1,2, {'commonX':1,'y_visible':2,'plot_height':300}],
    [3,{'plot_height':100}],
    {'plot_height':100,'sizing_mode':'scale_width'}
]

def testOldInterface():
    output_file("test_bokehDrawSAOldInterface.html")
    fig=bokehDrawSA(df, "A>0", "A","A:B:C:D","C",widgets,0,tooltips=tooltips, layout=figureLayout)

def testBokehDrawArraySA():
    output_file("test_bokehDrawSAArray.html")
    fig=bokehDrawSA.fromArray(df, "A>0", figureArray,widgets,tooltips=tooltips, layout=figureLayout)

def testBokehDrawArraySA_tree():
    output_file("test_bokehDrawSAArray_fromTTree.html")
    fig=bokehDrawSA.fromArray(tree, "A>0", figureArray, widgets, tooltips=tooltips, layout=figureLayout)

def testBokehDrawArrayWidget():
    output_file("test_BokehDrawArrayWidget.html")
    xxx=bokehDrawSA.fromArray(df, "A>0", figureArray, widgetParams, layout=figureLayoutDesc, tooltips=tooltips,widgetLayout=widgetLayoutDesc,sizing_mode="scale_width")

def testBokehDrawArrayWidgetNoScale():
    output_file("test_BokehDrawArrayWidgetNoScale.html")
    xxx=bokehDrawSA.fromArray(df, "A>0", figureArray, widgetParams, layout=figureLayoutDesc, tooltips=tooltips,widgetLayout=widgetLayoutDesc,sizing_mode=None)



#testOldInterface()
#testBokehDrawArraySA()
#testOldInterface_tree()
#testBokehDrawArraySA_tree()
#testBokehDrawArrayWidget()
#testBokehDrawArrayWidgetNoScale()
