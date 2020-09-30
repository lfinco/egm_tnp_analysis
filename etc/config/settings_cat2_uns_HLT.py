#############################################################
########## General settings
#############################################################
# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# flag to be Tested
flags = {
   
    'passingHLT_cat0'  : '(passingHLT  == 1)',
    'passingHLT_cat1'  : '(passingHLT  == 1)',
    'passingHLT_cat2'  : '(passingHLT  == 1)',
    'passingHLT_cat3'  : '(passingHLT  == 1)',
  
    }
baseOutDir = 'results/test'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'PhotonToRECO'

samplesDef = {
    'data'   : tnpSamples.HggUL2017['data_UL2017_UNS_STD'].clone(),
     #MC not used:
    'mcNom'  : tnpSamples.HggUL2017['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.HggUL2017['DY_amcatnloext'].clone(),
    'tagSel' : tnpSamples.HggUL2017['DY_madgraph'].clone(),
}
## can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.ICHEP2016['data_2016_runC_ele'] )
#samplesDef['data'].add_sample( tnpSamples.ICHEP2016['data_2016_runD_ele'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph_ele')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 33')

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

#set R9-eta weight
weightName = 'r9etaWeight'
if not samplesDef['data' ] is None: samplesDef['data'].set_weight(weightName)

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
    #BARREL (cat0 and cat2)
    { 'var' : 'ph_sc_abseta' , 'type': 'float', 'bins': [0.0,1.479] },
    #{ 'var' : 'ph_full5x5x_r9' , 'type': 'float', 'bins': [0.48,0.49,0.50,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.60,0.65,0.70,0.75,0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.92,0.94,0.96,0.98,2.]}, 
    { 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,28.,31.,35.,40.,45.,50.,60.,70.,90.,300.] },
 
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 40 && abs(tag_sc_eta) < 2.1 '

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
      
    ###low R9 EB cat2
    0 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    1 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    2 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    3 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    4 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    5 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    6 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    7 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    8 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
    9 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.85',
  
    #turn-on bin cat2
    # 0 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 1 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 2 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 3 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 4 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 5 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 6 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 7 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 8 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',
    # 9 : 'ph_full5x5x_r9 > 0.50 && ph_full5x5x_r9 < 0.56',

    #plateu bin cat2
    # 0 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 1 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 2 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 3 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 4 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 5 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 6 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 7 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 8 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
    # 9 : 'ph_full5x5x_r9 >= 0.56 && ph_full5x5x_r9 < 0.85',
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
]


tnpParAltSigFit = [
  
    #This is the model used.
    #Different bins can have different parameters. Keep track of them, so you can reproduce your results.
    
    #all R9 bin 0 3 4 5 6 8 9,  0 2 3 4 5 6 7 8 9 r9 plateau
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,100.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,100.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    "gmeanF[80, 65, 90]",
    "gsigmaF[8, 1, 10]"
  
    #all r9 bin 7, turn on 0? 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,130.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,130.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]"
 
    #bin 3 4 5 7 8 9 turnon
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,80]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]" 
    

    #bin 6 turnon
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,85.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,85.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]"

    #0 turnon bin 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,120.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,120.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

     #4? turnon bin
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,160.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,160.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0.01, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",
    
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,120.]","betaP[0.05,0.01,0.1]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,120.]","betaF[0.05,0.01,0.1]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,100.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,100.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

   ]
     
tnpParAltSigFit_addGaus = [
    #This is the model used when we add a gaussian more in the signal shape of both tags and probes (only used in bin 0 for seeded leg).
    #Different bins can have different parameters. Keep track of them, so you can reproduce your results.
    # bin 1 2 all R9, bin 1 r9 plateau
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,150.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,150.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    "gmeanF[80, 65, 90]",
    "gsigmaF[8, 1, 10]",
    "gmeanP[80, 65, 90]",
    "gsigmaP[8, 1, 10]",

    #bin 2 turnon
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",
    # "gmeanP[80, 65, 90]",
    # "gsigmaP[8, 1, 10]",

    #bin 1 turnon
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,65.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,65.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",
    # "gmeanP[80, 65, 90]",
    # "gsigmaP[8, 1, 10]",
        
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,160.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,160.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",
    # "gmeanP[80, 65, 90]",
    # "gsigmaP[8, 1, 10]",

]   
   
tnpParAltBkgFit = [

     #This is the model used for getting the syst. unc. due to the choice of the background function.
    # (bin 1 2 turnon/all r9 with addgaus)
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-2.,1.]",
    "alphaF[0.,-2 .,1 .]",
    "gmeanF[80, 65, 90]",
    "gsigmaF[8, 1, 10]", 
    "gmeanP[80, 65, 90]",
    "gsigmaP[8, 1, 10]",
    ]
