'''
Created on 6 Oct 2013

@author: phxlk
'''
from model import get_model_from_ROOT_file
from utils.theta_auto.model_summary import model_summary
from utils.theta_auto.bayesian import bayesian_limits
from utils.theta_auto.cls_limits import cls_limits
from utils.theta_auto.misc import chi2_test
from utils.theta_auto import config

model = get_model_from_ROOT_file('../files/test_unfolded.root', 'Higgs_125*')

# first, it is a good idea to generate a summary report to make sure everything has worked
# as expected. The summary will generate quite some information which should it make easy to spot
# errors like typos in the name of uncertainties, missing shape uncertaintie, etc.
model_summary(model)
limit_type = 'expected'

# 2. apply the methods
# 2.a. Bayesian limits
# Calculate expected and observed Bayesian limits. For faster run time of this example,
# only make a few mass points. (Omitting the 'signal_procsses' parameter completely would
# process all signals defined as signal processes before; see Section "Common Parameters"
# on the theta auto intro doxygen page for details)
plot_exp, plot_obs = bayesian_limits(model, what=limit_type, signal_processes = [['Higgs_125']])

# plot_exp and plot_obs are instances of plotutil.plotdata. they contain x/y values and
# bands. You can do many things with these objects such as inspect the x/y/ban
# data, pass then to plotutil.plot routine to make pdf plots, ...
# Here, we will just create text files of the plot data. This is useful if you want
# to apply your own plotting routines or present the result in a text Table.
plot_exp.write_txt('bayesian_limits_expected.txt')
if not limit_type == 'expected':
    plot_obs.write_txt('bayesian_limits_observed.txt')

# 2.b. CLs limits
# calculate cls limit plots. The interface is very similar to bayesian_limits. However, there are a few
# more options such as the definition of the test statistic which is usually a likelihood ratio but can differ in
# which parameters are minimized and which constraints / ranges are applied during minimization.
# Here, we stay with the default which fixes beta_signal=0
# for the background only hypothesis and lets it float freely for the signal+background hypothesis.
# See cls_limits documentation for more options.
# plot_exp, plot_obs = cls_limits(model, what=limit_type, signal_processes = [['Higgs_125']], debug_cls = True, debug = True)
# 
# # as for the bayesian limits: write the result to a text file
# plot_exp.write_txt('cls_limits_expected.txt')
# if not limit_type == 'expected':
#     plot_obs.write_txt('cls_limits_observed.txt')

# 3. compatibility tests:
# make a chi2 test by comparing the chi2 value distribution *after* fitting as obtained from background-only toys with
# a fit performed on data. The "signal_process_group" parameter is usually a list
# of the processes to consider together as the signal (which will be all scaled by beta_signal simultaneously).
# Here, we only include background and just use some arbitrary signal process, set the input beta_signal to zero ("toys:0.0")
# and also fix beta_signal to 0.0 during the fit ("fix:0.0").
p = chi2_test(model, signal_process_group = ['Higgs_125'], input = "toys:0.0", signal_prior = "fix:0.0")
print 'p-value from background-only chi2 test: ', p

# if one wants to include some signal in the comparison, one should make toys accordingly with signal, e.g.,
# with beta_signgl = 0.1 ("toys:0.1"). The signal_prior has a default of "flat" so this will now fit
# also the signal yield for each toy (and data) before computing chi2:
p = chi2_test(model, signal_process_group = ['Higgs_125'], input = "toys:0.12")
print 'p-value from chi2 test, including 0.12pb Higgs at m=125GeV: ', p

# model_summary, bayesian_limits, and cls_limits also write their results to the 'report' object
# which we can ask to write its results as html page to a certain directory. Use an existing, empty
# directory and point your web browser to it.

config.report.write_html('htmlout')

# After running theta-auto, you probably want to delete the 'analysis' directory which
# contains intermediate results. Keeping it avoids re-running theta unnecessarily for unchanged configurations
# (e.g., because you just want to change the plot). However, this directory can grow very large over time.