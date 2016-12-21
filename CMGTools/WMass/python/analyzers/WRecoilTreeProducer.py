from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ntupleFunctions import *

class RecoilTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(RecoilTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        aux_tree = self.tree

        tree_variables = [
            ("evt_number", "l"),
            ("muon_pt", float),
            ("muon_pz", float),
            ("muon_eta", float),
            ("muon_charge", float),

            ("nu_pt", float),
            ("nu_eta", float),
            ("h", float),
            ("h_nt",float),
            ("h_tk", float),
            # ("met", float),
            # ("w_pt", float),
            # ("w_pl", float),
            # ("w_cos_theta", float),
            # ("w_eta", float),
            # ("w_rapidity", float),
            # ("m_W", float),
            # ("mt_munu", float),
            # ("mt_munu_ptW0", float),
            # ("mt2_muon", float),
            # ("mt2_recoil", float),
            # ("mt2_recoil_1o", float),
            # ("mt2_recoiltk", float),
            # ("mt2_recoiltk_1o", float),
            # ("mt2_munu", float),
            # ("R", float),
            # ("T", float),
            # ("RplusT", float),

            ("u_par", float),
            ("u_perp", float),
            # ("hpt", float),
            ("u_lpar", float),
            ("u_lperp", float),
            ("recoil_pl", float),
            ("recoil_m", float),
            ("recoil_eta_mean", float),
            ("recoil_eta_sum", float),
            ("recoil_sum_et", float),
            ("recoil_sum_et2", float),
            ("leading_pt", float),
            ("leading12_pt_scalar_sum", float),
            ("leading12_pt_vector_sum", float),
            ("leading_eta", float),

            ("n_charged", int),
            ("u_par_tk", float),
            ("u_perp_tk", float),
            # ("hpt_tk", float),
            ("u_lpar_tk", float),
            ("u_lperp_tk", float),
            ("recoil_pl_tk", float),
            ("recoil_m_tk", float),
            ("recoil_eta_mean_tk", float),
            ("recoil_eta_sum_tk", float),
            ("recoil_sum_et_tk", float),
            ("recoil_sum_et2_tk", float),
            ("leading_pt_tk", float),
            ("leading12_pt_scalar_sum_tk", float),
            ("leading12_pt_vector_sum_tk", float),
            ("leading_eta_tk", float),


            ("n_neutral", int),
            ("u_par_nt", float),
            ("u_perp_nt", float),
            # ("hpt_nt", float),
            ("u_lpar_nt", float),
            ("u_lperp_nt", float),
            ("recoil_pl_nt", float),
            ("recoil_m_nt", float),
            ("recoil_eta_mean_nt", float),
            ("recoil_eta_sum_nt", float),
            ("recoil_sum_et_nt", float),
            ("recoil_sum_et2_nt", float),
            ("leading_pt_nt", float),
            ("leading12_pt_scalar_sum_nt", float),
            ("leading12_pt_vector_sum_nt", float),
            ("leading_eta_nt", float),

            ("c1_tk", float),
            ("c2_tk", float),
            ("d1_tk", float),
            ("d2_tk", float),
            ("e1_tk", float),
            ("e2_tk", float),
            ("c1_mu_tk", float),
            ("c2_mu_tk", float),

        ]

        for variable_name, variable_type in tree_variables:
            var(aux_tree, variable_name, variable_type)

    def process(self, iEvent, event):

        aux_tree = self.tree
        aux_tree.reset()

        fill(aux_tree, "evt_number", iEvent)

        fill(aux_tree, "muon_pt", event.muons[0].pt())
        fill(aux_tree, "muon_pz", event.muons[0].p4().Pz())
        fill(aux_tree, "muon_eta", event.muons[0].eta())
        fill(aux_tree, "muon_charge", event.muons[0].charge())
        fill(aux_tree, "h_pt_tk", event.recoil_p4_tk.Pt())

        aux_tree.tree.Fill()
