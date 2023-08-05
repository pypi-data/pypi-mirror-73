#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment.
# https://cortix.org

import logging

import numpy as np
import scipy.constants as const
from scipy.integrate import odeint

from cortix import Module
from cortix.support.phase_new import PhaseNew as Phase
from cortix import Quantity

class BWR(Module):
    '''
    Boiling water reactor single-point reactor.

    Notes
    -----
    These are the `port` names available in this module to connect to respective
    modules: `turbine`, and `pump`.
    See instance attribute `port_names_expected`.

    '''

    def __init__(self, params):
        '''
        Parameters
        ----------
        params: dict
            All parameters for the module in the form of a dictionary.

        '''

        super().__init__(ode_params, self):

        self.port_names_expected = ['coolant-inflow','coolant-outflow']

        quantities      = list()
        self.ode_params = dict()

        self.initial_time = 0.0 * const.day
        self.end_time     = 4 * const.hour
        self.time_step    = 10 * const.second
        self.show_time    = (False,10*const.second)

        self.log = logging.getLogger('cortix')

        # Coolant inflow phase history
        quantities = list()

        flowrate = Quantitiy(name='inflow-cool-flowrate',
                   formalName='Inflow Cool. Flowrate',
                   unit='kg/s', value=0.0)
        quantities.append(flowrate)

        temp = Quantitiy(name='inflow-cool-temp', formalName='Inflow Cool. Temperature',
               unit='K', value=0.0)
        quantities.append(temp)

        press = Quantitiy(name='inflow-cool-press',formalName='Inflow Cool. Pressure',
                unit='Pa', value=0.0)
        quantities.append(press)

        self.coolant_inflow_phase = Phase(self.initial_time, time_unit='s',
                quantities=quantities)

        # Coolant outflow phase history
        quantities = list()

        flowrate = Quantitiy(name='outflow-cool-flowrate',
                   formalName='Outflow Cool. Flowrate',
                   unit='kg/s', value=0.0)
        quantities.append(flowrate)

        temp = Quantitiy(name='outflow-cool-temp',
                   formalName='Outflow Cool. Temperature',
                   unit='K', value=0.0)
        quantities.append(temp)

        press = Quantitiy(name='outflow-cool-press',formalName='Outflow Cool. Pressure',
                   unit='Pa', value=0.0)
        quantities.append(press)

        quality = Quantitiy(name='steam-quality',formalName='Steam Quality',
                   unit='', value=0.0)
        quantities.append(quality)

        self.coolant_outflow_phase = Phase(self.initial_time, time_unit='s',
                quantities=quantities)

        # Neutron phase history
        quantities = list()

        neutron_dens = Quantitiy(name='neutron-dens',
                   formalName='Neutron Dens.',
                   unit='1/m^3', value=0.0)
        quantities.append(neutron_dens)

        delayed_neutrons_0 = np.zeros(6)

        delayed_neutron_cc = Quantitiy(name='delayed-neutrons-cc',
                   formalName='Delayed Neutrons',
                   unit='1/m^3', value=delayed_neutrons_0)
        quantities.append(delayed_neutron_cc)

        self.neutron_phase = Phase(self.initial_time, time_unit='s',
                quantities=quantities)

        #self.population_phase.SetValue('f0g', f0g_0, self.initial_time)

        #reactor paramaters
        quantities = list()

        fuel_temp = Quantity(name='fuel-temp', formalName='Fuel Temp.', unit='k', value=273.15)

        quantities.append(fuel_temp)

        reg_rod_position = Quantity(name='reg-rod-position', formalName='Regulating Rod Position', unit='m', value=0.0)

        quantities.append(reg_rod_position)

        self.reactor_phase = Phase(self.initial_time, time_unit='s', quantities=quantities)

        self.ode_params = ode_params

        # Initialize inflows to zero
        #self.ode_params['prison-inflow-rates']       = np.zeros(self.n_groups)
        #self.ode_params['parole-inflow-rates']       = np.zeros(self.n_groups)
        #self.ode_params['arrested-inflow-rates']     = np.zeros(self.n_groups)
        #self.ode_params['jail-inflow-rates']         = np.zeros(self.n_groups)
        #self.ode_params['adjudication-inflow-rates'] = np.zeros(self.n_groups)
        #self.ode_params['probation-inflow-rates']    = np.zeros(self.n_groups)

        return

    def run(self, *args):

       # self.__zero_ode_parameters()

        time = self.initial_time

        while time < self.end_time:

            if self.show_time[0] and abs(time%self.show_time[1]-0.0)<=1.e-1:
                self.log.info('time = '+str(round(time/const.minute,1)))

            # Communicate information
            #------------------------

            self.__call_ports(time)

            # Evolve one time step
            #---------------------

            time = self.__step( time )

    def __call_input_ports(self, time):

        # Interactions in the coolant-inflow port
        #----------------------------------------
        # one way "from" coolant-inflow

        # from
        self.send( time, 'coolant-inflow' )
        (check_time, inflow_state) = self.recv('coolant-inflow')
        assert abs(check_time-time) <= 1e-6

        inflow = self.coolant_inlet_phase.GetRow(time)
        self.coolant_inlet_phase.AddRow(time, inflow)
        self.coolant_inlet_phase.SetValue('inflow-cool-temp', inflow_state['inflow-cool-temp'], time)

    def __call_output_ports(self, time):
        # Interactions in the coolant-outflow port
        #-----------------------------------------
        # one way "to" coolant-outflow

        # to be, or not to be?
        message_time = self.recv('coolant-outflow')
        outflow_state = dict()
        outflow_cool_temp = self.coolant_outflow_phase.GetValue('outflow-cool-temp', time)

        outflow_state['outflow-cool-temp'] = outflow_cool_temp
        self.send( (message_time, outflow_state), 'coolant-outflow' )
        self.send( (message_time, outflow_state), 'coolant-inflow')

    def __step(self, time=0.0):
        r'''
        ODE IVP problem:
        Given the initial data at :math:`t=0`,
        :math:`u = (u_1(0),u_2(0),\ldots)`
        solve :math:`\frac{\text{d}u}{\text{d}t} = f(u)` in the interval
        :math:`0\le t \le t_f`.

        Parameters
        ----------
        time: float
            Time in SI unit.

        Returns
        -------
        None

        '''
        import iapws.iapws97 as steam

        # Get state values
        u_0 = self.__get_state_vector( time )

        t_interval_sec = np.linspace(0.0, self.time_step, num=2)

        (u_vec_hist, info_dict) = odeint( self.__f_vec,
                                          u_0, t_interval_sec,
                                          args=( self.params, ),
                                          rtol=1e-4, atol=1e-8, mxstep=200,
                                          full_output=True )

        assert info_dict['message'] =='Integration successful.', info_dict['message']

        u_vec = u_vec_hist[1,:]  # solution vector at final time step

        n_dens = u_vec[0]
        c_vec = u_vec[1:5]
        fuel_temp = u_vec[6]
        cool_temp = u_vec[7]

        time += self.time_step

        #update state variables
        outflow = self.coolant_outflow_phase.GetRow(time)
        neutrons = self.neutron_phase.GetRow(time)
        reactor = self.reactor_phase.GetRow(time)

        time += self.time_step

        self.coolant_outflow_phase.AddRow(time, outflow)
        self.neutron_phase.AddRow(time, neutrons)
        self.reactor_phase.AddRow(time, reactor)

        self.coolant_outflow_phase.SetValue('outflow-cool-temp', cool_temp, time)
        self.neutron_phase.SetValue('neutron-dens', n_dens, time)
        self.neutron_phase.SetValue('delayed-neutrons-cc', c_vec, time)
        self.reactor_phase.SetValue('fuel-temp', fuel_temp, time)

        return time

    def __get_state_vector(self, time):
        '''
        Return a numpy array of all unknowns ordered as below:
            neutron density (1), delayed neutron emmiter concentrations (6),
            termperature of fuel (1), temperature of coolant (1).
        '''

        u_list = list()

        u_vec = np.empty(0,dtype=np.float64)

        neutron_dens = self.neutron_phase.get_value('neutron-dens',time)/(const.centi)**3
        u_vec = np.append( u_vec, neutron_dens )

        delayed_neutrons_cc = self.neutron_phase.get_value('delayed-neutrons-cc',time)/(const.centi)**3
        u_vec = np.append( u_vec, delayed_neutrons_cc )

        fuel_temp = self.reactor_phase.GetValue('fuel-temp',time)
        u_vec = np.append( u_vec, fuel_temp)


       # for spc in self.aqueous_phase.species:
            #mass_cc = self.aqueous_phase.get_species_concentration(spc.name,time)
           # mass_cc = self.aqueous_phase.get_species_concentration(spc.name)
           # assert mass_cc is not None
           # u_list.append( mass_cc )
           # spc.flag = idx # the global id of the species
           # idx += 1

       # for spc in self.organic_phase.species:
            #mass_cc = self.organic_phase.get_species_concentration(spc.name,time)
           # mass_cc = self.organic_phase.get_species_concentration(spc.name)
           # assert mass_cc is not None
           # u_list.append( mass_cc )
          #  spc.flag = idx # the global id of the species
         #   idx += 1

       # for spc in self.vapor_phase.species:
            #mass_cc = self.vapor_phase.get_species_concentration(spc.name,time)
           # mass_cc = self.vapor_phase.get_species_concentration(spc.name)
           # assert mass_cc is not None
           # u_list.append( mass_cc )
           # spc.flag = idx # the global id of the species
           # idx += 1

        u_vec = np.array( u_list, dtype=np.float64 )

        # sanity check
        assert not u_vec[u_vec<0.0],'%r'%u_vec

        return u_vec

    def __alpha_tn_func(temp, params, self):
        import math
        import scipy.misc as diff
        import scipy.constants as sc
        import iapws.iapws97 as steam
        import iapws.iapws95 as steam2

        pressure = steam._PSat_T(temp)

        d_rho = steam2.IAPWS95(P=pressure, T=temp-1).drhodT_P

        #d_rho2 = diff.derivative(derivative_helper, temp) # dRho/dTm

        rho = 1 / steam._Region4(pressure, 0)['v'] # mass density, kg/m3

        Nm = ((rho * sc.kilo)/params['mod molar mass']) * sc.N_A * (sc.centi)**3 # number density of the moderator
        d_Nm =  ((d_rho * sc.kilo)/params['mod molar mass']) * sc.N_A * (sc.centi)**3 #dNm/dTm
        d_Nm = d_Nm * sc.zepto * sc.milli

        mod_macro_a = params['mod micro a'] * Nm # macroscopic absorption cross section of the moderator
        mod_macro_s = params['mod micro s'] * Nm # macroscopic scattering cross section of the moderator

        F = params['fuel macro a']/(params['fuel macro a'] + mod_macro_a) # thermal utilization, F
    #dF/dTm
        d_F = -1*(params['fuel macro a'] * params['mod micro a'] * d_Nm)/(params['fuel macro a'] + mod_macro_a)**2

        # Resonance escape integral, P
        P = math.exp((-1 * params['n fuel'] * (params['fuel_volume']) * params['I'])/(mod_macro_s * 3000))
        #dP/dTm
        d_P = P * (-1 * params['n fuel'] * params['fuel_volume'] * sc.centi**3 * params['mod micro s'] * d_Nm)/(mod_macro_s * 3000 * sc.centi**3)**2

        Eth = 0.0862 * temp # convert temperature to energy in MeV
        E1 = mod_macro_s/math.log(params['E0']/Eth) # neutron thermalization macroscopic cross section

        Df = 1/(3 * mod_macro_s * (1 - params['mod mu0'])) # neutron diffusion coefficient
        tau = Df/E1 # fermi age, tau
        #dTau/dTm
        d_tau = (((0.0862 * (Eth/params['E0'])) * 3 * Nm) - math.log(params['E0']/Eth) * (params['mod micro s'] * d_Nm))/((3 * Nm)**2 * (1 - params['mod mu0']))

        L = math.sqrt(1/(3 * mod_macro_s * mod_macro_a * (1 - params['mod mu0']))) # diffusion length L
        # dL/dTm
        d_L = 1/(2 * math.sqrt((-2 * d_Nm * sc.zepto * sc.milli)/(3 * params['mod micro s'] * params['mod micro a'] * (Nm * sc.zepto * sc.milli)**3 * (1 - params['mod mu0']))))

        # left term of the numerator of the moderator temperature feedback coefficient, alpha
        left_1st_term = d_tau * (params['buckling']**2 + L**2 * params['buckling']**4) #holding L as constant
        left_2nd_term = d_L * (2 * L * params['buckling']**2 + 2 * L * tau * params['buckling']**4) # holding tau as constant
        left_term = (P * F) * (left_1st_term + left_2nd_term) # combining with P and F held as constant

        # right term of the numerator of the moderator temperature feedback coefficient, alpha

        right_1st_term = (-1) * (1 + ((tau + L**2) * params['buckling']**2) + tau * L**2 * params['buckling']**4) # num as const
        right_2nd_term = F * d_P # holding thermal utilization as constant
        right_3rd_term = P * d_F # holding resonance escpae as constant
        right_term = right_1st_term * (right_2nd_term + right_3rd_term) # combining all three terms together

        # numerator and denominator
        numerator = left_term + right_term
        denominator = params['eta'] * params['epsilon'] * (F * P)**2

        alpha_tn = numerator/denominator


        alpha_tn = alpha_tn/3
        return alpha_tn

    def __rho_func( t, n_dens, temp, params, self ):
        '''
        Reactivity function.

        Parameters
        ----------
        t: float, required
            Time.
        temp_f: float, required
            Temperature at time t.
        params: dict, required
            Dictionary of quantities. It must have a `'rho_0'` key/value pair.

        Returns
        -------
        rho_t: float
            Value of reactivity.

        Examples
        --------
        '''

        rho_0  = params['rho_0']
        temp_ref = params['temp_0']
        n_dens_ss_operation = params['n_dens_ss_operation']
        alpha_n = params['alpha_n']

        if temp < 293.15: # if temperature is less than the starting temperature then moderator feedback is zero
            alpha_tn = 0

        else:
            alpha_tn = self.__alpha_tn_func(temp , self.params) #alpha_tn_func(temp, params)

        if t > params['malfunction start'] and t < params['malfunction end']: # reg rod held in position; only mod temp reactivity varies with time during malfunction
            alpha_n = params['alpha_n_malfunction']
            rho_t = rho_0 + alpha_n + alpha_tn * (temp - temp_ref)

        elif t > params['shutdown time']: # effectively the inverse of startup; gradually reduce reactivity and neutron density.
            rho_0 = -1 * n_dens * rho_0
            alpha_n = rho_0 - (alpha_tn * (temp - temp_ref))
            rho_t = rho_0

        elif n_dens < 1e-5: #controlled startup w/ blade; gradually increase neutron density to SS value.
            #rho_current = (1 - n_dens) * rho_0
            #alpha_n = rho_current - rho_0 - alpha_tn * (temp - temp_ref)
            #rho_t = rho_current
            #params['alpha_n_malfunction'] = alpha_n
            rho_t = rho_0

        else:
            rho_current = (1 - n_dens) * rho_0
            alpha_n = rho_current - rho_0 - alpha_tn * (temp - temp_ref)
            rho_t = rho_current
            params['alpha_n_malfunction'] = alpha_n
        #print(n_dens)

        return (rho_t, alpha_n, alpha_tn * (temp - temp_ref))

    def __q_source( t, params, self ):
        '''
        Neutron source delta function.

        Parameters
        ----------
        t: float, required
            Time.
        params: dict, required
            Dictionary of quantities. It must have a `'q_0'` key/value pair.

        Returns
        -------
        q: float
            Value of source.

        Examples
        --------
        '''
        q_0 = params['q_0']

        if t <= 1e-5: # small time value
            q = q_0
        else:
            q = 0.0
            params['q_source_status'] = 'out'

        return q

    def __sigma_fis_func( temp, params, self ):
        '''
        Place holder for implementation
        '''

        sigma_f = params['sigma_f_o']  * math.sqrt(298/temp) * math.sqrt(math.pi) * 0.5

        return(sigma_f)

    def __nuclear_pwr_dens_func( time, temp, n_dens, params, self ):
        '''
        Place holder for implementation
        '''
        n_dens = n_dens + self.__q_source(time, self.params) # include the neutrons from the initial source

        rxn_heat = params['fis_energy'] # get fission reaction energy J per reaction

        sigma_f = self.__sigma_fis_func( temp, self.params ) # m2

        fis_nuclide_num_dens = params['fis_nuclide_num_dens_fake'] #  #/m3

        Sigma_fis = sigma_f * fis_nuclide_num_dens # macroscopic cross section

        v_o = params['thermal_neutron_velo'] # m/s

        neutron_flux = n_dens * 4.5e14 * v_o

         #reaction rate density
        rxn_rate_dens = Sigma_fis * neutron_flux

        # nuclear power source
        q3prime = - rxn_heat * rxn_rate_dens # exothermic reaction W/m3
        #q3prime = - n_dens * 3323E6
        #print("q3prime")
        #print(q3prime)

        return q3prime

    def __heat_sink_rate( time, temp_f, temp_c, params, self):

        ht_coeff = params['ht_coeff']

        q_f = - ht_coeff * (temp_f - temp_c)
        #print(q_f)
        return q_f

    def __f_vec(time, u_vec, params, self):

        num_negatives = u_vec[u_vec < 0]
        if num_negatives.any() < 0:
            assert np.max(abs(u_vec[u_vec < 0])) <= 1e-8, 'u_vec = %r'%u_vec
        #assert np.all(u_vec >= 0.0), 'u_vec = %r'%u_vec

        q_source_t = self__.q_source(time, self.params)

        n_dens = u_vec[0] # get neutron dens

        c_vec = u_vec[1:-2] # get delayed neutron emitter concentration

        temp_f = u_vec[-2] # get temperature of fuel

        temp_c = u_vec[-1] # get temperature of coolant

        # initialize f_vec to zero 
        species_decay = params['species_decay']
        lambda_vec = np.array(species_decay)
        n_species  = len(lambda_vec)

        f_tmp = np.zeros(1+n_species+2,dtype=np.float64) # vector for f_vec return

        #----------------
        # neutron balance
        #----------------
        rho_t = self.__rho_func(time, n_dens, temp_c, self.params)[0]

        beta = params['beta']
        gen_time = params['gen_time']

        species_rel_yield = params['species_rel_yield']
        beta_vec = np.array(species_rel_yield) * beta

        assert len(lambda_vec)==len(beta_vec)

        f_tmp[0] = (rho_t - beta)/gen_time * n_dens + lambda_vec @ c_vec + q_source_t
        #if f_tmp[0] < 0 and time < params['shutdown time'] and n_dens < 1:
            #f_tmp[0] = 0

        #-----------------------------------
        # n species balances (implicit loop)
        #-----------------------------------
        f_tmp[1:-2] = beta_vec/gen_time * n_dens - lambda_vec * c_vec

        #--------------------
        # fuel energy balance
        #--------------------
        rho_f = params['fuel_dens']
        cp_f = params['cp_fuel']
        vol_fuel = params['fuel_volume']

        pwr_dens = self.__nuclear_pwr_dens_func( time, (temp_f+temp_c)/2, n_dens, self.params)

        heat_sink = self.__heat_sink_rate( time, temp_f, temp_c, self.params)

        #assert heat_sink <= 0.0,'heat_sink = %r'%heat_sink

        f_tmp[-2] =  -1/rho_f/cp_f * ( pwr_dens - heat_sink/vol_fuel )
        #-----------------------
        # coolant energy balance
        #-----------------------
        rho_c    = params['coolant_dens']
        cp_c     = params['cp_coolant']
        vol_cool = params['coolant_volume']

        # subcooled liquid
        turbine_calcs = turbine(time, temp_c,  params)
        t_runoff = turbine_calcs[0]
        x_runoff = turbine_calcs[2] #run the turbine, take the runoff and pass to condenser
        condenser_out = condenser(time, t_runoff, x_runoff, temp_c, params) #run the condenser, pass runoff to the pump
        pump_out = pump(time, condenser_out, temp_c, params) #run the pump, runoff returns to reactor as temp_in
        #print("time is ", time, "and inlet temperature is", temp_in, "\n")

        tau = params['tau_fake']

        heat_source = heat_sink
        temp_in = pump_out

        f_tmp[-1] = - 1/tau * (temp_c - temp_in) - 1./rho_c/cp_c/vol_cool * heat_source

        # pressure calculations

        #print(time)
        #print(u_vec)
        return f_tmp

    def __compute_outflow_rates(self, time, name):

        f0g = self.population_phase.GetValue('f0g',time)

        if name == 'arrested':

            c0rg = self.ode_params['commit-to-arrested-coeff-grps']
            m0rg = self.ode_params['commit-to-arrested-coeff-mod-grps']

            c00g = self.ode_params['general-commit-to-arrested-coeff-grps']
            m00g = self.ode_params['general-commit-to-arrested-coeff-mod-grps']

            f0 = self.ode_params['non-offender-adult-population']

            # Recidivism
            outflow_rates = c0rg * m0rg * np.abs(f0g) + c00g * m00g * f0

        return outflow_rates

    def __zero_ode_parameters(self):
        '''
        If ports are not connected the corresponding outflows must be zero.

        '''

        zeros = np.zeros(self.n_groups)

        p_names = [p.name for p in self.ports]

        if 'arrested' not in p_names:
            self.ode_params['commit-to-arrested-coeff-grps']     = zeros
            self.ode_params['commit-to-arrested-coeff-mod-grps'] = zeros

            self.ode_params['general-commit-to-arrested-coeff-grps']     = zeros
            self.ode_params['general-commit-to-arrested-coeff-mod-grps'] = zeros

        return
