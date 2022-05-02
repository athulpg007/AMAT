"""
test_manever.py

Tests for maneuver.py

"""

import numpy as np

class TestImportDeflection():
    def test_import_arrival(self):
        try:
            from AMAT.maneuver import ProbeOrbiterDeflection, ProbeProbeDeflection, OrbiterOrbiterDeflection
            return True
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Cannot import classes from AMAT.maneuver")
            assert False

try:
    from AMAT.maneuver import ProbeOrbiterDeflection, ProbeProbeDeflection, OrbiterOrbiterDeflection
except ModuleNotFoundError:
    raise ModuleNotFoundError("Cannot import classes from AMAT.maneuver")


class Test_ProbeOrbiterDeflection_Neptune:

    deflection = ProbeOrbiterDeflection("NEPTUNE", v_inf_vec_icrf_kms=np.array([17.78952518,  8.62038536,  3.15801163]),
                                       rp_probe=(24622+400)*1e3,  psi_probe=3*np.pi/2, h_EI_probe=1000e3,
                                       rp_space=(24622+4000)*1e3, psi_space=np.pi/2,
                                       r_dv_rp=1000)

    def test_theta_star_dv_probe(self):
        ans = self.deflection.theta_star_dv_probe
        rdv = self.deflection.probe.r_mag_bi(ans)/self.deflection.planetObj.RP
        assert abs(ans + 1.9866386) < 1e-6
        assert abs(rdv - self.deflection.r_dv_rp) < 1e-6

    def test_delta_theta_star_probe(self):
        assert abs(self.deflection.delta_theta_star_probe - 1.9866386) < 1e-6


    def test_v_vec_dv_maneuver(self):
        assert abs(self.deflection.dv_maneuver_mag - 65.7302) < 1e-2
        assert abs(self.deflection.TOF_probe - 14.17563) < 1e-2
        assert abs(self.deflection.TOF_space - 14.17647) < 1e-2


class Test_ProbeProbeDeflection_Neptune:

    deflection = ProbeProbeDeflection( "NEPTUNE",
                                       v_inf_vec_icrf_kms=np.array([17.78952518,  8.62038536,  3.15801163]),
                                       rp_probe1=(24622+400)*1e3,  psi_probe1=3*np.pi/2, h_EI_probe1=1000e3,
                                       rp_probe2=(24622+400)*1e3,  psi_probe2=np.pi/2,  h_EI_probe2=1000e3,
                                       r_dv_rp=4000)


    def test_v_vec_dv_maneuver(self):
        assert abs(self.deflection.dv_maneuver_mag - 15.6355338) < 1e-6
        assert abs(self.deflection.TOF_probe1 - 56.8684222) < 1e-6
        assert abs(self.deflection.TOF_probe2 - 56.8684222) < 1e-6
        assert abs(self.deflection.probe1.gamma_entry_inertial*180/np.pi - -10.5025297) < 1e-6
        assert abs(self.deflection.probe2.gamma_entry_inertial*180/np.pi - -10.5025297) < 1e-6
        assert abs(self.deflection.probe1.heading_entry_atm*180/np.pi - 14.9106075) < 1e-6
        assert abs(self.deflection.probe2.heading_entry_atm*180/np.pi - 167.5494031) < 1e-6


class Test_OrbiterOrbiterDeflection_Neptune:

    deflection = OrbiterOrbiterDeflection( "NEPTUNE",
                                       v_inf_vec_icrf_kms=np.array([17.78952518,  8.62038536,  3.15801163]),
                                       rp_space1=(24622+4000)*1e3,  psi_space1=3*np.pi/2,
                                       rp_space2=(24622+4000)*1e3,  psi_space2=np.pi/2,
                                       r_dv_rp=1000)


    def test_v_vec_dv_maneuver(self):
        assert abs(self.deflection.dv_maneuver_mag - 68.9076850) < 1e-6
        assert abs(self.deflection.TOF_space1 - 14.17643992231) < 1e-6
        assert abs(self.deflection.TOF_space2 - 14.17647834316) < 1e-6
