#############################################################
########## General settings
#############################################################
# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

# flag to be Tested
flags = {
    'passingVeto'   : '(passingVeto   == 1)',
    'passingLoose'  : '(passingLoose  == 1)',
    'passingMedium' : '(passingMedium == 1)',
    'passingTight'  : '(passingTight  == 1)',
    'passingMVA80'  : cutpass80,
    'passingMVA90'  : cutpass90,
    'passingHLT_cat0'  : '(passingHLT  == 1)',
    'passingHLT_cat1'  : '(passingHLT  == 1)',
    'passingHLT_cat2'  : '(passingHLT  == 1)',
    'passingHLT_cat3'  : '(passingHLT  == 1)',
    'passingL1_cat0'  : '(passingL1  == 1)',
    'passingL1_cat1'  : '(passingL1  == 1)',
    'passingL1_cat2'  : '(passingL1  == 1)',
    'passingL1_cat3'  : '(passingL1  == 1)',  
    'passingHLTl1_cat0'  : '(passingHLTl1  == 1)',
    'passingHLTl1_cat1'  : '(passingHLTl1  == 1)',

    'passingHLTl1_cat2'  : '(passingHLTl1  == 1)',
    'passingHLTl1_cat3'  : '(passingHLTl1  == 1)',

    }
baseOutDir = 'results/test'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'PhotonToRECO'#PhotonToRECO(L1)

samplesDef = {
    #'data'   : tnpSamples.SingleElectron_RunIIFall17_3_0_01['data_2017_seeded_STD_m11_min14_B'].clone(),
    #'data'   : tnpSamples.EGamma_Era2018_RR_17Sep2018_v1['data_2018_seeded_STD'].clone(),
    #'data'   : tnpSamples.Legacy16_SingleEle['data_2016_unseeded_STD_ReReco'].clone(),
    'data'   : tnpSamples.EGamma_Era2018_RR_17Sep2018_v2['data_2018_unseeded_LM'].clone(),
    #'data'   : tnpSamples.EGamma_Era2018_RR_17Sep2018_v2['DY_2018_unseeded_LM'].clone(),
    #'data'   : tnpSamples.SingleElectron_RunIIFall17['data_2017_B-F_seeded_STD'].clone(),
    'mcNom'  : tnpSamples.ICHEP2016['mc_DY_madgraph_ele'].clone(),
    'mcAlt'  : tnpSamples.ICHEP2016['mc_DY_amcatnlo_ele'].clone(),
    'tagSel' : tnpSamples.ICHEP2016['mc_DY_madgraph_ele'].clone(),
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
    #{ 'var' : 'phsc_abseta' , 'type': 'float', 'bins': [0.0,1.479] },
    #{ 'var' : 'ph_full5x5x_r9' , 'type': 'float', 'bins': [0.50,0.55,0.60,0.65,0.70,0.72,0.74,0.76,0.78,0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.92,0.94,0.96,0.98,2.]},#0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,2.] },

    #ENDCAP (cat1 and cat3)
    { 'var' : 'phsc_abseta' , 'type': 'float', 'bins': [1.566,2.5] },
    #{ 'var' : 'ph_full5x5x_r9' , 'type': 'float', 'bins': [0.80,0.82,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.] },

    #seeded leg
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0., 33.333, 35., 40., 45., 50., 60., 70., 90., 300.] }, 
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0., 35.,37., 40., 45., 50., 60., 70., 90., 300.] }, 
    #{ 'var' : 'expPU' , 'type': 'float', 'bins': [0.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,100.] }, 

    #unseeded leg
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,22.5,25.,27.5,30.,32.5,35.,40.,45.,50.,60.,70.,90.,300.] },#legacy 2016
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,28.,31.,35.,40.,45.,50.,60.,70.,90.,300.] },#2017 2018
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,25.,27.5,31.,33.3333,37.,40.,45.,50.,60.,70.,90.,300.] },
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,25.,27.5,30.,33.3333,35.,40.,45.,50.,60.,70.,90.,300.] },
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,22.5,25.,27.5,30.,33.3333,35.,40.,45.,50.,60.,70.,90.,300.] },
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,25.,28.,31.,35.,40.,45.,50.,60.,70.,90.,300.] },
    { 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0.,25.,28.,31.,35.,40.,45.,50.,60.,70.,90.,300.] },#low mass 2018
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 40 && abs(tag_sc_eta) < 2.1 && run > 315973'#these cuts are already applied in the tree, maybe it would be better tu cut at 35 GeV since we are using Ele35

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
       
    
    #high R9 EE cat1
    # 0 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 1 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 2 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 3 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 4 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 5 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 6 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 7 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 8 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 9 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # 10 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # #11 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',
    # #12 : 'ph_full5x5x_r9 > 0.90',# && ph_full5x5x_r9 < 1.0',

    0 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    1 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    2 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    3 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    4 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    5 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    6 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    7 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    8 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    9 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    10 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    #11 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',
    #12 : 'ph_full5x5x_r9 > 0.90 && ph_full5x5x_r9 < 0.93',

    # 0 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 1 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 2 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 3 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 4 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 5 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 6 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 7 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 8 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 9 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # 10 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # # #11 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
    # # #12 : 'ph_full5x5x_r9 > 0.93',# && ph_full5x5x_r9 < 1.0',
   
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1.87,0.00,10.000]",#"sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[15.,0.00,30.000]",#,"sigmaF[0.5,0.1,5.0]",
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[80.,50.,90.]","betaP[0.2, 0.,5]","gammaP[0.01, 0, 5]","peakP[90.0]",
    "acmsF[74.,50.,90.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    ]

# tnpParAltSigFit = [
#     "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.4,6.0]","sosF[1,0.5,5.0]",
#     "acmsP[75.,50.,150.]","betaP[0.04,0.01,0.1]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#     "acmsF[74.,50.,100.]","betaF[0.04,0.01,0.1]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#     ]

tnpParAltSigFit = [

    #bins  4,5,6,9,10 (full R9) 3? 5 6 8 (plateau)
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,110.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,90.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    #bins 0  (full R9), 0  (plateau)
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,150.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,100]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    
    #bin 9 (full R9) 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,210.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,130]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    #bin 8 (full R9) 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,120.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,130]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    
    #bin 10 (full R9)
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,250.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,200]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",


    #bin 1 7 (full R9), 2 5 6 7 8 9 10(plateau) 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,140.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,105.]","betaF[0.05,0.01,0.05]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",

    #bin 1 (plateau and turn-on)
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,140.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,105.]","betaF[0.05,0.01,0.04]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[5, 3, 8]",

    #bin 4 3 (plateau), 0,2,3,4,5,6,7,8,9,10 (turn-on) 2 3 8?(full r9)
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    "gmeanF[80, 65, 90]",
    "gsigmaF[8, 1, 10]",


   
    
    #==================================
    #    STD
    #some parameters could have been changed while testing LM
    # "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    # "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    # "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    # "gmeanF[80, 65, 90]",
    # "gsigmaF[8, 1, 10]",
    
    #HLT - 2018 - oly bin0
    #"meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    #"acmsP[60.,40.,100.]","betaP[0.05,0.01,0.1]","gammaP[0.1, 0, 1]","peakP[90.0]",
    #"acmsF[60.,40.,100.]","betaF[0.05,0.01,0.1]","gammaF[0.1, 0, 1]","peakF[90.0]",

    #==========================

    #HLT 2016
   #HLT
   #WITH REWEIGHTING
    #bin 0 1 3 4  
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    
    #bin 2 5
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,140.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 7
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,80.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 6 8
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    




#WITHOUT R9-ETA REWEIGHING
    #bin 0 1 4 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    
    #bin 2 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,140.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 5
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 6
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 7
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,80.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 8
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,240.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,90.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #L1

    #with reweighting
  
    #bin 0 2 3 4 5
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    
    #bin 1 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,80.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 6
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,0.9,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,150.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,100]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",

    #bin 7
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[5.,4.,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    
    #bin 8
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[0,-5,4.]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[5.,4.,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,90]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    


##########################

    #without reweighing
    #bin 1 2 5 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,140.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 0 4
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 3
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 6 7
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,2,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100


    #bin 8
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,170.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
   ]
     


tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    "gmeanF[80, 65, 90]",
    "gsigmaF[8, 1, 10]",
    ]
