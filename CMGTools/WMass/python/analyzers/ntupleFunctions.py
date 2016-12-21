def var(tree, varName, type=float, storageType="default"):
    tree.var(varName, type, storageType=storageType)

def fill(tree, varName, value):
    tree.fill(varName, value)


def bookP4(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_eta", float)
    # tree.var(pName + "_charge", int)

def fillP4(tree, pName, p4):
    tree.fill(pName + "_pt", p4.Pt())
    tree.fill(pName + "_phi", p4.Phi())
    tree.fill(pName + "_eta", p4.Eta())
    # tree.fill(pName + "_charge", particle.charge())


def bookMuonZ(tree, pName):
    tree.var(pName + "_pt", float)
    tree.var(pName + "_phi", float)
    tree.var(pName + "_eta", float)
    tree.var(pName + "_W_like_triggered", int)

def fillMuonZ(tree, pName, particle):
    tree.fill(pName + "_pt", particle.pt())
    tree.fill(pName + "_phi", particle.phi())
    tree.fill(pName + "_eta", particle.eta())
    tree.fill(pName + "_W_like_triggered", particle.W_like_triggered)


def bookRecoilInfo(tree, pName):
    """give pName = "tk", "tk_not_pv" or "nt" """
    tree.var("h_pt_" + pName, float)
    tree.var("h_sum_pt_" + pName, float)
    tree.var("h_sum_pt2_" + pName, float)
    tree.var("h_eta_mean_" + pName, float)
    tree.var("N_part_" + pName, float)
    bookP4(tree, "leading_particle_" + pName)
    bookP4(tree, "leading2_particle_" + pName)
    # tree.var("leading12_pt_scalar_sum_" + pName, float)
    tree.var("leading12_pt_vector_sum_" + pName, float)
    tree.var("ratio_vec_scalar_" + pName, float)
    tree.var("ratio_vec_scalar_2_" + pName, float)

def fillRecoilInfo(tree, event, pName):
    """give pName = "tk", "tk_not_pv" or "nt" """
    tree.fill("h_pt_"+pName, getattr(event, "h_p4_"+pName).Pt() )
    tree.fill("h_sum_pt_"+pName, getattr(event, "h_sum_pt_"+pName) )
    tree.fill("h_sum_pt2_"+pName, getattr(event, "h_sum_pt2_"+pName) )
    tree.fill("h_eta_mean_"+pName, getattr(event, "h_eta_mean_"+pName) )
    tree.fill("N_part_"+pName, getattr(event, "N_part_"+pName) )

    fillP4(tree, "leading_particle_"+pName, getattr(event, "leading_particles_p4_"+pName)[0] )
    fillP4(tree, "leading2_particle_"+pName, getattr(event, "leading_particles_p4_"+pName)[1] )
    # tree.fill("leading12_pt_scalar_sum_"+pName, getattr(event, "leading12_pt_scalar_sum_"+pName))
    tree.fill("leading12_pt_vector_sum_"+pName, getattr(event, "leading12_pt_vector_sum_"+pName))
    tree.fill("ratio_vec_scalar_"+pName, getattr(event, "ratio_vec_scalar_"+pName))
    tree.fill("ratio_vec_scalar_2_"+pName, getattr(event, "ratio_vec_scalar_2_"+pName))


def bookUparUperp(tree, pName):
    tree.var("u_par_" + pName, float)
    tree.var("u_perp_" + pName, float)

def fillUparUperp(tree, event, pName):
    tree.fill("u_par_" + pName, getattr(event, "u_par_" + pName))
    tree.fill("u_perp_" + pName, getattr(event, "u_perp_" + pName))
