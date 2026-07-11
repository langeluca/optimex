import bw2data as bd
from typing import Literal

DEFAULT_PROJECT = "optimex_remind"
DEFAULT_ECOINVENT_DB = "ecoinvent-3.12-cutoff"
DEFAULT_BIOSPHERE_DB = "ecoinvent-3.12-biosphere"
DEFAULT_CUSTOM_DB = "disco2very"

# Backwards-compatible module globals. They are configured when MyActivities is
# instantiated, so importing this module does not switch Brightway projects.
eidb = None
bsdb = None
disco2very = None

class MyActivities():
    """
    This class contains all the activities created by hand. The activities are generically stored in the database "disco2very".
    """

    def __init__(
        self,
        project: str = DEFAULT_PROJECT,
        ecoinvent_db: str = DEFAULT_ECOINVENT_DB,
        biosphere_db: str = DEFAULT_BIOSPHERE_DB,
        custom_db: str = DEFAULT_CUSTOM_DB,
        set_current: bool = True,
    ):
        """
        Initialize the class with a specified database.

        Parameters:
        project:
            Brightway project to use.
        ecoinvent_db:
            Name of the ecoinvent technosphere database.
        biosphere_db:
            Name of the biosphere database.
        custom_db:
            Name of the database where generated disco2very activities are stored.
        set_current:
            If True, switch Brightway to ``project`` during initialization.
        """

        if set_current:
            bd.projects.set_current(project)

        self.project = project
        self.ecoinvent_db_name = ecoinvent_db
        self.biosphere_db_name = biosphere_db
        self.custom_db_name = custom_db

        self.eidb = bd.Database(ecoinvent_db)
        self.bsdb = bd.Database(biosphere_db)
        self.db = bd.Database(custom_db)
        if custom_db not in bd.databases:
            self.db.register()

        global eidb, bsdb, disco2very
        eidb = self.eidb
        bsdb = self.bsdb
        disco2very = self.db
        
        # DEFINITION OF THE DEFAULT ACTIVITIES
        # electricity
        self.electricity = eidb.get(name="market for electricity, medium voltage", location="DE")
        # Cooling energy, at - 30 °C
        self.coolmin30 = self.db.get(name="cooling energy production, at -30 °C, propylene compression refrigeration system 1 MW", location="GLO")
        # Cooling energy, at - 75 °C
        self.coolmin75 = self.db.get(name="cooling energy production, at -75 °C", location="GLO")
        # Cooling energy, at 5 °C
        self.cool5 = eidb.get(name="market for cooling energy", location="GLO")
        # Cooling energy, at -15 °C
        self.coolmin15 = eidb.get(name="market for cooling energy, at -15 °C", location="GLO")
        # Cooling energy, at - 25 °C
        self.coolmin25 = eidb.get(name="cooling energy production, at -25 °C, propylene compression refrigeration system 1 MW", location="GLO")
        # Cooling energy, at -45 °C
        self.coolmin45 = eidb.get(name="market for cooling energy, at -45 °C", location="GLO")
        # Cooling energy, at -55 °C
        self.coolmin55 = eidb.get(name="market for cooling energy, at -55 °C", location="GLO")
        # Wastewater
        self.wastewater = eidb.get(name="market for wastewater, unpolluted", location="RoW")
        # Methanol
        self.methanol = eidb.get(name="methanol production, from natural gas reforming", location="DE")
        # How to adress the product flows?? -> negative technosphere exchanges  
        # propylene
        self.propylene = eidb.get(name="market for propylene", location="RER w/o RU")
        # lpg
        self.lpg = eidb.get(name="market for liquefied petroleum gas", location="Europe without Switzerland")
        # butene
        self.butene = eidb.get(name="market for butene, mixed", location="RER w/o RU")
        # pentene (modelled as pentane)
        self.pentene = eidb.get(name="market for pentane", location="GLO")
        # methane / NG
        self.methane =eidb.get(name="market for natural gas, high pressure", location="DE")
        # propane
        self.propane =eidb.get(name="market for propane", location="RoW")
        # coke
        self.coke = eidb.get(name="market for coke", location="RoW")
        # avoided burden
        self.avoidedburden = "none"
        # allocation category
        self.allocation = "none"
        # consideration of end-ol-life
        self.eol = "no"
        # CO2 defined as the biosphere activity "carbon dioxide, fossil" in compartment "air" and subcompartment "urban air close to ground"
        self.CO2 = bsdb.get("f9749677-9c9f-4678-ab55-c607dfdc2cb9")
        # H2O emissions defined as the biosphere activity "Water" in air [m³]
        self.H2O = bsdb.get("075e433b-4be4-448e-9510-9a5029c1ce94")
        # Construction of chemical factory as "chemical factory construction, organics" [unit]
        self.factory = eidb.get(name="chemical factory construction, organics", location="RER")
        # Industrial use of CO2 as the technosphere activity "market for carbon dioxide, in chemical industry, GLO" [kg]
        self.carbon_dioxide = eidb.get(name="market for carbon dioxide, in chemical industry", location="GLO")
        # Hydrogen use as "market for hydrogen, gaseous, low pressure, RER" [kg]
        self.hydrogen = eidb.get(name="market for hydrogen, gaseous, low pressure", location="RER")
        # Oxygen use as "market for oxygen, liquid, RER" [kg]
        self.oxygen = eidb.get(name="market for oxygen, liquid", location="RER")
        # Heat as "heat production, natural gas, at industrial furnace >100kW, Europe without Switzerland" [MJ]
        self.heat = eidb.get(name="heat production, natural gas, at industrial furnace >100kW", location="Europe without Switzerland")
        # Carbon monoxide as "market for carbon monoxide, RER [kg]"
        self.carbon_monoxide = eidb.get(name="market for carbon monoxide", location="RER")

    def _get_existing_activity(self, code):
        return bd.get_activity((self.custom_db_name, code))



    def create_MTO(self, avoidedburden: Literal["none", "half", "full"], allocation: Literal["none", "weight", "LHV", "carbon"],
                   eol: Literal["yes", "no"], electricity=None, coolmin30=None, coolmin75=None, coolmin25=None, cool5=None,
                   wastewater=None, methanol=None, propylene=None, pentene=None, methane=None, propane=None, coke=None,
                   butene=None, factory=None):
        """
        
        Create the activity "MTO" in the database "disco2very". The reference output is 1 kg of ethylene.
        Flows are based on [Dimian & Bildea, Energy efficient methanol-to-olefins process, 2017].
        User can define the activities linked to it, but not the amounts.
        Excess heat is not modelled, since no avoided burden is considered for it.
        
        With the definition of the parameter avoidedburden, it can decided if no avoided burden is considered (none), if 50 % of its impact
         is considered (half), or if all of it is considered (full).
        
        The parameter allocation is used to define if no allocation is considered (none), or if it is used, being based on weight (weight),
          the lower heating value (LHV) or the carbon content of the products (carbon).
        
        The parameter eol is used to define if the end-of-life of the product is considered (yes) or not (no). It is modeled as the
        stochiometrical oxidation of ethylene C2H2 + 3 O2 = 2 CO2 + 2 H20.



        Default parameters:
        - avoidedburden: none
        - allocation: none
        - eol: no
        - inputs:
            - electricity: german grid electricity, medium voltage:
                0,0595 kWh_el/kg_methanol * 1/0,167222 kg_methanol/kg_eth = 0,3570 kWh_el/kg_eth
            - cooling:  list of cooling demand by temperature level:
                - T = -30°C: (10700 kW)/(1000000 kg/h)*3,6 MJ/kWh = 0.3852 MJ/kg_MetOH * 1/0,16722 kg_MetOH/kg_eth = 2,304 MJ/kg_eth.
                    The reference uses two-stage propane refrigeration system. The closest in ecoinvent is one stage propylene refrigeration. 
                - T = -75°C: (2500 kW)/(1000000 kg/h)*3,6 MJ/kWh = 0.09 MJ/kg_methanol * 1/0,16722 kg_MetOH/kg_eth = 0,5382 MJ/kg_eth.
                    The reference uses a cascade of propane and ethylene refrigeration. The closest in ecoinvent is
                    "market for cooling energy, at -100°C".
                - T = -25°C: (5000 kW)/(1000000 kg/h)*3,6 MJ/kWh = 0.18 MJ/kg_methanol * 1/0,16722 kg_methanol/kg_eth = 1,076 MJ/kg_eth.
                    The reference uses an ammonia absorption chiller, which is not modelled in ecoinvent. The activity used is
                    "market for cooling energy, at -25°C".
                - T = 5°C: (2000 kW)/(1000000 kg/h)*3,6 MJ/kWh = 0.072 MJ/kg_methanol * 1/0,16722 kg_methanol/kg_eth = 0,4306 MJ/kg_eth.
                    The reference uses an ammonia absorption chiller, which is not modelled in ecoinvent. The activity used is
                    "market for cooling energy".
            - methanol: methanol production, from natural gas reforming, RER: 1 kg_methanol/0,16722 kg_eth = 5,9801 kg_MetOH/kg_eth
            - factory: chemical factory construction, organics, RER: 8.96e-12 kg_factory/kg_eth
        - outputs:
            - ethylene: market for ethylene: 1 kg_eth. Reference product.
            - propylene: market for propylene, RER: 1_kg_prop/kg_eth
            - pentene: market for pentane, GLO: 
                0,01672 kg_pentene/kg_methanol * 1/0,167222 kg_methanol/kg_eth * 72/70 kg_pentane/kg_pentene = 0,102844841 kg_pentane/kg_eth
            - Methane: market for natural gas, high pressure; DE:
                0,5 kg_methane/kg_fuel * 0,0209 kg_fuel/kg_methanol * 1/0,167222 kg_methanol/kg_eth * (8,314*288,15/(101,3*16)) m³_ng/kg_methane = 0,092369222 m³_ng/kg_eth
            - propane: market for propane; GLO: 
                0,5 kg_propane/kg_fuel * 0,0209 kg_fuel/kg_methanol * 1/0,167222 kg_methanol/kg_eth = 0,062492525 kg_propane/kg_eth
            - butene: market for butene, mixed; RER: 0,04599 kg_butene/kg_methanol * 1/0,167222 kg_methanol/kg_eth = 0,275026911 kg_butene/kg_eth
            - coke: market for coke, RoW:
                0,04762 kg_coke/kg_methanol * 1/0,16722 kg_methanol/kg_eth * 28,6 MJ_coke/kg_coke = 8,144552087 MJ_coke/kg_eth
            - wastewater: market for wastewater, unpolluted, RoW:
                0,53432 kg_w/kg_meth * 1e-3 m_w³/kg_w * 1/0,167222 kg_methanol/kg_eth = 0,003195 m_w³/kg_eth


        - SUM of considered products: 1 kg_eth + 1 kg_prop + 0,1 kh_pentene + 0,0625 kg_ng + 0,0625 kg_propane + 0,2750 kg_butene = 2,4946 kg_eth
            - mass share of ethylene among the considered products: 1 kg_eth / 2,4946 kg_eth = 0,40087

        LHV of the products:
            - ethylene: 47,195 MJ/kg (at 25 °C; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            - propylene: 45,799 MJ/kg (at 25 °C; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            - pentene: 45,031 MJ/kg (at 25 °C; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            - methane: 50,009 MJ/kg (at 25 °C; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            - propane: 46,357 MJ/kg (at 25 °C; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            - butene: 45,334 MJ/kg (at 25 °C for 1-Butene; source: https://www.chemeurope.com/en/encyclopedia/Heat_of_combustion.html)
            
            
        Total heat value in each product flow:
            - ethylene: 47,195 MJ/kg * 1 kg_eth = 47,195 MJ
            - propylene: 45,799 MJ/kg * 1 kg_prop = 45,799 MJ
            - pentene: 45,031 MJ/kg * 0,09998804 kg_pentene = 4,502561416 MJ
            - methane: 50,009 MJ/kg * 0,062492525 kg_ng = 3,125188674 MJ
            - propane: 46,357 MJ/kg * 0,062492525 kg_propane = 2,896965973 MJ
            - butene: 45,334 MJ/kg * 0,275026911 kg_butene = 12,46806997 MJ
            - SUM: 115,986786 MJ



        Returns: The created MTO activity
        """
        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if coolmin30 is None:
            coolmin30 = self.coolmin30
        if coolmin75 is None:
            coolmin75 = self.coolmin75
        if coolmin25 is None:
            coolmin25 = self.coolmin25
        if cool5 is None:
            cool5 = self.cool5
        if wastewater is None:
            wastewater = self.wastewater
        if methanol is None:
            methanol = self.methanol
        if propylene is None:
            propylene = self.propylene
        if pentene is None:
            pentene = self.pentene
        if methane is None:
            methane = self.methane
        if propane is None:
            propane = self.propane
        if coke is None:
            coke = self.coke
        if butene is None:
            butene = self.butene
        if avoidedburden is None:
            avoidedburden = self.avoidedburden
        if allocation is None:
            allocation = self.allocation
        if eol is None:
            eol = self.eol
        if factory is None:
            factory = self.factory



        # Check if avoided burden and allocation are being used simultaneously. If it's the case, raise an error
        if avoidedburden != "none" and allocation != "none":
            raise ValueError("Avoided burden and allocation cannot be used simultaneously. Please set either avoidedburden or allocation to 'none'.")

        # Definition of name and code of the activity, based on the parameters used for its construction
        name=(f"ethylene production, from methanol-to-olefins conversion. Avoided burden: {avoidedburden}; allocation: {allocation}. eol: {eol}")
        code =  (
        f"MTO|ab={avoidedburden}|alloc={allocation}|eol={eol}"
        f"|elec={electricity.key}|methanol={methanol.key}|wastewater={wastewater.key}"
        f"|cool5={cool5.key}|coolmin25={coolmin25.key}|coolmin30={coolmin30.key}|coolmin75={coolmin75.key}"
        f"|propylene={propylene.key}|pentene={pentene.key}|methane={methane.key}"
        f"|propane={propane.key}|coke={coke.key}|butene={butene.key}|factory={factory.key}"
        )
        
        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            mto = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            mto = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the methanol-to-olefins process. The reference product is ethylene and 1 kg is produced. Apart from it, propylene," \
                "pentene, methane, propane, coke and butene are produced. Methanol input: "+ methanol["name"]+". Electricity input: "+electricity["name"]+"." \
                "Wastewater input: "+wastewater["name"]+".Based on the paper [Dimian & Bildea, Energy efficient methanol-to-olefins process, 2017].",
                )

        mto.save()

        # Delete existing exchanges only
        for exc in list(mto.exchanges()):
            exc.delete()
        
        # quantification of the avoided burden as 0, 0.5 or 1, according to the avoidedburden parameter
        if avoidedburden == "none":
            burden_force = 0
        elif avoidedburden == "half":
            burden_force = 0.5
        elif avoidedburden == "full":
            burden_force = 1
        """
        #LHV allocation factors:
        #    - ethylene: 47,195 MJ / 115,987 MJ = 0,40690 this is the factor used for LHV allocation, since ethylene is the reference product.
        #    - propylene: 45,799 MJ / 115,987 MJ = 0,39486
        #    - pentene: 4,502561416 MJ / 115,987 MJ = 0,03882
        #    - methane: 3,125188674 MJ / 115,987 MJ = 0,02694
        #    - propane: 2,896965973 MJ / 115,987 MJ = 0,02498
        #    - butene: 12,46806997 MJ / 115,987 MJ = 0,10750

        Carbon content of the products:
            - ethylene: 2 kmol_C/kmol_eth * 1 kg_eth / (28 kg_eth/kmol_eth) = 0,071429 kmol_C
            - propylene: 3 kmol_C/kmol_prop * 1 kg_prop / (42 kg_prop/kmol_prop) = 0,071429 kmol_C
            - pentene: 5 kmol_C/kmol_pentene * 0,09998804 kg_pentene / (70 kg_pentene/kmol_pentene) = 0,007142003 kmol_C
            - methane: 1 kmol_C/kmol_ch4 * 0,062492525 kg_ch4 / (16 kg_ch4/kmol_ch4) = 0,003905783 kmol_C
            - propane: 3 kmol_C/kmol_propane * 0,062492525 kg_propane / (44 kg_propane/kmol_propane) = 0,004260854 kmol_C
            - butene: 4 kmol_C/kmol_butene * 0,275026911 kg_butene / (56 kg_butene/kmol_butene) = 0,019644779 kmol_C
            - SUM: 0,177810562 kmol_C

        Carbon allocation factors:
            - ethylene: 0,071429 kmol_C / 0,177810562 kmol_C = 0,401711635 this is the factor used for carbon allocation,
                since ethylene is the reference product.
            - propylene: 0,071429 kmol_C / 0,177810562 kmol_C = 0,401711635
            - pentene: 0,007142003 kmol_C / 0,177810562 kmol_C = 0,040166359
            - methane: 0,003905783 kmol_C / 0,177810562 kmol_C = 0,021965978
            - propane: 0,004260854 kmol_C / 0,177810562 kmol_C = 0,023962885
            - butene: 0,019644779 kmol_C / 0,177810562 kmol_C = 0,11048151
"""

        # Definition of the parameter for the allocation use
        if allocation == "none":
            allocation_force = 1 # full process impact is considered
        elif allocation == "weight":
            allocation_force = 0.4 # the mass share of ethylene among the considered hydrocarbons
        elif allocation == "LHV":
            allocation_force = 0.4068998 # the LHV share of ethylene in the total LHV of the products
        elif allocation == "carbon":
            allocation_force = 0.401711635 # the carbon share of ethylene in the total carbon content of the products


        # Add the production of ethylene, with the amount of 1 kg
        mto.new_exchange(
            type="production",
            name="ethylene",
            unit="kilogram",
            amount=1,
            input=mto.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Construction of the chemical factory
        mto.new_exchange(
            type="technosphere",
            name=factory["name"],
            unit=factory["unit"],
            amount=8.96e-12*allocation_force, # Per kg of ethylene produced, a share of 8.96e-12 kg of the chemical factory is produced.
            input=factory.key,
            ).save()
        
        
        # Electricity input
        mto.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=0.357014711*allocation_force,
            input=electricity.key,
            ).save()
        
        # Cooling energy, at -5 °C
        mto.new_exchange(
            type="technosphere",
            name=cool5["name"],
            unit=cool5["unit"],
            amount=0.4306*allocation_force,
            input=cool5.key,
            ).save()
        
        # Cooling energy, at -25 °C
        mto.new_exchange(
            type="technosphere",
            name=coolmin25["name"],
            unit=coolmin25["unit"],
            amount=1.076*allocation_force,
            input=coolmin25.key,
            ).save()
        
        # Cooling energy, at -30 °C
        mto.new_exchange(
            type="technosphere",
            name=coolmin30["name"],
            unit=coolmin30["unit"],
            amount=2.304*allocation_force,
            input=coolmin30.key,
            ).save()
        
        # Cooling energy, at -75 °C
        mto.new_exchange(
            type="technosphere",
            name=coolmin75["name"],
            unit=coolmin75["unit"],
            amount=0.5382*allocation_force,
            input=coolmin75.key,
            ).save()
        
        # Wastewater output in m³
        mto.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=-0.003194594*allocation_force,
            input=wastewater.key,
            ).save()
        
        # Methanol input
        mto.new_exchange(
            type="technosphere",
            name=methanol["name"],
            unit=methanol["unit"],
            amount=5.980145916*allocation_force,
            input=methanol.key,
            ).save()
        

        # Differentiation of the avoided burden calculations, for different avoided burden categories
        if avoidedburden != "none":
            # Propylene output
            mto.new_exchange(
                type="technosphere",
                name=propylene["name"],
                unit=propylene["unit"],
                amount=-1*burden_force,
                input=propylene.key,
                ).save()
        
            # LPG output
            mto.new_exchange(
                type="technosphere",
                name=pentene["name"],
                unit=pentene["unit"],
                amount=-0.102844841*burden_force,
                input=pentene.key, 
                ).save()
            
            # Methane output
            mto.new_exchange(
                type="technosphere",
                name=methane["name"],
                unit=methane["unit"],
                amount=-0.092369222*burden_force,
                input=methane.key,
                ).save()
            
            # Propane output
            mto.new_exchange(
                type="technosphere",
                name=propane["name"],
                unit=propane["unit"],
                amount=-0.062492525*burden_force,
                input=propane.key,
                ).save()
            
            # Coke output
            mto.new_exchange(
                type="technosphere",
                name=coke["name"],
                unit=coke["unit"],
                amount=-8.144552087*burden_force,
                input=coke.key,
                ).save()
        
            # Butene output
            mto.new_exchange(
                type="technosphere",
                name=butene["name"],
                unit=butene["unit"],
                amount=-0.275026911*burden_force,
                input=butene.key,
                ).save()

        # End-of-life of ethylene, if considered.
        if eol == "yes":
            mto.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=3.1373, # based on the stochiometrical oxidation of ethylene
                input=self.CO2.key,
                ).save()
            
            mto.new_exchange(
                type="biosphere",
                name=self.H2O["name"],
                unit=self.H2O["unit"],
                amount=1.6863, # [m³] based on the stochiometrical oxidation of ethylene and assuming water to be an ideal gas, p=1.013 bar, T=288.15 K
                input=self.H2O.key,
                ).save()

        # Definition of the reference product as ethylene
        mto['reference product'] = ("ethylene")
        mto.save()

        # Return the created MTO activity
        return mto
    
    def create_CO2hydr(self, eol: Literal["yes", "no"], electricity=None, carbon_dioxide=None, hydrogen=None, wastewater=None, factory=None):
        """
        Create the activity "CO2hydr" in the database "disco2very". The reference output is 1 kg of methanol.
        Flows are based on [Rihko-Struckmann et al., Assessment of Methanol Synthesis Utilizing Exhaust CO2 for Chemical Storage of
         Electrical Energy]. User can define the activities linked to it, but not the amounts.
        Excess heat is not modelled, since no avoided burden is considered for it.
        The parameter eol is used to define if the end-of-life of the product is considered (yes) or not (no). It is modeled as the
        stochiometrical oxidation of methanol CH3OH + 1,5 O2 = CO2 + 2 H20.

        Default parameters:
        - eol: no
        - inputs:
            - electricity: german grid electricity, medium voltage: 1,3288 kWh_el/kg_MethOH
            - factory: chemical factory construction, organics, RER: 3,5842e-12 units/kg_MetOH
            - co2: market for carbon dioxide, in chemical industry, GLO: 1,4358 kg_CO2/kg_MetOH
            - hydrogen: market for hydrogen, gaseous, low pressure, RER: 0,19732 kg_H2/kg_MetOH
        - outputs:
            - wastewater: market for wastewater, unpolluted, RoW: 5,6227*10^-4 m³_w/kg_MetOH
            - methanol: methanol production, from natural gas reforming, RER: 1 kg_MetOH (reference product)
        
        Returns: The created MTO activity
        """

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if wastewater is None:
            wastewater = self.wastewater
        if eol is None:
            eol = self.eol
        if hydrogen is None:
            hydrogen = self.hydrogen
        if carbon_dioxide is None:
            carbon_dioxide = self.carbon_dioxide
        if factory is None:
            factory = self.factory

        # Definition of name and code of the activity, based on the parameters used for its construction
        name=(f"methanol production, from CO2 hydrogenation. eol: {eol}")
        code = (f"CO2hydr | eol={eol}|elec={electricity.key}|co2={carbon_dioxide.key}|h2={hydrogen.key}|wastewater={wastewater.key}")
        
        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            co2hydr = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            co2hydr = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the CO2 hydrogenation process. The reference product is methanol and 1 kg is produced." \
                "Apart from it, wastewater is produced. Electricity input: "+electricity["name"]+". CO2 input: "+carbon_dioxide["name"]+"."
                "Hydrogen input: "+hydrogen["name"]+". Wastewater output: "+wastewater["name"]+". Based on the paper [Rihko-Struckmann et al.,"
                " Assessment of Methanol Synthesis Utilizing Exhaust CO2 for Chemical Storage of Electrical Energy, 2010].",
                )
            co2hydr.save()

        # Delete existing exchanges only
        for exc in list(co2hydr.exchanges()):
            exc.delete()        
       
        # Add the production of ethylene, with the amount of 1 kg
        co2hydr.new_exchange(
            type="production",
            name="methanol",
            unit="kilogram",
            amount=1,
            input=co2hydr.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Construction of the chemical factory
        co2hydr.new_exchange(
            type="technosphere",
            name=factory["name"],
            unit=factory["unit"],
            amount=3.5842e-12, # Per kg of methanol produced, a share of 3.5842e-12 kg of the chemical factory is produced.
            input=factory.key,
            ).save()
        
        
        # Electricity input
        co2hydr.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=1.32878456384964,
            input=electricity.key,
            ).save()
        
        # CO2 input
        co2hydr.new_exchange(
            type="technosphere",
            name=carbon_dioxide["name"],
            unit=carbon_dioxide["unit"],
            amount=1.435820454,
            input=carbon_dioxide.key,
            ).save()
        
        # Hydrogen input
        co2hydr.new_exchange(
            type="technosphere",
            name=hydrogen["name"],
            unit=hydrogen["unit"],
            amount=0.197319687,
            input=hydrogen.key,
            ).save()

        # Wastewater output in m³
        co2hydr.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=-0.000562265917602996,
            input=wastewater.key,
            ).save()
        

        
        # End-of-life of methanol, if considered.
        if eol == "yes":
            co2hydr.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=1.376092385, # based on the stochiometrical oxidation of methanol
                input=self.CO2.key,
                ).save()
            
            co2hydr.new_exchange(
                type="biosphere",
                name=self.H2O["name"],
                unit=self.H2O["unit"],
                amount=1.4762, # [m³] based on the stochiometrical oxidation of methanol and assuming water to be an ideal gas,
                # p=1.013 bar, T=288.15 K
                input=self.H2O.key,
                ).save()

        # Definition of the reference product as ethylene
        co2hydr['reference product'] = ("methanol")
        co2hydr.save()

        # Return the created CO2 hydrogenation activity
        return co2hydr
    
    def create_H2PEM(self, avoidedburden: Literal["none", "half", "full"], eol: Literal["yes", "no"], electricity=None, wastewater=None,
                     oxygen=None):
        """
        
        Create the activity "hydrogen_pem" in the database "disco2very". The reference output is 1 kg of hydrogen.
        Flows are based on [Bareiß et al., Life cycle assessment of hydrogen from proton exchange membrane water electrolysis in future
        energy systems, 2019].
        User can define the activities linked to it, but not the amounts.
        
        With the definition of the parameter avoidedburden, it can decided if no avoided burden is considered (none), if 50 % of its impact
         is considered (half), or if all of it is considered (full).
        
        No allocation for oxygen production is considered.
        
        The parameter eol is used to define if the end-of-life of the product is considered (yes) or not (no). It is modeled as the
        stochiometrical oxidation of hydrogen H2 + 0,5 O2 = H20.



        Default parameters:
        - avoidedburden: none
        - eol: no
        - inputs:
            - electricity: german grid electricity, medium voltage, DE: 56,005 kWh_el/kg_H2
            - water: water production, deionised, Europe without Switzerland: 8,936 kg_H2O/kg_H2
            - low-alloyed steel: market for steel, low-alloyed, GLO: 0,0067206 kg_la-steel/kg_H2
                - treatment of low-alloyed steel: treatment of waste reinforcement steel, recycling, RoW: 0,0067206 kg_la-steel_treat/kg_H2
            - high-alloyed steel: reinforcing steel production, Europe without Austria: 0,0026602 kg_ha-steel/kg_H2
                - treatment of high-alloyed steel: treatment of waste reinforcement steel, recycling, RoW: 0,0026602 kg_ha-steel_treat/kg_H2
            - aluminium: aluminium production, primary, ingot, RoW: 0,00014001 kg_Al/kg_H2
                - treatment of aluminium: market for waste aluminium, Europe without Switzerland: 0,00014001 kg_Al_treat/kg_H2
            - copper: market for copper, cathode, GLO: 0,00014001 kg_Cu/kg_H2
                - treatment of copper: market for waste copper, Europe without Switzerland: 0,00014001 kg_Cu_treat/kg_H2
            - plastic: market for plastic profiles, RER: 0,00042004 kg_plastic/kg_H2
                - treatment of plastic: market for waste plastic, mixed, recycling, RER: 0,00042004 kg_plastic_treat/kg_H2
            - electronic material (power, control): electronics production, for control units, RER: 0,0015401 kg_electronic/kg_H2
                - treatment of electronic material: market for used industrial electronic device, RoW: 0,0015401 kg_electronic_treat/kg_H2
            - process material (adsorbent, lubricant): market for lubricating oil, RER: 0,00028003 kg_lubricant/kg_H2
                - treatment of process material: market for waste mineral oil, Europe without Switzerland: 0,00028003 kg_lubricant_treat/kg_H2
            - concrete: concrete, all types to generic market for concrete, normal strength, RoW: 3,26696E-06 kg_concrete/kg_H2
                - treatment of concrete: market for waste concrete, Europe without Switzerland: 3,26696E-06 kg_concrete_treat/kg_H2
            - titanium: titanium production, GLO: 0,00073927 kg_Ti/kg_H2
                - treatment of titanium: market for inert waste, RER: 0,00073927 kg_Ti_treat/kg_H2
            - stainless steel: market for steel, chromium steel 18/8, GLO: 0,00014001 kg_sl-steel/kg_H2
                - treatment of stainless steel: treatment of waste reinforcement steel, recycling, RoW: 0,00014001 kg_sl-steel_treat/kg_H2
            - nafion: market for plastic profiles, RER: 2,2402e-5 kg_Nafion/kg_H2 (although the same input is used for plastic,
                nafion is still created seperately, since it might be changed in the future for another better suited activity)
                - treatment of nafion: market for waste plastic, mixed, recycling, RER: 2,2402e-5 kg_Nafion_treat/kg_H2
            - activated carbon: market for activated carbon, granular, GLO: 1,2601 e-5 kg_ac/kg_H2
                - treatment of activated carbon: treatment of spent activated carbon, granular, GLO: 1,2601 e-5 kg_ac_treat/kg_H2
            - iridium: iridium production, GLO: 1,0501e-6 kg_Ir/kg_H2
                - treatment of iridium: treatment of precious metal scrap, in anode slime, precious metal extraction, RoW,
                    reference product = platinum: 1,0501e-6 kg_Ir_treat/kg_H2;
            - platinum: market for platinum, GLO: 1,0501e-7 kg_Pt/kg_H2
                - treatment of platinum: treatment of automobile catalyst, RER, reference product = platinum: 1,0501e-7 kg_Pt_treat/kg_H2
        - outputs:
            - hydrogen: 1 kg_H2. Reference product.
            - oxygen: market for oxygen, liquid, RER: 7,9363 kg_O2/kg_H2
            - wastewater: market for wastewater, unpolluted, RoW: 2,2e-5 m³_w/kg_H2

        Returns: The created MTO activity
        """

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if wastewater is None:
            wastewater = self.wastewater
        if avoidedburden is None:
            avoidedburden = self.avoidedburden
        if oxygen is None:
            oxygen = self.oxygen
        if eol is None:
            eol = self.eol
        
        water=eidb.get(name="market for water, deionised", location="Europe without Switzerland")
        lasteel = eidb.get(name="market for steel, low-alloyed", location="GLO")
        hasteel = eidb.get(name="reinforcing steel production", location="Europe without Austria")
        aluminium = eidb.get(name="aluminium production, primary, ingot", location="RoW")
        copper = eidb.get(name="market for copper, cathode", location="GLO")
        plastic = eidb.get(name="market for plastic profiles", location="RER")
        electronic = eidb.get(name="electronics production, for control units", location="RER")
        lubricant = eidb.get(name="market for lubricating oil", location="RER")
        concrete = eidb.get(name="concrete, all types to generic market for concrete, normal strength", location="RoW")
        titanium = eidb.get(name="titanium production", location="GLO")
        slsteel = eidb.get(name="market for steel, chromium steel 18/8", location="GLO")
        activatedcarbon = eidb.get(name="market for activated carbon, granular", location="GLO")
        platinum = eidb.get(name="market for platinum", location="GLO")
        iridium = self.db.get(name="iridium production", location="GLO")
        nafion = eidb.get(name="market for plastic profiles", location="RER")
        treat_steel = eidb.get(name="treatment of waste reinforcement steel, recycling", location="RoW")
        treat_aluminium = eidb.get(name="market for waste aluminium", location="Europe without Switzerland")
        treat_copper = eidb.get(name="market for waste copper", location="Europe without Switzerland")
        treat_plastic = eidb.get(name="treatment of waste plastic, mixed, recycling", location="RER", product= "plastic, mixed, recycled")
        treat_electronic = eidb.get(name="market for used industrial electronic device", location="RoW")
        treat_lubricant = eidb.get(name="market for waste mineral oil", location="Europe without Switzerland")
        treat_concrete = eidb.get(name="market for waste concrete", location="Europe without Switzerland")
        treat_titanium = eidb.get(name="market for inert waste", location="RER")
        treat_activatedcarbon = eidb.get(name="market for spent activated carbon, granular", location="GLO")
        treat_iridium = eidb.get(name="treatment of precious metal from electronics scrap, in anode slime, precious metal extraction",
                                 location="RoW", product="palladium")
        treat_platinum = eidb.get(name="treatment of automobile catalyst", location="RER", product="platinum")

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"hydrogen production, from PEM water electrolysis. Avoided burden: {avoidedburden}; eol: {eol}")
        code = (f"H2PEM|ab={avoidedburden}|eol={eol}|elec={electricity.key}|wastewater={wastewater.key}|oxygen={oxygen.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            h2pem = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            h2pem = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the proton exchange membrane (PEM) water electrolysis process." \
                "The reference product is hydrogen and 1 kg is produced. Apart from it, oxygen and wastewater are produced." \
                "Electricity input: "+electricity["name"]+". Wastewater input: "+wastewater["name"]+". Oxygen input: "+oxygen["name"]+"."
                "Based on the paper [Bareiß et al., Life cycle assessment of hydrogen from proton exchange membrane water electrolysis"
                "in future energy systems, 2019].",
            )
            h2pem.save()

        # Delete existing exchanges only
        for exc in list(h2pem.exchanges()):
            exc.delete()

        # quantification of the avoided burden as 0, 0.5 or 1, according to the avoidedburden parameter
        if avoidedburden == "none":
            burden_force = 0
        elif avoidedburden == "half":
            burden_force = 0.5
        elif avoidedburden == "full":
            burden_force = 1

        # Add the production of ethylene, with the amount of 1 kg
        h2pem.new_exchange(
            type="production",
            name="hydrogen",
            unit="kilogram",
            amount=1,
            input=h2pem.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Electricity input
        h2pem.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=56.00509259,
            input=electricity.key,
            ).save()
        
        # Deionised water input
        h2pem.new_exchange(
            type="technosphere",
            name=water["name"],
            unit=water["unit"],
            amount=8.936011905,
            input=water.key,
            ).save()
        
        # Low-alloyed steel input
        h2pem.new_exchange(
            type="technosphere",
            name=lasteel["name"],
            unit=lasteel["unit"],
            amount=0.006720611,
            input=lasteel.key,
            ).save()
        
        # High-alloyed steel input
        h2pem.new_exchange(
            type="technosphere",
            name=hasteel["name"],
            unit=hasteel["unit"],
            amount=0.002660242,
            input=hasteel.key,
            ).save()
        
        # aluminium input
        h2pem.new_exchange(
            type="technosphere",
            name=aluminium["name"],
            unit=aluminium["unit"],
            amount=0.000140013,
            input=aluminium.key,
            ).save()
        
        # Copper input
        h2pem.new_exchange(
            type="technosphere",
            name=copper["name"],
            unit=copper["unit"],
            amount=0.000140013,
            input=copper.key,
            ).save()
        
        # plastic input
        h2pem.new_exchange(
            type="technosphere",
            name=plastic["name"],
            unit=plastic["unit"],
            amount=0.000420038,
            input=plastic.key,
            ).save()
        
        # electronic material input
        h2pem.new_exchange(
            type="technosphere",
            name=electronic["name"],
            unit=electronic["unit"],
            amount=0.00154014,
            input=electronic.key,
            ).save()
        
        # process material input
        h2pem.new_exchange(
            type="technosphere",
            name=lubricant["name"],
            unit=lubricant["unit"],
            amount=0.000280025,
            input=lubricant.key,
            ).save()
        
        # concrete input
        h2pem.new_exchange(
            type="technosphere",
            name=concrete["name"],
            unit=concrete["unit"],
            amount=3.26696e-06,
            input=concrete.key,
            ).save()
        
        # titanium input
        h2pem.new_exchange(
            type="technosphere",
            name=titanium["name"],
            unit=titanium["unit"],
            amount=0.000739267,
            input=titanium.key,
            ).save()
        
        # stainless steel input
        h2pem.new_exchange(
            type="technosphere",
            name=slsteel["name"],
            unit=slsteel["unit"],
            amount=0.000140013,
            input=slsteel.key,
            ).save()
        
        # nafion input
        h2pem.new_exchange(
            type="technosphere",
            name=nafion["name"],
            unit=nafion["unit"],
            amount=2.2402e-05,
            input=nafion.key,
            ).save()
        
        # activated carbon input
        h2pem.new_exchange(
            type="technosphere",
            name=activatedcarbon["name"],
            unit=activatedcarbon["unit"],
            amount=1.26011e-05,
            input=activatedcarbon.key,
            ).save()
        
        # iridium input
        h2pem.new_exchange(
            type="technosphere",
            name=iridium["name"],
            unit=iridium["unit"],
            amount=1.0501e-06,
            input=iridium.key,
            ).save()
        
        # platinum input
        h2pem.new_exchange(
            type="technosphere",
            name=platinum["name"],
            unit=platinum["unit"],
            amount=1.0501e-07,
            input=platinum.key,
            ).save()
        
        # Wastewater output in m³
        h2pem.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=-2.2e-05,
            input=wastewater.key,
            ).save()
        
        # Treatment of steel (low-alloyed, high-alloyed and stainless steel)
        # total amount of steel: 0.006720611 + 0.002660242 + 0.000140013 = 0.009520866
        h2pem.new_exchange(
            type="technosphere",
            name=treat_steel["name"],
            unit=treat_steel["unit"],
            amount=-0.009520866,
            input=treat_steel.key,
            ).save()
        
        # Treatment of aluminium
        h2pem.new_exchange(
            type="technosphere",
            name=treat_aluminium["name"],
            unit=treat_aluminium["unit"],
            amount=-0.000140013,
            input=treat_aluminium.key,
            ).save()
        
        # Treatment of copper
        h2pem.new_exchange(
            type="technosphere",
            name=treat_copper["name"],
            unit=treat_copper["unit"],
            amount=-0.000140013,
            input=treat_copper.key,
            ).save()
        
        # Treatment of plastic
        # total amount of plastic: 0.000420038 + 2.2402e-05 = 0.00044244
        h2pem.new_exchange(
            type="technosphere",
            name=treat_plastic["name"],
            unit=treat_plastic["unit"],
            amount=-0.00044244,
            input=treat_plastic.key,
            ).save()
        
        # Treatment of electronic material
        h2pem.new_exchange(
            type="technosphere",
            name=treat_electronic["name"],
            unit=treat_electronic["unit"],
            amount=-0.00154014,
            input=treat_electronic.key,
            ).save()
        
        # Treatment of lubricant
        h2pem.new_exchange(
            type="technosphere",
            name=treat_lubricant["name"],
            unit=treat_lubricant["unit"],
            amount=-0.000280025,
            input=treat_lubricant.key,
            ).save()
        
        # Treatment of concrete
        h2pem.new_exchange(
            type="technosphere",
            name=treat_concrete["name"],
            unit=treat_concrete["unit"],
            amount=-3.26696e-06,
            input=treat_concrete.key,
            ).save()
        
        # Treatment of titanium
        h2pem.new_exchange(
            type="technosphere",
            name=treat_titanium["name"],
            unit=treat_titanium["unit"],
            amount=-0.000739267,
            input=treat_titanium.key,
            ).save()
        
        # Treatment of activated carbon
        h2pem.new_exchange(
            type="technosphere",
            name=treat_activatedcarbon["name"],
            unit=treat_activatedcarbon["unit"],
            amount=-1.26011e-05,
            input=treat_activatedcarbon.key,
            ).save()
        
        # Treatment of iridium
        h2pem.new_exchange(
            type="technosphere",
            name=treat_iridium["name"],
            unit=treat_iridium["unit"],
            amount=-1.0501e-06,
            input=treat_iridium.key,
            ).save()
        
        # Treatment of platinum
        h2pem.new_exchange(
            type="technosphere",
            name=treat_platinum["name"],
            unit=treat_platinum["unit"],
            amount=-1.0501e-07,
            input=treat_platinum.key,
            ).save()
        

        # Differentiation of the avoided burden calculations, for different avoided burden categories
        if avoidedburden != "none":
            # Oxygen output
            h2pem.new_exchange(
                type="technosphere",
                name=oxygen["name"],
                unit=oxygen["unit"],
                amount=-7.936259921*burden_force,
                input=oxygen.key,
                ).save()
            
        

        # End-of-life of hydrogen, if considered.
        if eol == "yes":
            h2pem.new_exchange(
                type="biosphere",
                name=self.H2O["name"],
                unit=self.H2O["unit"],
                amount=8.936011905, # based on the stochiometrical oxidation of ethylene
                input=self.H2O.key,
                ).save()
            
        # Definition of the reference product as ethylene
        h2pem['reference product'] = ("hydrogen")
        h2pem.save()

        # Return the created H2 PEM activity
        return h2pem
    
    def create_DAC(self, electricity=None):
        """
        
        Create the activity "direct air capture, 2016" in the database "disco2very". The reference output is 1 kg of captured carbon dioxide.
        Flows are based on [S. Deutz & A. Bardow, Life-cycle assessment of an industrial direct air capture process based on temperature-
        vacuum swing adsorption, 2021 - https://doi.org/10.1038/s41560-020-00771-9] and on [G. Leonzio et al., Environmental performance of
        different sorbents, used for direct air capture, 2022 - https://doi.org/10.1016/j.spc.2022.04.004]. 
        User can define the activities linked to it, but not the amounts.


        Default parameters:
        - inputs:
            - electricity: german grid electricity, medium voltage, DE: 0,7 kWh_el/kg_CO2
            - heat: heat production, at heat pump 30kW, allocation exergy, Europe without Switzerland: 4,7 MJ_th/kg_CO2
            - dac_construction: construction of direct air capture, 2016, RER: 1,25e-8 units/kg_CO2 (disco2very activity,
                based on a capture rate of 4000kt_CO2/a and a lifetime of 20 years)
            - adsorbent: adsorbent, amine on alumina, DE: 0,0075 kg_adsorbent/kg_CO2 (disco2very activity)
            - co2_atm: carbon dioxide, in air: 1 kg_CO2_atm/kg_CO2 (biosphere flow, id: f9749677-9c9f-4678-ab55-c607dfdc2cb9)
            - adsorbent_treat: treatment of spent anion exchange resin from potable water production, municipal incineration,
                RoW: 0,0075 kg_adsorbent_treat/kg_CO2, reference product: spent anion exchange resin from potable water production
        - outputs:
            - co2_capt: market for carbon dioxide, in chemical industry, GLO: 1 kg_CO2_capt/kg_CO2 (reference product)
        Returns: The created MTO activity
        """
        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        heat = eidb.get(name="heat production, at heat pump 30kW, allocation exergy", location="Europe without Switzerland")
        dac_construction = self.db.get(name="construction of direct air capture, 2016", location="RER")
        adsorbent = self.db.get(name="adsorbent, amine on alumina", location="DE")
        adsorbent_treat = eidb.get(name="treatment of spent anion exchange resin from potable water production, municipal incineration",
                                   location="GLO", product="spent anion exchange resin from potable water production")

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"direct air capture, 2016")
        code = (f"DAC2016|elec={electricity.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            dac = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            dac = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the direct air capture of carbon dioxide, modelled for 2016. Heat is provided by a heat pump." \
                "Electricity input: "+electricity["name"]+". Based on the paper [Deutz&Bardow, Life-cycle assessment of an industrial direct air"
                "capture process based on temperature-vacuul swing adsorption, 2021].",
                )
            dac.save()

        # Delete existing exchanges only
        for exc in list(dac.exchanges()):
            exc.delete()


        # Add the production of captured co2, with the amount of 1 kg
        dac.new_exchange(
            type="production",
            name="carbon dioxide, in chemical industry",
            unit="kilogram",
            amount=1,
            input=dac.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Electricity input
        dac.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=0.7,
            input=electricity.key,
            ).save()
        
        # Heat input
        dac.new_exchange(
            type="technosphere",
            name=heat["name"],
            unit=heat["unit"],
            amount=4.7,
            input=heat.key,
            ).save()
        
        # DAC construction input
        dac.new_exchange(
            type="technosphere",
            name=dac_construction["name"],
            unit=dac_construction["unit"],
            amount=1.25e-08,
            input=dac_construction.key,
            ).save()
        
        # Adsorbent input
        dac.new_exchange(
            type="technosphere",
            name=adsorbent["name"],
            unit=adsorbent["unit"],
            amount=0.0075,
            input=adsorbent.key,
            ).save()
        
        # Treatment of adsorbent input
        dac.new_exchange(
            type="technosphere",
            name=adsorbent_treat["name"],
            unit=adsorbent_treat["unit"],
            amount=-0.0075,
            input=adsorbent_treat.key,
            ).save()
        
        # atmospheric co2 input
        dac.new_exchange(
            type="biosphere",
            name=self.CO2["name"],
            unit=self.CO2["unit"],
            amount=-1,
            input=self.CO2.key,
            ).save()
    
        # Definition of the reference product as carbon dioxide
        dac['reference product'] = ("carbon dioxide, in chemical industry")
        dac.save()

        # Return the created DAC activity
        return dac
    
    def create_eCO2R(self, eol:Literal["yes", "no"]="no", electricity=None, carbon_dioxide=None):
        r"""
        Create the activity "eCO2R" in the database "disco2very". The reference output is 1 kg of ethylene_pre_VL_sep.
        Values and calculations are based on [J.Wyndorps et. al. - 2021 - Is electrochemical Co2 reduction the future technology for
        power-to-chemicals? An environmental comparison with H2-based pathways] and on [M.Löffelholz et. al. - 2023 - Optimized scalable
        CuB catalyst with promising carbon footprint for the electrochemical CO2 reduction to ethylene] and on stochiometric calculations.
        Further information can be found in the excel research.xlsx in the disco2very GitHub repository and on 
        Literatur\LCI data\ProMet_V2.xlsx.

        Default parameters:
        - inputs:
            - eol: "no"
            - electricity: market for electricity, medium voltage, DE: 74,878 kWh_el/kg_C2H4_pre_VL_sep
            - market for water, deionised, Europe without Switzerland: 4,4249 kg_H2O/kg_C2H4_pre_VL_sep
            - carbon_dioxide: disco2very activity. direct air capture, 2016, RER: 9,2290 kg_CO2/kg_C2H4_pre_VL_sep
                (in total, 18,396 kg_CO2/kg_C2H4 are needed, but 9,1665 is provided by co2 captured by amine-wash)
            - copper_electrode: market for copper, cathode, GLO: 7,4E-11 kg_Cu/kg_C2H4_pre_VL_sep
            - chem_factory: chemical factory constructrion, RER: 7,32E-7 units/kg_C2H4_pre_VL_sep

        - outputs:
            - ethylene_pre_VL_sep: ethylene pre VL separation: 1 kg (reference product)
            - if eol=="yes"
                - biosphere flow: carbon dioxide, fossil; air; urbain air close to ground: 18,396 kg_CO2
        """

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if carbon_dioxide is None:
            carbon_dioxide = self.create_DAC(electricity=electricity)

        water = eidb.get(name="market for water, deionised", location="Europe without Switzerland")
        copper_electrode = eidb.get(name="market for copper, cathode", location="GLO")
        chem_factory = eidb.get(name="chemical factory construction", location="RER")

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"electrochemical CO2 reduction to ethylene. eol: {eol}")
        code = (f"eCO2R to ethylene|eol={eol}|elec={electricity.key}|co2={carbon_dioxide.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the electrochemical CO2 reduction to ethylene. Electricity input: "+electricity["name"]+"."
                "Carbon dioxide input: "+carbon_dioxide["name"]+". Based on the paper [J.Wyndorps et. al. - 2021 - Is electrochemical Co2"
                "reduction the future technology for power-to-chemicals? An environmental comparison with H2-based pathways] and on"
                "[M.Löffelholz et. al. - 2023 - Optimized scalable CuB catalyst with promising carbon footprint for the electrochemical CO2"
                "reduction to ethylene].",
            )
            eCO2R.save()

        # Delete existing exchanges only
        for exc in list(eCO2R.exchanges()):
            exc.delete()

        # Add the production of ethylene_pre_VL_sep, with the amount of 1 kg
        eCO2R.new_exchange(
            type="production",
            name="ethylene_pre_VL_sep",
            unit="kilogram",
            amount=1,
            input=eCO2R.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Electricity input
        eCO2R.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=74.878,
            input=electricity.key,
            ).save()
        
        # Water input
        eCO2R.new_exchange(
            type="technosphere",
            name=water["name"],
            unit=water["unit"],
            amount=4.4249,
            input=water.key,
            ).save()
        
        # Carbon dioxide input
        eCO2R.new_exchange(
            type="technosphere",
            name=carbon_dioxide["name"],
            unit=carbon_dioxide["unit"],
            amount=9.229,
            input=carbon_dioxide.key,
            ).save()
        
        # Copper electrode input
        eCO2R.new_exchange(
            type="technosphere",
            name=copper_electrode["name"],
            unit=copper_electrode["unit"],
            amount=7.4e-11,
            input=copper_electrode.key,
            ).save()
        
        # Chemical factory construction input
        eCO2R.new_exchange(
            type="technosphere",
            name=chem_factory["name"],
            unit=chem_factory["unit"],
            amount=7.32e-7,
            input=chem_factory.key,
            ).save()
        
        # BIOSPHERE EXCHANGES
        # EoL CO2 emissions
        if eol=="yes":
            eCO2R.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=18.396,
                input=self.CO2.key,
            ).save()
        
        # Definition of the reference product as ethylene_pre_VL_sep
        eCO2R['reference product'] = ("ethylene_pre_VL_sep")
        eCO2R.save()

        # Return the created eCO2R activity
        return eCO2R
    
    def create_eCO2R_VL_sep(self, electricity=None, ethylene_eCO2R=None):
        """
        Create the activity "vapor-liquid separation of ethylene, from eCO2R" in the database "disco2very". The reference output
        is 1 kg of ethylene_pre_DeOx. Values and calculations are based on
        [https://www.jmcampbell.com/tip-of-the-month/wp-content/uploads/2015/09/Sep_2015_Gas-Liquid-Separators-Sizing-Parameter-MM083015.pdf],
        [Design Two-Phase Separators Within the Right Limits], [ASME Boiler and Pressure Vessel Code, Section II, Part D, Table 1A] and
        [Perry's Chemical Engineers' Handbook - Table 2.30]

        User can define the electricity input.
        Default parameters:
        - inputs:
            - electricity: market for electricity, medium voltage, DE: 0,13390 kWh_el/kg_C2H4_pre_DeOx
            - steel: market for steel, low-alloyed, GLO: 3,0177E-06 kg_steel/kg_C2H4_pre_DeOx
            - ethylene_eCO2R: disco2very activity: electrochemical CO2 reduction to ethylene, DE: 1,0 kg_C2H4_pre_VL_sep/kg_C2H4_pre_DeOx
        - outputs:
            - ethylene_pre_DeOx: ethylene pre DeOx separation: 1 kg
            - CO2 emissions for EoL of by-products: biosphere flow: "carbon dioxide, fossil" in compartment "air" and subcompartment "urban air close to ground"
                amount: 2,361481 kg_CO2/kg_C2H4_pre_DeOx
        """

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if ethylene_eCO2R is None:
            ethylene_eCO2R = self.create_eCO2R(electricity=electricity)
        steel = eidb.get(name="market for steel, low-alloyed", location="GLO")
        
        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("vapor-liquid separation of ethylene, from eCO2R")
        code = (f"eCO2R to ethylene, VL sep|elec={electricity.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_VL_sep = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_VL_sep = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the vapor-liquid separation of ethylene from eCO2R. Electricity input: "+electricity["name"]+"."
                "Based on the RWTH scripts for [Chemische Energieumwandlung II] and for [Wärme- und Stoffübertragung I/II].",
            )
            eCO2R_VL_sep.save()

        # Delete existing exchanges only
        for exc in list(eCO2R_VL_sep.exchanges()):
            exc.delete()

        # Add the production of ethylene_pre_DeOx, with the amount of 1 kg
        eCO2R_VL_sep.new_exchange(
            type="production",
            name="ethylene_pre_DeOx",
            unit="kilogram",
            amount=1,
            input=eCO2R_VL_sep.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Electricity input
        eCO2R_VL_sep.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=0.133897031,
            input=electricity.key,
            ).save()
        
        # Steel input
        eCO2R_VL_sep.new_exchange(
            type="technosphere",
            name=steel["name"],
            unit=steel["unit"],
            amount=3.017679E-06,
            input=steel.key,
            ).save()
        
        # eCO2R input
        eCO2R_VL_sep.new_exchange(
            type="technosphere",
            name=ethylene_eCO2R["name"],
            unit=ethylene_eCO2R["unit"],
            amount=1.0,
            input=ethylene_eCO2R.key,
            ).save()

        # BIOSPHERE EXCHANGES
        # CO2 emissions for EoL of by-products
        eCO2R_VL_sep.new_exchange(
            type="biosphere",
            name=self.CO2["name"],
            unit=self.CO2["unit"],
            amount=2.361481,
            input=self.CO2.key,
            ).save()
        
        # Definition of the reference product as ethylene_pre_DeOx
        eCO2R_VL_sep['reference product'] = ("ethylene_pre_DeOx")
        eCO2R_VL_sep.save()

        # Return the created eCO2R_VL_sep activity
        return eCO2R_VL_sep
    
    def create_eCO2R_DeOx_sep(self, cool=None, electricity=None, ethylene_VL_sep=None):
        """
        Create the activity "eCO2R_DeOx_sep" in the database "disco2very". The reference output is 1 kg of ethylene_pre_aminewash.
        Values and calculations are based on the RWTH scripts for [Chemische Energieumwandlung II] and for [Wärme- und Stoffübertragung I/II].

        Default parameters:
        - inputs:
            - cooling energy: market for cooling energy, GLO: 0,010118339 MJ/kg_C2H4_pre_aminewash
            - ethylene_pre_DeOx: disco2very activity: vapor-liquid separation of ethylene, from eCO2R, DE: 1,0 kg_C2H4_pre_DeOx/kg_C2H4_pre_aminewash

        - outputs:
            - ethylene_pre_aminewash: ethylene pre amine wash separation: 1 kg
        """
        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if cool is None:
            cool = self.cool5
        if ethylene_VL_sep is None:
            ethylene_VL_sep = self.create_eCO2R_VL_sep(electricity=electricity)

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("electrochemical CO2 reduction, oxygen removal from byproduct stream")
        code = (f"eCO2R to ethylene, DeOx sep|elec={electricity.key}|cool={cool.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_DeOx_sep = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_DeOx_sep = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the oxygen removal from the byproduct stream of eCO2R. Cooling energy input: "+cool["name"]+".",
            )
            eCO2R_DeOx_sep.save()

            # Delete existing exchanges only
            for exc in list(eCO2R_DeOx_sep.exchanges()):
                exc.delete()

        # Add the production of ethylene_pre_aminewash, with the amount of 1 kg
        eCO2R_DeOx_sep.new_exchange(
            type="production",
            name="ethylene_pre_aminewash",
            unit="kilogram",
            amount=1,
            input=eCO2R_DeOx_sep.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Cooling energy input
        eCO2R_DeOx_sep.new_exchange(
            type="technosphere",
            name=cool["name"],
            unit=cool["unit"],
            amount= 0.010118339,
            input=cool.key,
            ).save()
        
        # eCO2R_VL_sep input
        eCO2R_DeOx_sep.new_exchange(
            type="technosphere",
            name=ethylene_VL_sep["name"],
            unit=ethylene_VL_sep["unit"],
            amount=1.0,
            input=ethylene_VL_sep.key,
            ).save()
        
        # Definition of the reference product as ethylene_pre_aminewash
        eCO2R_DeOx_sep['reference product'] = ("ethylene_pre_aminewash")
        eCO2R_DeOx_sep.save()

        # Return the created eCO2R_DeOx_sep activity
        return eCO2R_DeOx_sep 

    def create_eCO2R_aminewash_sep(self, heat=None, electricity=None, ethylene_DeOx_sep=None):
        """
        Create the activity "amine wash separation of ethylene, from eCO2R" in the database "disco2very". The reference output is 1 kg
        of ethylene_pre_TSA. Here, CO2 is removed from the byproduct stream of eCO2R by an amine wash separation. The CO2 is sent back
        to the eCO2R process, therefore it is not accounted as an emission in this activity.
        Values and calculations are based on [S.D.D'Angelo et al. - 2021 - Planetary Boundaries Analysis of Low-Carbon Ammonia
        Production Routes - Supplementary Infomation], [D.Vasiliu et al - 2019 - Short-cut method for assessing solvents for gas
        cleaning by reactive absorption], [M.Wagner et al - 2013 - Solubility of Carbon Dioxide in Aqueous Solutions of Monoethanolamine
        in the Low and High Gas Loading Regions], [Aronu et al. - 2011 - Solubility of CO2 in 15, 30, 45 and 60 mass% MEA from 40 to 120
        1C and model representation using the extended UNIQUAC framework], [A.Lawal et al. - 2009 - Dynamic modelling of CO2 absorption
        for post combustion capture in coal-fired power plants] and [Q.Xu - 2011 - Total Pressure and CO2 solubility at high temperature
        in aqueous amines].
        User can define the heat and electricity input.

        Default parameters:
        - inputs:
            - heat: market for heat, district or industrial, natural gas, Europe without Switzerland: 28,487337 MJ/kg_C2H4
            - eCO2R_DeOx_sep: disco2very activity: electrochemical CO2 reduction, oxygen removal from byproduct stream, DE:
                1,0 kg_C2H4_pre_aminewash/kg_C2H4
        - outputs:
            - ethylene_pre_TSA: ethylene production, before TSA: 1 kg_C2H4_pre_TSA/kg_C2H4 (reference product)
        """
        
        # Definition of parameters
        if heat is None:
            heat = eidb.get(name="market for heat, district or industrial, natural gas", location="Europe without Switzerland")
        if electricity is None:
            electricity = self.electricity
        if ethylene_DeOx_sep is None:
            ethylene_DeOx_sep = self.create_eCO2R_DeOx_sep(electricity=electricity)

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("amine wash separation of ethylene, from eCO2R")
        code = (f"eCO2R to ethylene, amine wash sep|heat={heat.key}|elec={electricity.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_aminewash_sep = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_aminewash_sep = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the amine wash separation of ethylene from eCO2R. Heat input: "+heat["name"]+".",
            )
            eCO2R_aminewash_sep.save()

        # Delete existing exchanges only
        for exc in list(eCO2R_aminewash_sep.exchanges()):
            exc.delete()

        # Add the production of ethylene_pre_TSA, with the amount of 1 kg
        eCO2R_aminewash_sep.new_exchange(
            type="production",
            name="ethylene_pre_TSA",
            unit="kilogram",
            amount=1,
            input=eCO2R_aminewash_sep.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Heat input
        eCO2R_aminewash_sep.new_exchange(
            type="technosphere",
            name=heat["name"],
            unit=heat["unit"],
            amount=28.487337,
            input=heat.key,
            ).save()
        
        # eCO2R_DeOx_sep input
        eCO2R_aminewash_sep.new_exchange(
            type="technosphere",
            name=ethylene_DeOx_sep["name"],
            unit=ethylene_DeOx_sep["unit"],
            amount=1.0,
            input=ethylene_DeOx_sep.key,
            ).save()
        
        # Definition of the reference product as ethylene_pre_TSA
        eCO2R_aminewash_sep['reference product'] = ("ethylene_pre_TSA")
        eCO2R_aminewash_sep.save()

        # Return the created eCO2R_aminewash_sep activity
        return eCO2R_aminewash_sep
    
    def create_eCO2R_TSA_sep(self, electricity=None, cool=None, heat=None, ethylene_aminewash_sep=None):
        """
        Create the activity "eCO2R_TSA_sep" in the database "disco2very". The reference output is 1 kg of ethylene_pre_cryo_sep.
        Values and calculations are based on [Perry's Chemical Engineers' Handbook, 7th Edition],
        [https://www.engineeringtoolbox.com/specific-heat-capacity-gases-d_159.html] and [E.Scuiller et al. - 2023 - New Approach for
        Measuring the Specific Heat Capacity of Reactive Adsorbents Using Calorimetry].
        User can define the heat, cooling energy and electricity input.

        Default parameters:
        - inputs:
            - cool: market for cooling energy, GLO: 3,06967977 MJ/kg_C2H4_pre_cryo_sep
            - heat: market for heat, district or industrial, natural gas, Europe without Switzerland: 3,079241549 MJ/kg_C2H4_pre_cryo_sep
            - ethylene_pre_aminewash: disco2very activity: amine wash separation of ethylene, from eCO2R, DE: 
                1,0 kg_C2H4_pre_aminewash/kg_C2H4_pre_cryo_sep
        
        - outputs:
            - ethylene_pre_cryo_sep: ethylene production, before cryogenic separation: 1 kg_C2H4_pre_cryo_sep/kg_C2H4 (reference product)
            - water: market for wastewater, unpolluted, RoW: 0,000763598 kg_H2O/kg_C2H4_pre_cryo_sep
        """

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if cool is None:
            cool = self.cool5
        if heat is None:
            heat = eidb.get(name="market for heat, district or industrial, natural gas", location="Europe without Switzerland")
        if ethylene_aminewash_sep is None:
            ethylene_aminewash_sep = self.create_eCO2R_aminewash_sep(electricity=electricity)
        wastewater = self.wastewater

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("temperature swing adsorption separation of ethylene, from eCO2R")
        code = (f"eCO2R to ethylene, TSA sep|elec={electricity.key}|cool={cool.key}|heat={heat.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_TSA_sep = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_TSA_sep = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the temperature swing adsorption (TSA) separation of ethylene from eCO2R." \
                "Cooling energy input: "+cool["name"]+". Heat input: "+heat["name"]+".",
                )
            eCO2R_TSA_sep.save()

            # Delete existing exchanges only
            for exc in list(eCO2R_TSA_sep.exchanges()):
                exc.delete()

        # Add the production of ethylene_pre_cryo_sep, with the amount of 1 kg
        eCO2R_TSA_sep.new_exchange(
            type="production",
            name="ethylene_pre_cryo_sep",
            unit="kilogram",
            amount=1,
            input=eCO2R_TSA_sep.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Cooling energy input
        eCO2R_TSA_sep.new_exchange(
            type="technosphere",
            name=cool["name"],
            unit=cool["unit"],
            amount=3.06967977,
            input=cool.key,
            ).save()
        
        # Heat input
        eCO2R_TSA_sep.new_exchange(
            type="technosphere",
            name=heat["name"],
            unit=heat["unit"],
            amount=3.079241549,
            input=heat.key,
            ).save()
        
        # ethylene_aminewash_sep input
        eCO2R_TSA_sep.new_exchange(
            type="technosphere",
            name=ethylene_aminewash_sep["name"],
            unit=ethylene_aminewash_sep["unit"],
            amount=1.0,
            input=ethylene_aminewash_sep.key,
            ).save()
        
        # Wastewater output
        eCO2R_TSA_sep.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=-0.000763598,
            input=wastewater.key,
            ).save()
        
        # Definition of the reference product as ethylene_pre_cryo_sep
        eCO2R_TSA_sep['reference product'] = ("ethylene_pre_cryo_sep")
        eCO2R_TSA_sep.save()

        # Return the created eCO2R_TSA_sep activity
        return eCO2R_TSA_sep

    def create_eCO2R_cryo_sep(self, eol:Literal["yes", "no"]="yes", electricity=None, cool16=None, coolmin15=None, coolmin25=None, coolmin45=None, coolmin55=None, coolmin75=None,
                              ethylene_TSA_sep=None):
        """        
        Create the activity "eCO2R_cryo_sep" in the database "disco2very". The reference output is 1 kg of ethylene.
        Values and calculations are based on https://www.engineeringtoolbox.com/specific-heat-capacity-gases-d_159.html,
        https://webbook.nist.gov/cgi/cbook.cgi?ID=C74851&Mask=7
        and on Perry's Chemical Engineers' Handbook, 7th Edition (ISBN: 0-07-115448-5).
        User can define the activities linked to it, but not the amounts.

        Default parameters:
        - inputs:
            - electricity: market for electricity, medium voltage, DE: 0,53290 kWh_el/kg_C2H4
            - cooling energy down to 16 °C: market for cooling energy, GLO: 2,0085 MJ/kg_C2H4
            - cooling energy from 16 °C to -15 °C: market for cooling energy, at -15 °C, GLO: 0,17912 MJ/kg_C2H4
            - cooling energy from -15 °C to -25 °C: market for cooling energy, at -25 °C, GLO: 0,057779 MJ/kg_C2H4
            - cooling energy from -25 °C to -45 °C: market for cooling energy, at -45 °C, GLO: 0,11556 MJ/kg_C2H4
            - cooling energy from -45 °C to -55 °C: market for cooling energy, at -55 °C, GLO: 0,057779 MJ/kg_C2H4
            - cooling energy from -55 °C to -76 °C:disco2very activity: cooling energy production, at -76 °C, GLO: 0,60715 MJ/kg_C2H4
            - eCO2R_TSA_sep: disco2very activity: temperature swing adsorption (TSA) separation of ethylene, from eCO2R, DE:
                    1,0 kg_C2H4_pre_cryo_sep/kg_C2H4
        - outputs:
            - ethylene: ethylene production, from electrochemical CO2 reduction, RER: 1 kg_C2H4/kg_C2H4 (reference product)
            - CO2 emissions for EoL of by-products: biosphere flow: "carbon dioxide, fossil" in compartment "air" and subcompartment "urban air close to ground"
                amount: 3,7296 kg_CO2/kg_C2H4
            """
            
         # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if cool16 is None:
            cool16 = self.cool5
        if coolmin15 is None:
            coolmin15 = self.coolmin15
        if coolmin25 is None:
            coolmin25 = self.coolmin25
        if coolmin45 is None:
            coolmin45 = self.coolmin45
        if coolmin55 is None:
            coolmin55 = self.coolmin55
        if coolmin75 is None:
            coolmin75 = self.coolmin75
        if ethylene_TSA_sep is None:
            ethylene_TSA_sep = self.create_eCO2R_TSA_sep(electricity=electricity)

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"cryogenic separation of ethylene, from eCO2R. eol: {eol}")
        code = (f"eCO2R to ethylene, cryo sep|eol={eol}|elec={electricity.key}|cool16={cool16.key}|cool-15={coolmin15.key}|"
                f"cool-25={coolmin25.key}|cool-45={coolmin45.key}|cool-55={coolmin55.key}|cool-75={coolmin75.key}")
        
        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_cryo_sep = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_cryo_sep = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the cryogenic separation of ethylene from eCO2R. Cooling energy input: "+cool16["name"]+";"
                ""+coolmin15["name"]+"; "+coolmin25["name"]+"; "+coolmin45["name"]+"; "+coolmin55["name"]+"; "+coolmin75["name"]+".",
                )
            eCO2R_cryo_sep.save()

        # Delete existing exchanges only
        for exc in list(eCO2R_cryo_sep.exchanges()):
            exc.delete()

    # Add the production of ethylene, with the amount of 1 kg
        eCO2R_cryo_sep.new_exchange(
            type="production",
            name="ethylene",
            unit="kilogram",
            amount=1,
            input=eCO2R_cryo_sep.key,
            ).save()
    
    # TECHNOSPHERE EXCHANGES
    # Electricity input
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=0.5324327,
            input=electricity.key,
            ).save()
    
        # Cooling energy down to 16 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=cool16["name"],
            unit=cool16["unit"],
            amount=2.0085,
            input=cool16.key,
            ).save()
    
        # Cooling energy from 16 °C to -15 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=coolmin15["name"],
            unit=coolmin15["unit"],
            amount=0.17912,
            input=coolmin15.key,
            ).save()
    
        # Cooling energy from -15 °C to -25 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=coolmin25["name"],
            unit=coolmin25["unit"],
            amount=0.057779,
            input=coolmin25.key,
            ).save()
    
        # Cooling energy from -25 °C to -45 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=coolmin45["name"],
            unit=coolmin45["unit"],
            amount=0.11556,
            input=coolmin45.key,
            ).save()
    
        # Cooling energy from -45 °C to -55 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=coolmin55["name"],
            unit=coolmin55["unit"],
            amount=0.057779,
            input=coolmin55.key,
            ).save()
    
        # Cooling energy from -55 °C to -76 °C
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=coolmin75["name"],
            unit=coolmin75["unit"],
            amount=0.60715,
            input=coolmin75.key,
            ).save()
        
        # Consumption of 1 kg of ethylene pre cryo
        eCO2R_cryo_sep.new_exchange(
            type="technosphere",
            name=ethylene_TSA_sep["name"],
            unit=ethylene_TSA_sep["unit"],
            amount=1,
            input=ethylene_TSA_sep.key,
            ).save()
    
        # BIOSPHERE EXCHANGES
        # CO2 emissions for EoL of by-products
        if eol=="yes":
            eCO2R_cryo_sep.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=3.7296,
                input=self.CO2.key,
                ).save()
        
        # Definition of the reference product as carbon dioxide
        eCO2R_cryo_sep['reference product'] = ("ethylene")
        eCO2R_cryo_sep.save()

        # Return the created eCO2R_cryo_sep activity
        return eCO2R_cryo_sep
    
    def create_CC_point_source(self):
        """Creates the activity, "carbon capture, point source" in the database "disco2very". The reference output is 1 kg of
        captured carbon dioxide. It is nothing more than a flow of "market for carbon dioxide production, liquid"", with a carbon credit,
        modelled by the biosphere flow "Carbon dioxide, fossil; air; urban air close to ground".
    
        Parameters:
        - inputs:
            - co2_in: carbon dioxide production, liquid, RER: 1 kg_CO2/kg_CO2_capt
            - co2_credit: Carbon dioxide fossil; air; urban air close to ground: -1 kg_CO2_atm/kg_CO2_capt
                (biosphere flow, id: f9749677-9c9f-4678-ab55-c607dfdc2cb9)
    
        - outputs:
            - co2_capt: market for carbon dioxide, in chemical industry, GLO: 1 kg_CO2_capt/kg_CO2_capt (reference product)
        """

        # Definition of parameters
        co2_in = eidb.get(name="carbon dioxide production, liquid", location="RER")
        co2_credit = self.CO2

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("carbon capture, point source")
        code = ("CC point source")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            CC_point_source = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            CC_point_source = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the capture of carbon dioxide from a point source. It is modelled as a flow of" \
                "'carbon dioxide production, liquid', with a carbon credit, modelled by the biosphere flow 'Carbon dioxide, fossil; air;" \
                "urban air close to ground'.",
                )
            CC_point_source.save()

        # Delete existing exchanges only
        for exc in list(CC_point_source.exchanges()):
            exc.delete()

        # Add the production of captured co2, with the amount of 1 kg
        CC_point_source.new_exchange(
            type="production",
            name="market for carbon dioxide, in chemical industry",
            unit="kilogram",
            amount=1,
            input=CC_point_source.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Carbon dioxide input
        CC_point_source.new_exchange(
            type="technosphere",
            name=co2_in["name"],
            unit=co2_in["unit"],
            amount=1,
            input=co2_in.key,
            ).save()
        
        # BIOSPHERE EXCHANGES
        # Carbon dioxide credit
        CC_point_source.new_exchange(
            type="biosphere",
            name=co2_credit["name"],
            unit=co2_credit["unit"],
            amount=-1,
            input=co2_credit.key,
            ).save()
        
        # Definition of the reference product as captured carbon dioxide
        CC_point_source['reference product'] = ("market for carbon dioxide, in chemical industry")
        CC_point_source.save()
        
        # Return the created CC_point_source activity
        return CC_point_source

    def create_RWGS_CO(self, eol: Literal["yes", "no"]="no", electricity=None, carbon_dioxide=None, hydrogen=None, heat=None, factory=None):
        """
        Creates the activity "reverse water gas shift reaction to CO" in the database "disco2very". The reference
        output is 1 kg of carbon monoxide, still mixed with byproducts: water vapour and residual CO2. Flows are
        based on [M. Bachmann et al. - Syngas from What? Comparative Life-Cycle Assessment for Syngas Production
        from Biomass, CO2, and Steel Mill Off-Gases - 2023] and [Sternberg et al. - Life Cycle Assessment of
        Power-to-Gas: Syngas vs Methane - 2016], but further refined with stochiometric calculations. User can
        define the activities linked to it, but not the amounts.
        
        Default parameters:
        - inputs:
            - eol: "no"
            - electricity: market for electricity, medium voltage, DE: 1,3389 kWh_el/kg_CO
            - carbon_dioxide: market for carbon dioxide, in chemical industry, GLO: 1,58 kg_CO2/kg_CO
            - hydrogen: market for hydrogen, gaseous, low pressure, RER: 0,07212 kg_H2/kg_CO
            - heat: heat production, natural gas, at industrial furnace >100kW, Europe without Switzerland: 2,2 MJ/kg_CO
            - factory: chemical factory construction, organics, RER: 3,5842e-12 units/kg_CO
        - outputs:
            - carbon_monoxide_pre_cooling: 1kg_CO (reference product)
            - if eol=="yes":
                - biosphere flow: carbon dioxide, fossil; air; urbain air close to ground: 2,5712 kg_CO2
            
            Returns: The created RWGS_CO activity."""
        
        # Definition of parameters

        if electricity is None:
            electricity = self.electricity
        if carbon_dioxide is None:
            carbon_dioxide = self.carbon_dioxide
        if hydrogen is None:
            hydrogen = self.hydrogen
        if heat is None:
            heat = self.heat
        if factory is None:
            factory = self.factory
        
        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"reverse water gas shift reaction to CO. eol: {eol}")
        code = (f"RWGS to CO|eol={eol}|elec={electricity.key}|co2={carbon_dioxide.key}|h2={hydrogen.key}|heat={heat.key}|factory={factory.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            RWGS_CO = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            RWGS_CO = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the reverse water gas shift reaction to produce carbon monoxide." \
                "The reference product is carbon monoxide and 1 kg is produced. Electricity input: "+electricity["name"]+"."
                "Carbon dioxide input: "+carbon_dioxide["name"]+". Hydrogen input: "+hydrogen["name"]+". Heat input: "+heat["name"]+"."
                "Factory construction: "+factory["name"]+". Based on the paper [M. Bachmann et al. - Syngas from What?"
                "Comparative Life-Cycle Assessment for Syngas Production from Biomass, CO2, and Steel Mill Off-Gases - 2023] and"
                "on [Sternberg et al. - Life Cycle Assessment of Power-to-Gas: Syngas vs Methane - 2016].",
                )
            RWGS_CO.save()

        # Delete existing exchanges only
        for exc in list(RWGS_CO.exchanges()):
            exc.delete()

        # Add the production of carbon monoxide, with the amount of 1 kg
        RWGS_CO.new_exchange(
            type="production",
            name="carbon monoxide",
            unit="kilogram",
            amount=1,
            input=RWGS_CO.key,
            ).save()

        # TECHNOSPHERE EXCHANGES
        # Electricity input
        RWGS_CO.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=1.3389,
            input=electricity.key,
            ).save()
        
        # Carbon dioxide input
        RWGS_CO.new_exchange(
            type="technosphere",
            name=carbon_dioxide["name"],
            unit=carbon_dioxide["unit"],
            amount=1.58,
            input=carbon_dioxide.key,
            ).save()
        
        # Hydrogen input
        RWGS_CO.new_exchange(
            type="technosphere",
            name=hydrogen["name"],
            unit=hydrogen["unit"],
            amount=0.07212,
            input=hydrogen.key,
            ).save()
        
        # Heat input
        RWGS_CO.new_exchange(
            type="technosphere",
            name=heat["name"],
            unit=heat["unit"],
            amount=2.2,
            input=heat.key,
            ).save()
        
        # Factory construction input
        RWGS_CO.new_exchange(
            type="technosphere",
            name=factory["name"],
            unit=factory["unit"],
            amount=3.5842e-12,
            input=factory.key,
            ).save()
        
        # BIOSPHERE EXCHANGES
        # EoL CO2 emissions
        if eol=="yes":
            RWGS_CO.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=2.5712,
                input=self.CO2.key,
            ).save()
        
        
        # Definition of the reference product as carbon monoxide
        RWGS_CO['reference product'] = ("carbon monoxide pre cooling")
        RWGS_CO.save()

        # Return the created RWGS_CO activity
        return RWGS_CO
    
    def create_RWGS_CO_COOLING(self, cooling=None, rwgs_co=None):
        """
        Creates the activity "cooling of RWGS to CO" in the database "disco2very". The reference
        output is 1 kg of carbon monoxide, still mixed with byproducts: water vapour and residual
        CO2. This activity represents the cooling of the output stream of the RWGS reactor,
        from 1173 K down to 303 K, to condensate part of the water vapour and separate it from the
        carbon monoxide. Calculations are based on the Antoine equation. User can define the
        cooling input, but not the amount.

        Default parameters:
        - inputs:
            - cooling: market for cooling energy, GLO: 3,8887 MJ/kg_CO
            - rwgs_co: disco2very activity: reverse water gas shift reaction to CO, DE:
                1 kg_CO/kg_CO
        - outputs:
            - carbon_monoxide_pre_TSA: 1 kg_CO (reference product)
            - water: market for wastewater, unpolluted, RoW: 0,00061464 m³_H2O/kg_CO
        """
        # Definition of parameters
        if cooling is None:
            cooling = self.cool5
        if rwgs_co is None:
            rwgs_co = self.create_RWGS_CO()
        wastewater = self.wastewater

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = ("cooling of RWGS to CO")
        code = (f"cooling of RWGS to CO|cool={cooling.key}|rwgs={rwgs_co.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            RWGS_CO_cooling = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            RWGS_CO_cooling = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the cooling of the output stream of the reverse water gas" \
                "shift (RWGS) reactor to separate carbon monoxide from water vapour. Cooling energy input:" \
                ""+cooling["name"]+". Based on calculations with the Antoine equation.",
                )
            RWGS_CO_cooling.save()

        # Delete existing exchanges only
        for exc in list(RWGS_CO_cooling.exchanges()):
            exc.delete()
        
        # Add the production of carbon monoxide, with the amount of 1 kg
        RWGS_CO_cooling.new_exchange(
            type="production",
            name="carbon monoxide",
            unit="kilogram",
            amount=1,
            input=RWGS_CO_cooling.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Cooling energy input
        RWGS_CO_cooling.new_exchange(
            type="technosphere",
            name=cooling["name"],
            unit=cooling["unit"],
            amount=3.8887,
            input=cooling.key,
            ).save()
        
        # RWGS_CO input
        RWGS_CO_cooling.new_exchange(
            type="technosphere",
            name=rwgs_co["name"],
            unit=rwgs_co["unit"],
            amount=1,
            input=rwgs_co.key,
            ).save()
        
        # Wastewater output
        RWGS_CO_cooling.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=0.00061464,
            input=wastewater.key,
            ).save()
        
        # Definition of the reference product as carbon monoxide
        RWGS_CO_cooling['reference product'] = ("carbon monoxide pre TSA")
        RWGS_CO_cooling.save()

        # Return the created RWGS_CO_cooling activity
        return RWGS_CO_cooling

    def create_RWGS_TSA(self, eol: Literal["yes", "no"]="yes", heat=None, cooling=None, rwgs_co_cooling=None):
        """
        Creates the activity "RWGS_TSA" in the database "disco2very". The reference output is 1 kg of carbon monoxide,
        with a purity of 99% and traces of carbon dioxide. This activity represents the temperature swing adsorption
        (TSA) separation of the remaining water vapour from the carbon monoxide after the cooling step (activity 
        "cooling of RWGS to CO"). Calculations are based on [Perry's Chemical Engineers' Handbook, 7th Edition], on
        [https://www.engineeringtoolbox.com/specific-heat-capacity-gases-d_159.html], on [E.Scuiller et al. - 2023 - New
        Approach for Measuring the Specific Heat Capacity of Reactive Adsorbents Using Calorimetry] and on an isostere
        plot form the RWTH course [Einbindung regenerativer Energegiesysteme - Übung 7]. User can define the heat and
        cooling inputs, but not the amounts.

        Default parameters:
        - inputs:
            - eol: "yes"
            - heat: market for heat, district or industrial, natural gas, Europe without Switzerland: 0,13736 MJ/kg_CO
            - cooling: market for cooling energy, GLO: 0,11045 MJ/kg_CO
            - rwgs_co_cooling: disco2very activity: cooling of RWGS to CO, DE: 1 kg_CO/kg_CO
        - outputs:
            - carbon monoxide (reference product): 1 kg_CO
            - water: market for wastewater, unpolluted, RoW: 2,87E-05 m³_H2O/kg_CO
            - if eol=="yes":
                - carbon dioxide, fossil; air; urban air close to ground: 1,58 kg_CO2
        """
        # Definition of parameters
        if heat is None:
            heat = eidb.get(name="market for heat, district or industrial, natural gas", location="Europe without Switzerland")
        if cooling is None:
            cooling = self.cool5
        if rwgs_co_cooling is None:
            rwgs_co_cooling = self.create_RWGS_CO_COOLING()

        wastewater = self.wastewater

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"TSA separation of RWGS to CO. eol: {eol}")
        code = (f"RWGS to CO, TSA sep|eol={eol}|heat={heat.key}|cool={cooling.key}|rwgs_cool={rwgs_co_cooling.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            RWGS_TSA = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            RWGS_TSA = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the temperature swing adsorption (TSA) separation of carbon monoxide from water" \
                "vapour after the cooling step of the RWGS output stream. Heat input: "+heat["name"]+". Cooling energy input: "+cooling["name"]+"." \
                "Based on [Perry's Chemical Engineers' Handbook, 7th Edition], on [https://www.engineeringtoolbox.com/specific-heat-capacity-gases-d_159.html],"
                "on [E.Scuiller et al. - 2023 - New Approach for Measuring the Specific Heat Capacity of Reactive Adsorbents Using Calorimetry] and on"
                "an isostere plot form the RWTH course [Einbindung regenerativer Energegiesysteme - Übung 7].",
                )
            RWGS_TSA.save()

        # Delete existing exchanges only
        for exc in list(RWGS_TSA.exchanges()):
            exc.delete()

        # Add the production of carbon monoxide, with the amount of 1 kg
        RWGS_TSA.new_exchange(
            type="production",
            name="carbon monoxide",
            unit="kilogram",
            amount=1,
            input=RWGS_TSA.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Heat input
        RWGS_TSA.new_exchange(
            type="technosphere",
            name=heat["name"],
            unit=heat["unit"],
            amount=0.13736,
            input=heat.key,
            ).save()
        
        # Cooling energy input
        RWGS_TSA.new_exchange(
            type="technosphere",
            name=cooling["name"],
            unit=cooling["unit"],
            amount=0.11045,
            input=cooling.key,
            ).save()
        
        # RWGS_CO_COOLING input
        RWGS_TSA.new_exchange(
            type="technosphere",
            name=rwgs_co_cooling["name"],
            unit=rwgs_co_cooling["unit"],
            amount=1,
            input=rwgs_co_cooling.key,
            ).save()
        
        # Wastewater output
        RWGS_TSA.new_exchange(
            type="technosphere",
            name=wastewater["name"],
            unit=wastewater["unit"],
            amount=2.87E-05,
            input=wastewater.key,
            ).save()
        
        # BIOSPHERE EXCHANGES
        # EoL CO2 emissions
        if eol=="yes":
            RWGS_TSA.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=1.58,
                input=self.CO2.key,
            ).save()
            
        # Definition of the reference product as carbon monoxide
        RWGS_TSA['reference product'] = ("carbon monoxide")
        RWGS_TSA.save()

        # Return the created RWGS_TSA activity
        return RWGS_TSA

    def create_Syngas(self, eol: Literal["yes", "no"]="yes", hydrogen=None, carbon_monoxide=None, ratio_h2_to_co=3):
        """
        Creates the activity "syngas production from CO and H2" in the database "disco2very".
        The reference output is 1 kg of syngas. The user can define the hydrogen and carbon
        monoxide activities, as well as the molar ratio of H2 to CO in the syngas. This activity
        is purely a mixing of the two gases.
        
        Default parameters:
        - inputs:
            - eol: "yes"
            - ratio_h2_to_co: double, molar ratio of H2:CO: 3
            - carbon_monoxide: market for carbon monoxide, RER:
                m_CO = M_CO*(1 kg_SG)/(ratio_h2_to_co*M_H2+M_CO)
            - hydrogen: market for hydrogen, gaseous, low pressure, RER:
                m_H2 = M_H2*ratio_h2_to_co*(1 kg_SG)/(ratio_h2_to_co*M_H2+M_CO)

        - outputs:
            - syngas: 1 kg of syngas, with the defined molar ratio of H2 to CO (reference product)
            - if eol=="yes":
                - carbon dioxide, fossil; air; urban air close to ground: m_CO2 = m_CO * M_CO2/M_CO
        """

        # Definition of parameters:
        M_H2    = 2.016 # [kg/kmol]
        M_CO    = 28.01 # [kg/kmol]
        M_CO2   = 44.01 # [kg/kmol]
        
        # Calculation of hydrogen and CO mass, based on the defined molar ratio H2:CO
        m_CO = M_CO / (ratio_h2_to_co*M_H2 + M_CO)
        m_H2 = M_H2 * ratio_h2_to_co / (ratio_h2_to_co*M_H2 + M_CO)

        # Calculation of EoL CO2 emissions, based on CO mass and its stochiometric combustion
        m_CO2 = m_CO * M_CO2/M_CO

        if hydrogen is None:
            hydrogen = self.hydrogen
        if carbon_monoxide is None:
            carbon_monoxide = self.carbon_monoxide

        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"syngas production from CO and H2. eol: {eol}")
        code = (f"syngas from CO and H2|eol={eol}|h2={hydrogen.key}|co={carbon_monoxide.key}|ratio={ratio_h2_to_co}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            Syngas = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            Syngas = self.db.new_activity(
                name=name,
                code=code,
                location="RER",
                unit="kilogram",
                comment="This process represents the production of syngas from carbon monoxide and" \
                "hydrogen. It is a pure mixing process, where the user can define the molar ratio of" \
                "H2 to CO in the syngas. The reference product is 1 kg of syngas with a H2:CO molar ratio" \
                "of "+str(ratio_h2_to_co)+". Hydrogen input: "+hydrogen["name"]+". Carbon monoxide input: "
                +carbon_monoxide["name"]+".",
                )
            Syngas.save()

        # Delete existing exchanges only
        for exc in list(Syngas.exchanges()):
            exc.delete()

        # Add the production of syngas, with the amount of 1 kg
        Syngas.new_exchange(
            type="production",
            name="synthesis gas, "+str(ratio_h2_to_co)+" to 1",
            unit="kilogram",
            amount=1,
            input=Syngas.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Carbon monoxide input
        Syngas.new_exchange(
            type="technosphere",
            name=carbon_monoxide["name"],
            unit=carbon_monoxide["unit"],
            amount=m_CO,
            input=carbon_monoxide.key,
            ).save()
        
        # Hydrogen input
        Syngas.new_exchange(
            type="technosphere",
            name=hydrogen["name"],
            unit=hydrogen["unit"],
            amount=m_H2,
            input=hydrogen.key,
            ).save()
        
        # BIOSPHERE EXCHANGES
        # EoL CO2 emissions
        if eol=="yes":
            Syngas.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=m_CO2,
                input=self.CO2.key,
            ).save()
        
        # Definition of the reference product as syngas
        Syngas['reference product'] = ("synthesis gas, "+str(ratio_h2_to_co)+" to 1")
        Syngas.save()

        # Return the created Syngas activity
        return Syngas
    
    def create_eCO2R_to_CO(self, type: Literal["TUC", "Covestro"]= "TUC", current_density: Literal["1", "3"]="1", eol: Literal["yes", "no"]="no", electricity=None,
                           carbon_dioxide=None, water=None):
        """
        Creates the activity "electrochemical CO2 reduction to CO" in the database "disco2very". The reference output
        is 1 kg of carbon monoxide, still mixed with CO2, H2 and O2. This activity represents the electrochemical reduction of CO2 to CO. The user can decide
        if the process is modelled based on laboratory results from the Covestro cell, with the current density of 1 or 3 kA/m², or from the cell of the
        Technical University of Clausthal (TUC), with a current density of 1 kA/m². Further values and calculations are based on [M. Löffelholz et al. -
        2023 - Optimized scalable CuB catalyst with promising carbon footprint for the electrochemical CO2 reduction to ethylene], [J. Wyndorps et al. -
        2021 - Is electrochemical Co2 reduction the future technology for power-to-chemicals? An environmental comparison with H2-based pathways], and 
        [L.Ai et at. - 2022 - A Prospective Life Cycle Assessment of Electrochemical CO2 Reduction to Selective Formic Acid and Ethylene]

        Default parameters:
        - inputs:
            - eol: "no"
            - type: "TUC" or "Covestro", defines the cell to be modelled. Default is "TUC".
            - current_density: "1" or "3" [kA/m²], defines the current density to be modelled for the Covestro cell (TUC is only modelled for 1 kA/m²).
                Default is "1".
            - electricity: market for electricity, medium voltage, DE:
                - TUC, 1 kA/m²      : 7,5314 kWh_el/kg_CO
                - Covestro, 1 kA/m² : 16,538 kWh_el/kg_CO
                - Covestro, 3 kA/m² : 66,016 kWh_el/kg_CO
            - carbon_dioxide: disco2very activity: direct air capture, 2016, RER: 6,2849 kg_CO2/kg_CO
            - water: market for water, deionised, Europe without Switzerland:
                - TUC, 1 kA/m²      : 0,065984 kg_H2O/kg_CO
                - Covestro, 1 kA/m² : 0,12152 kg_H2O/kg_CO
                - Covestro, 3 kA/m² : 0,93505 kg_H2O/kg_CO
        
        - outputs:
            - CO_pre_DeOx: 1 kg of carbon monoxide, still mixed with CO2, H2 and O2 (reference product)
            - if eol=="yes":
                - carbon dioxde, fossil; air; urban air close to ground: 6,28490 kg_CO2
        """

        assert not (type=="TUC" and current_density!="1"), 'This configuration is not modeled. Please switch the type to Covestro or the current_density to 1'

        # Definition of parameters
        if electricity is None:
            electricity = self.electricity
        if carbon_dioxide is None:
            carbon_dioxide = self.create_DAC(electricity=electricity)
        if water is None:
            water = eidb.get(name="market for water, deionised", location="Europe without Switzerland")
        
        # Definition of name and code of the activity, based on the parameters used for its construction
        name = (f"electrochemical CO2 reduction to CO. eol: {eol}")
        code = (f"eCO2R to CO|eol={eol}|type={type}|current_density={current_density}|elec={electricity.key}|co2={carbon_dioxide.key}|h2o={water.key}")

        # Get the existing activity or create a new one
        from bw2data.errors import UnknownObject
        try:
            eCO2R_CO = self._get_existing_activity(code)
        except (UnknownObject, KeyError):
            eCO2R_CO = self.db.new_activity(
                name=name,
                code=code,
                location="DE",
                unit="kilogram",
                comment="This process represents the electrochemical reduction of CO2 to CO. The user can choose if the process is modelled based on the" \
                "cell of the Technical University of Clausthal (TUC) or on the cell of Covestro, as well as the current density to be modelled for the" \
                "Covestro cell. Electricity input: "+electricity["name"]+". Carbon dioxide input: "+carbon_dioxide["name"]+". Water input: "+water["name"]+"."
                "Based on [M. Löffelholz et al. - 2023 - Optimized scalable CuB catalyst with promising carbon footprint for the electrochemical CO2 reduction"
                "to ethylene], [J. Wyndorps et al. - 2021 - Is electrochemical Co2 reduction the future technology for power-to-chemicals? An environmental"
                "comparison with H2-based pathways], and [L.Ai et at. - 2022 - A Prospective Life Cycle Assessment of Electrochemical CO2 Reduction to"
                "Selective Formic Acid and Ethylene].",
                )
            eCO2R_CO.save()

        # Delete existing exchanges only
        for exc in list(eCO2R_CO.exchanges()):
            exc.delete()

        # Add the production of carbon monoxide, with the amount of 1 kg
        eCO2R_CO.new_exchange(
            type="production",
            name="CO_pre_DeOx",
            unit="kilogram",
            amount=1,
            input=eCO2R_CO.key,
            ).save()
        
        # TECHNOSPHERE EXCHANGES
        # Electricity input
        eCO2R_CO.new_exchange(
            type="technosphere",
            name=electricity["name"],
            unit=electricity["unit"],
            amount=16.538 if type=="Covestro" and current_density=="1" else 66.016 if type=="Covestro" and current_density=="3" else 7.5314,
            input=electricity.key,
            ).save()
        
        # Carbon dioxide input
        eCO2R_CO.new_exchange(
            type="technosphere",
            name=carbon_dioxide["name"],
            unit=carbon_dioxide["unit"],
            amount=6.2849,
            input=carbon_dioxide.key,
            ).save()
        
        # Water input
        eCO2R_CO.new_exchange(
            type="technosphere",
            name=water["name"],
            unit=water["unit"],
            amount=0.12152 if type=="Covestro" and current_density=="1" else 0.93505 if type=="Covestro" and current_density=="3" else 0.065984,
            input=water.key,
            ).save()
        
        # BIOSPHERE FLOWS
        # EoL CO2 emissions
        if eol=="yes":
            eCO2R_CO.new_exchange(
                type="biosphere",
                name=self.CO2["name"],
                unit=self.CO2["unit"],
                amount=6.28490,
                input=self.CO2.key,
            ).save()
        
        # Definition of the reference product as CO_pre_DeOx
        eCO2R_CO['reference product'] = ("CO_pre_DeOx")
        eCO2R_CO.save()

        # Return the created eCO2R_CO activity
        return eCO2R_CO
