from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.statistics.Counter import Counter, Counters
from itertools import combinations

class WMassEventSelection(Analyzer):
    '''
    TODO: aggiungere i counters?
          aggiungere la selezione sui vertici
    '''

    def beginLoop(self):
        super(WMassEventSelection,self).beginLoop()

        self.counters.addCounter('events')
        self.counters.counter('events').register('All events')

        if not hasattr(self.cfg_ana,"muon_max_dz"):
            self.cfg_ana.muon_max_dz = 0.1

        if not hasattr(self.cfg_ana, "mass_region"):
            self.cfg_ana.mass_region = [60,110]

    def process(self, iEvent, event):

        if self.cfg_ana.event_type == "Z":

            for muon in event.muons:
                if not (muon.looseId() and muon.dz() < self.cfg_ana.muon_max_dz):
                    event.muons.remove(muon)


            Zpair_cand = []
            for m1, m2 in combinations(event.muons, 2):
                if m1.charge()*m2.charge() != -1:
                    continue
                if not m1.associatedVertex is m2.associatedVertex:
                    continue

                M = (m1.p4() + m2.p4()).M()
                if M > self.cfg_ana.mass_region[1] or M < self.cfg_ana.mass_region[0]:
                    continue

                Zpair_cand.append([m1, m2])


            if not len(Zpair_cand) == 1:
                return False

            event.muons = Zpair_cand[0]


            event.muons.sort(key=lambda x: x.p4().Pt(), reverse=True)

            if self.cfg_ana.met_type == "tkmet":
                aux_met = event.met_tk
            elif self.cfg_ana.met_type == "pfmet":
                aux_met = event.met_pf
            else:
                print "ERROR, GIVE TO WMassEventSelection EITHER tkmet OR pfmet"
                return False

            for muon1, muon2 in zip(event.muons, reversed(event.muons)):
                met_plus_muon = aux_met.p4() + muon2.p4()
                if muon1.tightId() and muon1.p4().Pt() > self.cfg_ana.pt_muon_thr and met_plus_muon.Pt() > self.cfg_ana.met_thr:
                    muon1.W_like_triggered = True
                else:
                    muon1.W_like_triggered = False
            if not len([muon for muon in event.muons if muon.W_like_triggered]) != 0:
                return False

            return True


        else:
            return False
