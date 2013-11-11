'''
Created on 6 Oct 2013

@author: kreczko
'''
from utils.theta_auto.Model import build_model_from_rootfile


def get_model_from_ROOT_file(root_file, signal_histograms='combined_MET__Higgs_unfolded*'):
    '''
    The root file is assumed to contain histograms of the form
    __sample__
    '''
    model = build_model_from_rootfile(root_file)
    # If the prediction histogram is zero, but data is non-zero, the negative log-likelihood
    # is infinity which causes problems for some methods. Therefore, we set all histogram
    # bin entries to a small, but positive value:
    model.fill_histogram_zerobins()
    # define what the signal processes are. All other processes are assumed to make up the 
    # 'background-only' model.
    model.set_signal_processes(signal_histograms)
    
    # Add some lognormal rate uncertainties. The first parameter is the name of the
    # uncertainty (which will also be the name of the nuisance parameter), the second
    # is the 'effect' as a fraction, the third one is the process name. The fourth parameter
    # is optional and denotes the channl. The default '*' means that the uncertainty applies
    # to all channels in the same way.
    # Note that you can use the same name for a systematic here as for a shape
    # systematic. In this case, the same parameter will be used; shape and rate changes 
    # will be 100% correlated.
#     model.add_lognormal_uncertainty('vjets_rate', 0.50, 'zjets')
#     model.add_lognormal_uncertainty('vjets_rate', 0.50, 'wjets')
    model.add_lognormal_uncertainty('ttbar_rate', 0.15, 'TTJet')
#     model.add_lognormal_uncertainty('ttbar_rate', 0.30, 'singletop')
#     model.add_lognormal_uncertainty('qcd_rate', 1.0, 'qcd')
    
    # the qcd model is from data, so do not apply a lumi uncertainty on that:
    for process in model.processes:
        if process == 'qcd': 
            continue
        model.add_lognormal_uncertainty('lumi', 0.022, process)
        
    # Specifying all uncertainties manually can be error-prone. You can also execute
    # a automatically generated file using python's execfile here
    # which contains these statements, or read in a text file, etc. Remember: this is a
    # python script, so use this power!
#     model.add_lognormal_uncertainty('TTJetsScale', 0.092, 'TTJet', 'combined_MET')
#     model.add_lognormal_uncertainty('TTJetsMatching', 0.061, 'TTJet', 'combined_MET')
#     model.add_lognormal_uncertainty('scale_vjets', -1.33, 'zjets', 'mu_htlep')
#     model.add_lognormal_uncertainty('scale_vjets', -0.537, 'zjets', 'mu_mtt')
#     model.add_lognormal_uncertainty('VJetsMatching', 0.120, 'zjets', 'mu_htlep')
#     model.add_lognormal_uncertainty('VJetsMatching', -0.324, 'zjets', 'mu_mtt')
#     model.add_lognormal_uncertainty('scale_vjets', -0.660, 'wjets', 'mu_htlep')
#     model.add_lognormal_uncertainty('scale_vjets', -0.719, 'wjets', 'mu_mtt')
#     model.add_lognormal_uncertainty('VJetsMatching', 0.333, 'wjets', 'mu_htlep')
#     model.add_lognormal_uncertainty('VJetsMatching', 0.085, 'wjets', 'mu_mtt')
    
    return model
