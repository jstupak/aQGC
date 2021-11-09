from ROOT import *
from sys import argv

norm=False

inputs=argv[1:]

f0=TFile(inputs[0])
keys=f0.GetListOfKeys()

for k in keys:
    c=TCanvas()
    m=0
    for f in inputs:

        i=inputs.index(f)
        f=TFile(f)
        SetOwnership(f,False)
        o=f.Get(k.GetName())

        if type(o)!=type(TH1F()): continue

        try:
            if norm: o.Scale(1./o.Integral(0,o.GetNbinsX()+2))
        except: continue
        o.SetLineColor(i+1)
        o.SetLineStyle(i+1)
        if i==0:
            first=o
            o.Draw()
        else: o.Draw("SAME")

        m=max(m,o.GetMaximum())
    first.SetMaximum(1.25*m)
    c.Modified()
    c.SaveAs(o.GetName()+'.pdf')
