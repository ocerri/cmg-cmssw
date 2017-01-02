from UtilsFunctions import particle2TLorenzVector

def var(tree, varName, type=float, storageType="default"):
    tree.var(varName, type, storageType=storageType)

def fill(tree, varName, value):
    tree.fill(varName, value)


def bookP4(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_eta", float)

def fillP4(tree, pName, p4):
    tree.fill(pName + "_pt", p4.Pt())
    tree.fill(pName + "_phi", p4.Phi())
    tree.fill(pName + "_eta", p4.Eta())

def bookVB(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_pz", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_Y", float)
    tree.var(pName + "_M", float)

def fillVB(tree, event, pName, p4 = None):
    if p4 == None:
        p4 = particle2TLorenzVector(getattr(event, pName))
    tree.fill(pName + "_pt", p4.Pt())
    tree.fill(pName + "_pz", p4.Pz())
    tree.fill(pName + "_phi", p4.Phi())
    tree.fill(pName + "_Y", p4.Rapidity())
    tree.fill(pName + "_M", p4.M())

def bookMuonZgen(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_eta", float)

def fillMuonZgen(tree, pName, particle):
    tree.fill(pName + "_pt", particle.pt())
    tree.fill(pName + "_phi", particle.phi())
    tree.fill(pName + "_eta", particle.eta())

def bookMuonZ(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_eta", float)
    tree.var(pName + "_W_like_triggered", float)

def fillMuonZ(tree, pName, particle):
    tree.fill(pName + "_pt", particle.pt())
    tree.fill(pName + "_phi", particle.phi())
    tree.fill(pName + "_eta", particle.eta())
    tree.fill(pName + "_W_like_triggered", particle.W_like_triggered)


def bookRecoilInfo(tree, pName):
    """give pName = "tk", "tk_not_pv" or "nt" """
    tree.var("h_pt_" + pName, float)
    tree.var("h_eta_" + pName, float)
    tree.var("h_phi_" + pName, float)
    tree.var("h_sum_pt_" + pName, float)
    # tree.var("h_sum_pt2_" + pName, float)
    # tree.var("h_eta_mean_" + pName, float)
    tree.var("N_part_" + pName, float)

    bookP4(tree, "leading_particle_" + pName)
    # bookP4(tree, "leading2_particle_" + pName)
    # tree.var("leading12_pt_scalar_sum_" + pName, float)
    # tree.var("leading12_pt_vector_sum_" + pName, float)
    # tree.var("ratio_vec_scalar_" + pName, float)
    tree.var("ratio_vec_scalar_2_" + pName, float)

def fillRecoilInfo(tree, event, pName):
    """give pName = "tk", "tk_not_pv" or "nt" """
    tree.fill("h_pt_"+pName, getattr(event, "h_p4_"+pName).Pt() )
    tree.fill("h_eta_"+pName, getattr(event, "h_p4_"+pName).Eta() )
    tree.fill("h_phi_"+pName, getattr(event, "h_p4_"+pName).Phi() )
    tree.fill("h_sum_pt_"+pName, getattr(event, "h_sum_pt_"+pName) )
    # tree.fill("h_sum_pt2_"+pName, getattr(event, "h_sum_pt2_"+pName) )
    # tree.fill("h_eta_mean_"+pName, getattr(event, "h_eta_mean_"+pName) )
    tree.fill("N_part_"+pName, getattr(event, "N_part_"+pName) )

    fillP4(tree, "leading_particle_"+pName, getattr(event, "leading_particles_p4_"+pName)[0] )
    # fillP4(tree, "leading2_particle_"+pName, getattr(event, "leading_particles_p4_"+pName)[1] )
    # tree.fill("leading12_pt_scalar_sum_"+pName, getattr(event, "leading12_pt_scalar_sum_"+pName))
    # tree.fill("leading12_pt_vector_sum_"+pName, getattr(event, "leading12_pt_vector_sum_"+pName))
    # tree.fill("ratio_vec_scalar_"+pName, getattr(event, "ratio_vec_scalar_"+pName))
    tree.fill("ratio_vec_scalar_2_"+pName, getattr(event, "ratio_vec_scalar_2_"+pName))


def bookUparUperp(tree, pName):
    tree.var("u_par_" + pName, float)
    tree.var("u_perp_" + pName, float)

def fillUparUperp(tree, event, pName):
    tree.fill("u_par_" + pName, getattr(event, "u_par_" + pName))
    tree.fill("u_perp_" + pName, getattr(event, "u_perp_" + pName))


def bookCorrectionCoeff(tree):
    tree.var("c1_tk",float)
    tree.var("c2_tk",float)
    tree.var("d1_tk",float)
    tree.var("d2_tk",float)
    tree.var("e1_tk",float)
    tree.var("e2_tk",float)
    tree.var("c1_mu_tk",float)
    tree.var("c2_mu_tk",float)

def fillCorrectionCoeff(tree, event):
    tree.fill("c1_tk",event.c1_tk)
    tree.fill("c2_tk",event.c2_tk)
    tree.fill("d1_tk",event.d1_tk)
    tree.fill("d2_tk",event.d2_tk)
    tree.fill("e1_tk",event.e1_tk)
    tree.fill("e2_tk",event.e2_tk)
    tree.fill("c1_mu_tk",event.c1_mu_tk)
    tree.fill("c2_mu_tk",event.c2_mu_tk)
