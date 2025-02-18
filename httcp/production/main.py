# coding: utf-8

"""
Column production methods related to higher-level features.
"""
import functools

from columnflow.production import Producer, producer
from columnflow.production.categories import category_ids
from columnflow.production.normalization import normalization_weights
from columnflow.production.cms.seeds import deterministic_seeds
from columnflow.production.cms.mc_weight import mc_weight
#from columnflow.production.cms.muon import muon_weights
from columnflow.selection.util import create_collections_from_masks
from columnflow.util import maybe_import
from columnflow.columnar_util import EMPTY_FLOAT, Route, set_ak_column

from httcp.production.mutau_vars import dilepton_mass, mT, rel_charge
from httcp.production.weights import pu_weight, muon_weight, tau_weight
from httcp.production.sample_split import split_dy
from httcp.calibration.tau import tau_energy_scale

np = maybe_import("numpy")
ak = maybe_import("awkward")
coffea = maybe_import("coffea")
maybe_import("coffea.nanoevents.methods.nanoaod")

# helpers
set_ak_column_f32 = functools.partial(set_ak_column, value_type=np.float32)
set_ak_column_i32 = functools.partial(set_ak_column, value_type=np.int32)

@producer(
    uses={
        # nano columns
        "Jet.pt",
    },
    produces={
        # new columns
        "ht", "n_jet",
    },
)
def features(self: Producer, events: ak.Array, **kwargs) -> ak.Array:
    events = set_ak_column(events, "ht", ak.sum(events.Jet.pt, axis=1))
    events = set_ak_column(events, "n_jet", ak.num(events.Jet.pt, axis=1), value_type=np.int32)

    return events



@producer(
    uses={
        # nano columns
        "Electron.pt", "Electron.eta", "Electron.phi", "Electron.mass",
        "Muon.pt", "Muon.eta", "Muon.phi", "Muon.mass",
        "Tau.pt", "Tau.eta", "Tau.phi", "Tau.mass",
    },
    produces={
        # new columns
        "hcand_invm", "hcand_dr",
    },
)
def hcand_features(
        self: Producer, 
        events: ak.Array,
        hcand_pair: ak.Array,
        **kwargs
) -> ak.Array:

    hcand_pair_p4 = ak.firsts(1 * hcand_pair, axis=1)
    hcand1 = hcand_pair_p4[:,0:1]
    hcand2 = hcand_pair_p4[:,1:2]

    mass = (hcand1 + hcand2).mass
    dr = ak.firsts(hcand1.metric_table(hcand2), axis=1)
    
    #from IPython import embed; embed()
    events = set_ak_column_f32(events, "hcand_invm", ak.firsts(mass))
    events = set_ak_column_f32(events, "hcand_dr", ak.firsts(dr))

    return events


@producer(
    uses={
        rel_charge, category_ids, features, normalization_weights , dilepton_mass, mT, pu_weight, muon_weight, tau_weight, split_dy
    },
    produces={
        rel_charge, category_ids, features, normalization_weights, dilepton_mass, mT, pu_weight, muon_weight, tau_weight, split_dy
    },
)
def main(self: Producer, events: ak.Array, **kwargs) -> ak.Array:
    from IPython import embed; embed()
    events = self[rel_charge](events, **kwargs)
    events = self[category_ids](events, **kwargs)
    if self.dataset_inst.is_mc:
        events = self[normalization_weights](events, **kwargs)
        processes = self.dataset_inst.processes.names()
        if ak.any(['dy' in proc for proc in processes]):
            print("Splitting Drell-Yan dataset...")
            events = self[split_dy](events, **kwargs)
        events = self[pu_weight](events, **kwargs)
        events = self[muon_weight](events, **kwargs)
        events = self[tau_weight](events, **kwargs) 
           
    # features
    events = self[dilepton_mass](events, **kwargs)
    events = self[mT](events, **kwargs)
    return events


# @producer(
#     uses={
#         features, category_ids, normalization_weights, deterministic_seeds, #muon_weights,
#     },
#     produces={
#         features, category_ids, normalization_weights, deterministic_seeds, #muon_weights,
#     },
# )
# def main(self: Producer, events: ak.Array, **kwargs) -> ak.Array:
#     #from IPython import embed; embed()
#     #1/0
#     # features
#     events = self[features](events, **kwargs)

#     # category ids
#     events = self[category_ids](events, **kwargs)

#     # deterministic seeds
#     events = self[deterministic_seeds](events, **kwargs)

#     # mc-only weights
#     if self.dataset_inst.is_mc:
#         # normalization weights
#         events = self[normalization_weights](events, **kwargs)

#         # muon weights
#         #events = self[muon_weights](events, **kwargs)
    
#     return events
