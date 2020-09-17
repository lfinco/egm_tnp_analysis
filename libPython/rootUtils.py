import ROOT as rt
import math
from fitUtils import *
#from fitSimultaneousUtils import *    
def removeNegativeBins(h):
    for i in xrange(h.GetNbinsX()):
	if (h.GetBinContent(i) < 0):
            h.SetBinContent(i, 0)


def makePassFailHistograms( sample, flag, bindef, var ):
    ## open rootfile
    tree = rt.TChain(sample.tree)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)
    
    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    ## open outputFile
    outfile = rt.TFile(sample.histFile,'recreate')
    hPass = [] 
    hPassRaw = []
    hFail = []
    for ib in range(len(bindef['bins'])):
        hPass.append(rt.TH1D('%s_Pass' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
      
        #same as hPass in case of no prescale weight applied
        hPassRaw.append(rt.TH1D('%s_PassRaw' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hFail.append(rt.TH1D('%s_Fail' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hPass[ib].Sumw2()
        hPassRaw[ib].Sumw2()
        hFail[ib].Sumw2()
    
        cuts = bindef['bins'][ib]['cut']
        if sample.mcTruth :
            cuts = '%s && mcTrue==1' % cuts
        if not sample.cut is None :
            cuts = '%s && %s' % (cuts,sample.cut)

        notflag = '!(%s)' % flag
#        for aVar in bindef['bins'][ib]['vars'].keys():
#            if 'pt' in aVar or 'pT' in aVar or 'et' in aVar or 'eT' in aVar:
#                ## for high pT change the failing spectra to any probe to get statistics
#                if bindef['bins'][ib]['vars'][aVar]['min'] > 89: notflag = '( %s  || !(%s) )' % (flag,flag)

        #if sample.isMC and not sample.weight is None: #line commented to use weights also on data
        
        if not sample.weight is None:
            cutPass = '( %s && %s ) * %s ' % (cuts,    flag, sample.weight)
            cutFail = '( %s && %s ) * %s ' % (cuts, notflag, sample.weight)
            if sample.maxWeight < 999:
                cutPass = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts,    flag, sample.weight,sample.maxWeight,sample.weight)
                cutFail = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts, notflag, sample.weight,sample.maxWeight,sample.weight)
        else:
            cutPass = '( %s && %s )' % (cuts,    flag)
            cutFail = '( %s && %s )' % (cuts, notflag)
        
        tree.Draw('%s >> %s' % (var['name'],hPass[ib].GetName()),cutPass,'goff')
        tree.Draw('%s >> %s' % (var['name'],hPassRaw[ib].GetName()),cutPass,'goff')
        #print  "hRaw name is " , hPassRaw[ib].GetName()
        tree.Draw('%s >> %s' % (var['name'],hFail[ib].GetName()),cutFail,'goff')

        
        removeNegativeBins(hPass[ib])
        removeNegativeBins(hFail[ib])

        hPass[ib].Write(hPass[ib].GetName())
        hPassRaw[ib].Write(hPassRaw[ib].GetName())
        hFail[ib].Write(hFail[ib].GetName())

        bin1 = 1
        bin2 = hPass[ib].GetXaxis().GetNbins()
        epass = rt.Double(-1.0)
        efail = rt.Double(-1.0)
        passI = hPass[ib].IntegralAndError(bin1,bin2,epass)
        failI = hFail[ib].IntegralAndError(bin1,bin2,efail)
        eff   = 0
        e_eff = 0
        if passI > 0 :
            itot  = (passI+failI)
            eff   = passI / (passI+failI)
            e_eff = math.sqrt(passI*passI*efail*efail + failI*failI*epass*epass) / (itot*itot)
        print cuts
        print '    ==> pass: %.1f +/- %.1f ; fail : %.1f +/- %.1f : eff: %1.3f +/- %1.3f' % (passI,epass,failI,efail,eff,e_eff)
    outfile.Close()


def makePassFailHistogramsWhenPrescaling( sample, flag, bindef, var ):
    ## open rootfile
    tree = rt.TChain(sample.tree)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)
    
    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    ## open outputFile
    outfile = rt.TFile(sample.histFile,'recreate')
    hPass = []
    hPassRaw = []
    hFail = []

    for ib in range(len(bindef['bins'])):
        hPass.append(rt.TH1D('%s_Pass' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hPassRaw.append(rt.TH1D('%s_PassRaw' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hFail.append(rt.TH1D('%s_Fail' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        #print "my test: ",'%s_Pass' % bindef['bins'][ib]['name']
        hPass[ib].Sumw2() 
        hPassRaw[ib].Sumw2()
        hFail[ib].Sumw2()
    
        cuts = bindef['bins'][ib]['cut']
        if sample.mcTruth :
            cuts = '%s && mcTrue==1' % cuts
        if not sample.cut is None :
            cuts = '%s && %s' % (cuts,sample.cut)

        notflag = '!(%s)' % flag
#        for aVar in bindef['bins'][ib]['vars'].keys():
#            if 'pt' in aVar or 'pT' in aVar or 'et' in aVar or 'eT' in aVar:
#                ## for high pT change the failing spectra to any probe to get statistics
#                if bindef['bins'][ib]['vars'][aVar]['min'] > 89: notflag = '( %s  || !(%s) )' % (flag,flag)

        ##############################
        #if sample.isMC and not sample.weight is None: #line commented to use weights also on data
        
        if not sample.weight is None:
            cutPassRaw = '( %s && %s ) * %s ' % (cuts,    flag, sample.weight)
            cutFail = '( %s && %s ) * %s ' % (cuts, notflag, sample.weight)
            if sample.maxWeight < 999:
                print "maxWeight is ", sample.maxWeight
                cutPassRaw = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts,    flag, sample.weight,sample.maxWeight,sample.weight)
                cutFail = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts, notflag, sample.weight,sample.maxWeight,sample.weight)
            if not sample.prescale is None:
                cutPass = '( %s && %s ) * %s * %s' % (cuts,    flag, sample.weight,sample.prescale)
                if sample.maxWeight < 999:#never true for us
                    print "maxWeight is ", sample.maxWeight
                    cutPass = '( %s && %s ) * (%s < %f ? %s : 1.0 )* (%s < %f ? %s : 1.0 )' % (cuts,    flag, sample.prescale,sample.maxWeight,sample.prescale,sample.weight,sample.maxWeight,sample.weight)
            else:
                cutPass = '( %s && %s ) * %s' % (cuts,    flag,sample.weight)
        else:      
            cutPassRaw = '( %s && %s )' % (cuts,    flag)
            cutFail = '( %s && %s )' % (cuts, notflag)
            if not sample.prescale is None:
                cutPass = '( %s && %s ) * %s ' % (cuts,    flag, sample.prescale)
                #if sample.maxWeight < 999:
                    #cutPass = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts,    flag, sample.prescale,sample.maxWeight,sample.prescale)
            else:
                cutPass = '( %s && %s )' % (cuts,    flag)


              
        #print "my cuts: "
        #print " cutPassRaw: " ,cutPassRaw
        #print " cutPass: " ,cutPass
        #print " cutFail: ", cutFail

 
        #############################################   

        tree.Draw('%s >> %s' % (var['name'],hPass[ib].GetName()),cutPass,'goff')
        tree.Draw('%s >> %s' % (var['name'],hPassRaw[ib].GetName()),cutPassRaw,'goff')
        tree.Draw('%s >> %s' % (var['name'],hFail[ib].GetName()),cutFail,'goff')
       
        
        removeNegativeBins(hPass[ib]) 
        removeNegativeBins(hPassRaw[ib])
        removeNegativeBins(hFail[ib])

        hPass[ib].Write(hPass[ib].GetName())
        hPassRaw[ib].Write(hPassRaw[ib].GetName())
        hFail[ib].Write(hFail[ib].GetName())

        bin1 = 1
        bin2 = hPass[ib].GetXaxis().GetNbins()
        epass = rt.Double(-1.0) 
        epassraw = rt.Double(-1.0)
        efail = rt.Double(-1.0)
        passI = hPass[ib].IntegralAndError(bin1,bin2,epass)
        passRawI = hPassRaw[ib].IntegralAndError(bin1,bin2,epassraw)
        failI = hFail[ib].IntegralAndError(bin1,bin2,efail)
        eff   = 0
        e_eff = 0
        if passRawI > 0 :
            itot  = (passRawI+failI)
            eff   = passI / (passRawI+failI)
            e_eff = math.sqrt(epass*epass + eff*eff*(epassraw*epassraw+efail*efail))/itot

 
        print cuts
        print '    ==> pass: %.1f +/- %.1f ; fail : %.1f +/- %.1f : eff: %1.3f +/- %1.3f' % (passI,epass,failI,efail,eff,e_eff)
    outfile.Close()

def histPlotter( filename, tnpBin, plotDir ):
    print 'opening ', filename
    print '  get canvas: ' , '%s_Canv' % tnpBin['name']
    rootfile = rt.TFile(filename,"read")

    c = rootfile.Get( '%s_Canv' % tnpBin['name'] )
    c.Print( '%s/%s.png' % (plotDir,tnpBin['name']))


def computeEffi( n1,n2,e1,e2):
    effout = []
    #print n1, n2, n1+n2
  
###FIXME
    #eff   = n1/(n1+n2)
    #le_eff = 1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
    #he_eff =  1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
###FIXME
    if n1+n2 != 0:
        eff   = n1/(n1+n2)
        le_eff = 1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
        he_eff =  1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)

        if(eff == 0.5000):
            eff   = 0
            le_eff = 0
            he_eff =  0
    else: 
        eff   = 0
        le_eff = 0
        he_eff =  0

    #if e_eff < 0.001 : e_eff = 0.001
    if le_eff < 0.001 : le_eff = 0.001
    if he_eff < 0.001 : he_eff = 0.001

    # alpha = (1.0 - .68540158589942957)/2;
    # if(n1 == 0): le = 0
    # else: le = rt.Math.beta_quantile(   alpha, n1,   n2+1 );
    
    # if(n2 == 0): he = 1.0 
    # else: he = rt.Math.beta_quantile( 1-alpha, n1+1, n2  );
    # le_eff = eff - le
    # he_eff = he -eff
    # print eff, le, he
    

    effout.append(eff)
    #effout.append(e_eff)
    effout.append(le_eff)
    effout.append(he_eff)
    
    return effout

def computeEffiWhenPrescaling( n1,n1raw,n2,e1,e1raw,e2):
    effout = []
    #print n1, n2, n1+n2
###FIXME
    if n1+n2 != 0:
        eff   = n1/(n1raw+n2)
        if eff > 1. : eff =1.
        le_eff = abs(1/(n1raw+n2)*math.sqrt(e1*e1+eff*eff*(e1raw*e1raw+e2*e2)))
        he_eff =  abs(1/(n1raw+n2)*math.sqrt(e1*e1+eff*eff*(e1raw*e1raw+e2*e2)))
         
        #if he_eff + eff > 1. : he_eff = 1-eff #to be commented when obtaining final efficiencies (PV efficiency will lower later the measuement, so he_eff + eff will be < 1)
        #if le_eff < 0.001 : le_eff = 0.001
        #if he_eff < 0.001 : he_eff = 0.001

    else: 
        eff   = 0
        le_eff = 0
        he_eff =  0
###FIXME
    # eff   = n1/(n1raw+n2)
    # if eff > 1. : eff =1.
    # le_eff = 1/(n1raw+n2)*math.sqrt(e1*e1+eff*eff*(e1raw*e1raw+e2*e2))
    # he_eff =  1/(n1raw+n2)*math.sqrt(e1*e1+eff*eff*(e1raw*e1raw+e2*e2))
    # if he_eff + eff > 1. : he_eff = 1-eff
    # if le_eff < 0.001 : le_eff = 0.001
    # if he_eff < 0.001 : he_eff = 0.001

    effout.append(eff)
    #effout.append(e_eff)
    effout.append(le_eff)
    effout.append(he_eff)

    return effout


import os.path
def getAllEffi( info, bindef ):
    effis = {}
    if not info['mcNominal'] is None and os.path.isfile(info['mcNominal']):
        rootfile = rt.TFile( info['mcNominal'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['mcNominal'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcNominal'] = [-1,-1]

    if not info['tagSel'] is None and os.path.isfile(info['tagSel']):
        rootfile = rt.TFile( info['tagSel'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['tagSel'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['tagSel'] = [-1,-1]
        
    if not info['mcAlt'] is None and os.path.isfile(info['mcAlt']):
        rootfile = rt.TFile( info['mcAlt'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        bin1 = 1
        bin2 = hP.GetXaxis().GetNbins()
        eP = rt.Double(-1.0)
        eF = rt.Double(-1.0)
        nP = hP.IntegralAndError(bin1,bin2,eP)
        nF = hF.IntegralAndError(bin1,bin2,eF)

        effis['mcAlt'] = computeEffi(nP,nF,eP,eF)
        rootfile.Close()
    else: effis['mcAlt'] = [-1,-1]

    if not info['dataNominal'] is None and os.path.isfile(info['dataNominal']) :
        #rootfile = rt.TFile( info['dataNominal'], 'read' )
        rootfile = rt.TFile( info['dataAltSig'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')
        
        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataNominal'] = computeEffi(nP,nF,eP,eF)
    else:
        effis['dataNominal'] = [-1,-1]
    
    #original way (for fitting):
    if not info['dataAltSig'] is None and os.path.isfile(info['dataAltSig']) :
        rootfile = rt.TFile( info['dataAltSig'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()

        #ePlo = fitresP.floatParsFinal().find('nSigP').getErrorLo()
        #eFlo = fitresF.floatParsFinal().find('nSigF').getErrorLo()
        #ePhi = fitresP.floatParsFinal().find('nSigP').getErrorHi()
        #eFhi = fitresF.floatParsFinal().find('nSigF').getErrorHi()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        #if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        #if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataAltSig'] = computeEffi(nP,nF,eP,eF)

    else:
        effis['dataAltSig'] = [-1,-1]
    
    #for cut and count:
    if not info['dataAltSigCnC'] is None and os.path.isfile(info['dataAltSigCnC']):
        rootfile = rt.TFile( info['data'], 'read' )
        
        hP = rootfile.Get('%s_Pass'%bindef['name'])#hP.Integral() number of passing probe (integral of the distribution minus number of over/underflow events
        hF = rootfile.Get('%s_Fail'%bindef['name'])#hF.Integral() number of failing probe (integral of the distribution minus number of over/underflow events

        #print hP.Integral(),hF.Integral(),  math.sqrt(hP.Integral()), math.sqrt(hF.Integral())
        #nP = hP.Integral()
        #nF = hF.Integral()
        #eP = math.sqrt(hP.Integral())
        #eF = math.sqrt(hF.Integral())
        #rootfile.Close()
        #effis['dataAltSigCnC'] = computeEffi(eP*eP,eF*eF,eP,eF)#cut and count values

        #I guess the previous commands don't contain the error associated to the R9-eta reweighting, so we could do the following, which is giving uncertainties slightly better than the squared root , but I think it is more correct (and there is still the fact that if e<0.001 e=0.001)
        eP = rt.Double(-1)
        eF = rt.Double(-1)
        nbins = hP.GetNbinsX()
        nP = hP.IntegralAndError(0,nbins+1,eP)
        nF = hF.IntegralAndError(0,nbins+1,eF)

        rootfile.Close()

        effis['dataAltSigCnC'] = computeEffi(nP,nF,eP,eF)#cut and count values
      
    else:
        effis['dataAltSigCnC'] = [-1,-1]
    
    
    #cut and count with prescale weight
    if not info['dataAltSigPresCnC'] is None and os.path.isfile(info['dataAltSigPresCnC']) :
        #rootfile = rt.TFile( info['dataAltSigPresCnC'], 'read' )
        #from ROOT import RooFit,RooFitResult
        #fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        #fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])
        hPraw = rootfile.Get('%s_PassRaw'%bindef['name'])
        #hP.Sumw2()
        #hPraw.Sumw2() 
        #hF.Sumw2()
        nbins = hP.GetNbinsX()
        #getprint '%s_Pass'%bindef['name']
        #print hP.Integral(),hF.Integral(),  math.sqrt(hP.Integral()), math.sqrt(hF.Integral())
        #print nP,nF,eP,ePlo, ePhi, eF, eFlo, eFhi
        
        eP = rt.Double(-1)
        ePraw = rt.Double(-1)
        eF = rt.Double(-1)
        nP = hP.IntegralAndError(0,nbins+1,eP)
        nPraw = hPraw.IntegralAndError(0,nbins+1,ePraw)
        nF = hF.IntegralAndError(0,nbins+1,eF)
        #eP = math.sqrt(hP.Integral()) #fixme: this should be larger than the sqrt of number of (weighted) events
        #ePraw = math.sqrt(hPraw.Integral())
        #eF = math.sqrt(hF.Integral())
        #nP = hP.Integral() 
        #nPraw = hPraw.Integral()
        #nF = hF.Integral()
        #print "print errors: ",eP, ePraw, eF
        #print math.sqrt(hP.Integral()),   math.sqrt(hPraw.Integral()),math.sqrt(hF.Integral())  
        #print hP.Integral(),  hPraw.Integral(),hF.Integral()  

        rootfile.Close()

        effis['dataAltSigPresCnC'] = computeEffiWhenPrescaling(nP,nPraw,nF,eP,ePraw,eF)#cut and count values when prescaling
  
    else:
        effis['dataAltSigPresCnC'] = [-1,-1]

    if not info['dataAltBkg'] is None and os.path.isfile(info['dataAltBkg']):
        rootfile = rt.TFile( info['dataAltBkg'], 'read' )
        from ROOT import RooFit,RooFitResult
        fitresP = rootfile.Get( '%s_resP' % bindef['name']  )
        fitresF = rootfile.Get( '%s_resF' % bindef['name'] )

        nP = fitresP.floatParsFinal().find('nSigP').getVal()
        nF = fitresF.floatParsFinal().find('nSigF').getVal()
        eP = fitresP.floatParsFinal().find('nSigP').getError()
        eF = fitresF.floatParsFinal().find('nSigF').getError()
        rootfile.Close()

        rootfile = rt.TFile( info['data'], 'read' )
        hP = rootfile.Get('%s_Pass'%bindef['name'])
        hF = rootfile.Get('%s_Fail'%bindef['name'])

        if eP > math.sqrt(hP.Integral()) : eP = math.sqrt(hP.Integral())
        if eF > math.sqrt(hF.Integral()) : eF = math.sqrt(hF.Integral())
        rootfile.Close()

        effis['dataAltBkg'] = computeEffi(nP,nF,eP,eF)
    else:
        effis['dataAltBkg'] = [-1,-1]
    return effis

def getAddSyst( eff1, eff2, syst1p,syst1m):
    effout = []

    #print eff1, eff2, syst1p,syst1m
    syst_tot_p = math.sqrt(syst1p*syst1p + (eff1-eff2)*(eff1-eff2))
    syst_tot_m = math.sqrt(syst1m*syst1m + (eff1-eff2)*(eff1-eff2))

    #print syst_tot_p, syst_tot_m 
    if (syst1p >  syst_tot_p) or (syst1m >  syst_tot_m):
        print "#######ERROR: final syst less than original error!!!!!!##########"

    
    effout.append(syst_tot_p)
    effout.append(syst_tot_m)
    
    return effout
