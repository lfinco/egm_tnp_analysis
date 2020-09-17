from libPython.tnpClassUtils import tnpSample

#github branches
#LegacyReReco2016: https://github.com/swagata87/egm_tnp_analysis/tree/Legacy2016_94XIDv2 
#ReReco2017: https://github.com/swagata87/egm_tnp_analysis/tree/tnp_2017datamc_IDV2_10_2_0
#PromptReco2018: https://github.com/swagata87/egm_tnp_analysis/tree/egm_tnp_Prompt2018_102X_10222018_MC102XECALnoiseFix200kRelVal
#UL2017: https://github.com/swagata87/egm_tnp_analysis/blob/UL2017Final/etc/inputs/tnpSampleDef.py


### my repositories

UL2017 = 'file:/afs/cern.ch/user/l/lfinco/work/Hgg/test/CMSSW_10_6_8/src/flashgg/Validation/test/'
egmUL2017 = '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2017_MINIAOD_Nm1/'

HggUL2017 = {
   
    'data_UL2017_SEED_STD' : tnpSample('data_UL2017_SEED_STD' , UL2017 + 'STD_SEED_17UL_200807/htot_r9eta.root' , lumi = 41.5),
    'data_UL2017_UNS_STD' : tnpSample('data_UL2017_UNS_STD' , UL2017 + 'STD_UNS_17UL_200807/htot_r9eta.root' , lumi = 41.5),
 
    #not used, just there for making the code runnable
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       egmUL2017 + 'DYJetsToEE.root ',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       egmUL2017 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
                                       egmUL2017 + 'DYJetsToLL_amcatnloFXFX.root',
                                       isMC = True, nEvts =  -1 ),

    }

