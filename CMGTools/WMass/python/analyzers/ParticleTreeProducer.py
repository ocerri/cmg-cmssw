from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ntupleFunctions import *
from math import sqrt

class ParticleTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ParticleTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        # p4, pdgid, n_vertici, delta Z, is from PV

        T = self.tree

        # var(T, "n_evt", int)
        var(T, "n_vtx", int)
        var(T, "n_pile_up", int)
        bookParticle(T, "ptc")
        var(T, "dz", float)
        var(T, "dx", float)
        var(T, "dy", float)
        var(T, "dxy", float)
        var(T, "packed_from_pv", float)
        var(T, "distance_pv_closest_vtx", float)

    def process(self, iEvent, event):
        T = self.tree

        for particle in event.pf_candidates:
            if particle.charge() == 0:
                continue
            T.reset()

            # fill(T, 'n_evt', event.eventId)
            fill(T, "n_vtx", len(event.goodVertices))

            for puInfo in event.pileUpInfo:
                if puInfo.getBunchCrossing() == 0:
                    fill(T, 'n_pile_up', puInfo.nPU())

            fillParticle(T, "ptc", particle)

            fill(T, "dz", particle.vz() - event.goodVertices[0].z())
            dx = particle.vx() - event.goodVertices[0].x()
            dy = particle.vy() - event.goodVertices[0].y()
            fill(T, "dx", dx)
            fill(T, "dy", dy)
            fill(T, "dxy", sqrt(dx**2 + dy**2))

            fill(T, "packed_from_pv", particle.fromPV())

            distances_pv_vtx = [abs(vtx.z() - event.goodVertices[0].z()) for vtx in event.goodVertices[1:]]
            if len(distances_pv_vtx) != 0:
                distance_pv_closest_vtx = min(distances_pv_vtx)
            else:
                distance_pv_closest_vtx = -1

            fill(T, "distance_pv_closest_vtx", distance_pv_closest_vtx)

            T.tree.Fill()
