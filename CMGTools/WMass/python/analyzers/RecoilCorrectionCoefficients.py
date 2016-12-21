from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TLorentzVector, TVector3, TVector2, TMath
from copy import deepcopy


class RecoilCorrectionCoefficients(Analyzer):
    '''
    Compute Josh coefficients

    TODO Nick: carica correttamente le cose di partenza
    '''

    def process(self, iEvent, event):

        recoil = TVector2(event.Prec.Px(), event.Prec.Py())
        mu_par = TVector2(event.Pmu.Px(), event.Pmu.Py())

        mu_par /= (mu_par.Mod())
        mu_perp = mu_par.Rotate(TMath.Pi()/2.)

        tk_recoil = TVector2(sum_recoil_p4_tk.Px(), sum_recoil_p4_tk.Py())
        tk_recoil_perp = tk_recoil.Rotate(TMath.Pi()/2.)

        if tk_recoil.Mod() != 0:
            c1_tk = (recoil * tk_recoil) / (tk_recoil.Mod2())
            c2_tk = (recoil * tk_recoil_perp) / (tk_recoil_perp.Mod2())

            tk_d_vec = recoil - tk_recoil
            d1_tk = tk_d_vec.Mod()
            d2_tk = tk_d_vec.Phi() - tk_recoil.Phi()
            d2_tk = reduce_angle(d2_tk)

            e1_tk = recoil.Mod() / (tk_recoil.Mod())
            e2_tk = recoil.Phi() - tk_recoil.Phi()
            e2_tk = reduce_angle(e2_tk)

            c1_mu_tk = (recoil * mu_par) / (tk_recoil * mu_par)
            c2_mu_tk = (recoil * mu_perp) / (tk_recoil * mu_perp)
        else:
            c1_tk = 0.
            c2_tk = 0.

            tk_d_vec = recoil - tk_recoil
            d1_tk = tk_d_vec.Mod()
            d2_tk = tk_d_vec.Phi() - tk_recoil.Phi()
            d2_tk = reduce_angle(d2_tk)

            e1_tk = 0.
            e2_tk = recoil.Phi() - tk_recoil.Phi()
            e2_tk = reduce_angle(e2_tk)

            c1_mu_tk = 0.
            c2_mu_tk = 0.

        event.c1_tk = c1_tk
        event.c2_tk = c2_tk
        event.d1_tk = d1_tk
        event.d2_tk = d2_tk
        event.e1_tk = e1_tk
        event.e2_tk = e2_tk
        event.c1_mu_tk = c1_mu_tk
        event.c2_mu_tk = c2_mu_tk
