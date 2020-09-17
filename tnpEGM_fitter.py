
### python specific import
import argparse
import os
import sys
import pickle
import shutil
import ROOT,copy
from ROOT import std
from array import array
from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TFile, TDirectory
from ROOT import gROOT

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--addGaus'    , action='store_true'  , help = 'add gaussian to alternate signal model failing probe')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('--PresCnC'    , action ='store_true', help ='weight the pass distribution by prescales and perform cut and count instead of fitting')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')
parser.add_argument('--dir'       , default = 'test'       , help ='name of output folder in results/')

args = parser.parse_args()

print '===> settings %s <===' % args.settings
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
print importSetting
exec(importSetting)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot


if args.flag is None:
    print '[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py'
    sys.exit(0)
    
if not args.flag in tnpConf.flags.keys() :
    print '[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag
    print '  --> define in settings first'
    print '  In settings I found flags: '
    print tnpConf.flags.keys()
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print '===>  Output directory: '
print outputDirectory


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print tnpBins['bins'][ib]['name']
        print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( outputDirectory ):
            shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print 'created dir: %s ' % outputDirectory
    print 'bining created successfully... '
    print 'Note than any additional call to createBins will overwrite directory %s' % outputDirectory
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )


if args.createHists:

    import libPython.histUtils as tnpHist

    for sampleType in tnpConf.samplesDef.keys():
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : continue
        if sampleType == args.sample or args.sample == 'all' :
            print 'creating histogram for sample '
            sample.dump()
            var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if sample.mcTruth:
                var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if args.PresCnC:  
                tnpRoot.makePassFailHistogramsWhenPrescaling(sample, tnpConf.flags[args.flag], tnpBins, var )
            else:
                tnpRoot.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )
            #if computing the prescaled path efficiency: 
            #
    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
if sampleToFit is None:
    print '[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings'
    sys.exit(1)

sampleMC = tnpConf.samplesDef['mcNom']

if sampleMC is None:
    print '[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings'
    sys.exit(1)
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'mcRef'     , sampleMC )
    setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altBkgFit' , '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )



### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = tnpConf.samplesDef['mcNom']

if  args.doFit:
    sampleToFit.dump()
    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            if args.altSig and not args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altSig and args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )

    args.doPlot = True
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fileName = sampleToFit.nominalFit
    fitType  = 'nominalFit'
    if args.altSig : 
        fileName = sampleToFit.altSigFit
        fitType  = 'altSigFit'
    if args.altBkg : 
        fileName = sampleToFit.altBkgFit
        fitType  = 'altBkgFit'
        
    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( fileName, tnpBins['bins'][ib], plottingDir )

    print ' ===> Plots saved in <======='
#    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        #'dataNominal' : sampleToFit.nominalFit,
        'dataNominal'        : sampleToFit.histFile,
        'dataAltSig'  : sampleToFit.altSigFit ,
        'dataAltSigCnC'  : sampleToFit.altSigFit ,
        'dataAltSigPresCnC'  : sampleToFit.altSigFit ,
        'dataAltBkg'  : sampleToFit.altBkgFit,
        'mcNominal'   : sampleToFit.mcRef.histFile,
        'mcAlt'       : None,
        'tagSel'      : None
        }

    if not tnpConf.samplesDef['mcAlt' ] is None:
        info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    if not tnpConf.samplesDef['tagSel'] is None:
        info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
    print "cut and count results with presel ignoring for the std efficiencies)"
    #if args.PresCnC:
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            #print astr
            fOut.write( astr + '\n' )
            #astr = '### var2 : %s' % v2Range[1]
            #print astr
            fOut.write( astr + '\n' )
           
        #astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f' % (
        #print effis['dataAltSig' ][0]#,effis['dataAltSig'][1],effis['dataAltSig'][2]
            
        
        astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataAltSigPresCnC' ][0],effis['dataAltSigPresCnC'][1],effis['dataAltSigPresCnC'][2]
            
            )
            
        print astr 


    # for ib in range(len(tnpBins['bins'])):
    #     effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
    #     print "ib ",ib    
    #     ### formatting assuming 2D bining -- to be fixed        
    #     v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
    #     #v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
    #     if ib == 0 :
    #         astr = '### var1 : %s' % v1Range[1]
    #         print astr
    #         fOut.write( astr + '\n' )
    #         #astr = '### var2 : %s' % v2Range[1]
    #         #print astr
    #         fOut.write( astr + '\n' )
           
    #     #astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f' % (
    #     #print effis['dataAltSig' ][0]#,effis['dataAltSig'][1],effis['dataAltSig'][2]
            
        
    #     astr =  '%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
    #         float(v1Range[0]), float(v1Range[2]),
    #         #float(v2Range[0]), float(v2Range[2]),
    #         effis['dataAltSigPresCnC' ][0],effis['dataAltSigPresCnC'][1],effis['dataAltSigPresCnC'][2]
            
    #         )
            
    #     print astr 


        
    print "fit results"
    #else:
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
        
        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            #print astr
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            #print astr
            fOut.write( astr + '\n' )
            
     
        
        # #common use:
       
        astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            
            effis['dataAltSig' ][0],effis['dataAltSig'][1],effis['dataAltSig'][2]
            
        )
        print astr

    if args.altBkg:
     
        print "alternative background fit results"
        #else:
        for ib in range(len(tnpBins['bins'])):
            effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
            
            ### formatting assuming 2D bining -- to be fixed        
            v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
            v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
            if ib == 0 :
                astr = '### var1 : %s' % v1Range[1]
                #print astr
                fOut.write( astr + '\n' )
                astr = '### var2 : %s' % v2Range[1]
                #print astr
                fOut.write( astr + '\n' )
                                
                # #common use:
                
            astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
                float(v1Range[0]), float(v1Range[2]),
                float(v2Range[0]), float(v2Range[2]),
                
                effis['dataAltBkg' ][0],effis['dataAltBkg'][1],effis['dataAltBkg'][2]
                    
            ) 
            print astr
                
        print "final values with additional systematics"
    
        for ib in range(len(tnpBins['bins'])):
            effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
            effis_bkg = tnpRoot.getAddSyst( effis['dataAltSig' ][0], effis['dataAltBkg' ][0],effis['dataAltSig'][1],effis['dataAltSig'][2] )
            
            ### formatting assuming 2D bining -- to be fixed        
            v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
            v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
            if ib == 0 :
                astr = '### var1 : %s' % v1Range[1]
                #print astr
                fOut.write( astr + '\n' )
                astr = '### var2 : %s' % v2Range[1]
                #print astr
                fOut.write( astr + '\n' )
                
            # astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
            #     float(v1Range[0]), float(v1Range[2]),
            #     float(v2Range[0]), float(v2Range[2]),
                
            #     #effis['dataAltSig' ][0], effis_bkg[0], effis_bkg[1]
            #     "values = cms.vdouble(",effis['dataAltSig'][0],"), uncertainties = cms.vdouble(",effis_bkg[0],",",effis_bkg[1],")),"
            # )   
            # print astr

            astr =   '%s%8.10f%s%8.10f%s%8.10f%s' %(
              
                "values = cms.vdouble(",effis['dataAltSig'][0],"), uncertainties = cms.vdouble(",effis_bkg[0],",",effis_bkg[1],")),"
            )   
            print astr

            
        #for the systematic file:
        #astr =  '%s%8.10f%s%8.10f%s%8.10f%s' %(
            #"values = cms.vdouble(",effis['dataAltSig' ][0],"), uncertainties = cms.vdouble(",effis['dataAltSig'][1],",",effis['dataAltSig'][2],")),"
       # ) 
        
       
    
    print "cut and count results"   
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
        
        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        #v3Range = tnpBins['bins'][ib]['title'].split(';')[3].split('<')#used to fill systematics file
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print astr
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print astr
            fOut.write( astr + '\n' )
            
        astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.5f\t%5.5f\t%5.5f' % (
        #astr =  '%+.1f\t%+.1f\t%+.1f\t%+.1f\t%+.1f\t%+.1f\t%s%0.10f%s%0.10f%s%0.10f%s' % (
            #float(v3Range[0]), float(v3Range[2]),
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            
            effis['dataAltSigCnC' ][0],effis['dataAltSigCnC'][1],effis['dataAltSigCnC'][2]           
            #"values = cms.vdouble(", effis['dataAltSigCnC' ][0],"), uncertainties = cms.vdouble(",effis['dataAltSigCnC'][1],",",effis['dataAltSigCnC'][2],"))," 
            
            )
        
        print astr 
        
    


       
        #fOut.write( astr + '\n' )
        #fOut.write( astr_cnc + '\n' )
        #fOut.write( astr_pres_cnc + '\n' )
        #fOut.close()
    
        #print 'Effis saved in file : ',  effFileName

    #effCanvasFile = TFile("efficiency.root")
   
   
  
   
    #c=TCanvas("ph_full5x5x_r9_PLOT","ph_full5x5x_r9_PLOT")
    #c=TCanvas("event_nPV_PLOT","event_nPV_PLOT")
   
    x, xe = array('f'), array('f')
    y, ye_l, ye_h = array('f'), array('f'), array('f')
    y_cnc, ye_cnc_l, ye_cnc_h = array('f'), array('f'), array('f')
    y_pres, ye_pres_l, ye_pres_h = array('f'), array('f'), array('f')
    y_bkg, ye_bkg_l, ye_bkg_h = array('f'), array('f'), array('f')

    #xArray, yArray, yeArray, xeArray = array('f'), array('f'), array('f'), array('f')
    
    
    n = len(tnpBins['bins'])#normal case, with all bins
   # print "print " , n
    for ib in range(n):#normal case, with all bins
    
    #n = len(tnpBins['bins'])-1#in case you want to delete the first bin
    #for ibin in range(n):#in case you want to delete the first bin
        #ib=ibin+1#in case you want to delete the first bin
       
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )
        effis_bkg = tnpRoot.getAddSyst( effis['dataAltSig' ][0], effis['dataAltBkg' ][0],effis['dataAltSig'][1],effis['dataAltSig'][2] )
        vXRange = tnpBins['bins'][ib]['title'].split(';')[2].split('<')

        #if args.PresCnC:
        y_pres.append(effis['dataAltSigPresCnC' ][0])
        ye_pres_l.append(effis['dataAltSigPresCnC'][1])
        ye_pres_h.append(effis['dataAltSigPresCnC'][2])
            
        #else:
        y.append(effis['dataAltSig' ][0])
        ye_l.append(effis['dataAltSig'][1])
        ye_h.append(effis['dataAltSig'][2])
        
        y_cnc.append(effis['dataAltSigCnC' ][0])
        ye_cnc_l.append(effis['dataAltSigCnC'][1])
        ye_cnc_h.append(effis['dataAltSigCnC'][2]) 


        if args.altBkg:
            y_bkg.append(effis['dataAltSig' ][0])
            ye_bkg_l.append(effis_bkg[0])
            ye_bkg_h.append(effis_bkg[1])


        #for pT - Hgg
        #print tnpConf.biningDef[1]['bins']
        #print tnpConf.biningDef[0]['bins']


        #to be commented for egm studies
        if tnpConf.biningDef[1]['bins'][ib+1] == 300:
            x.append(125)
        elif tnpConf.biningDef[1]['bins'][ib+1] == 2:
            x.append(1)
        elif tnpConf.biningDef[1]['bins'][ib+1] == 100:
            x.append(60)

      

        #for n vertices (Hgg)
        #print tnpConf.biningDef[1]['bins']
        #if tnpConf.biningDef[1]['bins'][ib+1] == 140:
            #x.append(80)

        #to be commented for egm studies    
        else:
            x.append(tnpConf.biningDef[1]['bins'][ib+1])
            
        #for egm studies (for Hgg use if, elif and else above)
        #x.append(tnpConf.biningDef[1]['bins'][ib+1])
        xe.append(0.)
  

    #print y[0], y[1],y[2],y[3],y[4],y[5],y[6],y[7],y[8]
    #print ye[0], ye[1],ye[2],ye[3],ye[4],ye[5],ye[6],ye[7],ye[8]
    #print x[0], x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]
    #print tnpBins['bins'][ib]['title']
    #print tnpBins['bins'][ib]['title'].split(';')[2]
    #print tnpBins['bins'][ib]['title'].split(';')[2].split(' < ')[1]
   
    if "cat0" in args.flag:
        cat = "_cat0"
    elif  "cat1" in args.flag:
        cat= "_cat1"
    elif  "cat2" in args.flag:
        cat= "_cat2"
    elif  "cat3" in args.flag:
        cat= "_cat3"
    else:
        cat = ""

    if "passingHLT_" in args.flag:
        effFile = TFile("results/"+args.dir+"/passingHLT"+cat+"/efficiency-data-passingHLT"+cat+".root","RECREATE")
        effDir1 = effFile.mkdir("PhotonToRECO")
        effDir2 = effFile.mkdir("PhotonToRECO/passingHLT/")
        effDir3_fit = effFile.mkdir("PhotonToRECO/passingHLT/fit_eff_plots")
        effDir3_fit.cd("passingHLT/fit_eff_plots")
        
    elif "passingL1_" in args.flag:
        effFile = TFile("results/"+args.dir+"/passingL1"+cat+"/efficiency-data-passingL1"+cat+".root","RECREATE")
        effDir1 = effFile.mkdir("PhotonToRECO")
        effDir2 = effFile.mkdir("PhotonToRECO/passingL1/")
        effDir3_fit = effFile.mkdir("PhotonToRECO/passingL1/fit_eff_plots")
        effDir3_fit.cd("passingL1/fit_eff_plots")
        
    elif "passingHLTl1_" in args.flag:
        effFile = TFile("results/"+args.dir+"/passingHLTl1"+cat+"/efficiency-data-passingHLTl1"+cat+".root","RECREATE")
        effDir1 = effFile.mkdir("PhotonToRECOL1")
        effDir2 = effFile.mkdir("PhotonToRECOL1/passingHLTl1/")
        effDir3_fit = effFile.mkdir("PhotonToRECOL1/passingHLTl1/fit_eff_plots")
        effDir3_fit.cd("passingHLTl1/fit_eff_plots")

    else:
        effFile = TFile("results/"+args.dir+"/passingHLT/efficiency-data-passingHLT.root","RECREATE")
        effDir1 = effFile.mkdir("EGamma")
        effDir2 = effFile.mkdir("EGamma/passingHLT/")
        effDir3_fit = effFile.mkdir("EGamma/passingHLT/fit_eff_plots")
        effDir3_fit.cd("passingHLT/fit_eff_plots")   



    #c=TCanvas("event_nPV_PLOT","event_nPV_PLOT")
    #c = TCanvas("ph_et_PLOT","ph_et_PLOT")
    #c = TCanvas("ph_iso03_PLOT","ph_iso03_PLOT")
    #c = TCanvas("ph_trkiso_PLOT","ph_trkiso_PLOT")
    c = TCanvas("ph_full5x5x_r9","ph_full5x5x_r9")
    #c = TCanvas("ph_sieie","ph_sieie")
    #c = TCanvas("ph_hoe","ph_hoe")
    gEff = TGraphAsymmErrors(n,x,y,xe,xe,ye_l,ye_h)
    gEff.GetYaxis().SetTitle("Efficiency");
    #gEff.SetName("ph_et_PLOT");
    #gEff.GetXaxis().SetTitle("probe electron p_{T}");
    gEff.SetName("ph_full5x5x_r9_PLOT");
    gEff.GetXaxis().SetTitle("probe electron R_{9}");
    #gEff.SetName("ph_sieie_PLOT");
    #gEff.GetXaxis().SetTitle("probe electron #sigma_{i#eta i#eta}");
    #gEff.SetName("ph_hoe_PLOT");
    #gEff.GetXaxis().SetTitle("probe electron H/E");
    #gEff.SetName("event_nPV_PLOT");
    #gEff.GetXaxis().SetTitle("N_{PV}");
    #gEff.SetName("ph_Iso03_PLOT");
    #gEff.GetXaxis().SetTitle("probe Iso_{03}");
    #gEff.SetName("ph_trkiso_PLOT");
    #gEff.GetXaxis().SetTitle("probe Iso_{track}");
    gEff.GetYaxis().SetRangeUser(0,1);
    gEff.SetMarkerStyle(20);
    gEff.Draw("PAE");
    c.Write()
    

    if "passingHLT_" in args.flag:
        effDir3_cnc = effFile.mkdir("PhotonToRECO/passingHLT/cnt_eff_plots") 
        effDir3_cnc.cd("passingHLT/cnt_eff_plots")
        
    elif "passingL1_" in args.flag:
        effDir3_cnc = effFile.mkdir("PhotonToRECO/passingL1/cnt_eff_plots")
        effDir3_cnc.cd("passingL1/cnt_eff_plots")
        
    elif "passingHLTl1_" in args.flag:
        effDir3_cnc = effFile.mkdir("PhotonToRECOL1/passingHLTl1/cnt_eff_plots")
        effDir3_cnc.cd("passingHLTl1/cnt_eff_plots")

    else: 
        effDir3_cnc = effFile.mkdir("EGamma/passingHLT/cnt_eff_plots")
        effDir3_cnc.cd("passingHLT/cnt_eff_plots")


    #c_cnc.cd()
    #c_cnc = TCanvas("ph_et_PLOT","ph_et_PLOT")
    #c_cnc = TCanvas("ph_iso03_PLOT","ph_iso03_PLOT")
    #c_cnc = TCanvas("ph_trkiso_PLOT","ph_trkiso_PLOT")
    c_cnc =TCanvas("ph_full5x5x_r9","ph_full5x5x_r9")
    #c_cnc =TCanvas("ph_sieie","ph_sieie")
    #c_cnc =TCanvas("ph_hoe","ph_hoe")
    #c_cnc =TCanvas("event_nPV_PLOT","event_nPV_PLOT")
    if args.PresCnC:
        gEff_pres = TGraphAsymmErrors(n,x,y_pres,xe,xe,ye_pres_l,ye_pres_h)
        gEff_pres.GetYaxis().SetTitle("Efficiency");
        #gEff_pres.SetName("ph_et_PLOT");
        #gEff_pres.GetXaxis().SetTitle("probe electron p_{T}");
        gEff_pres.SetName("ph_full5x5x_r9_PLOT");
        gEff_pres.GetXaxis().SetTitle("probe electron R_{9}");
        #gEff_pres.SetName("ph_sieie_PLOT");
        #gEff_pres.GetXaxis().SetTitle("probe electron #sigma_{i#eta i#eta}");
        #gEff_pres.SetName("ph_hoe_PLOT");
        #gEff_pres.GetXaxis().SetTitle("probe electron H/E");
        #gEff_pres.SetName("event_nPV_PLOT");
        #gEff.GetXaxis().SetTitle("N_{PV}");
        #gEff_pres.SetName("ph_iso03_PLOT");
        #gEff_pres.GetXaxis().SetTitle("probe Iso_{03}");
        #gEff_pres.SetName("ph_trkiso_PLOT");
        #gEff_pres.GetXaxis().SetTitle("probe Iso_{track}");
        gEff_pres.GetYaxis().SetRangeUser(0,1);
        gEff_pres.SetMarkerStyle(20);
        gEff_pres.Draw("PAE");

    else:
        gEff_cnc = TGraphAsymmErrors(n,x,y_cnc,xe,xe,ye_cnc_l,ye_cnc_h)
        gEff_cnc.GetYaxis().SetTitle("Efficiency");
        #gEff_cnc.SetName("ph_et_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("probe electron p_{T}");
        gEff_cnc.SetName("ph_full5x5x_r9_PLOT"); 
        gEff_cnc.GetXaxis().SetTitle("probe electron R_{9}");
        #gEff_cnc.SetName("ph_sieie_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("probe electron #sigma_{i#eta i#eta}");
        #gEff_cnc.SetName("ph_hoe_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("probe electron H/E");
        #gEff_cnc.SetName("event_nPV_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("N_{PV}");
        #gEff_cnc.SetName("ph_iso03_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("probe Iso_{03}");
        #gEff_cnc.SetName("ph_trkiso_PLOT");
        #gEff_cnc.GetXaxis().SetTitle("probe Iso_{track}");
        gEff_cnc.GetYaxis().SetRangeUser(0,1);
        gEff_cnc.SetMarkerStyle(20);
        gEff_cnc.Draw("PAE");

   
    #gEff.Draw("ph_et_PLOT")
    #c.Update()
    c_cnc.Write()
    
    if args.altBkg:

        if "passingHLT_" in args.flag:
            effDir3_bkg = effFile.mkdir("PhotonToRECO/passingHLT/fit_syst_eff_plots") 
            effDir3_bkg.cd("passingHLT/fit_syst_eff_plots")
        
        elif "passingL1_" in args.flag:
            effDir3_bkg = effFile.mkdir("PhotonToRECO/passingL1/fit_syst_eff_plots")
            effDir3_bkg.cd("passingL1/fit_syst_eff_plots")
            
        elif "passingHLTl1_" in args.flag:
            effDir3_bkg = effFile.mkdir("PhotonToRECOL1/passingHLTl1/fit_syst_eff_plots")
            effDir3_bkg.cd("passingHLTl1/fit_syst_eff_plots")
            
        else: 
            effDir3_bkg = effFile.mkdir("EGamma/passingHLT/fit_syst_eff_plots")
            effDir3_bkg.cd("passingHLT/fit_syst_eff_plots")

        #c_bkg=TCanvas("event_nPV_PLOT","event_nPV_PLOT")
        c_bkg = TCanvas("ph_et_PLOT","ph_et_PLOT")
        #c_bkg = TCanvas("ph_iso03_PLOT","ph_iso03_PLOT")
        #c_bkg = TCanvas("ph_trkiso_PLOT","ph_trkiso_PLOT")
        #c_bkg = TCanvas("ph_full5x5x_r9","ph_full5x5x_r9")
        #c_bkg = TCanvas("ph_sieie","ph_sieie")
        #c_bkg = TCanvas("ph_hoe","ph_hoe")
        gEff_bkg = TGraphAsymmErrors(n,x,y_bkg,xe,xe,ye_bkg_l,ye_bkg_h)
        gEff_bkg.GetYaxis().SetTitle("Efficiency");
        gEff_bkg.SetName("ph_et_PLOT");
        gEff_bkg.GetXaxis().SetTitle("probe electron p_{T}");
        #gEff_bkg.SetName("ph_full5x5x_r9_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("probe electron R_{9}");
        #gEff_bkg.SetName("ph_sieie_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("probe electron #sigma_{i#eta i#eta}");
        #gEff_bkg.SetName("ph_hoe_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("probe electron H/E");
        #gEff_bkg.SetName("event_nPV_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("N_{PV}");
        #gEff_bkg.SetName("ph_Iso03_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("probe Iso_{03}");
        #gEff_bkg.SetName("ph_trkiso_PLOT");
        #gEff_bkg.GetXaxis().SetTitle("probe Iso_{track}");
        gEff_bkg.GetYaxis().SetRangeUser(0,1);
        gEff_bkg.SetMarkerStyle(20);
        gEff_bkg.Draw("PAE");
        c_bkg.Write()
    
    
    print 'Effis saved in file : ',  effFileName
    #import libPython.EGammaID_scaleFactors as egm_sf
    #egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)
