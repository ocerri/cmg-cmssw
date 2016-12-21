from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TLorentzVector, TVector3, TVector2, TMath
from copy import deepcopy
from UtilsFunctions import compute_u_projections, particle2TLorenzVector


class RecoilAnalyzer(Analyzer):
    '''
    Loop on PF candidates, skipping muons and storing useful variables.

    First declaring the auxiliar variables for tracks from primary vertex (tk),
    for tracks not from primary vertex (tk_not_pv), for neutral (nt).
    Secondly, loop on the candidates to compute the variables.
    Eventually, store the variables as attributes of the object event.

    TODO: add some kind of isolation?
    '''

    def computeFurtherVariables(self, event):
        # event.leading_particle_p4_tk = event.leading_particles_p4_tk[0]
        # event.leading2_particle_p4_tk = event.leading_particles_p4_tk[1]
        # event.leading12_pt_scalar_sum_tk = event.leading_particles_p4_tk[0].Pt() +\
        #                                    event.leading_particles_p4_tk[1].Pt()
        event.leading12_pt_vector_sum_tk = (event.leading_particles_p4_tk[0] + event.leading_particles_p4_tk[1]).Pt()
        if event.h_sum_pt_nt != 0:
            event.ratio_vec_scalar_tk = event.h_p4_tk.Pt() / event.h_sum_pt_tk
            event.ratio_vec_scalar_2_tk = event.h_p4_tk.Pt()**2 / event.h_sum_pt2_tk
        else:
            event.ratio_vec_scalar_tk = -1
            event.ratio_vec_scalar_2_tk = -1

        # event.leading_particle_p4_tk_not_pv = event.leading_particles_p4_tk_not_pv[0]
        # event.leading2_particle_p4_tk_not_pv = event.leading_particles_p4_tk_not_pv[1]
        # event.leading12_pt_scalar_sum_tk_not_pv = event.leading_particles_p4_tk_not_pv[0].Pt() +\
                                        #    event.leading_particles_p4_tk_not_pv[1].Pt()
        event.leading12_pt_vector_sum_tk_not_pv = (event.leading_particles_p4_tk_not_pv[0] +
                                            event.leading_particles_p4_tk_not_pv[1]).Pt()
        if event.h_sum_pt_tk_not_pv != 0:
            event.ratio_vec_scalar_tk_not_pv = event.h_p4_tk_not_pv.Pt() / event.h_sum_pt_tk_not_pv
            event.ratio_vec_scalar_2_tk_not_pv = event.h_p4_tk_not_pv.Pt()**2 / event.h_sum_pt2_tk_not_pv
        else:
            event.ratio_vec_scalar_tk_not_pv = -1
            event.ratio_vec_scalar_2_tk_not_pv = -1
        # event.leading_particle_p4_nt = event.leading_particles_p4_nt[0]
        # event.leading2_particle_p4_nt = event.leading_particles_p4_nt[1]
        # event.leading12_pt_scalar_sum_nt = event.leading_particles_p4_nt[0].Pt() +\
                                        #    event.leading_particles_p4_nt[1].Pt()
        event.leading12_pt_vector_sum_nt = (event.leading_particles_p4_nt[0] + event.leading_particles_p4_nt[1]).Pt()

        if event.h_sum_pt_nt != 0:
            event.ratio_vec_scalar_nt = event.h_p4_nt.Pt() / event.h_sum_pt_nt
            event.ratio_vec_scalar_2_nt = event.h_p4_nt.Pt()**2 / event.h_sum_pt2_nt
        else:
            event.ratio_vec_scalar_nt = -1
            event.ratio_vec_scalar_2_nt = -1

    def computeUprojectionsWRTmuons(self, event):
        muons = sorted(event.muons, key=lambda x: x.charge(), reverse=True)
        pos_muon = muons[0]
        neg_muon = muons[1]

        event.u_par_pos_tk, event.u_perp_pos_tk = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_tk)
        event.u_par_neg_tk, event.u_perp_neg_tk = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_tk)

        event.u_par_pos_tk_not_pv, event.u_perp_pos_tk_not_pv = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_tk_not_pv)
        event.u_par_neg_tk_not_pv, event.u_perp_neg_tk_not_pv = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_tk_not_pv)

        event.u_par_pos_nt, event.u_perp_pos_nt = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_nt)
        event.u_par_neg_nt, event.u_perp_neg_nt = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_nt)

    def process(self, iEvent, event):

        if self.cfg_comp.isMC:
            # Get the recoil MC information
            # ideal recoil and projection, particle, mean eta and stuff like this
            pass

        h_p4_tk = TLorentzVector(0., 0., 0., 0.)
        h_sum_pt_tk = 0
        h_sum_pt2_tk = 0
        h_eta_mean_tk = 0
        N_part_tk = 0
        leading_particles_p4_tk = [TLorentzVector(0., 0., 0., 0.), TLorentzVector(0., 0., 0., 0.)]

        h_p4_tk_not_pv = TLorentzVector(0., 0., 0., 0.)
        h_sum_pt_tk_not_pv = 0
        h_sum_pt2_tk_not_pv = 0
        h_eta_mean_tk_not_pv = 0
        N_part_tk_not_pv = 0
        leading_particles_p4_tk_not_pv = [TLorentzVector(0., 0., 0., 0.), TLorentzVector(0., 0., 0., 0.)]

        h_p4_nt = TLorentzVector(0., 0., 0., 0.)
        h_sum_pt_nt = 0
        h_sum_pt2_nt = 0
        h_eta_mean_nt = 0
        N_part_nt = 0
        leading_particles_p4_nt = [TLorentzVector(0., 0., 0., 0.), TLorentzVector(0., 0., 0., 0.)]

        for particle in event.pf_candidates:
            p4 = particle2TLorenzVector(particle)
            pt = p4.Pt()
            eta = p4.Eta()
            if abs(particle.pdgId()) == 13:
                if pt == event.muons[0].pt() or pt == event.muons[1].pt():
                    continue

            charge = particle.charge()
            if (charge != 0 and particle.fromPV()):
                h_p4_tk = h_p4_tk + p4
                if pt > leading_particles_p4_tk[0].Pt():
                    leading_particles_p4_tk[1] = deepcopy(leading_particles_p4_tk[0])
                    leading_particles_p4_tk[0] = deepcopy(p4)
                elif pt > leading_particles_p4_tk[1].Pt():
                    leading_particles_p4_tk[1] = deepcopy(p4)
                h_sum_pt_tk += p4.Pt()
                h_sum_pt2_tk += p4.Pt()**2
                h_eta_mean_tk += eta
                N_part_tk += 1
            elif (charge != 0 and not particle.fromPV()):
                h_p4_tk_not_pv += p4
                if pt > leading_particles_p4_tk_not_pv[0].Pt():
                    leading_particles_p4_tk_not_pv[1] = deepcopy(leading_particles_p4_tk_not_pv[0])
                    leading_particles_p4_tk_not_pv[0] = deepcopy(p4)
                elif pt > leading_particles_p4_tk_not_pv[1].Pt():
                    leading_particles_p4_tk_not_pv[1] = deepcopy(p4)
                h_sum_pt_tk_not_pv += p4.Pt()
                h_sum_pt2_tk_not_pv += p4.Pt()**2
                h_eta_mean_tk_not_pv += eta
                N_part_tk_not_pv += 1
            elif charge == 0:
                h_p4_nt += p4
                if pt > leading_particles_p4_nt[0].Pt():
                    leading_particles_p4_nt[1] = deepcopy(leading_particles_p4_nt[0])
                    leading_particles_p4_nt[0] = deepcopy(p4)
                elif pt > leading_particles_p4_nt[1].Pt():
                    leading_particles_p4_nt[1] = deepcopy(p4)
                h_sum_pt_nt += p4.Pt()
                h_sum_pt2_nt += p4.Pt()**2
                h_eta_mean_nt += eta
                N_part_nt += 1

        event.h_p4_tk = h_p4_tk
        event.h_sum_pt_tk = h_sum_pt_tk
        event.h_sum_pt2_tk = h_sum_pt2_tk
        event.h_eta_mean_tk = h_eta_mean_tk
        event.N_part_tk = N_part_tk
        event.leading_particles_p4_tk = leading_particles_p4_tk

        event.h_p4_tk_not_pv = h_p4_tk_not_pv
        event.h_sum_pt_tk_not_pv = h_sum_pt_tk_not_pv
        event.h_sum_pt2_tk_not_pv = h_sum_pt2_tk_not_pv
        event.h_eta_mean_tk_not_pv = h_eta_mean_tk_not_pv
        event.N_part_tk_not_pv = N_part_tk_not_pv
        event.leading_particles_p4_tk_not_pv = leading_particles_p4_tk_not_pv

        event.h_p4_nt = h_p4_nt
        event.h_sum_pt_nt = h_sum_pt_nt
        event.h_sum_pt2_nt = h_sum_pt2_nt
        event.h_eta_mean_nt = h_eta_mean_nt
        event.N_part_nt = N_part_nt
        event.leading_particles_p4_nt = leading_particles_p4_nt

        self.computeFurtherVariables(event)
        self.computeUprojectionsWRTmuons(event)
