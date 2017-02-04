from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ROOT import TLorentzVector
from ntupleFunctions import *
from math import sqrt, log
from copy import deepcopy
from UtilsFunctions import kt_distance, deltaR
import numpy as np

class NeutralParticleTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(NeutralParticleTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        # p4, pdgid, n_vertici, delta Z, is from PV

        T = self.tree

        var(T, "n_evt", int)
        var(T, "n_vtx", int)
        var(T, "n_pile_up", int)
        if self.cfg_comp.isMC:
            bookVB(T, "Wgen", lite =1)

        bookMuonZ(T, "muon", lite =1)

        bookParticle(T, "ptc", lite =1)
        var(T, "deltaR_from_muon")
        # bookP4(T, "leading_track")
        var(T, "deltaR_from_leading_track")
        var(T, "anti_kt_from_leading_track")
        # bookP4(T, "closest_pv_track")
        var(T, "deltaR_pv")
        var(T, "anti_kt_pv")
        var(T, "w_pv")

        # bookP4(T, "closest_pu_track")
        var(T, "deltaR_pu")
        var(T, "anti_kt_pu")
        var(T, "w_pu")


    def process(self, iEvent, event):
        T = self.tree

        part_arr = np.array(event.pf_candidates,dtype = event.pf_candidates[0].__class__)

        for particle in part_arr:
            if particle.charge() != 0 or abs(particle.pdgId()) < 5 or particle.pt<0.250: #pdgId = 1 o 2 sono i depositi nel calo forward
                continue
            T.reset()

            fill(T, 'n_evt', event.eventId)
            fill(T, "n_vtx", len(event.goodVertices))

            for puInfo in event.pileUpInfo:
                if puInfo.getBunchCrossing() == 0:
                    fill(T, 'n_pile_up', puInfo.nPU())

            if self.cfg_comp.isMC:
                fillVB(T, event, "Wgen", lite =1)

            fillMuonZ(T, "muon", event.muon_W, lite =1)

            fillParticle(T, "ptc", particle, lite =1)
            fill(T, "deltaR_from_muon", deltaR(part1=event.muon_W, part2=particle))

            leading_track_p4 = TLorentzVector(0, 0, 0, 0)
            closest_pv_track_p4 = TLorentzVector(0, 0, 0, 0)
            deltaR_min_pv = -1.
            anti_kt_pv = -1.
            closest_pu_track_p4 = TLorentzVector(0, 0, 0, 0)
            deltaR_min_pu = -1.
            anti_kt_pu = -1.

            DRmax = 0.3
            w_pu = 0.
            w_pv = 0.

            p4 = particle2TLorenzVector(particle)

            for track in part_arr:
                if track.charge() == 0 or track.pt() < 0.350:
                    continue
                if abs(track.pdgId()) == 13:
                    pt = track.pt()
                    if hasattr(event, "muon_W"):
                        if track.pdgId() == event.muon_W.pdgId() and 0.9*event.muon_W.pt() < pt < 1.1*event.muon_W.pt():
                            continue
                    elif hasattr(event, "muons"):
                        if track.pdgId() == event.muons[0].pdgId() and 0.9*event.muons[0].pt() < pt < 1.1*event.muons[0].pt():
                            continue
                        if track.pdgId() == event.muons[1].pdgId() and 0.9*event.muons[1].pt() < pt < 1.1*event.muons[1].pt():
                            continue

                dz = track.vz() - event.goodVertices[0].z()
                dx = track.vx() - event.goodVertices[0].x()
                dy = track.vy() - event.goodVertices[0].y()
                is_fromPV = ((dx**2 + dy**2)/0.03**2) + (dz/0.05)**2 < 1
                p4_tk = particle2TLorenzVector(track)

                aux_deltaR = deltaR(p41=p4_tk, p42=p4)
                aux_kt = kt_distance(p4_tk, p4)

                if is_fromPV:
                    if track.pt() > leading_track_p4.Pt():
                        leading_track_p4 = deepcopy(p4_tk)
                    if aux_deltaR < deltaR_min_pv or deltaR_min_pv == -1:
                        deltaR_min_pv = aux_deltaR
                    if aux_kt < anti_kt_pv or anti_kt_pv == -1:
                        anti_kt_pv = aux_kt

                    if aux_deltaR < DRmax:
                        w_pv += log(track.pt()/aux_deltaR)
                else:
                    if aux_deltaR < deltaR_min_pu or deltaR_min_pu == -1:
                        deltaR_min_pu = aux_deltaR
                    if aux_kt < anti_kt_pu or anti_kt_pu == -1:
                        anti_kt_pu = aux_kt

                    if aux_deltaR < DRmax:
                        w_pu += log(track.pt()/aux_deltaR)

            # fillP4(T, "leading_track", leading_track_p4)
            if leading_track_p4.Pt() != 0:
                fill(T, "anti_kt_from_leading_track", kt_distance(leading_track_p4, particle2TLorenzVector(particle)))
                fill(T, "deltaR_from_leading_track", deltaR(p41=leading_track_p4, part2=particle))
            else:
                fill(T, "anti_kt_from_leading_track", -1)
                fill(T, "deltaR_from_leading_track", -1)

            # fillP4(T, "closest_pv_track", closest_pv_track_p4)
            fill(T, "deltaR_pv", deltaR_min_pv)
            fill(T, "anti_kt_pv", anti_kt_pv)
            fill(T, "w_pv", w_pv)

            # fillP4(T, "closest_pu_track", closest_pu_track_p4)
            fill(T, "deltaR_pu", deltaR_min_pu)
            fill(T, "anti_kt_pu", anti_kt_pu)
            fill(T, "w_pu", w_pu)


            T.tree.Fill()
