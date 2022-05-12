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



class Test_Interplanetary_Uranus_High_Energy:
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





