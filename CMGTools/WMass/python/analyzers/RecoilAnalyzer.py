from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TLorentzVector, TVector3, TVector2, TMath
from copy import deepcopy
from UtilsFunctions import compute_u_projections, particle2TLorenzVector, deltaR


class RecoilAnalyzer(Analyzer):
    '''
    Loop on PF candidates, skipping muons and storing useful variables.

    First declaring the auxiliar variables for tracks from primary vertex (tk),
    for tracks not from primary vertex (tk_not_pv), for neutral (nt).
    Secondly, loop on the candidates to compute the variables.
    Eventually, store the variables as attributes of the object event.

    TODO: add some kind of isolation?
    '''

    def computeJetVariables(self, event):
        if self.cfg_ana.event_type == "W":
            M_p4 = particle2TLorenzVector(event.muon_W)
            event.total_jet_p4 = TLorentzVector(0, 0, 0, 0)
            for jet in event.jets_pf_chs:
                jet_p4 = particle2TLorenzVector(jet)
                if deltaR(p41=jet_p4, p42=M_p4) < 0.4:
                    event.jets_pf_chs.remove(jet)
                else:
                    event.total_jet_p4 += particle2TLorenzVector(jet)

            if len(event.jets_pf_chs) > 0:
                jet_p4 = particle2TLorenzVector(event.jets_pf_chs[0])
                event.jet_p4 = jet_p4
                event.u_par_jet, event.u_perp_jet = compute_u_projections(p4Ref=M_p4, p42=event.jet_p4)
                event.u_par_total_jet, event.u_perp_total_jet = compute_u_projections(p4Ref=M_p4, p42=event.total_jet_p4)
            else:
                event.u_par_jet, event.u_perp_jet = (0, 0)
                event.u_par_total_jet = 0
                event.u_perp_total_jet = 0
                event.jet_p4 = TLorentzVector(0, 0, 0, 0)
                event.total_jet_p4 = TLorentzVector(0, 0, 0, 0)

    def computeFurtherVariables(self, event):
        event.leading12_pt_vector_sum_tk = (event.leading_particles_p4_tk[0] + event.leading_particles_p4_tk[1]).Pt()
        event.leading12_pt_scalar_sum_tk = event.leading_particles_p4_tk[0].Pt() + event.leading_particles_p4_tk[1].Pt()
        if event.h_sum_pt_tk != 0:
            event.ratio_vec_scalar_tk = event.h_p4_tk.Pt() / event.h_sum_pt_tk
            event.ratio_vec_scalar_2_tk = event.h_p4_tk.Pt()**2 / event.h_sum_pt2_tk
        else:
            event.ratio_vec_scalar_tk = -1
            event.ratio_vec_scalar_2_tk = -1


        event.leading12_pt_vector_sum_tk_not_pv = (event.leading_particles_p4_tk_not_pv[0] + event.leading_particles_p4_tk_not_pv[1]).Pt()
        event.leading12_pt_scalar_sum_tk_not_pv = event.leading_particles_p4_tk_not_pv[0].Pt() + event.leading_particles_p4_tk_not_pv[1].Pt()
        if event.h_sum_pt_tk_not_pv != 0:
            event.ratio_vec_scalar_tk_not_pv = event.h_p4_tk_not_pv.Pt() / event.h_sum_pt_tk_not_pv
            event.ratio_vec_scalar_2_tk_not_pv = event.h_p4_tk_not_pv.Pt()**2 / event.h_sum_pt2_tk_not_pv
        else:
            event.ratio_vec_scalar_tk_not_pv = -1
            event.ratio_vec_scalar_2_tk_not_pv = -1


        event.leading12_pt_vector_sum_nt = (event.leading_particles_p4_nt[0] + event.leading_particles_p4_nt[1]).Pt()
        event.leading12_pt_scalar_sum_nt = event.leading_particles_p4_nt[0].Pt() + event.leading_particles_p4_nt[1].Pt()

        if event.h_sum_pt_nt != 0:
            event.ratio_vec_scalar_nt = event.h_p4_nt.Pt() / event.h_sum_pt_nt
            event.ratio_vec_scalar_2_nt = event.h_p4_nt.Pt()**2 / event.h_sum_pt2_nt
        else:
            event.ratio_vec_scalar_nt = -1
            event.ratio_vec_scalar_2_nt = -1

    def computeUprojectionsWRTmuons(self, event):
        if self.cfg_ana.event_type == "W":
            M_p4 = particle2TLorenzVector(event.muon_W)

            event.u_par_tk, event.u_perp_tk = compute_u_projections(p4Ref=M_p4, p42=event.h_p4_tk)
            event.u_par_tk_not_pv, event.u_perp_tk_not_pv = compute_u_projections(p4Ref=M_p4, p42=event.h_p4_tk_not_pv)
            event.u_par_nt, event.u_perp_nt = compute_u_projections(p4Ref=M_p4, p42=event.h_p4_nt)

            if self.cfg_comp.isMC:
                Mgen_p4 = particle2TLorenzVector(event.muon_gen_HS)
                Wgen_p4 = -particle2TLorenzVector(event.Wgen)

                event.u_par_MC, event.u_perp_MC = compute_u_projections(p4Ref=Mgen_p4, p42=Wgen_p4)

        if self.cfg_ana.event_type == "Z":
            muons = sorted(event.muons, key=lambda x: x.charge(), reverse=True)
            pos_muon = muons[0]
            neg_muon = muons[1]

            event.u_par_pos_tk, event.u_perp_pos_tk = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_tk)
            event.u_par_neg_tk, event.u_perp_neg_tk = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_tk)

            event.u_par_pos_tk_not_pv, event.u_perp_pos_tk_not_pv = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_tk_not_pv)
            event.u_par_neg_tk_not_pv, event.u_perp_neg_tk_not_pv = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_tk_not_pv)

            event.u_par_pos_nt, event.u_perp_pos_nt = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=event.h_p4_nt)
            event.u_par_neg_nt, event.u_perp_neg_nt = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=event.h_p4_nt)

            event.u_par_pos_Z, event.u_perp_pos_Z = compute_u_projections(p4Ref=particle2TLorenzVector(pos_muon), p42=-event.Zreco_p4)
            event.u_par_neg_Z, event.u_perp_neg_Z = compute_u_projections(p4Ref=particle2TLorenzVector(neg_muon), p42=-event.Zreco_p4)

    def process(self, iEvent, event):

        if self.cfg_comp.isMC:
            # Get the recoil MC information
            # ideal recoil and projection, particle, mean eta and stuff like this
            sumPt_genp = TLorentzVector(0., 0., 0., 0.)
            for part in event.gen_particles:
                if part.status()==1:
                    sumPt_genp += particle2TLorenzVector(part)

            # print "sumPt status 1 = ", sumPt_genp.Pt()
            event.SumStatus1_p4 = sumPt_genp

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
            dz = particle.vz() - event.goodVertices[0].z()
            dx = particle.vx() - event.goodVertices[0].x()
            dy = particle.vy() - event.goodVertices[0].y()
            is_fromPV = ((dx**2 + dy**2)/0.03**2) + (dz/0.05)**2 < 1
            # is_fromPV = abs(particle.vz() - event.goodVertices[0].z()) < self.cfg_ana.tracks_max_dz
            if abs(particle.pdgId()) == 13:
                if hasattr(event,"muon_W"):
                    if particle.pdgId() == event.muon_W.pdgId() and 0.9*event.muon_W.pt() < pt < 1.1*event.muon_W.pt():
                        continue
                elif hasattr(event, "muons"):
                    if particle.pdgId() == event.muons[0].pdgId() and 0.9*event.muons[0].pt() < pt < 1.1*event.muons[0].pt():
                        continue
                    if particle.pdgId() == event.muons[1].pdgId() and 0.9*event.muons[1].pt() < pt < 1.1*event.muons[1].pt():
                        continue

            charge = particle.charge()
            if (charge != 0 and is_fromPV):
                h_p4_tk = h_p4_tk + p4
                if pt > leading_particles_p4_tk[0].Pt():
                    leading_particles_p4_tk[1] = deepcopy(leading_particles_p4_tk[0])
                    leading_particles_p4_tk[0] = deepcopy(p4)
                elif pt > leading_particles_p4_tk[1].Pt():
                    leading_particles_p4_tk[1] = deepcopy(p4)
                h_sum_pt_tk += p4.Pt()
                h_sum_pt2_tk += p4.Pt()*p4.Pt()
                h_eta_mean_tk += eta
                N_part_tk += 1
            elif (charge != 0 and not is_fromPV):
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
        if N_part_tk == 0: N_part_tk = 1
        event.h_eta_mean_tk = h_eta_mean_tk/N_part_tk
        event.N_part_tk = N_part_tk
        event.leading_particles_p4_tk = leading_particles_p4_tk
        event.m_inv_tk = h_p4_tk.M()

        event.h_p4_tk_not_pv = h_p4_tk_not_pv
        event.h_sum_pt_tk_not_pv = h_sum_pt_tk_not_pv
        event.h_sum_pt2_tk_not_pv = h_sum_pt2_tk_not_pv
        if N_part_tk_not_pv == 0: N_part_tk_not_pv = 1
        event.h_eta_mean_tk_not_pv = h_eta_mean_tk_not_pv/N_part_tk_not_pv
        event.N_part_tk_not_pv = N_part_tk_not_pv
        event.leading_particles_p4_tk_not_pv = leading_particles_p4_tk_not_pv
        event.m_inv_tk_not_pv = h_p4_tk_not_pv.M()

        event.h_p4_nt = h_p4_nt
        event.h_sum_pt_nt = h_sum_pt_nt
        event.h_sum_pt2_nt = h_sum_pt2_nt
        if N_part_nt == 0: N_part_nt = 1
        event.h_eta_mean_nt = h_eta_mean_nt/N_part_nt
        event.N_part_nt = N_part_nt
        event.leading_particles_p4_nt = leading_particles_p4_nt
        event.m_inv_nt = h_p4_nt.M()

        self.computeFurtherVariables(event)
        self.computeUprojectionsWRTmuons(event)
        self.computeJetVariables(event)
