# coding: utf-8

"""
Configuration of the CPinHToTauTau analysis.
"""

import law
import order as od

from columnflow.util import maybe_import
#from columnflow.columnar_util import EMPTY_FLOAT, ColumnCollection
#from columnflow.config_util import (
#    get_root_processes_from_campaign, add_shift_aliases, get_shifts_from_sources, add_category,
#    verify_config_processes,
#)

ak = maybe_import("awkward")

#
# the main analysis object
#
analysis_httcp = ana = od.Analysis(
    name="analysis_httcp",
    id=1,
)

# analysis-global versions
# (see cfg.x.versions below for more info)
ana.x.versions = {}

# files of bash sandboxes that might be required by remote tasks
# (used in cf.HTCondorWorkflow)
ana.x.bash_sandboxes = ["$CF_BASE/sandboxes/cf.sh"]
default_sandbox = law.Sandbox.new(law.config.get("analysis", "default_columnar_sandbox"))
if default_sandbox.sandbox_type == "bash" and default_sandbox.name not in ana.x.bash_sandboxes:
    ana.x.bash_sandboxes.append(default_sandbox.name)

# files of cmssw sandboxes that might be required by remote tasks
# (used in cf.HTCondorWorkflow)
ana.x.cmssw_sandboxes = [
    "$CF_BASE/sandboxes/cmssw_default.sh",
]

# config groups for conveniently looping over certain configs
# (used in wrapper_factory)
ana.x.config_groups = {}


#
# setup configs
#
from httcp.config.configs_run2ul_SR import add_config as add_config_run2ul_SR
#from cmsdb.campaigns.run2_2017_nano_local_v10 import campaign_run2_2017_nano_local_v10

# add_config_run2ul_SR(
#     analysis_httcp,
#     campaign_run2_2017_nano_local_v10.copy(),
#     config_name=campaign_run2_2017_nano_local_v10.name,
#     config_id=2,
# )

from httcp.config.run3_preEE import add_run3_preEE
from cmsdb.campaigns.run3_2022_preEE_nano_tau_v12 import campaign_run3_2022_preEE_nano_tau_v12

add_run3_preEE(analysis_httcp,
                  campaign_run3_2022_preEE_nano_tau_v12.copy(),
                  config_name=f"{campaign_run3_2022_preEE_nano_tau_v12.name}",
                  config_id = 22)

add_run3_preEE(analysis_httcp,
                  campaign_run3_2022_preEE_nano_tau_v12.copy(),
                  config_name=f"{campaign_run3_2022_preEE_nano_tau_v12.name}_limited",
                  config_id = 221,
                  limit_dataset_files=1)