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
    'data'   : tnpSamples.HggUL2017['data_UL2017_SEED_STD'].clone(),
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
   
    #ENDCAP (cat1 and cat3)
    { 'var' : 'ph_sc_abseta' , 'type': 'float', 'bins': [1.566,2.5] },
    
    #{ 'var' : 'ph_sc_et' , 'type': 'float', 'bins': [0., 35.,37., 40., 45., 50., 60., 70., 90., 300.] }, 
    #{ 'var' : 'ph_full5x5x_r9' , 'type': 'float', 'bins': [0.10,0.20,0.30,0.40,0.48,0.49,0.50,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.60,0.65,0.70,0.75,0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.92,0.94,0.96,0.98,2.]},#0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,2.] },
    { 'var' : 'ph_full5x5x_r9' , 'type': 'float', 'bins': [0.50,0.55,0.60,0.65,0.70,0.72,0.74,0.76,0.78,0.80,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.90,0.92,0.94,0.96,0.98,2.]},#0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,2.] },
    #{ 'var' : 'expPU' , 'type': 'float', 'bins': [0.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,100.] }, 
    #{ 'var' : 'event_nPV' , 'type': 'float', 'bins': [0.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,100.] }, 

]
#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 40 && abs(tag_sc_eta) < 2.1'#tag selection

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 

    # ###low R9 EE cat3
    # 0 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 1 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 2 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 3 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 4 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 5 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 6 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 7 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # 8 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    # #9 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    #10 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    ## 11 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',
    ## 12 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.90',


    # ###low R9 EE cat3 - turn-on bin
    # 0 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 1 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 2 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 3 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 4 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 5 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 6 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 7 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 8 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 9 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # 10 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # ## 11 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',
    # ## 12 : 'ph_full5x5x_r9 > 0.80 && ph_full5x5x_r9 < 0.84',

    # ###low R9 EE cat3 R9 plateau bin
    # 0 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 1 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 2 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 3 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 4 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 5 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 6 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 7 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    # 8 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    ##9 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    #10 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    ## 11 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',
    ## 12 : 'ph_full5x5x_r9 >= 0.84 && ph_full5x5x_r9 < 0.90',


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
    "acmsP[80.,50.,100.]","betaP[0.2, 0.,5]","gammaP[0.01, 0, 5]","peakP[90.0]",
    "acmsF[74.,50.,100.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    ]

# tnpParAltSigFit = [
#     "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.4,6.0]","sosF[1,0.5,5.0]",
#     "acmsP[75.,50.,150.]","betaP[0.04,0.01,0.1]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#     "acmsF[74.,50.,100.]","betaF[0.04,0.01,0.1]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#     ]

tnpParAltSigFit = [


    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    #HLT
    #bin 0 1 2 3 4 7 8 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,200.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    
    #bin 5
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,260.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,260.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
   
    #bin 6
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,1,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

  
    
    #L1
   #with reweighing

    #bin 0
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,150.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 1 2   
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,140.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
   
    #bin 3, 4
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,2,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,240.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,220.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

     #bin 5? bin 8? 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,2,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 5?
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,260.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,260.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 6
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[3.0,2.5,4.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[3.0,2.6,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,170.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,110.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",


    #bin 7 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,170.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

############################
    #without reweighing
    #bin 0 1 3  
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,140.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    #bin 2
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,220.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,150.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 4 
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100

    #bin 5
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,2,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    #"acmsP[75.,50.,240.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,220.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100
    
    
    # #bin 6 
    # "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    # "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,2,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    # "acmsP[75.,50.,230.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    # "acmsF[60.,50.,160.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100


    #bin 7 8
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[75.,50.,170.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,200.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",#100


   ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
