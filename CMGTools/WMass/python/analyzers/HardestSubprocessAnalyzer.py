from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TLorentzVector, TVector3, TVector2, TMath
from copy import deepcopy


class HardestSubprocesAnalyzer(Analyzer):
    '''
    TODO: retrieve muons, Z and h from gen particles and store them.
        capirci qualcosa
    '''

    def process(self, iEvent, event):
        # Save Muons and Z
        # event.hardest_ubproces = stuff
        pass


        if self.cfg_comp.isMC:
            foundZ = False
            for genp in event.genParticles:
              # if math.fabs(genp.pdgId())==23:
              if math.fabs(genp.pdgId())==23 and genp.status()==62:
                foundZ = True
                # print 'genp.pdgId()=',genp.pdgId(), 'genp.status()=',genp.status(), 'genp.numberOfDaughters()=',genp.numberOfDaughters()
                # # if(genp.numberOfDaughters()>0 and genp.status()==62):
                # if(genp.numberOfDaughters()>0):
                  # print 'genp.daughter(0)',genp.daughter(0).pdgId(),'status',genp.daughter(0).status()
                  # if(genp.numberOfDaughters()>1):
                    # print 'genp.daughter(1)',genp.daughter(1).pdgId(),'status',genp.daughter(1).status()

            # if not foundZ: print 'NO Z FOUND!!!'

            genZ_dummy = [ genp for genp in event.genParticles if \
                                 math.fabs(genp.pdgId())==23 and (self.cfg_ana.doMad or genp.status()==62 )
                                 ]
            if len(genZ_dummy)==1:
              event.genZ = [ genp for genp in genZ_dummy if \
                                   math.fabs(genp.daughter(0).pdgId())==13
                                   ]
              event.genMuPos = []
              event.genMuNeg = []
              event.genMuPosStatus1 = []
              event.genMuNegStatus1 = []

              if len(event.genZ)==1:
              # if the genp event is selected, associate gen muons
                if(event.genZ[0].daughter(0).charge()>0):
                  event.genMuPos.append(event.genZ[0].daughter(0))
                  # print event.genZ[0].daughter(0).pdgId(),' event.genZ[0].daughter(0).charge()= ',event.genZ[0].daughter(0).charge()
                  event.genMuNeg.append(event.genZ[0].daughter(1))
                else:
                  event.genMuPos.append(event.genZ[0].daughter(1))
                  event.genMuNeg.append(event.genZ[0].daughter(0))

                if(len(event.genMuNeg) >0):
                  event.genMuNegStatus1.append(returnMuonDaughterStatus1(self,event.genMuNeg[0]))
                if(len(event.genMuPos) >0):
                  event.genMuPosStatus1.append(returnMuonDaughterStatus1(self,event.genMuPos[0]))

                event.genZ_PostFSR = event.genMuNegStatus1[0].p4() + event.genMuPosStatus1[0].p4()
                event.genZ_mt = mT(self,event.genZ[0].daughter(0).p4() , event.genZ[0].daughter(1).p4())
                event.muPosGenDeltaRgenP=1e6
                event.muNegGenDeltaRgenP=1e6

              else:
                # if the genp is not signal, don't save genp but do not exit
                # -----> events which will pass the reconstruction but are not signal
                # can be considered as background (for example, in Z+Jets, from Z decaying into electrons, taus)
                event.savegenpZ=False
            else:
              event.savegenpZ=False


        pass
