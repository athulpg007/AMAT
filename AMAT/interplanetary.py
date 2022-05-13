import pandas as pd
import matplotlib.pyplot as plt

from AMAT.launcher import Launcher

class Interplanetary:

	def __init__(self, ID, datafile, sheet_name, Lcdate_format):
		self.ID = ID
		self.datafile = datafile
		self.sheet_name = sheet_name

		self.df = pd.read_excel(self.datafile, sheet_name=sheet_name)
		self.Lcdate = pd.to_datetime(list(map(str, self.df['Lcdate'].values)), format=Lcdate_format)
		self.C3 = self.df["LC3"]
		self.TOF = self.df["TOF"]
		self.Avinf = self.df["Avinf"]

	def compute_launch_capability(self, launcherObj):
		return launcherObj.launchMass(self.C3)

	def plot_launch_mass_vs_launch_date(self, launcherObj):
		Lcmass = self.compute_launch_capability(launcherObj)

		plt.figure(figsize=(8,6))
		plt.plot(self.Lcdate, Lcmass, marker='o', color='g', linestyle='None')
		plt.title(self.ID+" : "+launcherObj.ID, fontsize=14)
		plt.xlabel(r'Launch Year', fontsize=14)
		plt.ylabel("Launch capability, kg", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')
		plt.ylim(max(0, sorted(set(Lcmass))[1])-100, max(Lcmass)+100)

		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()

	def plot_TOF_vs_launch_date(self):

		plt.figure(figsize=(8,6))
		plt.plot(self.Lcdate, self.TOF, marker='o', color='g', linestyle='None')
		plt.title(self.ID, fontsize=14)
		plt.xlabel(r'Launch Year', fontsize=14)
		plt.ylabel("TOF, years", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')

		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()

	def plot_Avinf_vs_launch_date(self):

		plt.figure(figsize=(8,6))
		plt.plot(self.Lcdate, self.Avinf, marker='o', color='g', linestyle='None')
		plt.title(self.ID, fontsize=14)
		plt.xlabel(r'Launch Year', fontsize=14)
		plt.ylabel(r"Arrival $V_{\infty}$, km/s", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')

		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()

	def plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self, launcherObj, scale=20):

		Lcmass = self.compute_launch_capability(launcherObj)

		plt.figure(figsize=(8,6))
		plt.scatter(self.Lcdate, self.Avinf, c=Lcmass, marker='o', cmap='jet',
					vmin = max(0, sorted(set(Lcmass))[1]), vmax = max(Lcmass), s=scale)
		cbar = plt.colorbar()
		cbar.ax.tick_params(labelsize=14)
		cbar.set_label(r'Launch capability, kg', labelpad=-20, y=1.05, rotation=0, fontsize=14)
		cbar.ax.tick_params(axis='y', direction='in')
		plt.title(self.ID, fontsize=14)
		plt.xlabel(r'Launch Year', fontsize=14)
		plt.ylabel(r"Arrival $V_{\infty}$, km/s", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')

		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()



	def plot_launch_mass_vs_TOF(self, launcherObj):
		Lcmass = self.compute_launch_capability(launcherObj)

		plt.figure(figsize=(8,6))
		plt.plot(self.TOF, Lcmass, marker='o', color='g', linestyle='None')
		plt.title(self.ID+" : "+launcherObj.ID, fontsize=14)
		plt.xlabel(r'TOF, years', fontsize=14)
		plt.ylabel("Launch capability, kg", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')
		plt.ylim(max(0, sorted(set(Lcmass))[1])-100, max(Lcmass)+100)


		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()



	def plot_launch_mass_vs_TOF_with_vinf_colorbar(self, launcherObj, scale=20):
		Lcmass = self.compute_launch_capability(launcherObj)

		plt.figure(figsize=(8,6))
		plt.scatter(self.TOF, Lcmass, c=self.Avinf , marker='o', cmap='jet',
					vmin=self.Avinf.min(), vmax=self.Avinf.max(), s=scale)
		cbar = plt.colorbar()
		cbar.ax.tick_params(labelsize=14)
		cbar.set_label(r'$V_{\infty}$, km/s', labelpad=-20, y=1.05, rotation=0, fontsize=14)
		cbar.ax.tick_params(axis='y', direction='in')
		plt.title(self.ID+" : "+launcherObj.ID, fontsize=14)
		plt.xlabel(r'TOF, years', fontsize=14)
		plt.ylabel("Launch capability, kg", fontsize=14)
		plt.xticks(fontsize=14)
		plt.yticks(fontsize=14)
		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')
		plt.ylim(max(0, sorted(set(Lcmass))[1])-100, max(Lcmass)+100)


		plt.legend(loc='upper right', fontsize=12, framealpha=0.8)

		ax.xaxis.set_tick_params(direction='in', which='both')
		ax.yaxis.set_tick_params(direction='in', which='both')

		ax.xaxis.set_tick_params(width=2, length=8)
		ax.yaxis.set_tick_params(width=2, length=8)

		ax.xaxis.set_tick_params(width=1, length=6, which='minor')
		ax.yaxis.set_tick_params(width=1, length=6, which='minor')

		ax.xaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.xaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		ax.yaxis.grid(which='major', color='k', linestyle='dotted', linewidth=0.5)
		ax.yaxis.grid(which='minor', color='k', linestyle='dotted', linewidth=0.0)

		for axis in ['top', 'bottom', 'left', 'right']:
			ax.spines[axis].set_linewidth(2)

		plt.show()



class Test_Interplanetary_Uranus_Chem:
	interplanetary1 = Interplanetary(ID="Uranus Chem.",
									 datafile='../interplanetary-data-private/uranus/uranus-chem.xlsx',
									 sheet_name='uranus-chem',
									 Lcdate_format="%Y%m%d")

	launcher1 = Launcher('Falcon Heavy Expendable with Kick',
						 datafile='../launcher-data/falcon-heavy-expendable-w-star-48.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)
		print(ans)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)



class Test_Interplanetary_Uranus_SEP:
	interplanetary1 = Interplanetary(ID="Uranus SEP",
									 datafile='../interplanetary-data-private/uranus/uranus-sep.xlsx',
									 sheet_name='Sheet1',
									 Lcdate_format="%Y%m%d")

	launcher1 = Launcher('Falcon Heavy Expendable with Kick',
						 datafile='../launcher-data/falcon-heavy-expendable-w-star-48.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)




class Test_Interplanetary_Uranus_High_Energy_FHE:
	interplanetary1 = Interplanetary(ID="Uranus High Energy",
									 datafile='../interplanetary-data-private/uranus/uranus-high-energy.xlsx',
									 sheet_name='Sheet1',
									 Lcdate_format=None)

	launcher1 = Launcher('Falcon Heavy Expendable with Kick',
						 datafile='../launcher-data/falcon-heavy-expendable-w-star-48.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)

	def test_plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self):
		self.interplanetary1.plot_Avinf_vs_launch_date_with_launch_mass_colorbar(launcherObj=self.launcher1)


class Test_Interplanetary_Uranus_High_Energy_SLS_Block_1:
	interplanetary1 = Interplanetary(ID="Uranus High Energy",
									 datafile='../interplanetary-data-private/uranus/uranus-high-energy.xlsx',
									 sheet_name='Sheet1',
									 Lcdate_format=None)

	launcher1 = Launcher('SLS Block 1',
						 datafile='../launcher-data/sls-block-1.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)

	def test_plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self):
		self.interplanetary1.plot_Avinf_vs_launch_date_with_launch_mass_colorbar(launcherObj=self.launcher1)


class Test_Interplanetary_Uranus_High_Energy_SLS_Block_1B:
	interplanetary1 = Interplanetary(ID="Uranus High Energy",
									 datafile='../interplanetary-data-private/uranus/uranus-high-energy.xlsx',
									 sheet_name='Sheet1',
									 Lcdate_format=None)

	launcher1 = Launcher('SLS Block 1B',
						 datafile='../launcher-data/sls-block-1B.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)

	def test_plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self):
		self.interplanetary1.plot_Avinf_vs_launch_date_with_launch_mass_colorbar(launcherObj=self.launcher1)



class Test_Interplanetary_Uranus_High_Energy_SLS_Block_1B_with_kick:
	interplanetary1 = Interplanetary(ID="Uranus High Energy",
									 datafile='../interplanetary-data-private/uranus/uranus-high-energy.xlsx',
									 sheet_name='Sheet1',
									 Lcdate_format=None)

	launcher1 = Launcher('SLS Block 1B with kick stage',
						 datafile='../launcher-data/sls-block-1B-with-kick.csv')

	def test_load_data(self):
		assert self.interplanetary1.df is not None

	def test_compute_launch_capability(self):
		ans =  self.interplanetary1.compute_launch_capability(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_launch_date(self):
		self.interplanetary1.plot_launch_mass_vs_launch_date(launcherObj=self.launcher1)

	def test_plot_TOF_vs_launch_date(self):
		self.interplanetary1.plot_TOF_vs_launch_date()

	def test_plot_Avinf_vs_launch_date(self):
		self.interplanetary1.plot_Avinf_vs_launch_date()

	def test_plot_launch_mass_vs_TOF(self):
		self.interplanetary1.plot_launch_mass_vs_TOF(launcherObj=self.launcher1)

	def test_plot_launch_mass_vs_TOF_with_vinf_colorbar(self):
		self.interplanetary1.plot_launch_mass_vs_TOF_with_vinf_colorbar(launcherObj=self.launcher1)

	def test_plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self):
		self.interplanetary1.plot_Avinf_vs_launch_date_with_launch_mass_colorbar(launcherObj=self.launcher1)




