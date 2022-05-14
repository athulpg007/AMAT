# SOURCE FILENAME : interplanetary.py
# AUTHOR          : Athul Pradeepkumar Girija, athulpg007@gmail.com
# DATE CREATED    : 05/13/2022, 19:02 MT
# DATE MODIFIED   : 05/13/2022, 19:03 MT
# REMARKS         : Selection of a feasible interplanetary trajectory from
#					a database for mission studies.


import pandas as pd
import matplotlib.pyplot as plt

from AMAT.launcher import Launcher

class Interplanetary:
	"""
	Stores a dataframe containing interplanetary data from an external source.

	Attributes
	----------
	ID : str
		string identifier for the interplanetary dataset
	datafile : filepath
		Excel file containing interplanetary trajectory data
	sheet_name : str
		Sheet name containing trajectory data
	df : pandas.DataFrame object
		dataframe containing the interplanetary trajectory data
	Lcdate : pandas.Series
		Series containing launch date datetime objects
	C3 : pandas.Series
		Series containing launch C3
	TOF : pandas.Series
		Series containing time of flight, years
	Avinf : pandas.Series
		Series containing arrival vinf magnitude, km/s
	"""

	def __init__(self, ID, datafile, sheet_name, Lcdate_format):
		"""

		Parameters
		----------
		ID : str
			string identifier for the interplanetary dataset
		datafile : filepath
			Excel file containing interplanetary trajectory data
		sheet_name : str
			Sheet name containing trajectory data
		Lcdate_format : str
			strftime() for launch date format e.g. "%Y%m%d"
		"""
		self.ID = ID
		self.datafile = datafile
		self.sheet_name = sheet_name

		self.df = pd.read_excel(self.datafile, sheet_name=sheet_name)
		self.Lcdate = pd.to_datetime(list(map(str, self.df['Lcdate'].values)), format=Lcdate_format)
		self.C3 = self.df["LC3"]
		self.TOF = self.df["TOF"]
		self.Avinf = self.df["Avinf"]

	def compute_launch_capability(self, launcherObj):
		"""
		Parameters
		----------
		launcherObj : AMAT.launcher.Launcher object

		Returns
		-------
		ans : numpy.ndarray
			array containing the launch mass capability for C3 values in the
			trajectory dataset
		"""
		return launcherObj.launchMass(self.C3)

	def plot_launch_mass_vs_launch_date(self, launcherObj):
		"""
		Scatter plot of the launch capability as a function of launch date.

		Parameters
		----------
		launcherObj : AMAT.launcher.Launcher object
			AMAT Launcher object

		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter of the launch capability as a function of launch date
		"""
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

		plt.savefig('../plots/'+self.ID+"_"+launcherObj.ID+"_"+"launch_mass_vs_launch_date"+'.png', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/'+self.ID+"_"+launcherObj.ID+"_"+"launch_mass_vs_launch_date"+'.pdf', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/'+self.ID+"_"+launcherObj.ID+"_"+"launch_mass_vs_launch_date"+'.eps', dpi=300, bbox_inches='tight')

		plt.show()

	def plot_TOF_vs_launch_date(self):
		"""
		Scatter plot of the time of flight as a function of launch date.

		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter of the launch capability as a function of launch date
		"""

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

		plt.savefig('../plots/' + self.ID + "_" + "TOF_vs_launch_date" + '.png', dpi=300,  bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "TOF_vs_launch_date" + '.pdf', dpi=300,  bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "TOF_vs_launch_date" + '.eps', dpi=300,  bbox_inches='tight')

		plt.show()

	def plot_Avinf_vs_launch_date(self):
		"""
		Scatter plot of the arrival vinf magnitude as a function of launch date.

		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter of the arrival vinf magnitude as a function of launch date
		"""

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

		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date" + '.png', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date" + '.pdf', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date" + '.eps', dpi=300, bbox_inches='tight')

		plt.show()

	def plot_Avinf_vs_launch_date_with_launch_mass_colorbar(self, launcherObj, scale=20):
		"""
		Scatter plot of the arrival vinf magnitude as a function of launch date
		with launch capability colorbar.

		Parameters
		-------
		launcherObj : AMAT.launcher.Launcher object
			AMAT Launcher object
		scale : float
			scatter plot marker size, defaults to 20


		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter of the arrival vinf magnitude as a function of launch date
			with launch capability colorbar.

		"""

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

		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date_launch_mass_colorbar" + '.png', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date_launch_mass_colorbar" + '.pdf', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "Avinf_vs_launch_date_launch_mass_colorbar" + '.eps', dpi=300, bbox_inches='tight')

		plt.show()



	def plot_launch_mass_vs_TOF(self, launcherObj):
		"""
		Scatter plot of the launch mass as a function of TOF.

		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter plot of the launch mass as a function of TOF.
		"""
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

		plt.savefig('../plots/' + self.ID + "_" + launcherObj.ID + "_" + "launch_mass_vs_TOF" + '.png', dpi=300, box_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + launcherObj.ID + "_" + "launch_mass_vs_TOF" + '.pdf', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + launcherObj.ID + "_" + "launch_mass_vs_TOF" + '.eps', dpi=300, bbox_inches='tight')

		plt.show()



	def plot_launch_mass_vs_TOF_with_vinf_colorbar(self, launcherObj, scale=20):
		"""
		Scatter plot of the launch mass as a function of TOF
		with arrival vinf colorbar.

		Parameters
		-------
		launcherObj : AMAT.launcher.Launcher object
			AMAT Launcher object
		scale : float
			scatter plot marker size, defaults to 20


		Returns
		-------
		ans : matplotlib.figure.Figure
			Scatter plot of the launch mass as a function of TOF
			with arrival vinf colorbar.

		"""

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

		plt.savefig('../plots/' + self.ID + "_" + "launch_mass_vs_TOF_Avinf_colorbar" + '.png', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "launch_mass_vs_TOF_Avinf_colorbar" + '.pdf', dpi=300, bbox_inches='tight')
		plt.savefig('../plots/' + self.ID + "_" + "launch_mass_vs_TOF_Avinf_colorbar" + '.eps', dpi=300, bbox_inches='tight')

		plt.show()

