from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ROOT import TLorentzVector
from ntupleFunctions import *
from math import sqrt, log
from copy import deepcopy
from UtilsFunctions import *
import numpy as np

class AllParticleTree(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(AllParticleTree, self).__init__(cfg_ana, cfg_comp, looperName)

    def computeFurtherVariables(self, event):
        if event.h_sum_pt_tk != 0:
            event.ratio_vec_scalar_tk = event.h_p4_tk.Pt() / event.h_sum_pt_tk
        else:
            event.ratio_vec_scalar_tk = -1


        if event.h_sum_pt_nt != 0:
            event.ratio_vec_scalar_nt = event.h_p4_nt.Pt() / event.h_sum_pt_nt
        else:
            event.ratio_vec_scalar_nt = -1

    def computeUprojectionsWRTmuons(self, event):
        M_p4 = particle2TLorenzVector(event.muon_W)

        event.u_par_tk, event.u_perp_tk = compute_u_projections(p4Ref=M_p4, p42=event.h_p4_tk)
        event.u_par_nt, event.u_perp_nt = compute_u_projections(p4Ref=M_p4, p42=event.h_p4_nt)

        if self.cfg_comp.isMC:
            Mgen_p4 = particle2TLorenzVector(event.muon_gen_HS)
            Wgen_p4 = -particle2TLorenzVector(event.Wgen)

            event.u_par_MC, event.u_perp_MC = compute_u_projections(p4Ref=Mgen_p4, p42=Wgen_p4)

    def declareVariables(self):
        # p4, pdgid, n_vertici, delta Z, is from PV

        T = self.tree

        var(T, "n_evt", int)
        var(T, "n_vtx", int)
        var(T, "n_pile_up", int)
        if self.cfg_comp.isMC:
            bookVB(T, "Wgen", lite =1)
            bookUparUperp(T,"MC")


        bookMuonZ(T, "muon", lite =1)

        bookRecoilInfo(T, "tk", lite =1)
        bookUparUperp(T,"tk")

        bookRecoilInfo(T, "nt", lite =1)
        bookUparUperp(T,"nt")


        var(T, "N_tk", int)
        T.vector("ptk_pt","N_tk", maxlen=100)
        T.vector("ptk_phi","N_tk", maxlen=100)
        T.vector("ptk_eta","N_tk", maxlen=100)
        T.vector("ptk_u_par","N_tk", maxlen=100)

        var(T, "N_nt", int)
        T.vector("pnt_pt","N_nt", maxlen=300)
        T.vector("pnt_phi","N_nt", maxlen=300)
        T.vector("pnt_eta","N_nt", maxlen=300)
        T.vector("pnt_u_par","N_nt", maxlen=300)

        # var(T, "N_k0", int)
        # T.vector("pk0_pt","N_k0", maxlen=300)
        # T.vector("pk0_phi","N_k0", maxlen=300)
        # T.vector("pk0_eta","N_k0", maxlen=300)
        # T.vector("pk0_u_par","N_k0", maxlen=300)


    def process(self, iEvent, event):
        T = self.tree

        T.reset()

        fill(T, 'n_evt', event.eventId)
        fill(T, "n_vtx", len(event.goodVertices))

        for puInfo in event.pileUpInfo:
            if puInfo.getBunchCrossing() == 0:
                fill(T, 'n_pile_up', puInfo.nPU())

        if self.cfg_comp.isMC:
            fillVB(T, event, "Wgen", lite =1)

        fillMuonZ(T, "muon", event.muon_W, lite =1)

        h_p4_tk = TLorentzVector(0., 0., 0., 0.)
        h_sum_pt_tk = 0
        N_tk = 0
        ptk_pt = []
        ptk_phi = []
        ptk_eta = []
        ptk_u_par = []

        h_p4_nt = TLorentzVector(0., 0., 0., 0.)
        h_sum_pt_nt = 0
        N_nt = 0
        pnt_pt = []
        pnt_phi = []
        pnt_eta = []
        pnt_u_par = []

        part_arr = np.array(event.pf_candidates,dtype = event.pf_candidates[0].__class__)

        for particle in part_arr:

            p4 = particle2TLorenzVector(particle)
            pt = p4.Pt()
            if pt < 0.2: continue
            eta = p4.Eta()
            phi = p4.Phi()
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

                h_sum_pt_tk += p4.Pt()


                N_tk += 1

                ptk_pt.append(pt)
                aux_phi = reduce_angle(3.1415926535 + phi - event.muon_W.phi())
                ptk_phi.append(aux_phi)
                ptk_eta.append(eta)
                aux_upar = compute_u_par(partRef = event.muon_W, p42 = p4)
                ptk_u_par.append(aux_upar)

            elif charge == 0 and particle.pdgId()>5:
                h_p4_nt = h_p4_nt + p4

                h_sum_pt_nt += p4.Pt()


                N_nt += 1

                pnt_pt.append(pt)
                aux_phi = reduce_angle(3.1415926535 + phi - event.muon_W.phi())
                pnt_phi.append(aux_phi)
                pnt_eta.append(eta)
                aux_upar = compute_u_par(partRef = event.muon_W, p42 = p4)
                pnt_u_par.append(aux_upar)

        event.h_p4_tk = h_p4_tk
        event.h_sum_pt_tk = h_sum_pt_tk
        event.N_tk = N_tk

        event.h_p4_nt = h_p4_nt
        event.h_sum_pt_nt = h_sum_pt_nt
        event.N_nt = N_nt


        self.computeFurtherVariables(event)
        self.computeUprojectionsWRTmuons(event)

        fillUparUperp(T, event, "MC")



        fillRecoilInfo(T, event, "tk", lite = 1)
        fillUparUperp(T, event, "tk")

        fillRecoilInfo(T, event, "nt", lite = 1)
        fillUparUperp(T, event, "nt")


        if N_tk>0:
            ptk_pt, ptk_phi, ptk_eta, ptk_u_par = zip(*sorted(zip(ptk_pt, ptk_phi, ptk_eta, ptk_u_par),key=lambda x: x[0], reverse=True))
            ptk_pt = list(ptk_pt)[:100]
            ptk_phi = list(ptk_phi)[:100]
            ptk_eta = list(ptk_eta)[:100]
            ptk_u_par = list(ptk_u_par)[:100]
            if N_tk>99: N_tk = 99

        fill(T, 'N_tk', N_tk)
        T.vfill("ptk_pt",ptk_pt)
        T.vfill("ptk_phi",ptk_phi)
        T.vfill("ptk_eta",ptk_eta)
        T.vfill("ptk_u_par",ptk_u_par)

        if N_nt>0:
            pnt_pt, pnt_phi, pnt_eta, pnt_u_par = zip(*sorted(zip(pnt_pt, pnt_phi, pnt_eta, pnt_u_par),key=lambda x: x[0], reverse=True))
            pnt_pt = list(pnt_pt)[:300]
            pnt_phi = list(pnt_phi)[:300]
            pnt_eta = list(pnt_eta)[:300]
            pnt_u_par = list(pnt_u_par)[:300]
            if N_nt>299: N_nt = 299
        else:
            N_nt = 1
            pnt_pt = [0]
            pnt_phi = [0]
            pnt_eta = [0]
            pnt_u_par = [0]


        fill(T, 'N_nt', N_nt)
        T.vfill("pnt_pt",pnt_pt)
        T.vfill("pnt_phi",pnt_phi)
        T.vfill("pnt_eta",pnt_eta)
        T.vfill("pnt_u_par",pnt_u_par)


        T.tree.Fill()
