# Import necessary libraries for program
class Imports:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import matplotlib.pyplot as plt
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    from jugaad_data.nse import index_raw
    import nsepy
    from nsepy import get_history
    from datetime import date
    import Article
    from scipy.stats import zscore
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.impute import SimpleImputer
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline

# User inputs name of company and goes through a personality test
class UserInteraction:
    class UserSearch:
        def search_company(initials):
                return nse_companies.get(initials.upper(), "Company not found")

        while True:
            initials = input("Enter NSE Initials (or 'quit' to exit): ")
            if initials.lower() == 'quit':
                break
            print(search_company(initials))

    # User does Personality Test
    class PersonalityTest:
        from abc import ABC, abstractmethod
        from enum import Enum

        class NetWorth(Enum):
            UNDER_100K = 1
            ONE_HUNDRED_TO_FIVE_HUNDRED_K = 2
            OVER_FIVE_HUNDRED_K = 3

        class IncomeLevel(Enum):
            UNDER_50K = 1
            FIFTY_TO_100K = 2
            OVER_100K = 3

        class AgeGroup(Enum):
            UNDER_30 = 1
            THIRTY_TO_FIFTY = 2
            OVER_FIFTY = 3

        class InvestmentExperience(Enum):
            BEGINNER = 1
            INTERMEDIATE = 2
            ADVANCED = 3

        class FinancialGoal(Enum):
            RETIREMENT = 1
            WEALTH_ACCUMULATION = 2
            INCOME_GENERATION = 3

        class InvestmentStyle(Enum):
            CONSERVATIVE = 1
            MODERATE = 2
            AGGRESSIVE = 3

        class InvestmentHorizon(Enum):
            SHORT_TERM = 1
            MEDIUM_TERM = 2
            LONG_TERM = 3

        class RiskTolerance(Enum):
            LOW = 1
            MEDIUM = 2
            HIGH = 3

        class Occupation(Enum):
            STUDENT = 1
            WORKING_PROFESSIONAL = 2
            BUSINESS_OWNER = 3

        class Education(Enum):
            HIGH_SCHOOL = 1
            COLLEGE = 2
            POSTGRADUATE = 3

        class MaritalStatus(Enum):
            SINGLE = 1
            MARRIED = 2
            DIVORCED = 3

        class Dependents(Enum):
            NONE = 1
            ONE = 2
            TWO_OR_MORE = 3

        class MultipleChoiceQuestion:
            def __init__(self, category, weight, question, options):
                self.category = category
                self.weight = weight
                self.question = question
                self.options = options

        class InvestmentProfile:
            def __init__(self, style, horizon, tolerance, goal, experience, age, income, net_worth, occupation, education, marital_status, dependents):
                self.style = style
                self.horizon = horizon
                self.tolerance = tolerance
                self.goal = goal
                self.experience = experience
                self.age = age
                self.income = income
                self.net_worth = net_worth
                self.occupation = occupation
                self.education = education
                self.marital_status = marital_status
                self.dependents = dependents

        class Question(ABC):
            def __init__(self, category, weight):
                self.category = category
                self.weight = weight
                self.options = []

            def ask(self):
                pass
        class InvestingPersonalityTest:
            def __init__(self):
                self.questions = [
                    MultipleChoiceQuestion("Risk Tolerance", 2, "How much risk are you willing to take?", ["Very little", "Some", "A lot"]),
                    MultipleChoiceQuestion("Investment Horizon", 3, "What is your investment time frame?", ["Less than 1 year", "1-5 years", "More than 5 years"]),
                    MultipleChoiceQuestion("Investment Style", 2, "What is your investment goal?", ["Preserve capital", "Generate income", "Grow wealth"]),
                    MultipleChoiceQuestion("Financial Goal", 2, "What is your financial goal?", ["Retirement", "Wealth accumulation", "Income generation"]),
                    MultipleChoiceQuestion("Investment Experience", 1, "What is your investment experience?", ["Beginner", "Intermediate", "Advanced"]),
                    MultipleChoiceQuestion("Age", 1, "What is your age?", ["Under 30", "30-50", "Over 50"]),
                    MultipleChoiceQuestion("Income", 1, "What is your annual income?", ["Less than $50,000", "$50,000-$100,000", "More than $100,000"]),
                    MultipleChoiceQuestion("Net Worth", 1, "What is your net worth?", ["Less than $100,000", "$100,000-$500,000", "More than $500,000"]),
                    MultipleChoiceQuestion("Occupation", 1, "What is your occupation?", ["Student", "Working professional", "Business owner"]),
                    MultipleChoiceQuestion("Education", 1, "What is your education level?", ["High school", "College", "Postgraduate"]),
                    MultipleChoiceQuestion("Marital Status", 1, "What is your marital status?", ["Single", "Married", "Divorced"]),
                    MultipleChoiceQuestion("Dependents", 1, "How many dependents do you have?", ["None", "One", "Two or more"]),
                    # Add more questions here
                ]

            def administer_test(self):
                answers = {}
                for question in self.questions:
                    answer = input(question.question + " ")
                    answers[question.category] = answer
                return answers

            def calculate_profile(self, answers):
                style= self.calculate_investment_style(answers)
                horizon = self.calculate_investment_horizon(answers)
                tolerance = self.calculate_risk_tolerance(answers)
                goal = self.calculate_financial_goal(answers)
                experience = self.calculate_investment_experience(answers)
                age = self.calculate_age(answers)
                income = self.calculate_income(answers)
                net_worth = self.calculate_net_worth(answers)
                occupation = self.calculate_occupation(answers)
                education = self.calculate_education(answers)
                marital_status = self.calculate_marital_status(answers)
                dependents = self.calculate_dependents(answers)

                return InvestmentProfile(style, horizon, tolerance, goal, experience, age, income, net_worth, occupation, education, marital_status, dependents)

            def calculate_investment_style(self, answers):
                if answers["Investment Style"] == "Preserve capital":
                    return InvestmentStyle.CONSERVATIVE
                elif answers["Investment Style"] == "Generate income":
                    return InvestmentStyle.MODERATE
                else:
                    return InvestmentStyle.AGGRESSIVE

            def calculate_investment_horizon(self, answers):
                if answers["Investment Horizon"] == "Less than 1 year":
                    return InvestmentHorizon.SHORT_TERM
                elif answers["Investment Horizon"] == "1-5 years":
                    return InvestmentHorizon.MEDIUM_TERM
                else:
                    return InvestmentHorizon.LONG_TERM

            def calculate_risk_tolerance(self, answers):
                if answers["Risk Tolerance"] == "Very little":
                    return RiskTolerance.LOW
                elif answers["Risk Tolerance"] == "Some":
                    return RiskTolerance.MEDIUM
                else:
                    return RiskTolerance.HIGH

            def calculate_financial_goal(self, answers):
                if answers["Financial Goal"] == "Retirement":
                    return FinancialGoal.RETIREMENT
                elif answers["Financial Goal"] == "Wealth accumulation":
                    return FinancialGoal.WEALTH_ACCUMULATION
                else:
                    return FinancialGoal.INCOME_GENERATION

            def calculate_investment_experience(self, answers):
                if answers["Investment Experience"] == "Beginner":
                    return InvestmentExperience.BEGINNER
                elif answers["Investment Experience"] == "Intermediate":
                    return InvestmentExperience.INTERMEDIATE
                else:
                    return InvestmentExperience.ADVANCED

            def calculate_age(self, answers):
                if answers["Age"] == "Under 30":
                    return AgeGroup.UNDER_30
                elif answers["Age"] == "30-50":
                    return AgeGroup.THIRTY_TO_FIFTY
                else:
                    return AgeGroup.OVER_FIFTY

            def calculate_income(self, answers):
                if answers["Income"] == "Less than $50,000":
                    return IncomeLevel.UNDER_50K
                elif answers["Income"] == "$50,000-$100,000":
                    return IncomeLevel.FIFTY_TO_100K
                else:
                    return IncomeLevel.OVER_100K

            def calculate_net_worth(self, answers):
                if answers["Net Worth"] == "Less than $100,000":
                    return NetWorth.UNDER_100K
                elif answers["Net Worth"] == "$100,000-$500,000":
                    return NetWorth.ONE_HUNDRED_TO_FIVE_HUNDRED_K
                else:
                    return NetWorth.OVER_FIVE_HUNDRED_K

            def calculate_occupation(self, answers):
                if answers["Occupation"] == "Student":
                    return Occupation.STUDENT
                elif answers["Occupation"] == "Working professional":
                    return Occupation.WORKING_PROFESSIONAL
                else:
                    return Occupation.BUSINESS_OWNER

            def calculate_education(self, answers):
                if answers["Education"] == "High school":
                    return Education.HIGH_SCHOOL
                elif answers["Education"] == "College":
                    return Education.COLLEGE
                else:
                    return Education.POSTGRADUATE

            def calculate_marital_status(self, answers):
                if answers["Marital Status"] == "Single":
                    return MaritalStatus.SINGLE
                elif answers["Marital Status"] == "Married":
                    return MaritalStatus.MARRIED
                else:
                    return MaritalStatus.DIVORCED

            def calculate_dependents(self, answers):
                if answers["Dependents"] == "None":
                    return Dependents.NONE
                elif answers["Dependents"] == "One":
                    return Dependents.ONE
                else:
                    return Dependents.TWO_OR_MORE

            def main():
                test = InvestingPersonalityTest()
                answers = test.administer_test()
                profile = test.calculate_profile(answers)
                print("Your investment profile is:")
                print("Investment Style:", profile.style)
                print("Investment Horizon:", profile.horizon)
                print("Risk Tolerance:", profile.tolerance)
                print("Financial Goal:", profile.goal)
                print("Investment Experience:", profile.experience)
                print("Age:", profile.age)
                print("Income:", profile.income)
                print("Net Worth:", profile.net_worth)
                print("Occupation:", profile.occupation)
                print("Education:", profile.education)
                print("Marital Status:", profile.marital_status)
                print("Dependents:", profile.dependents)

            if __name__ == "__main__":
                main()

# Directory of  2384 companies
class NSEcorp:    
    nse_companies = {
            "INFY"; "Infosys",
            "TCS" ; "Tata Consultancy Services",
            "HDFCBANK"; "HDFC Bank",
            "RELIANCE" ; "Reliance Industries Limited",
            "TCS" ; "Tata Consultancy Services Limited",
            "HDFCBANK" ; "HDFC Bank Limited",
            "ICICIBANK" ; "ICICI Bank Limited",
            "BHARTIARTL" ; "Bharti Airtel Limited",
            "SBIN" ; "State Bank of India",
            "INFY" ; "Infosys Limited",
            "LICI" ; "Life Insurance Corporation Of India",
            "ITC" ; "ITC Limited",
            "HINDUNILVR" ; "Hindustan Unilever Limited",
            "LT" ; "Larsen & Toubro Limited",
            "BAJFINANCE" ; "Bajaj Finance Limited",
            "HCLTECH" ; "HCL Technologies Limited",
            "MARUTI" ; "Maruti Suzuki India Limited",
            "SUNPHARMA" ; "Sun Pharmaceutical Industries Limited",
            "ADANIENT" ; "Adani Enterprises Limited",
            "KOTAKBANK" ; "Kotak Mahindra Bank Limited",
            "TITAN" ; "Titan Company Limited",
            "ONGC" ; "Oil & Natural Gas Corporation Limited",
            "TATAMOTORS" ; "Tata Motors Limited",
            "NTPC" ; "NTPC Limited",
            "AXISBANK" ; "Axis Bank Limited",
            "DMART" ; "Avenue Supermarts Limited",
            "ADANIGREEN" ; "Adani Green Energy Limited",
            "ADANIPORTS" ; "Adani Ports and Special Economic Zone Limited",
            "ULTRACEMCO" ; "UltraTech Cement Limited",
            "ASIANPAINT" ; "Asian Paints Limited",
            "COALINDIA" ; "Coal India Limited",
            "BAJAJFINSV" ; "Bajaj Finserv Limited",
            "BAJAJ-AUTO" ; "Bajaj Auto Limited",
            "POWERGRID" ; "Power Grid Corporation of India Limited",
            "NESTLEIND" ; "Nestle India Limited",
            "WIPRO" ; "Wipro Limited",
            "M&M" ; "Mahindra & Mahindra Limited",
            "IOC" ; "Indian Oil Corporation Limited",
            "JIOFIN" ; "Jio Financial Services Limited",
            "HAL" ; "Hindustan Aeronautics Limited",
            "DLF" ; "DLF Limited",
            "ADANIPOWER" ; "Adani Power Limited",
            "JSWSTEEL" ; "JSW Steel Limited",
            "TATASTEEL" ; "Tata Steel Limited",
            "SIEMENS" ; "Siemens Limited",
            "IRFC" ; "Indian Railway Finance Corporation Limited",
            "VBL" ; "Varun Beverages Limited",
            "ZOMATO" ; "Zomato Limited",
            "PIDILITIND" ; "Pidilite Industries Limited",
            "GRASIM" ; "Grasim Industries Limited",
            "SBILIFE" ; "SBI Life Insurance Company Limited",
            "BEL" ; "Bharat Electronics Limited",
            "LTIM" ; "LTIMindtree Limited",
            "TRENT" ; "Trent Limited",
            "PNB" ; "Punjab National Bank",
            "INDIGO" ; "InterGlobe Aviation Limited",
            "BANKBARODA" ; "Bank of Baroda",
            "HDFCLIFE" ; "HDFC Life Insurance Company Limited",
            "ABB" ; "ABB India Limited",
            "BPCL" ; "Bharat Petroleum Corporation Limited",
            "PFC" ; "Power Finance Corporation Limited",
            "GODREJCP" ; "Godrej Consumer Products Limited",
            "TATAPOWER" ; "Tata Power Company Limited",
            "HINDALCO" ; "Hindalco Industries Limited",
            "HINDZINC" ; "Hindustan Zinc Limited",
            "TECHM" ; "Tech Mahindra Limited",
            "AMBUJACEM" ; "Ambuja Cements Limited",
            "INDUSINDBK" ; "IndusInd Bank Limited",
            "CIPLA" ; "Cipla Limited",
            "GAIL" ; "GAIL (India) Limited",
            "RECLTD" ; "REC Limited",
            "BRITANNIA" ; "Britannia Industries Limited",
            "UNIONBANK" ; "Union Bank of India",
            "ADANIENSOL" ; "Adani Energy Solutions Limited",
            "IOB" ; "Indian Overseas Bank",
            "LODHA" ; "Macrotech Developers Limited",
            "EICHERMOT" ; "Eicher Motors Limited",
            "CANBK" ; "Canara Bank",
            "TATACONSUM" ; "TATA CONSUMER PRODUCTS Limited",
            "DRREDDY" ; "Dr. Reddy's Laboratories Limited",
            "TVSMOTOR" ; "TVS Motor Company Limited",
            "ZYDUSLIFE" ; "Zydus Lifesciences Limited",
            "ATGL" ; "Adani Total Gas Limited",
            "VEDL" ; "Vedanta Limited",
            "CHOLAFIN" ; "Cholamandalam Investment and Finance Company Limited",
            "HAVELLS" ; "Havells India Limited",
            "HEROMOTOCO" ; "Hero MotoCorp Limited",
            "DABUR" ; "Dabur India Limited",
            "SHREECEM" ; "SHREE CEMENT Limited",
            "MANKIND" ; "Mankind Pharma Limited",
            "BAJAJHLDNG" ; "Bajaj Holdings & Investment Limited",
            "DIVISLAB" ; "Divi's Laboratories Limited",
            "APOLLOHOSP" ; "Apollo Hospitals Enterprise Limited",
            "NHPC" ; "NHPC Limited",
            "SHRIRAMFIN" ; "Shriram Finance Limited",
            "BOSCHLTD" ; "Bosch Limited",
            "TORNTPHARM" ; "Torrent Pharmaceuticals Limited",
            "ICICIPRULI" ; "ICICI Prudential Life Insurance Company Limited",
            "IDBI" ; "IDBI Bank Limited",
            "JSWENERGY" ; "JSW Energy Limited",
            "JINDALSTEL" ; "Jindal Steel & Power Limited",
            "BHEL" ; "Bharat Heavy Electricals Limited",
            "INDHOTEL" ; "The Indian Hotels Company Limited",
            "CUMMINSIND" ; "Cummins India Limited",
            "ICICIGI" ; "ICICI Lombard General Insurance Company Limited",
            "CGPOWER" ; "CG Power and Industrial Solutions Limited",
            "MCDOWELL-N" ; "United Spirits Limited",
            "HDFCAMC" ; "HDFC Asset Management Company Limited",
            "MAXHEALTH" ; "Max Healthcare Institute Limited",
            "SOLARINDS" ; "Solar Industries India Limited",
            "MOTHERSON" ; "Samvardhana Motherson International Limited",
            "INDUSTOWER" ; "Indus Towers Limited",
            "POLYCAB" ; "Polycab India Limited",
            "OFSS" ; "Oracle Financial Services Software Limited",
            "SRF" ; "SRF Limited",
            "IRCTC" ; "Indian Railway Catering And Tourism Corporation Limited",
            "COLPAL" ; "Colgate Palmolive (India) Limited",
            "LUPIN" ; "Lupin Limited",
            "NAUKRI" ; "Info Edge (India) Limited",
            "TIINDIA" ; "Tube Investments of India Limited",
            "INDIANB" ; "Indian Bank",
            "HINDPETRO" ; "Hindustan Petroleum Corporation Limited",
            "BERGEPAINT" ; "Berger Paints (I) Limited",
            "YESBANK" ; "Yes Bank Limited",
            "TORNTPOWER" ; "Torrent Power Limited",
            "OIL" ; "Oil India Limited",
            "SBICARD" ; "SBI Cards and Payment Services Limited",
            "IDEA" ; "Vodafone Idea Limited",
            "MARICO" ; "Marico Limited",
            "GODREJPROP" ; "Godrej Properties Limited",
            "AUROPHARMA" ; "Aurobindo Pharma Limited",
            "UCOBANK" ; "UCO Bank"
            "BANKINDIA" ; "Bank of India",
            "PERSISTENT" ; "Persistent Systems Limited",
            "MUTHOOTFIN" ; "Muthoot Finance Limited",
            "NMDC" ; "NMDC Limited",
            "ALKEM" ; "Alkem Laboratories Limited",
            "PIIND" ; "PI Industries Limited",
            "LTTS" ; "L&T Technology Services Limited",
            "GICRE" ; "General Insurance Corporation of India"
            "TATACOMM" ; "Tata Communications Limited",
            "JSL" ; "Jindal Stainless Limited",
            "MRF" ; "MRF Limited",
            "SAIL" ; "Steel Authority of India Limited",
            "PGHH" ; "Procter & Gamble Hygiene and Health Care Limited",
            "SUZLON" ; "Suzlon Energy Limited",
            "LINDEINDIA" ; "Linde India Limited",
            "SUPREMEIND" ; "Supreme Industries Limited",
            "CONCOR" ; "Container Corporation of India Limited",
            "OBEROIRLTY" ; "Oberoi Realty Limited",
            "ASTRAL" ; "Astral Limited",
            "IDFCFIRSTB" ; "IDFC First Bank Limited",
            "RVNL" ; "Rail Vikas Nigam Limited",
            "BHARATFORG" ; "Bharat Forge Limited",
            "CENTRALBK" ; "Central Bank of India"
            "JSWINFRA" ; "JSW Infrastructure Limited",
            "POLICYBZR" ; "PB Fintech Limited",
            "ASHOKLEY" ; "Ashok Leyland Limited",
            "THERMAX" ; "Thermax Limited",
            "PHOENIXLTD" ; "The Phoenix Mills Limited",
            "GMRINFRA" ; "GMR Airports Infrastructure Limited",
            "TATAELXSI" ; "Tata Elxsi Limited",
            "PATANJALI" ; "Patanjali Foods Limited",
            "SJVN" ; "SJVN Limited",
            "PRESTIGE" ; "Prestige Estates Projects Limited",
            "ACC" ; "ACC Limited",
            "NYKAA" ; "FSN E-Commerce Ventures Limited",
            "SUNDARMFIN" ; "Sundaram Finance Limited",
            "UBL" ; "United Breweries Limited",
            "ABCAPITAL" ; "Aditya Birla Capital Limited",
            "MPHASIS" ; "MphasiS Limited",
            "BALKRISIND" ; "Balkrishna Industries Limited",
            "DIXON" ; "Dixon Technologies (India) Limited",
            "MAHABANK" ; "Bank of Maharashtra"
            "KALYANKJIL" ; "Kalyan Jewellers India Limited",
            "SCHAEFFLER" ; "Schaeffler India Limited",
            "AWL" ; "Adani Wilmar Limited",
            "APLAPOLLO" ; "APL Apollo Tubes Limited",
            "TATATECH" ; "Tata Technologies Limited",
            "SONACOMS" ; "Sona BLW Precision Forgings Limited",
            "KPITTECH" ; "KPIT Technologies Limited",
            "FACT" ; "Fertilizers and Chemicals Travancore Limited",
            "PSB" ; "Punjab & Sind Bank"
            "PETRONET" ; "Petronet LNG Limited",
            "L&TFH" ; "L&T Finance Holdings Limited",
            "UNOMINDA" ; "UNO Minda Limited",
            "PAGEIND" ; "Page Industries Limited",
            "MRPL" ; "Mangalore Refinery and Petrochemicals Limited",
            "AUBANK" ; "AU Small Finance Bank Limited",
            "MAZDOCK" ; "Mazagon Dock Shipbuilders Limited",
            "HUDCO" ; "Housing & Urban Development Corporation Limited",
            "GUJGASLTD" ; "Gujarat Gas Limited",
            "NIACL" ; "The New India Assurance Company Limited",
            "CRISIL" ; "CRISIL Limited",
            "AIAENG" ; "AIA Engineering Limited",
            "FEDERALBNK" ; "The Federal Bank  Limited",
            "IREDA" ; "Indian Renewable Energy Development Agency Limited",
            "VOLTAS" ; "Voltas Limited",
            "DALBHARAT" ; "Dalmia Bharat Limited",
            "POONAWALLA" ; "Poonawalla Fincorp Limited",
            "MEDANTA" ; "Global Health Limited",
            "IRB" ; "IRB Infrastructure Developers Limited",
            "3MINDIA" ; "3M India Limited",
            "MFSL" ; "Max Financial Services Limited",
            "M&MFIN" ; "Mahindra & Mahindra Financial Services Limited",
            "UPL" ; "UPL Limited",
            "HONAUT" ; "Honeywell Automation India Limited",
            "BSE" ; "BSE Limited",
            "FLUOROCHEM" ; "Gujarat Fluorochemicals Limited",
            "COFORGE" ; "Coforge Limited",
            "LICHSGFIN" ; "LIC Housing Finance Limited",
            "GLAXO" ; "GlaxoSmithKline Pharmaceuticals Limited",
            "DELHIVERY" ; "Delhivery Limited",
            "BDL" ; "Bharat Dynamics Limited",
            "STARHEALTH" ; "Star Health and Allied Insurance Company Limited",
            "FORTIS" ; "Fortis Healthcare Limited",
            "BIOCON" ; "Biocon Limited",
            "COROMANDEL" ; "Coromandel International Limited",
            "NLCINDIA" ; "NLC India Limited",
            "TATAINVEST" ; "Tata Investment Corporation Limited",
            "JKCEMENT" ; "JK Cement Limited",
            "IPCALAB" ; "IPCA Laboratories Limited",
            "METROBRAND" ; "Metro Brands Limited",
            "KEI" ; "KEI Industries Limited",
            "ESCORTS" ; "Escorts Kubota Limited",
            "LLOYDSME" ; "Lloyds Metals And Energy Limited",
            "GLAND" ; "Gland Pharma Limited",
            "IGL" ; "Indraprastha Gas Limited",
            "NAM-INDIA" ; "Nippon Life India Asset Management Limited",
            "APOLLOTYRE" ; "Apollo Tyres Limited",
            "JUBLFOOD" ; "Jubilant Foodworks Limited",
            "POWERINDIA" ; "Hitachi Energy India Limited",
            "MSUMI" ; "Motherson Sumi Wiring India Limited",
            "BANDHANBNK" ; "Bandhan Bank Limited",
            "DEEPAKNTR" ; "Deepak Nitrite Limited",
            "ZFCVINDIA" ; "ZF Commercial Vehicle Control Systems India Limited",
            "AJANTPHARM" ; "Ajanta Pharma Limited",
            "KPRMILL" ; "K.P.R. Mill Limited",
            "SYNGENE" ; "Syngene International Limited",
            "EIHOTEL" ; "EIH Limited",
            "APARINDS" ; "Apar Industries Limited",
            "NATIONALUM" ; "National Aluminium Company Limited",
            "TATACHEM" ; "Tata Chemicals Limited",
            "GLENMARK" ; "Glenmark Pharmaceuticals Limited",
            "HINDCOPPER" ; "Hindustan Copper Limited",
            "GODREJIND" ; "Godrej Industries Limited",
            "NH" ; "Narayana Hrudayalaya Ltd."
            "BLUESTARCO" ; "Blue Star Limited",
            "EXIDEIND" ; "Exide Industries Limited",
            "ENDURANCE" ; "Endurance Technologies Limited",
            "JBCHEPHARM" ; "JB Chemicals & Pharmaceuticals Limited",
            "PAYTM" ; "One 97 Communications Limited",
            "ANGELONE" ; "Angel One Limited",
            "MOTILALOFS" ; "Motilal Oswal Financial Services Limited",
            "ITI" ; "ITI Limited",
            "360ONE" ; "360 ONE WAM Limited",
            "CARBORUNIV" ; "Carborundum Universal Limited",
            "AARTIIND" ; "Aarti Industries Limited",
            "SUNTV" ; "Sun TV Network Limited",
            "KIOCL" ; "KIOCL Limited",
            "ISEC" ; "ICICI Securities Limited",
            "RADICO" ; "Radico Khaitan Limited",
            "SUNDRMFAST" ; "Sundram Fasteners Limited",
            "CREDITACC" ; "CREDITACCESS GRAMEEN Limited",
            "COCHINSHIP" ; "Cochin Shipyard Limited",
            "HATSUN" ; "Hatsun Agro Product Limited",
            "MANYAVAR" ; "Vedant Fashions Limited",
            "CYIENT" ; "Cyient Limited",
            "GET&D" ; "GE T&D India Limited",
            "BRIGADE" ; "Brigade Enterprises Limited",
            "TIMKEN" ; "Timken India Limited",
            "NBCC" ; "NBCC (India) Limited",
            "JBMA" ; "JBM Auto Limited",
            "GILLETTE" ; "Gillette India Limited",
            "KANSAINER" ; "Kansai Nerolac Paints Limited",
            "LAURUSLABS" ; "Laurus Labs Limited",
            "GRINDWELL" ; "Grindwell Norton Limited",
            "FIVESTAR" ; "Five-Star Business Finance Limited",
            "SWANENERGY" ; "Swan Energy Limited",
            "CHOLAHLDNG" ; "Cholamandalam Financial Holdings Limited",
            "IRCON" ; "Ircon International Limited",
            "SKFINDIA" ; "SKF India Limited",
            "BSOFT" ; "BIRLASOFT Limited",
            "ASTERDM" ; "Aster DM Healthcare Limited",
            "RELAXO" ; "Relaxo Footwears Limited",
            "SONATSOFTW" ; "Sonata Software Limited",
            "GSPL" ; "Gujarat State Petronet Limited",
            "RATNAMANI" ; "Ratnamani Metals & Tubes Limited",
            "ABFRL" ; "Aditya Birla Fashion and Retail Limited",
            "APLLTD" ; "Alembic Pharmaceuticals Limited",
            "PFIZER" ; "Pfizer Limited",
            "RAMCOCEM" ; "The Ramco Cements Limited",
            'SIGNATURE' ; "Signatureglobal (India) Limited",
            "PEL" ; "Piramal Enterprises Limited",
            "ELGIEQUIP" ; "Elgi Equipments Limited",
            "LALPATHLAB" ; "Dr. Lal Path Labs Ltd."
            "EMAMILTD" ; "Emami Limited",
            "SANOFI" ; "Sanofi India Limited",
            "JYOTICNC" ; "Jyoti CNC Automation Limited",
            "TRIDENT" ; "Trident Limited",
            "CASTROLIND" ; "Castrol India Limited",
            "KAJARIACER" ; "Kajaria Ceramics Limited",
            "KAYNES" ; "Kaynes Technology India Limited",
            "CENTURYTEX" ; "Century Textiles & Industries Limited",
            "CHALET" ; "Chalet Hotels Limited",
            "DEVYANI" ; "Devyani International Limited",
            "CDSL" ; "Central Depository Services (India) Limited",
            "KEC" ; "KEC International Limited",
            "SCHNEIDER" ; "Schneider Electric Infrastructure Limited",
            "IDFC" ; "IDFC Limited",
            "BATAINDIA" ; "Bata India Limited",
            "CIEINDIA" ; "CIE Automotive India Limited",
            "KPIL" ; "Kalpataru Projects International Limited",
            "RRKABEL" ; "R R Kabel Limited",
            "SUMICHEM" ; "Sumitomo Chemical India Limited",
            "NATCOPHARM" ; "Natco Pharma Limited",
            "SUVENPHAR" ; "Suven Pharmaceuticals Limited",
            "CROMPTON" ; "Crompton Greaves Consumer Electricals Limited",
            "TRITURBINE" ; "Triveni Turbine Limited",
            "PPLPHARMA" ; "Piramal Pharma Limited",
            "INOXWIND" ; "Inox Wind Limited",
            "ACE" ; "Action Construction Equipment Limited",
            "ATUL" ; "Atul Limited",
            "CGCL" ; "Capri Global Capital Limited",
            "TVSHLTD" ; "TVS Holdings Limited",
            "SHYAMMETL" ; "Shyam Metalics and Energy Limited",
            "NUVAMA" ; "Nuvama Wealth Management Limited",
            "KIMS" ; "Krishna Institute of Medical Sciences Limited",
            "CELLO" ; "Cello World Limited",
            "PNBHOUSING" ; "PNB Housing Finance Limited",
            "REDINGTON" ; "Redington Limited",
            "LAXMIMACH" ; "Lakshmi Machine Works Limited",
            "JYOTHYLAB" ; "Jyothy Labs Limited",
            "CESC" ; "CESC Limited",
            "GODFRYPHLP" ; "Godfrey Phillips India Limited",
            "NSLNISP" ; "NMDC Steel Limited",
            "RITES" ; "RITES Limited",
            "CONCORDBIO" ; "Concord Biotech Limited",
            "INDIAMART" ; "Indiamart Intermesh Limited",
            "AEGISCHEM" ; "Aegis Logistics Limited",
            "OLECTRA" ; "Olectra Greentech Limited",
            "WHIRLPOOL" ; "Whirlpool of India Limited",
            "ANANDRATHI" ; "Anand Rathi Wealth Limited",
            "NAVINFLUOR" ; "Navin Fluorine International Limited",
            "JWL" ; "Jupiter Wagons Limited",
            "APTUS" ; "Aptus Value Housing Finance India Limited",
            "FINCABLES" ; "Finolex Cables Limited",
            "FINPIPE" ; "Finolex Industries Limited",
            "POLYMED" ; "Poly Medicure Limited",
            "VINATIORGA" ; "Vinati Organics Limited",
            "INTELLECT" ; "Intellect Design Arena Limited",
            "JAIBALAJI" ; "Jai Balaji Industries Limited",
            "J&KBANK" ; "The Jammu & Kashmir Bank Limited",
            "KARURVYSYA" ; "Karur Vysya Bank Limited",
            "BLUEDART" ; "Blue Dart Express Limited",
            "MANAPPURAM" ; "Manappuram Finance Limited",
            "AFFLE" ; "Affle (India) Limited",
            "NCC" ; "NCC Limited",
            "RBLBANK" ; "RBL Bank Limited",
            "TTML" ; "Tata Teleservices (Maharashtra) Limited",
            "BASF" ; "BASF India Limited",
            "VGUARD" ; "V-Guard Industries Limited",
            "CAMS" ; "Computer Age Management Services Limited",
            "GESHIP" ; "The Great Eastern Shipping Company Limited",
            "CENTURYPLY" ; "Century Plyboards (India) Limited",
            "CLEAN" ; "Clean Science and Technology Limited",
            "JINDALSAW" ; "Jindal Saw Limited",
            "FSL" ; "Firstsource Solutions Limited",
            "ZENSARTECH" ; "Zensar Technologies Limited",
            "SOBHA" ; "Sobha Limited",
            "CHAMBLFERT" ; "Chambal Fertilizers & Chemicals Limited",
            "DATAPATTNS" ; "Data Patterns (India) Limited",
            "CHENNPETRO" ; "Chennai Petroleum Corporation Limited",
            "WELCORP" ; "Welspun Corp Limited",
            "MGL" ; "Mahanagar Gas Limited",
            "KSB" ; "Ksb Limited",
            "WELSPUNLIV" ; "Welspun Living Limited",
            "HSCL" ; "Himadri Speciality Chemical Limited",
            "DCMSHRIRAM" ; "DCM Shriram Limited",
            "ASTRAZEN" ; "AstraZeneca Pharma India Limited",
            "ZEEL" ; "Zee Entertainment Enterprises Limited",
            "BEML" ; "BEML Limited",
            "HFCL" ; "HFCL Limited",
            "RAINBOW" ; "Rainbow Childrens Medicare Limited",
            "ABSLAMC" ; "Aditya Birla Sun Life AMC Limited",
            "HONASA" ; "Honasa Consumer Limited",
            "ASAHIINDIA" ; "Asahi India Glass Limited",
            "PVRINOX" ; "PVR INOX Limited",
            "ARE&M" ; "Amara Raja Energy & Mobility Limited",
            "IIFL" ; "IIFL Finance Limited",
            "BLS" ; "BLS International Services Limited",
            "ALOKINDS" ; "Alok Industries Limited",
            "VTL" ; "Vardhman Textiles Limited",
            "GRINFRA" ; "G R Infraprojects Limited",
            "HBLPOWER" ; "HBL Power Systems Limited",
            "WESTLIFE" ; "WESTLIFE FOODWORLD Limited",
            "RKFORGE" ; "Ramkrishna Forgings Limited",
            "KIRLOSENG" ; "Kirloskar Oil Engines Limited",
            "TITAGARH" ; "TITAGARH RAIL SYSTEMS Limited",
            "FINEORG" ; "Fine Organic Industries Limited",
            "AMBER" ; "Amber Enterprises India Limited",
            "BIKAJI" ; "Bikaji Foods International Limited",
            "SWSOLAR" ; "Sterling and Wilson Renewable Energy Limited",
            "RAYMOND" ; "Raymond Limited",
            "IEX" ; "Indian Energy Exchange Limited",
            "SPARC" ; "Sun Pharma Advanced Research Company Limited",
            "GRAPHITE" ; "Graphite India Limited",
            "SPLPETRO" ; "Supreme Petrochem Limited",
            "RAILTEL" ; "Railtel Corporation Of India Limited",
            "INGERRAND" ; "Ingersoll Rand (India) Limited",
            "ECLERX" ; "eClerx Services Limited",
            "JUNIPER" ; "Juniper Hotels Limited",
            "ERIS" ; "Eris Lifesciences Limited",
            "RHIM" ; "RHI MAGNESITA INDIA Limited",
            "ENGINERSIN" ; "Engineers India Limited",
            "MAHSEAMLES" ; "Maharashtra Seamless Limited",
            "HAPPSTMNDS" ; "Happiest Minds Technologies Limited",
            "JKTYRE" ; "JK Tyre & Industries Limited",
            "TEJASNET" ; "Tejas Networks Limited",
            "PNCINFRA" ; "PNC Infratech Limited",
            "NEWGEN" ; "Newgen Software Technologies Limited",
            "INOXINDIA" ; "INOX India Limited",
            "TANLA" ; "Tanla Platforms Limited",
            "BIRLACORPN" ; "Birla Corporation Limited",
            "BBTC" ; "Bombay Burmah Trading Corporation Limited",
            "GMDCLTD" ; "Gujarat Mineral Development Corporation Limited",
            "NUVOCO" ; "Nuvoco Vistas Corporation Limited",
            "AKZOINDIA" ; "Akzo Nobel India Limited",
            "CEATLTD" ; "CEAT Limited",
            "RPOWER" ; "Reliance Power Limited",
            "RELINFRA" ; "Reliance Infrastructure Limited",
            "GPIL" ; "Godawari Power And Ispat Limited",
            "ELECON" ; "Elecon Engineering Company Limited",
            "ANANTRAJ" ; "Anant Raj Limited",
            "ELECTCAST" ; "Electrosteel Castings Limited",
            "DBREALTY" ; "D B Realty Limited",
            "EQUITASBNK" ; "Equitas Small Finance Bank Limited",
            "KFINTECH" ; "Kfin Technologies Limited",
            "BAJAJELEC" ; "Bajaj Electricals Limited",
            "LATENTVIEW" ; "Latent View Analytics Limited",
            "JPPOWER" ; "Jaiprakash Power Ventures Limited",
            "GRANULES" ; "Granules India Limited",
            "AAVAS" ; "Aavas Financiers Limited",
            "AETHER" ; "Aether Industries Limited",
            "UTIAMC" ; "UTI Asset Management Company Limited",
            "LEMONTREE" ; "Lemon Tree Hotels Limited",
            "JKLAKSHMI" ; "JK Lakshmi Cement Limited",
            "GPPL" ; "Gujarat Pipavav Port Limited",
            "SFL" ; "Sheela Foam Limited",
            "PCBL" ; "PCBL Limited",
            "MAPMYINDIA" ; "C.E. Info Systems Limited",
            "ROUTE" ; "ROUTE MOBILE Limited",
            "CANFINHOME" ; "Can Fin Homes Limited",
            "CUB" ; "City Union Bank Limited",
            "SAPPHIRE" ; "Sapphire Foods India Limited",
            "CAPLIPOINT" ; "Caplin Point Laboratories Limited",
            "MINDACORP" ; "Minda Corporation Limited",
            "MMTC" ; "MMTC Limited",
            "PTCIL" ; "PTC Industries Limited",
            "IFCI" ; "IFCI Limited",
            "PRAJIND" ; "Praj Industries Limited",
            "VOLTAMP" ; "Voltamp Transformers Limited",
            "SCI" ; "Shipping Corporation Of India Limited",
            "USHAMART" ; "Usha Martin Limited",
            "EIDPARRY" ; "EID Parry India Limited",
            "RTNINDIA" ; "RattanIndia Enterprises Limited",
            "ANURAS" ; "Anupam Rasayan India Limited",
            "GLS" ; "Glenmark Life Sciences Limited",
            "DOMS" ; "DOMS Industries Limited",
            "INFIBEAM" ; "Infibeam Avenues Limited",
            "FORCEMOT" ; "FORCE MOTORS LTD"
            "ZYDUSWELL" ; "Zydus Wellness Limited",
            "STARCEMENT" ; "Star Cement Limited",
            "GODREJAGRO" ; "Godrej Agrovet Limited",
            "TTKPRESTIG" ; "TTK Prestige Limited",
            "ALKYLAMINE" ; "Alkyl Amines Chemicals Limited",
            "GNFC" ; "Gujarat Narmada Valley Fertilizers and Chemicals Limited",
            "KPIGREEN" ; "KPI Green Energy Limited",
            "CRAFTSMAN" ; "Craftsman Automation Limited",
            "MAHLIFE" ; "Mahindra Lifespace Developers Limited",
            "REDTAPE" ; "Redtape Limited",
            "JUBLPHARMA" ; "Jubilant Pharmova Limited",
            "NETWEB" ; "Netweb Technologies India Limited",
            "NETWORK18" ; "Network18 Media & Investments Limited",
            "PRSMJOHNSN" ; "Prism Johnson Limited",
            "METROPOLIS" ; "Metropolis Healthcare Limited",
            "CERA" ; "Cera Sanitaryware Limited",
            "SBFC" ; "SBFC Finance Limited",
            "GRSE" ; "Garden Reach Shipbuilders & Engineers Limited",
            "KIRLOSBROS" ; "Kirloskar Brothers Limited",
            "UJJIVANSFB" ; "Ujjivan Small Finance Bank Limited",
            "SHRIPISTON" ; "Shriram Pistons & Rings Limited",
            "RENUKA" ; "Shree Renuka Sugars Limited",
            "RATEGAIN" ; "Rategain Travel Technologies Limited",
            "WOCKPHARMA" ; "Wockhardt Limited",
            "SAFARI" ; "Safari Industries (India) Limited",
            "HAPPYFORGE" ; "Happy Forgings Limited",
            "TECHNOE" ; "Techno Electric & Engineering Company Limited",
            "SHOPERSTOP" ; "Shoppers Stop Limited",
            "IBULHSGFIN" ; "Indiabulls Housing Finance Limited",
            "SYRMA" ; "Syrma SGS Technology Limited",
            "TEGA" ; "Tega Industries Limited",
            "ACI" ; "Archean Chemical Industries Limited",
            "MEDPLUS" ; "Medplus Health Services Limited",
            "MAHSCOOTER" ; "Maharashtra Scooters Limited",
            "NEULANDLAB" ; "Neuland Laboratories Limited",
            "AZAD" ; "Azad Engineering Limited",
            "ESABINDIA" ; "Esab India Limited",
            "GALAXYSURF" ; "Galaxy Surfactants Limited",
            "ZENTEC" ; "Zen Technologies Limited",
            "JSWHL" ; "JSW Holdings Limited",
            "TV18BRDCST" ; "TV18 Broadcast Limited",
            "HOMEFIRST" ; "Home First Finance Company India Limited",
            "MHRIL" ; "Mahindra Holidays & Resorts India Limited",
            "POWERMECH" ; "Power Mech Projects Limited",
            "KTKBANK" ; "The Karnataka Bank Limited",
            "JLHL" ; "Jupiter Life Line Hospitals Limited",
            "MASTEK" ; "Mastek Limited",
            "PGHL" ; "Procter & Gamble Health Limited",
            "THOMASCOOK" ; "Thomas Cook  (India)  Limited",
            "CCL" ; "CCL Products (India) Limited",
            "GSFC" ; "Gujarat State Fertilizers & Chemicals Limited",
            "RAJESHEXPO" ; "Rajesh Exports Limited",
            "QUESS" ; "Quess Corp Limited",
            "VARROC" ; "Varroc Engineering Limited",
            "TMB" ; "Tamilnad Mercantile Bank Limited",
            "MANINFRA" ; "Man Infraconstruction Limited",
            "EASEMYTRIP" ; "Easy Trip Planners Limited",
            "VIPIND" ; "VIP Industries Limited",
            "IONEXCHANG" ; "ION Exchange (India) Limited",
            "RESPONIND" ; "Responsive Industries Limited",
            "MIDHANI" ; "Mishra Dhatu Nigam Limited",
            "EMIL" ; "Electronics Mart India Limited",
            "GAEL" ; "Gujarat Ambuja Exports Limited",
            "BALRAMCHIN" ; "Balrampur Chini Mills Limited",
            "STAR" ; "Strides Pharma Science Limited",
            "JUBLINGREA" ; "Jubilant Ingrevia Limited",
            "SARDAEN" ; "Sarda Energy & Minerals Limited",
            "JMFINANCIL" ; "JM Financial Limited",
            "SOUTHBANK" ; "The South Indian Bank Limited",
            "HEG" ; "HEG Limited",
            "CHEMPLASTS" ; "Chemplast Sanmar Limited",
            "ARVIND" ; "Arvind Limited",
            "RCF" ; "Rashtriya Chemicals and Fertilizers Limited",
            "NAVA" ; "NAVA Limited",
            "ALLCARGO" ; "Allcargo Logistics Limited",
            "ICIL" ; "Indo Count Industries Limited",
            "IWEL" ; "Inox Wind Energy Limited",
            "KNRCON" ; "KNR Constructions Limited",
            "FDC" ; "FDC Limited",
            "RELIGARE" ; "Religare Enterprises Limited",
            "GRAVITA" ; "Gravita India Limited",
            "RUSTOMJEE" ; "Keystone Realtors Limited",
            "MARKSANS" ; "Marksans Pharma Limited",
            "NIITMTS" ; "NIIT Learning Systems Limited",
            "AHLUCONT" ; "Ahluwalia Contracts (India) Limited",
            "JUSTDIAL" ; "Just Dial Limited",
            "TRIVENI" ; "Triveni Engineering & Industries Limited",
            "TVSSCS" ; "TVS Supply Chain Solutions Limited",
            "GARFIBRES" ; "Garware Technical Fibres Limited",
            "VESUVIUS" ; "Vesuvius India Limited",
            "SAREGAMA" ; "Saregama India Limited",
            "DBL" ; "Dilip Buildcon Limited",
            "INDIASHLTR" ; "India Shelter Finance Corporation Limited",
            "BLUEJET" ; "Blue Jet Healthcare Limited",
            "BALAMINES" ; "Balaji Amines Limited",
            "ISGEC" ; "Isgec Heavy Engineering Limited",
            "AVANTIFEED" ; "Avanti Feeds Limited",
            "INDIACEM" ; "The India Cements Limited",
            "BECTORFOOD" ; "Mrs. Bectors Food Specialities Limited",
            "CAMPUS" ; "Campus Activewear Limited",
            "LTFOODS" ; "LT Foods Limited",
            "VIJAYA" ; "Vijaya Diagnostic Centre Limited",
            "GOCOLORS" ; "Go Fashion (India) Limited",
            "BORORENEW" ; "BOROSIL RENEWABLES Limited",
            "LXCHEM" ; "Laxmi Organic Industries Limited",
            "GREENLAM" ; "Greenlam Industries Limited",
            "DEEPAKFERT" ; "Deepak Fertilizers and Petrochemicals Corporation Limited",
            "CMSINFO" ; "CMS Info Systems Limited",
            "KRBL" ; "KRBL Limited",
            "ETHOSLTD" ; "Ethos Limited",
            "TEXRAIL" ; "Texmaco Rail & Engineering Limited",
            "TCI" ; "Transport Corporation of India Limited",
            "IBREALEST" ; "Indiabulls Real Estate Limited",
            "JINDWORLD" ; "Jindal Worldwide Limited",
            "EMUDHRA" ; "eMudhra Limited",
            "PDSL" ; "PDS Limited",
            "GANESHHOUC" ; "Ganesh Housing Corporation Limited",
            "CSBBANK" ; "CSB Bank Limited",
            "SHAREINDIA" ; "Share India Securities Limited",
            "IFBIND" ; "IFB Industries Limited",
            "PRINCEPIPE" ; "Prince Pipes And Fittings Limited",
            "VAIBHAVGBL" ; "Vaibhav Global Limited",
            "ARVINDFASN" ; "Arvind Fashions Limited",
            "EDELWEISS" ; "Edelweiss Financial Services Limited",
            "SENCO" ; "Senco Gold Limited",
            "SPANDANA" ; "Spandana Sphoorty Financial Limited",
            "INDIGOPNTS" ; "Indigo Paints Limited",
            "GENUSPOWER" ; "Genus Power Infrastructures Limited",
            "SYMPHONY" ; "Symphony Limited",
            "HGINFRA" ; "H.G. Infra Engineering Limited",
            "TIPSINDLTD" ; "TIPS Industries Limited",
            "SIS" ; "SIS Limited",
            "MSTCLTD" ; "Mstc Limited",
            "NESCO" ; "Nesco Limited",
            "SANGHVIMOV" ; "Sanghvi Movers Limited",
            "SANDUMA" ; "Sandur Manganese & Iron Ores Limited",
            "UJJIVAN" ; "Ujjivan Financial Services Limited",
            "ITDCEM" ; "ITD Cementation India Limited",
            "CYIENTDLM" ; "Cyient DLM Limited",
            "EPL" ; "EPL Limited",
            "SUPRAJIT" ; "Suprajit Engineering Limited",
            "SUNTECK" ; "Sunteck Realty Limited",
            "HEMIPROP" ; "Hemisphere Properties India Limited",
            "MOIL" ; "MOIL Limited",
            "TIMETECHNO" ; "Time Technoplast Limited",
            "ASTRAMICRO" ; "Astra Microwave Products Limited",
            "TRIL" ; "Transformers And Rectifiers (India) Limited",
            "WONDERLA" ; "Wonderla Holidays Limited",
            "ASKAUTOLTD" ; "ASK Automotive Limited",
            "LLOYDSENGG" ; "LLOYDS ENGINEERING WORKS Limited",
            "GMMPFAUDLR" ; "GMM Pfaudler Limited",
            "SURYAROSNI" ; "Surya Roshni Limited",
            "VSTIND" ; "VST Industries Limited",
            "PTC" ; "PTC India Limited",
            "JKPAPER" ; "JK Paper Limited",
            "SANSERA" ; "Sansera Engineering Limited",
            "CHOICEIN" ; "Choice International Limited",
            "AURIONPRO" ; "Aurionpro Solutions Limited",
            "PAISALO" ; "Paisalo Digital Limited",
            "ITDC" ; "India Tourism Development Corporation Limited",
            "HNDFDS" ; "Hindustan Foods Limited",
            "PARADEEP" ; "Paradeep Phosphates Limited",
            "KESORAMIND" ; "Kesoram Industries Limited",
            "HCC" ; "Hindustan Construction Company Limited",
            "ORCHPHARMA" ; "Orchid Pharma Limited",
            "JAMNAAUTO" ; "Jamna Auto Industries Limited",
            "ICRA" ; "ICRA Limited",
            "RSYSTEMS" ; "R Systems International Limited",
            "PRUDENT" ; "Prudent Corporate Advisory Services Limited",
            "MTARTECH" ; "Mtar Technologies Limited",
            "UTKARSHBNK" ; "Utkarsh Small Finance Bank Limited",
            "RAIN" ; "Rain Industries Limited",
            "DYNAMATECH" ; "Dynamatic Technologies Limited",
            "JAICORPLTD" ; "Jai Corp Limited",
            "RBA" ; "Restaurant Brands Asia Limited",
            "GATEWAY" ; "Gateway Distriparks Limited",
            "PURVA" ; "Puravankara Limited",
            "GUJALKALI" ; "Gujarat Alkalies and Chemicals Limited",
            "NAZARA" ; "Nazara Technologies Limited",
            "RALLIS" ; "Rallis India Limited",
            "VRLLOG" ; "VRL Logistics Limited",
            "GABRIEL" ; "Gabriel India Limited",
            "DODLA" ; "Dodla Dairy Limited",
            "JKIL" ; "J.Kumar Infraprojects Limited",
            "ROLEXRINGS" ; "Rolex Rings Limited",
            "WABAG" ; "VA Tech Wabag Limited",
            "PRICOLLTD" ; "Pricol Limited",
            "HCG" ; "Healthcare Global Enterprises Limited",
            "AGI" ; "AGI Greenpac Limited",
            "DBCORP" ; "D.B.Corp Limited",
            "FUSION" ; "Fusion Micro Finance Limited",
            "DHANUKA" ; "Dhanuka Agritech Limited",
            "MASFIN" ; "MAS Financial Services Limited",
            "SULA" ; "Sula Vineyards Limited",
            "TDPOWERSYS" ; "TD Power Systems Limited",
            "GALLANTT" ; "Gallantt Ispat Limited",
            "JAYNECOIND" ; "Jayaswal Neco Industries Limited",
            "GULFOILLUB" ; "Gulf Oil Lubricants India Limited",
            "SAMHI" ; "Samhi Hotels Limited",
            "TEAMLEASE" ; "Teamlease Services Limited",
            "KIRLPNU" ; "Kirloskar Pneumatic Company Limited",
            "EPIGRAL" ; "Epigral Limited",
            "TIIL" ; "Technocraft Industries (India) Limited",
            "GOPAL" ; "Gopal Snacks Limited",
            "JTEKTINDIA" ; "Jtekt India Limited",
            "HEIDELBERG" ; "HeidelbergCement India Limited",
            "SUNDARMHLD" ; "Sundaram Finance Holdings Limited",
            "RTNPOWER" ; "RattanIndia Power Limited",
            "STLTECH" ; "Sterlite Technologies Limited",
            "JPASSOCIAT" ; "Jaiprakash Associates Limited",
            "PATELENG" ; "Patel Engineering Limited",
            "ASHOKA" ; "Ashoka Buildcon Limited",
            "SINDHUTRAD" ; "Sindhu Trade Links Limited",
            "PGEL" ; "PG Electroplast Limited",
            "NFL" ; "National Fertilizers Limited",
            "ENTERO" ; "Entero Healthcare Solutions Limited",
            "JSFB" ; "Jana Small Finance Bank Limited",
            "GOKEX" ; "Gokaldas Exports Limited",
            "BANCOINDIA" ; "Banco Products (I) Limited",
            "VMART" ; "V-Mart Retail Limited",
            "SHANTIGEAR" ; "Shanthi Gears Limited",
            "GHCL" ; "GHCL Limited",
            "SUDARSCHEM" ; "Sudarshan Chemical Industries Limited",
            "WELENT" ; "Welspun Enterprises Limited",
            "FEDFINA" ; "Fedbank Financial Services Limited",
            "NOCIL" ; "NOCIL Limited",
            "TARC" ; "TARC Limited",
            "KKCL" ; "Kewal Kiran Clothing Limited",
            "ORIENTELEC" ; "Orient Electric Limited",
            "BOROLTD" ; "Borosil Limited",
            "KIRLOSIND" ; "Kirloskar Industries Limited",
            'BALMLAWRIE' ; "Balmer Lawrie & Company Limited",
            "FCL" ; "Fineotex Chemical Limited",
            "GRWRHITECH" ; "Garware Hi-Tech Films Limited",
            "SHARDAMOTR" ; "Sharda Motor Industries Limited",
            "PARKHOTELS" ; "Apeejay Surrendra Park Hotels Limited",
            "MAXESTATES" ; "Max Estates Limited",
            "TI" ; "Tilaknagar Industries Limited",
            "AMIORG" ; "Ami Organics Limited",
            "ORIENTCEM" ; "Orient Cement Limited",
            "SHILPAMED" ; "Shilpa Medicare Limited",
            "AARTIDRUGS" ; "Aarti Drugs Limited",
            "LGBBROSLTD" ; "LG Balakrishnan & Bros Limited",
            "AARTIPHARM" ; "Aarti Pharmalabs Limited",
            "TCIEXP" ; "TCI Express Limited",
            "WSTCSTPAPR" ; "West Coast Paper Mills Limited",
            "ADVENZYMES" ; "Advanced Enzyme Technologies Limited",
            "PRIVISCL" ; "Privi Speciality Chemicals Limited",
            "GREENPANEL" ; "Greenpanel Industries Limited",
            "VENUSPIPES" ; "Venus Pipes & Tubes Limited",
            "BBOX" ; "Black Box Limited",
            "IIFLSEC" ; "IIFL Securities Limited",
            "PILANIINVS" ; "Pilani Investment and Industries Corporation Limited",
            "ROSSARI" ; "Rossari Biotech Limited",
            "KSL" ; "Kalyani Steels Limited",
            "DCBBANK" ; "DCB Bank Limited",
            "IMAGICAA" ; "Imagicaaworld Entertainment Limited",
            "BAJAJHIND" ; "Bajaj Hindusthan Sugar Limited",
            "DCAL" ; "Dishman Carbogen Amcis Limited",
            "HARSHA" ; "Harsha Engineers International Limited",
            "BBL" ; "Bharat Bijlee Limited",
            "YATHARTH" ; "Yatharth Hospital & Trauma Care Services Limited",
            "ORISSAMINE" ; "The Orissa Minerals Development Company Limited",
            "THANGAMAYL" ; "Thangamayil Jewellery Limited",
            "ZAGGLE" ; "Zaggle Prepaid Ocean Services Limited",
            "BHARATRAS" ; "Bharat Rasayan Limited",
            "KOLTEPATIL" ; "Kolte - Patil Developers Limited",
            "KSCL" ; "Kaveri Seed Company Limited",
            "MEDIASSIST" ; "Medi Assist Healthcare Services Limited",
            "INOXGREEN" ; "Inox Green Energy Services Limited",
            "HATHWAY" ; "Hathway Cable & Datacom Limited",
            "SSWL" ; "Steel Strips Wheels Limited",
            "UNICHEMLAB" ; "Unichem Laboratories Limited",
            'CIGNITITEC' ; "Cigniti Technologies Limited",
            "IMFA" ; "Indian Metals & Ferro Alloys Limited",
            "ASHAPURMIN" ; "Ashapura Minechem Limited",
            "HGS" ; "Hinduja Global Solutions Limited",
            "MUTHOOTMF" ; "Muthoot Microfin Limited",
            "SUBROS" ; "Subros Limited",
            "RAMKY" ; "Ramky Infrastructure Limited",
            "SUNFLAG" ; "Sunflag Iron And Steel Company Limited",
            "CARERATING" ; "CARE Ratings Limited",
            "GENSOL" ; "Gensol Engineering Limited",
            "SKIPPER" ; "Skipper Limited",
            "LAOPALA" ; "La Opala RG Limited",
            "LUMAXTECH" ; "Lumax Auto Technologies Limited",
            "DCXINDIA" ; "DCX Systems Limited",
            "BOMDYEING" ; "Bombay Dyeing & Mfg Company Limited",
            "HIKAL" ; "Hikal Limited",
            "JISLJALEQS" ; "Jain Irrigation Systems Limited",
            "CUPID" ; "Cupid Limited",
            "AVALON" ; "Avalon Technologies Limited",
            "LUXIND" ; "Lux Industries Limited",
            "NUCLEUS" ; "Nucleus Software Exports Limited",
            "TASTYBITE" ; "Tasty Bite Eatables Limited",
            "SOTL" ; "Savita Oil Technologies Limited",
            "ARVSMART" ; "Arvind SmartSpaces Limited",
            "SANDHAR" ; "Sandhar Technologies Limited",
            "SALASAR" ; "Salasar Techno Engineering Limited",
            "NEOGEN" ; "Neogen Chemicals Limited",
            "DATAMATICS" ; "Datamatics Global Services Limited",
            "JTLIND" ; "JTL INDUSTRIES Limited",
            "ANUP" ; "The Anup Engineering Limited",
            "HERITGFOOD" ; "Heritage Foods Limited",
            "THYROCARE" ; "Thyrocare Technologies Limited",
            "VADILALIND" ; "Vadilal Industries Limited",
            "NAVNETEDUL" ; "Navneet Education Limited",
            "DISHTV" ; "Dish TV India Limited",
            "KDDL" ; "KDDL Limited",
            "KALAMANDIR" ; "Sai Silks (Kalamandir) Limited",
            "LANDMARK" ; "Landmark Cars Limited",
            "INDOCO" ; "Indoco Remedies Limited",
            "BAJAJCON" ; "Bajaj Consumer Care Limited",
            "TVSSRICHAK" ; "TVS Srichakra Limited",
            "CARTRADE" ; "Cartrade Tech Limited",
            "SBCL" ; "Shivalik Bimetal Controls Limited",
            "FIEMIND" ; "Fiem Industries Limited",
            "PRAKASH" ; "Prakash Industries Limited",
            "DELTACORP" ; "Delta Corp Limited",
            "RAJRATAN" ; "Rajratan Global Wire Limited",
            "IDEAFORGE" ; "Ideaforge Technology Limited",
            "MAHLOG" ; "Mahindra Logistics Limited",
            "PFOCUS" ; "Prime Focus Limited",
            "GREAVESCOT" ; "Greaves Cotton Limited",
            "DOLLAR" ; "Dollar Industries Limited",
            "UFLEX" ; "UFLEX Limited",
            "UNITECH" ; "Unitech Limited",
            "BFUTILITIE" ; "BF Utilities Limited",
            "SHARDACROP" ; "Sharda Cropchem Limited",
            "BANARISUG" ; "Bannari Amman Sugars Limited",
            "SEQUENT" ; "Sequent Scientific Limited",
            "GREENPLY" ; "Greenply Industries Limited",
            "MAITHANALL" ; "Maithan Alloys Limited",
            "SHK" ; "S H Kelkar and Company Limited",
            "SUNCLAY" ; "Sundaram Clayton Limited",
            "GUFICBIO" ; "Gufic Biosciences Limited",
            "BLSE" ; "BLS E-Services Limited",
            "DIACABS" ; "Diamond Power Infrastructure Limited",
            "ESAFSFB" ; "ESAF Small Finance Bank Limited",
            "VSTTILLERS" ; "V.S.T Tillers Tractors Limited",
            "HLEGLAS" ; "HLE Glascoat Limited",
            "BCG" ; "Brightcom Group Limited",
            "GOODLUCK" ; "Goodluck India Limited",
            "SWARAJENG" ; "Swaraj Engines Limited",
            "SEAMECLTD" ; "Seamec Limited",
            "SMLISUZU" ; "SML Isuzu Limited",
            "ASHIANA" ; "Ashiana Housing Limited",
            "DALMIASUG" ; "Dalmia Bharat Sugar and Industries Limited",
            "HINDWAREAP" ; "Hindware Home Innovation Limited",
            "SAGCEM" ; "Sagar Cements Limited",
            "SAKSOFT" ; "Saksoft Limited",
            "APOLLO" ; "Apollo Micro Systems Limited",
            "SUPRIYA" ; "Supriya Lifescience Limited",
            "AUTOAXLES" ; "Automotive Axles Limited",
            "STYLAMIND" ; "Stylam Industries Limited",
            "FLAIR" ; "Flair Writing Industries Limited",
            "VINDHYATEL" ; "Vindhya Telelinks Limited",
            "CARYSIL" ; "CARYSIL Limited",
            "THEJO" ; "Thejo Engineering Limited",
            "MPSLTD" ; "MPS Limited",
            "MARATHON" ; "Marathon Nextgen Realty Limited",
            "ISMTLTD" ; "ISMT Limited",
            "FILATEX" ; "Filatex India Limited",
            "NRBBEARING" ; "NRB Bearing Limited",
            "JCHAC" ; "Johnson Controls - Hitachi Air Conditioning India Limited",
            "MOLDTKPAC" ; "Mold-Tek Packaging Limited",
            "DREAMFOLKS" ; "Dreamfolks Services Limited",
            "GMRP&UI" ; "GMR Power and Urban Infra Limited",
            'SHALBY' ; "Shalby Limited",
            "INNOVACAP" ; "Innova Captab Limited",
            "PFS" ; "PTC India Financial Services Limited",
            "AJMERA" ; "Ajmera Realty & Infra India Limited",
            "HMAAGRO" ; "HMA Agro Industries Limited",
            "NILKAMAL" ; "Nilkamal Limited",
            "RPGLIFE" ; "RPG Life Sciences Limited",
            "TATVA" ; "Tatva Chintan Pharma Chem Limited",
            "STYRENIX" ; "Styrenix Performance Materials Limited",
            "QUICKHEAL" ; "Quick Heal Technologies Limited",
            "ACCELYA" ; "Accelya Solutions India Limited",
            "REPCOHOME" ; "Repco Home Finance Limited",
            "PCJEWELLER" ; "PC Jeweller Limited",
            "APOLLOPIPE" ; "Apollo Pipes Limited",
            "GANECOS" ; "Ganesha Ecosphere Limited",
            "PARAGMILK" ; "Parag Milk Foods Limited",
            "BAJEL" ; "Bajel Projects Limited",
            "PSPPROJECT" ; "PSP Projects Limited",
            "GIPCL" ; "Gujarat Industries Power Company Limited",
            "XPROINDIA" ; "Xpro India Limited",
            "PITTIENG" ; "Pitti Engineering Limited",
            "SHAKTIPUMP" ; "Shakti Pumps (India) Limited",
            "TIDEWATER" ; "Tide Water Oil Company (India) Limited",
            "SHAILY" ; "Shaily Engineering Plastics Limited",
            "EVEREADY" ; "Eveready Industries India Limited",
            "CONFIPET" ; "Confidence Petroleum India Limited",
            "POLYPLEX" ; "Polyplex Corporation Limited",
            "TAJGVK" ; "Taj GVK Hotels & Resorts Limited",
            "TIRUMALCHM" ; "Thirumalai Chemicals Limited",
            "SPECTRUM" ; "Spectrum Electrical Industries Limited",
            "PARAS" ; "Paras Defence and Space Technologies Limited",
            "EXICOM" ; "Exicom Tele-Systems Limited",
            "PGIL" ; "Pearl Global Industries Limited",
            "MANORAMA" ; "Manorama Industries Limited",
            "SOMANYCERA" ; "Somany Ceramics Limited",
            "KINGFA" ; "Kingfa Science & Technology (India) Limited",
            "FINOPB" ; "Fino Payments Bank Limited",
            "UNIPARTS" ; "Uniparts India Limited",
            "INDOSTAR" ; "IndoStar Capital Finance Limited",
            "DIVGIITTS" ; "Divgi Torqtransfer Systems Limited",
            "HINDOILEXP" ; "Hindustan Oil Exploration Company Limited",
            "SEPC" ; "SEPC Limited",
            "INDIAGLYCO" ; "India Glycols Limited",
            "IPL" ; "India Pesticides Limited",
            "GENESYS" ; "Genesys International Corporation Limited",
            "SANGHIIND" ; "Sanghi Industries Limited",
            "BSHSL" ; "Bombay Super Hybrid Seeds Limited",
            "SATIN" ; "Satin Creditcare Network Limited",
            "AXISCADES" ; "AXISCADES Technologies Limited",
            "ARTEMISMED" ; "Artemis Medicare Services Limited",
            "SASKEN" ; "Sasken Technologies Limited",
            "EIHAHOTELS" ; "EIH Associated Hotels Limited",
            "DHANI" ; "Dhani Services Limited",
            "PRECWIRE" ; "Precision Wires India Limited",
            "VIDHIING" ; "Vidhi Specialty Food Ingredients Limited",
            "APCOTEXIND" ; "Apcotex Industries Limited",
            "HUHTAMAKI" ; "Huhtamaki India Limited",
            "LUMAXIND" ; "Lumax Industries Limited",
            "GOCLCORP" ; "GOCL Corporation Limited",
            "WENDT" ; "Wendt (India) Limited",
            "DEN" ; "Den Networks Limited",
            "YATRA" ; "Yatra Online Limited",
            "HONDAPOWER" ; "Honda India Power Products Limited",
            "KCP" ; "KCP Limited",
            "EMSLimited" ; "EMS Limited",
            "JAGRAN" ; "Jagran Prakashan Limited",
            "SANGAMIND" ; "Sangam (India) Limited",
            "BEPL" ; "Bhansali Engineering Polymers Limited",
            "CAPACITE" ; "Capacit'e Infraprojects Limited",
            "NPST" ; "Network People Services Technologies Limited",
            "SUVEN" ; "Suven Life Sciences Limited",
            "MANINDS" ; "Man Industries (India) Limited",
            "DIAMONDYD" ; "Prataap Snacks Limited",
            "CENTUM" ; "Centum Electronics Limited",
            "VENKEYS" ; "Venky's (India) Limited",
            "IKIO" ; "IKIO Lighting Limited",
            "TCNSBRANDS" ; "TCNS Clothing Co. Limited",
            "OPTIEMUS" ; "Optiemus Infracom Limited",
            "MOREPENLAB" ; "Morepen Laboratories Limited",
            "MUKANDLTD" ; "Mukand Limited",
            "UDS" ; "Updater Services Limited",
            "ALEMBICLTD" ; "Alembic Limited",
            "RAMASTEEL" ; "Rama Steel Tubes Limited",
            "IOLCP" ; "IOL Chemicals and Pharmaceuticals Limited",
            "MBAPL" ; "Madhya Bharat Agro Products Limited",
            "MMFL" ; "MM Forgings Limited",
            "VAKRANGEE" ; "Vakrangee Limited",
            "TARSONS" ; "Tarsons Products Limited",
            "ASTEC" ; "Astec LifeSciences Limited",
            "JSLL" ; "Jeena Sikho Lifecare Limited",
            'VISHNU' ; "Vishnu Chemicals Limited",
            "TTKHLTCARE" ; "TTK Healthcare Limited",
            "MTNL" ; "Mahanagar Telephone Nigam Limited",
            "RPTECH" ; "Rashi Peripherals Limited",
            "RPSGVENT" ; "RPSG VENTURES Limited",
            "ORIENTHOT" ; "Oriental Hotels Limited",
            "GTLINFRA" ; "GTL Infrastructure Limited",
            "WEBELSOLAR" ; "Websol Energy System Limited",
            "JASH" ; "Jash Engineering Limited",
            "UGROCAP" ; "Ugro Capital Limited",
            "SDBL" ; "Som Distilleries & Breweries Limited",
            "HPL" ; "HPL Electric & Power Limited",
            "TCPLPACK" ; "TCPL Packaging Limited",
            "ADFFOODS" ; "ADF Foods Limited",
            "HMT" ; "HMT Limited",
            "MOL" ; "Meghmani Organics Limited",
            "MUFIN" ; "Mufin Green Finance Limited",
            "THEMISMED" ; "Themis Medicare Limited",
            "PANAMAPET" ; "Panama Petrochem Limited",
            "MANGLMCEM" ; "Mangalam Cement Limited",
            "SIGNPOST" ; "Signpost India Limited",
            "HITECH" ; "Hi-Tech Pipes Limited",
            "MAYURUNIQ" ; "Mayur Uniquoters Ltd"
            "SIYSIL" ; "Siyaram Silk Mills Limited",
            "JINDALPOLY" ; "Jindal Poly Films Limited",
            "KRSNAA" ; "Krsnaa Diagnostics Limited",
            "DEEPINDS" ; "Deep Industries Limited",
            "PNBGILTS" ; "PNB Gilts Limited",
            "HIL" ; "HIL Limited",
            "RICOAUTO" ; "Rico Auto Industries Limited",
            "BFINVEST" ; "BF Investment Limited",
            "GANDHAR" ; "Gandhar Oil Refinery (India) Limited",
            "IFGLEXPOR" ; "IFGL Refractories Limited",
            "BARBEQUE" ; "Barbeque Nation Hospitality Limited",
            "ANDHRAPAP" ; "ANDHRA PAPER Limited",
            "IRMENERGY" ; "IRM Energy Limited",
            "RIIL" ; "Reliance Industrial Infrastructure Limited",
            "SHRIRAMPPS" ; "Shriram Properties Limited",
            "'GLOBUSSPR'" ; "Globus Spirits Limited",
            "DREDGECORP" ; "Dredging Corporation of India Limited",
            'RUPA' ; "Rupa & Company Limited",
            "SJS" ; "S.J.S. Enterprises Limited",
            "PARACABLES" ; "Paramount Communications Limited",
            "EXPLEOSOL" ; "Expleo Solutions Limited",
            "PRECAM" ; "Precision Camshafts Limited",
            "BHARATWIRE" ; "Bharat Wire Ropes Limited",
            "GTPL" ; "GTPL Hathway Limited",
            "VPRPL" ; "Vishnu Prakash R Punglia Limited",
            "ADORWELD" ; "Ador Welding Limited",
            "DPABHUSHAN" ; "D. P. Abhushan Limited",
            "FOSECOIND" ; "Foseco India Limited",
            "SCILAL" ; "Shipping Corporation of India Land and Assets Limited",
            "SESHAPAPER" ; "Seshasayee Paper and Boards Limited",
            "JINDRILL" ; "Jindal Drilling And Industries Limited",
            "YASHO" ; "Yasho Industries Limited",
            "GREENPOWER" ; "Orient Green Power Company Limited",
            "NITINSPIN" ; "Nitin Spinners Limited",
            "GOLDIAM" ; "Goldiam International Limited",
            "PIXTRANS" ; "Pix Transmissions Limited",
            "SIGACHI" ; "Sigachi Industries Limited",
            "ARMANFIN" ; "Arman Financial Services Limited",
            "MONARCH" ; "Monarch Networth Capital Limited",
            "AMRUTANJAN" ; "Amrutanjan Health Care Limited",
            "FMGOETZE" ; "Federal-Mogul Goetze (India) Limited",
            "PENIND" ; "Pennar Industries Limited",
            "GEPIL" ; "GE Power India Limited",
            "PVSL" ; "Popular Vehicles and Services Limited",
            "JUBLINDS" ; "Jubilant Industries Limited",
            "63MOONS" ; "63 moons technologies Limited",
            "CANTABIL" ; "Cantabil Retail India Limited",
            "RAMCOIND" ; "Ramco Industries Limited",
            "JYOTISTRUC" ; "Jyoti Structures Limited",
            "VSSL" ; "Vardhman Special Steels Limited",
            "HERCULES" ; "Hercules Hoists Limited",
            "NSIL" ; "Nalwa Sons Investments Limited",
            "HLVLTD" ; "HLV Limited",
            "SURYODAY" ; "Suryoday Small Finance Bank Limited",
            "TNPL" ; "Tamil Nadu Newsprint & Papers Limited",
            "SUBEXLTD" ; "Subex Limited",
            "RISHABH" ; "Rishabh Instruments Limited",
            "SERVOTECH" ; "Servotech Power Systems Limited",
            "BHAGCHEM" ; "Bhagiradha Chemicals & Industries Limited",
            "ATFL" ; "Agro Tech Foods Limited",
            "OMAXE" ; "Omaxe Limited",
            "EVERESTIND" ; "Everest Industries Limited",
            "PREMEXPLN" ; "Premier Explosives Limited",
            "GNA" ; "GNA Axles Limited",
            "GOKULAGRO" ; "Gokul Agro Resources Limited",
            "TALBROAUTO" ; "Talbros Automotive Components Limited",
            "DCMSRIND" ; "DCM Shriram Industries Limited",
            "NELCO" ; "NELCO Limited",
            "KICL" ; "Kalyani Investment Company Limited",
            "MOTISONS" ; "Motisons Jewellers Limited",
            "5PAISA" ; "5Paisa Capital Limited",
            "KIRIINDUS" ; "Kiri Industries Limited",
            "CAPITALSFB" ; "Capital Small Finance Bank Limited",
            "INDRAMEDCO" ; "Indraprastha Medical Corporation Limited",
            "AEROFLEX" ; "Aeroflex Industries Limited",
            "SIRCA" ; "Sirca Paints India Limited",
            "SHANKARA" ; "Shankara Building Products Limited",
            "FAIRCHEMOR" ; "Fairchem Organics Limited",
            "BLKASHYAP" ; "B. L. Kashyap and Sons Limited",
            "TFCILTD" ; "Tourism Finance Corporation of India Limited",
            "SADHNANIQ" ; "Sadhana Nitrochem Limited",
            "INDNIPPON" ; "India Nippon Electricals Limited",
            "GVKPIL" ; "GVK Power & Infrastructure Limited",
            "RANEHOLDIN" ; "Rane Holdings Limited",
            "GEOJITFSL" ; "Geojit Financial Services Limited",
            "DCW" ; "DCW Limited",
            "SBGLP" ; "Suratwwala Business Group Limited",
            "BCLIND" ; "Bcl Industries Limited",
            "SMSPHARMA" ; "SMS Pharmaceuticals Limited",
            "DPSCLTD" ; "DPSC Limited",
            "CAMLINFINE" ; "Camlin Fine Sciences Limited",
            "CONTROLPR" ; "Control Print Limited",
            "REFEX" ; "Refex Industries Limited",
            "KRISHANA" ; "Krishana Phoschem Limited",
            "EKC" ; "Everest Kanto Cylinder Limited",
            "WHEELS" ; "Wheels India Limited",
            "JITFINFRA" ; "JITF Infralogistics Limited",
            "V2RETAIL" ; "V2 Retail Limited",
            "SALZERELEC" ; "Salzer Electronics Limited",
            "UNIVCABLES" ; "Universal Cables Limited",
            "SPAL" ; "S. P. Apparels Limited",
            "EPACK" ; "EPACK Durable Limited",
            "SWELECTES" ; "Swelect Energy Systems Limited",
            "GPTHEALTH" ; "GPT Healthcare Limited",
            "HITECHGEAR" ; "The Hi-Tech Gears Limited",
            "INSECTICID" ; "Insecticides (India) Limited",
            "PENINLAND" ; "Peninsula Land Limited",
            'SHREDIGCEM' ; "Shree Digvijay Cement Co.Ltd"
            "SPIC" ; "Southern Petrochemicals Industries Corporation  Limited",
            "NIITLTD" ; "NIIT Limited",
            "BIGBLOC" ; "Bigbloc Construction Limited",
            "ORIANA" ; "Oriana Power Limited",
            "SPCENET" ; "Spacenet Enterprises India Limited",
            "SHALPAINTS" ; "Shalimar Paints Limited",
            "KAMDHENU" ; "Kamdhenu Limited",
            "STOVEKRAFT" ; "Stove Kraft Limited",
            "RKSWAMY" ; "R K Swamy Limited",
            "NAVKARCORP" ; "Navkar Corporation Limited",
            "BUTTERFLY" ; "Butterfly Gandhimathi Appliances Limited",
            "DHAMPURSUG" ; "Dhampur Sugar Mills Limited",
            "NDTV" ; "New Delhi Television Limited",
            "ARIHANTSUP" ; "Arihant Superstructures Limited",
            "VASCONEQ" ; "Vascon Engineers Limited",
            "KUANTUM" ; "Kuantum Papers Limited",
            "APTECHT" ; "Aptech Limited",
            "INDIANHUME" ; "Indian Hume Pipe Company Limited",
            "ROSSELLIND" ; "Rossell India Limited",
            "AHL" ; "Abans Holdings Limited",
            "SOLARA" ; "Solara Active Pharma Sciences Limited",
            "SUMMITSEC" ; "Summit Securities Limited",
            "ALICON" ; "Alicon Castalloy Limited",
            "KSOLVES" ; "Ksolves India Limited",
            "IGPL" ; "IG Petrochemicals Limited",
            "STEELCAS" ; "Steelcast Limited",
            "POKARNA" ; "Pokarna Limited",
            "ATL" ; "Allcargo Terminals Limited",
            "ATULAUTO" ; "Atul Auto Limited",
            "GANESHBE" ; "Ganesh Benzoplast Limited",
            "COSMOFIRST" ; "COSMO FIRST Limited",
            "AWHCL" ; "Antony Waste Handling Cell Limited",
            "DWARKESH" ; "Dwarikesh Sugar Industries Limited",
            "HARIOMPIPE" ; "Hariom Pipe Industries Limited",
            "SMCGLOBAL" ; "SMC Global Securities Limited",
            "MADRASFERT" ; "Madras Fertilizers Limited",
            "DSSL" ; "Dynacons Systems & Solutions Limited",
            "STEELXIND" ; "STEEL EXCHANGE INDIA Limited",
            "MONTECARLO" ; "Monte Carlo Fashions Limited",
            "E2E" ; "E2E Networks Limited",
            "VERTOZ" ; "Vertoz Advertising Limited",
            "GIRIRAJ" ; "Giriraj Civil Developers Limited",
            "NGLFINE" ; "NGL Fine-Chem Limited",
            "IGARASHI" ; "Igarashi Motors India Limited",
            "JAYBARMARU" ; "Jay Bharat Maruti Limited",
            "AVTNPL" ; "AVT Natural Products Limited",
            "SKYGOLD" ; "Sky Gold Limited",
            "TVTODAY" ; "TV Today Network Limited",
            "XCHANGING" ; "Xchanging Solutions Limited",
            "ANDHRSUGAR" ; "The Andhra Sugars Limited",
            "ACLGATI" ; "Allcargo Gati Limited",
            "KOPRAN" ; "Kopran Limited",
            "ENIL" ; "Entertainment Network (India) Limited",
            "VERANDA" ; "Veranda Learning Solutions Limited",
            "MVGJL" ; "Manoj Vaibhav Gems N Jewellers Limited",
            "OMINFRAL" ; "OM INFRA Limited",
            "ZOTA" ; "Zota Health Care Limited",
            "SNOWMAN" ; "Snowman Logistics Limited",
            "RAJRILTD" ; "Raj Rayon Industries Limited",
            "PUNJABCHEM" ; "Punjab Chemicals & Crop Protection Limited",
            "KITEX" ; "Kitex Garments Limited",
            "TEXINFRA" ; "Texmaco Infrastructure & Holdings Limited",
            "IMPAL" ; "India Motor Parts and Accessories Limited",
            "HIMATSEIDE" ; "Himatsingka Seide Limited",
            "DOLATALGO" ; "Dolat Algotech Limited",
            "MANGCHEFER" ; "Mangalore Chemicals & Fertilizers Limited",
            "AGARIND" ; "Agarwal Industrial Corporation Limited",
            "REPRO" ; "Repro India Limited",
            "DOLPHIN" ; "Dolphin Offshore Enterprises (India) Limited",
            "UTTAMSUGAR" ; "Uttam Sugar Mills Limited",
            "CENTRUM" ; "Centrum Capital Limited",
            "HESTERBIO" ; "Hester Biosciences Limited",
            "BETA" ; "Beta Drugs Limited",
            'MARINE' ; "Marine Electricals (India) Limited",
            "BLISSGVS" ; "Bliss GVS Pharma Limited",
            "MSPL" ; "MSP Steel & Power Limited",
            "LINCOLN" ; "Lincoln Pharmaceuticals Limited",
            "SAURASHCEM" ; "Saurashtra Cement Limited",
            "MATRIMONY" ; "Matrimony.Com Limited",
            "HARDWYN" ; "Hardwyn India Limited",
            "GMBREW" ; "GM Breweries Limited",
            "SURAJEST" ; "Suraj Estate Developers Limited",
            "SICALLOG" ; "Sical Logistics Limited",
            "TREL" ; "Transindia Real Estate Limited",
            "PAKKA" ; "PAKKA Limited",
            "HERANBA" ; "Heranba Industries Limited",
            "RAMRAT" ; "Ram Ratna Wires Limited",
            "DVL" ; "Dhunseri Ventures Limited",
            "NACLIND" ; "NACL Industries Limited",
            "RML" ; "Rane (Madras) Limited",
            "NELCAST" ; "Nelcast Limited",
            "KOKUYOCMLN" ; "Kokuyo Camlin Limited",
            "ALLSEC" ; "Allsec Technologies Limited",
            "MACPOWER" ; "Macpower CNC Machines Limited",
            "INNOVANA" ; "Innovana Thinklabs Limited",
            "ROTO" ; "Roto Pumps Limited",
            "STERTOOLS" ; "Sterling Tools Limited",
            "MUKKA" ; "Mukka Proteins Limited",
            "TIL" ; "TIL Limited",
            "CSLFINANCE" ; "CSL Finance Limited",
            "GICHSGFIN" ; "GIC Housing Finance Limited",
            "SATIA" ; "Satia Industries Limited",
            "MUFTI" ; "Credo Brands Marketing Limited",
            "CREST" ; "Crest Ventures Limited",
            "AVADHSUGAR" ; "Avadh Sugar & Energy Limited",
            "WINDLAS" ; "Windlas Biotech Limited",
            "KRYSTAL" ; "Krystal Integrated Services Limited",
            "YUKEN" ; "Yuken India Limited",
            "ASIANENE" ; "Asian Energy Services Limited",
            "SPORTKING" ; "Sportking India Limited",
            "KOTYARK" ; "Kotyark Industries Limited",
            "CLSEL" ; "Chaman Lal Setia Exports Limited",
            "KAMOPAINTS" ; "Kamdhenu Ventures Limited",
            "HUBTOWN" ; "Hubtown Limited",
            "VALIANTORG" ; "Valiant Organics Limited",
            "INDOTECH" ; "Indo Tech Transformers Limited",
            "COFFEEDAY" ; "Coffee Day Enterprises Limited",
            "SYNCOMF" ; "Syncom Formulations (India) Limited",
            "NDRAUTO" ; "Ndr Auto Components Limited",
            "DHANBANK" ; "Dhanlaxmi Bank Limited",
            "ONEPOINT" ; "One Point One Solutions Limited",
            "HIRECT" ; "Hind Rectifiers Limited",
            "KABRAEXTRU" ; "Kabra Extrusion Technik Limited",
            "REMUS" ; "Remus Pharmaceuticals Limited",
            "INDORAMA" ; "Indo Rama Synthetics (India) Limited",
            "GULPOLY" ; "Gulshan Polyols Limited",
            "HEUBACHIND" ; "Heubach Colorants India Limited",
            "OAL" ; "Oriental Aromatics Limited",
            "CREATIVE" ; "Creative Newtech Limited",
            "ONWARDTEC" ; "Onward Technologies Limited",
            "URJA" ; "Urja Global Limited",
            "PVP" ; "PVP Ventures Limited",
            "ROHLTD" ; "Royal Orchid Hotels Limited",
            "BLAL" ; "BEML Land Assets Limited",
            "SATINDLTD" ; "Sat Industries Limited",
            "VIMTALABS" ; "Vimta Labs Limited",
            "ZUARIIND" ; "ZUARI INDUSTRIES Limited",
            "GSLSU" ; "Global Surfaces Limited",
            "NAHARSPING" ; "Nahar Spinning Mills Limited",
            "MANALIPETC" ; "Manali Petrochemicals Limited",
            "SASTASUNDR" ; "Sastasundar Ventures Limited",
            "DLINKINDIA" ; "D-Link (India) Limited",
            "RGL" ; "Renaissance Global Limited",
            "FOCUS" ; "Focus Lighting and Fixtures Limited",
            "GANDHITUBE" ; "Gandhi Special Tubes Limited",
            "KELLTONTEC" ; "Kellton Tech Solutions Limited",
            "PLATIND" ; "Platinum Industries Limited",
            "KERNEX" ; "Kernex Microsystems (India) Limited",
            "RAMCOSYS" ; "Ramco Systems Limited",
            "WALCHANNAG" ; "Walchandnagar Industries Limited",
            "CHEMFAB" ; "Chemfab Alkalis Limited",
            "UNIENTER" ; "Uniphos Enterprises Limited",
            "SARVESHWAR" ; "Sarveshwar Foods Limited",
            "BODALCHEM" ; "Bodal Chemicals Limited",
            "SEMAC" ; "SEMAC CONSULTANTS Limited",
            "VISAKAIND" ; "Visaka Industries Limited",
            "LIKHITHA" ; "Likhitha Infrastructure Limited",
            "WEL" ; "Wonder Electricals Limited",
            "ASAL" ; "Automotive Stampings and Assemblies Limited",
            "AMNPLST" ; "Amines & Plasticizers Limited",
            "GPTINFRA" ; "GPT Infraprojects Limited",
            "NINSYS" ; "NINtec Systems Limited",
            "SHIVALIK" ; "Shivalik Rasayan Limited",
            "VHL" ; "Vardhman Holdings Limited",
            "OWAIS" ; "Owais Metal And Mineral Processing Limited",
            "TRACXN" ; "Tracxn Technologies Limited",
            "EXCELINDUS" ; "Excel Industries Limited",
            "INFOBEAN" ; "InfoBeans Technologies Limited",
            "SANDESH" ; "The Sandesh Limited",
            "EIMCOELECO" ; "Eimco Elecon (India) Limited",
            "CENTENKA" ; "Century Enka Limited",
            "HPAL" ; "HP Adhesives Limited",
            "MICEL" ; "MIC Electronics Limited",
            "FAZE3Q" ; "Faze Three Limited",
            "ORIENTPPR" ; "Orient Paper & Industries Limited",
            "MAXIND" ; "Max India Limited",
            "GRPLTD" ; "GRP Limited",
            "DENORA" ; "De Nora India Limited",
            "ASALCBR" ; "Associated Alcohols & Breweries Ltd."
            "GKWLimited" ; "GKW Limited",
            "VLSFINANCE" ; "VLS Finance Limited",
            "SPECIALITY" ; "Speciality Restaurants Limited",
            "CHEMCON" ; "Chemcon Speciality Chemicals Limited",
            "SRHHYPOLTD" ; "Sree Rayalaseema Hi-Strength Hypo Limited",
            "PPL" ; "Prakash Pipes Limited",
            "NCLIND" ; "NCL Industries Limited",
            "HEXATRADEX" ; "Hexa Tradex Limited",
            "DECCANCE" ; "Deccan Cements Limited",
            "SUTLEJTEX" ; "Sutlej Textiles and Industries Limited",
            "SPENCERS" ; "Spencer's Retail Limited",
            "BASILIC" ; "Basilic Fly Studio Limited",
            "SILVERTUC" ; "Silver Touch Technologies Limited",
            "SCHAND" ; "S Chand And Company Limited",
            "AGSTRA" ; "AGS Transact Technologies Limited",
            "DYCL" ; "Dynamic Cables Limited",
            "ALPEXSOLAR" ; "Alpex Solar Limited",
            "RADIANTCMS" ; "Radiant Cash Management Services Limited",
            "AMBIKCO" ; "Ambika Cotton Mills Limited",
            "BAJAJHCARE" ; "Bajaj Healthcare Limited",
            "RSWM" ; "RSWM Limited",
            "SAKAR" ; "Sakar Healthcare Limited",
            "MUNJALAU" ; "Munjal Auto Industries Limited",
            "HMVL" ; "Hindustan Media Ventures Limited",
            "ELDEHSG" ; "Eldeco Housing And Industries Limited",
            "INDOAMIN" ; "Indo Amines Limited",
            "DENTALKART" ; "Vasa Denticity Limited",
            "VIKASLIFE" ; "Vikas Lifecare Limited",
            "RUSHIL" ; "Rushil Decor Limited",
            "ADSL" ; "Allied Digital Services Limited",
            "BCONCEPTS" ; "Brand Concepts Limited",
            "DBOL" ; "Dhampur Bio Organics Limited",
            "LINC" ; "Linc Limited",
            "RADHIKAJWE" ; "Radhika Jeweltech Limited",
            "DHARMAJ" ; "Dharmaj Crop Guard Limited",
            "MAGADSUGAR" ; "Magadh Sugar & Energy Limited",
            "CHEVIOT" ; "Cheviot Company Limited",
            "VINYAS" ; "Vinyas Innovative Technologies Limited",
            "BALAJITELE" ; "Balaji Telefilms Limited",
            "OSWALGREEN" ; "Oswal Greentech Limited",
            "ICEMAKE" ; "Ice Make Refrigeration Limited",
            "GFLLimited" ; "GFL Limited",
            "PANACEABIO" ; "Panacea Biotec Limited",
            "STCINDIA" ; "The State Trading Corporation of India Limited",
            "TRU" ; "TruCap Finance Limited",
            "UGARSUGAR" ; "The Ugar Sugar Works Limited",
            "MAANALU" ; "Maan Aluminium Limited",
            "NRAIL" ; "N R Agarwal Industries Limited",
            "JAGSNPHARM" ; "Jagsonpal Pharmaceuticals Limited",
            "GHCLTEXTIL" ; "GHCL Textiles Limited",
            "ASIANTILES" ; "Asian Granito India Limited",
            "DAVANGERE" ; "Davangere Sugar Company Limited",
            "POCL" ; "Pondy Oxides & Chemicals Limited",
            "KOTHARIPET" ; "Kothari Petrochemicals Limited",
            "CONSOFINVT" ; "Consolidated Finvest & Holdings Limited",
            "ACL" ; "Andhra Cements Limited",
            "ZUARI" ; "Zuari Agro Chemicals Limited",
            "GRMOVER" ; "GRM Overseas Limited",
            "BEDMUTHA" ; "Bedmutha Industries Limited",
            "SUKHJITS" ; "Sukhjit Starch & Chemicals Limited",
            "ESTER" ; "Ester Industries Limited",
            "WSI" ; "W S Industries (I) Limited",
            "TNPETRO" ; "Tamilnadu PetroProducts Limited",
            "FOODSIN" ; "Foods & Inns Limited",
            "THEINVEST" ; "The Investment Trust Of India Limited",
            "DHUNINV" ; "Dhunseri Investments Limited",
            "TBZ" ; "Tribhovandas Bhimji Zaveri Limited",
            "EMKAYTOOLS" ; "Emkay Taps and Cutting Tools Limited",
            "KECL" ; "Kirloskar Electric Company Limited",
            "EMAMIPAP" ; "Emami Paper Mills Limited",
            "ELECTHERM" ; "Electrotherm (India) Limited",
            "LOKESHMACH" ; "Lokesh Machines Limited",
            "SELAN" ; "Selan Exploration Technology Limited",
            "AVG" ; "AVG Logistics Limited",
            "SAHANA" ; "Sahana System Limited",
            "DMCC" ; "DMCC SPECIALITY CHEMICALS Limited",
            "NECLIFE" ; "Nectar Lifesciences Limited",
            "BIRLACABLE" ; "Birla Cable Limited",
            "GOACARBON" ; "Goa Carbon Limited",
            "JGCHEM" ; "J.G.Chemicals Limited",
            "ANNAPURNA" ; "Annapurna Swadisht Limited",
            "3IINFOLTD" ; "3i Infotech Limited",
            "WEALTH" ; "Wealth First Portfolio Managers Limited",
            "PARSVNATH" ; "Parsvnath Developers Limited",
            "ADVANIHOTR" ; "Advani Hotels & Resorts (India) Limited",
            "KRITI" ; "Kriti Industries (India) Limited",
            "ELIN" ; "Elin Electronics Limited",
            "DPWIRES" ; "D P Wires Limited",
            "MEGASOFT" ; "Megasoft Limited",
            "OCCL" ; "Oriental Carbon & Chemicals Limited",
            "MUNJALSHOW" ; "Munjal Showa Limited",
            "ZEEMEDIA" ; "Zee Media Corporation Limited",
            "SOLEX" ; "Solex Energy Limited",
            "MMP" ; "MMP Industries Limited",
            "CHEMBOND" ; "Chembond Chemicals Ltd"
            "JAYAGROGN" ; "Jayant Agro Organics Limited",
            "JPOLYINVST" ; "Jindal Poly Investment and Finance Company Limited",
            "MANAKSIA" ; "Manaksia Limited",
            "SREEL" ; "Sreeleathers Limited",
            "ONMOBILE" ; "OnMobile Global Limited",
            "SBC" ; "SBC Exports Limited",
            "SPMLINFRA" ; "SPML Infra Limited",
            "BHAGERIA" ; "Bhageria Industries Limited",
            "VALIANTLAB" ; "Valiant Laboratories Limited",
            "MENONBE" ; "Menon Bearings Limited",
            "KILITCH" ; "Kilitch Drugs (India) Limited",
            "PAVNAIND" ; "Pavna Industries Limited",
            "KHAICHEM" ; "Khaitan Chemicals & Fertilizers Limited",
            "FCSSOFT" ; "FCS Software Solutions Limited",
            "MALLCOM" ; "Mallcom (India) Limited",
            "NRL" ; "Nupur Recyclers Limited",
            "PHANTOMFX" ; "Phantom Digital Effects Limited",
            "APEX" ; "Apex Frozen Foods Limited",
            "KAMATHOTEL" ; "Kamat Hotels (I) Limited",
            "HTMEDIA" ; "HT Media Limited",
            "RUBYMILLS" ; "The Ruby Mills Limited",
            "ALBERTDAVD" ; "Albert David Limited",
            "KODYTECH" ; "Kody Technolab Limited",
            "LGHL" ; "Laxmi Goldorna House Limited",
            "PRIMESECU" ; "Prime Securities Limited",
            "RBZJEWEL" ; "RBZ Jewellers Limited",
            "PLASTIBLEN" ; "Plastiblends India Limited",
            "IRISDOREME" ; "Iris Clothings Limited",
            "PDMJEPAPER" ; "Pudumjee Paper Products Limited",
            "INDSWFTLAB" ; "Ind-Swift Laboratories Limited",
            "MIRZAINT" ; "Mirza International Limited",
            "STEL" ; "Stel Holdings Limited",
            "SAKUMA" ; "Sakuma Exports Limited",
            "SIMPLEXINF" ; "Simplex Infrastructures Limited",
            "ARROWGREEN" ; "Arrow Greentech Limited",
            "VINYLINDIA" ; "Vinyl Chemicals (India) Limited",
            "OSWALAGRO" ; "Oswal Agro Mills Limited",
            "HINDCOMPOS" ; "Hindustan Composites Limited",
            "ARIHANTCAP" ; "Arihant Capital Markets Limited",
            "MBLINFRA" ; "MBL Infrastructure Limited",
            "DEEPENR" ; "DEEP ENERGY RESOURCES Limited",
            "ORICONENT" ; "Oricon Enterprises Limited",
            "SHREYAS" ; "Shreyas Shipping & Logistics Limited",
            "SKMEGGPROD" ; "SKM Egg Products Export (India) Limited",
            "ORIENTCER" ; "ORIENT CERATECH Limited",
            "DIGISPICE" ; "DiGiSPICE Technologies Limited",
            "ZODIAC" ; "Zodiac Energy Limited",
            "KRISHIVAL" ; "Krishival Foods Limited",
            "JETAIRWAYS" ; "Jet Airways (India) Limited",
            "RATNAVEER" ; "Ratnaveer Precision Engineering Limited",
            "JINDALPHOT" ; "Jindal Photo Limited",
            "RADIOCITY" ; "Music Broadcast Limited",
            "HCL-INSYS" ; "HCL Infosystems Limited",
            "RBL" ; "Rane Brake Lining Limited",
            "KHADIM" ; "Khadim India Limited",
            "AXITA" ; "Axita Cotton Limited",
            "ASMS" ; "Bartronics India Limited",
            "BIRLAMONEY" ; "Aditya Birla Money Limited",
            "VISHNUINFR" ; "Vishnusurya Projects and Infra Limited",
            "VLEGOV" ; "VL E-Governance & IT Solutions Limited",
            "BBTCL" ; "B&B Triplewall Containers Limited",
            "NAGAFERT" ; "Nagarjuna Fertilizers and Chemicals Limited",
            "GEECEE" ; "GeeCee Ventures Limited",
            "RACE" ; "Race Eco Chain Limited",
            "RITCO" ; "Ritco Logistics Limited",
            "TCLCONS" ; "Tantia Constructions Limited",
            "BALAXI" ; "BALAXI PHARMACEUTICALS Limited",
            "PYRAMID" ; "Pyramid Technoplast Limited",
            "REMSONSIND" ; "Remsons Industries Limited",
            "UFO" ; "UFO Moviez India Limited",
            "ACCENTMIC" ; "Accent Microcell Limited",
            "PTL" ; "PTL Enterprises Limited",
            "INDOBORAX" ; "Indo Borax & Chemicals Limited",
            "MOLDTECH" ; "Mold-Tek Technologies Limited",
            "MAZDA" ; "Mazda Limited",
            "MINDTECK" ; "Mindteck (India) Limited",
            "COOLCAPS" ; "Cool Caps Industries Limited",
            "ALLETEC" ; "All E Technologies Limited",
            "20MICRONS" ; "20 Microns Limited",
            "VIKASECO" ; "Vikas EcoTech Limited",
            "ORIENTBELL" ; "Orient Bell Limited",
            "DONEAR" ; "Donear Industries Limited",
            "CAREERP" ; "Career Point Limited",
            "INTLCONV" ; "International Conveyors Limited",
            "SHREEPUSHK" ; "Shree Pushkar Chemicals & Fertilisers Limited",
            "PRITIKAUTO" ; "Pritika Auto Industries Limited",
            "DIAMINESQ" ; "Diamines & Chemicals Limited",
            "SILINV" ; "SIL Investments Limited",
            "BANSWRAS" ; "Banswara Syntex Limited",
            "SADBHAV" ; "Sadbhav Engineering Limited",
            "APCL" ; "Anjani Portland Cement Limited",
            "NAHARINDUS" ; "Nahar Industrial Enterprises Limited",
            "DUGLOBAL" ; "DUDIGITAL GLOBAL Limited",
            "GEEKAYWIRE" ; "Geekay Wires Limited",
            "SGIL" ; "Synergy Green Industries Limited",
            "TIRUPATI" ; "Shree Tirupati Balajee FIBC Limited",
            "MEDICAMEQ" ; "Medicamen Biotech Limited",
            "MEGATHERM" ; "Megatherm Induction Limited",
            "TPLPLASTEH" ; "TPL Plastech Limited",
            "RSSOFTWARE" ; "R. S. Software (India) Limited",
            "RBMINFRA" ; "Rbm Infracon Limited",
            "WANBURY" ; "Wanbury Limited",
            "GENUSPAPER" ; "Genus Paper & Boards Limited",
            "KANORICHEM" ; "Kanoria Chemicals & Industries Limited",
            "VSTL" ; "Vibhor Steel Tubes Limited",
            "LIBERTSHOE" ; "Liberty Shoes Limited",
            "GLOBAL" ; "Global Education Limited",
            "BRNL" ; "Bharat Road Network Limited",
            "NOVAAGRI" ; "Nova Agritech Limited",
            "TVSELECT" ; "TVS Electronics Limited",
            "VINSYS" ; "Vinsys IT Services India Limited",
            "NDL" ; "Nandan Denim Limited",
            "KRITINUT" ; "Kriti Nutrients Limited",
            "NAHARCAP" ; "Nahar Capital and Financial Services Limited",
            "CLEDUCATE" ; "CL Educate Limited",
            "ZIMLAB" ; "Zim Laboratories Limited",
            "SHIVAMAUTO" ; "Shivam Autotech Limited",
            "SYSTANGO" ; "Systango Technologies Limited",
            "UNIDT" ; "United Drilling Tools Limited",
            "SARLAPOLY" ; "Sarla Performance Fibers Limited",
            "WTICAB" ; "Wise Travel India Limited",
            "KRITIKA" ; "Kritika Wires Limited",
            "TRF" ; "TRF Limited",
            "AUTOIND" ; "Autoline Industries Limited",
            "MUTHOOTCAP" ; "Muthoot Capital Services Limited",
            "PURVFLEXI" ; "Purv Flexipack Limited",
            "NBIFIN" ; "N. B. I. Industrial Finance Company Limited",
            "AYMSYNTEX" ; "AYM Syntex Limited",
            "MIRCELECTR" ; "MIRC Electronics Limited",
            "NAHARPOLY" ; "Nahar Poly Films Limited",
            "IITL" ; "Industrial Investment Trust Limited",
            "GOLDTECH" ; "AION-TECH SOLUTIONS Limited",
            "VENUSREM" ; "Venus Remedies Limited",
            "KRISHNADEF" ; "Krishna Defence and Allied Industries Limited",
            "WINDMACHIN" ; "Windsor Machines Limited",
            "APS" ; "Australian Premium Solar (India) Limited",
            "APOLSINHOT" ; "Apollo Sindoori Hotels Limited",
            "BPL" ; "BPL Limited",
            "CYBERTECH" ; "Cybertech Systems And Software Limited",
            "KOTARISUG" ; "Kothari Sugars And Chemicals Limited",
            "IL&FSENGG" ; "IL&FS Engineering and Construction Company Limited",
            "SHIVAUM" ; "Shiv Aum Steels Limited",
            "ESSARSHPNG" ; "Essar Shipping Limited",
            "CELLECOR" ; "Cellecor Gadgets Limited",
            "PROZONER" ; "Prozone Realty Limited",
            "AARTISURF" ; "Aarti Surfactants Limited",
            "LAL" ; "Lorenzini Apparels Limited",
            "CINELINE" ; "Cineline India Limited",
            "TECHLABS" ; "Trident Techlabs Limited",
            "FELIX" ; "Felix Industries Limited",
            "NIPPOBATRY" ; "Indo-National Limited",
            "PREMIERPOL" ; "Premier Polyfilm Limited",
            "VARDHACRLC" ; "Vardhman Acrylics Limited",
            "RPPINFRA" ; "R.P.P. Infra Projects Limited",
            "HIGREEN" ; "Hi-Green Carbon Limited",
            "SURANI" ; "Surani Steel Tubes Limited",
            "NILAINFRA" ; "Nila Infrastructures Limited",
            'KAYA' ; "Kaya Limited",
            "SJLOGISTIC" ; "S J Logistics (India) Limited",
            "CRAYONS" ; "Crayons Advertising Limited",
            "NITCO" ; "Nitco Limited",
            "EUROBOND" ; "Euro Panel Products Limited",
            "MEDICO" ; "Medico Remedies Limited",
            "ALANKIT" ; "Alankit Limited",
            "EMAMIREAL" ; "Emami Realty Limited",
            "SAAKSHI" ; "Saakshi Medtech and Panels Limited",
            "SEJALLTD" ; "Sejal Glass Limited",
            "SHEMAROO" ; "Shemaroo Entertainment Limited",
            "BEWLTD" ; "BEW Engineering Limited",
            "IFBAGRO" ; "IFB Agro Industries Limited",
            "DICIND" ; "DIC India Limited",
            "PRECOT" ; "Precot Limited",
            "ASAHISONG" ; "Asahi Songwon Colors Limited",
            "ORBTEXP" ; "Orbit Exports Limited",
            "MODISONLTD" ; "MODISON Limited",
            "AURUM" ; "Aurum PropTech Limited",
            "KDL" ; "Kore Digital Limited",
            "EXXARO" ; "Exxaro Tiles Limited",
            "KARNIKA" ; "Karnika Industries Limited",
            "SAHYADRI" ; "Sahyadri Industries Limited",
            "SKP" ; "SKP Bearing Industries Limited",
            "KCPSUGIND" ; "KCP Sugar and Industries Corporation Limited",
            "MKPL" ; "M K Proteins Limited",
            "MANAKSTEEL" ; "Manaksia Steels Limited",
            "UNIVPHOTO" ; "Universus Photo Imagings Limited",
            "SCPL" ; "Sheetal Cool Products Limited",
            "SIGMA" ; "Sigma Solve Limited",
            "IZMO" ; "IZMO Limited",
            "SINTERCOM" ; "Sintercom India Limited",
            "FOCE" ; "Foce India Limited",
            "PODDARMENT" ; "Poddar Pigments Limited",
            "PLAZACABLE" ; "Plaza Wires Limited",
            "DCMNVL" ; "DCM Nouvelle Limited",
            "SHYAMCENT" ; "Shyam Century Ferrous Limited",
            "SAKHTISUG" ; "Sakthi Sugars Limited",
            "ESFL" ; "Essen Speciality Films Limited",
            "ATMASTCO" ; "Atmastco Limited",
            "KORE" ; "Jay Jalaram Technologies Limited",
            "LYKALABS" ; "Lyka Labs Limited",
            "STARPAPER" ; "Star Paper Mills Limited",
            "SRGHFL" ; "SRG Housing Finance Limited",
            "HINDMOTORS" ; "Hindustan Motors Limited",
            "PONNIERODE" ; "Ponni Sugars (Erode) Limited",
            "ASHIMASYN" ; "Ashima Limited",
            "KOTHARIPRO" ; "Kothari Products Limited",
            "GOKUL" ; "Gokul Refoils and Solvent Limited",
            "HITECHCORP" ; "Hitech Corporation Limited",
            "DIGIKORE" ; "Digikore Studios Limited",
            "KNAGRI" ; "KN Agri Resources Limited",
            "URAVI" ; "Uravi T and Wedge Lamps Limited",
            "LAWSIKHO" ; "Addictive Learning Technology Limited",
            "GOLDSTAR" ; "Goldstar Power Limited",
            "TCL" ; "Thaai Casting Limited",
            "RUCHIRA" ; "Ruchira Papers Limited",
            "MAHEPC" ; "Mahindra EPC Irrigation Limited",
            "PROV" ; "Proventus Agrocom Limited",
            "OSIAHYPER" ; "Osia Hyper Retail Limited",
            "MAWANASUG" ; "Mawana Sugars Limited",
            "RHL" ; "Robust Hotels Limited",
            "NATHBIOGEN" ; "Nath Bio-Genes (India) Limited",
            "EIFFL" ; "Euro India Fresh Foods Limited",
            "SARTELE" ; "Sar Televenture Limited",
            "VIPULLTD" ; "Vipul Limited",
            "ESSENTIA" ; "Integra Essentia Limited",
            "MWL" ; "Mangalam Worldwide Limited",
            "UCAL" ; "UCAL Limited",
            "PASUPTAC" ; "Pasupati Acrylon Limited",
            "DRONE" ; "Drone Destination Limited",
            "INFINIUM" ; "Infinium Pharmachem Limited",
            "COASTCORP" ; "Coastal Corporation Limited",
            "MOS" ; "Mos Utility Limited",
            "BIL" ; "Bhartiya International Limited",
            "INDTERRAIN" ; "Indian Terrain Fashions Limited",
            "ARIES" ; "Aries Agro Limited",
            "SHREERAMA" ; "Shree Rama Multi-Tech Limited",
            "DYNPRO" ; "Dynemic Products Limited",
            "SHERA" ; "Shera Energy Limited",
            "MHLXMIRU" ; "Mahalaxmi Rubtech Limited",
            "NDLVENTURE" ; "NDL Ventures Limited",
            "GULFPETRO" ; "GP Petroleums Limited",
            "TAKE" ; "Take Solutions Limited",
            "EQUIPPP" ; "Equippp Social Impact Technologies Limited",
            "SMLT" ; "Sarthak Metals Limited",
            "HARRMALAYA" ; "Harrisons  Malayalam Limited",
            "UMAEXPORTS" ; "Uma Exports Limited",
            "LANCORHOL" ; "Lancor Holdings Limited",
            "PROPEQUITY" ; "P. E. Analytics Limited",
            "SOFTTECH" ; "Softtech Engineers Limited",
            "MANOMAY" ; "Manomay Tex India Limited",
            "REPL" ; "Rudrabhishek Enterprises Limited",
            "RANASUG" ; "Rana Sugars Limited",
            "NEWJAISA" ; "Newjaisa Technologies Limited",
            "SHREYANIND" ; "Shreyans Industries Limited",
            "IVC" ; "IL&FS Investment Managers Limited",
            "RAJTV" ; "Raj Television Network Limited",
            "VIPCLOTHNG" ; "VIP Clothing Limited",
            "ABINFRA" ; "A B Infrabuild Limited",
            "TIPSFILMS" ; "Tips Films Limited",
            "SOUTHWEST" ; "South West Pinnacle Exploration Limited",
            "ABAN" ; "Aban Offshore Limited",
            "AIRAN" ; "Airan Limited",
            "SUPREMEPWR" ; "Supreme Power Equipment Limited",
            'VIRINCHI' ; "Virinchi Limited",
            "GOYALSALT" ; "Goyal Salt Limited",
            "TRIGYN" ; "Trigyn Technologies Limited",
            "EMKAY" ; "Emkay Global Financial Services Limited",
            "INDOTHAI" ; "Indo Thai Securities Limited",
            "RAJMET" ; "Rajnandini Metal Limited",
            "RAMAPHO" ; "Rama Phosphates Limited",
            "MGEL" ; "Mangalam Global Enterprise Limited",
            "LORDSCHLO" ; "Lords Chloro Alkali Limited",
            "SWARAJ" ; "Swaraj Suiting Limited",
            "RPPL" ; "Rajshree Polypack Limited",
            "ALMONDZ" ; "Almondz Global Securities Limited",
            "TEMBO" ; "Tembo Global Industries Limited",
            "ZODIACLOTH" ; "Zodiac Clothing Company Limited",
            "ASCOM" ; "Ascom Leasing & Investments Limited",
            "PILITA" ; "PIL ITALICA LIFESTYLE Limited",
            "AARON" ; "Aaron Industries Limited",
            "JAYSREETEA" ; "Jayshree Tea & Industries Limited",
            "KRISHCA" ; "Krishca Strapping Solutions Limited",
            "INTENTECH" ; "Intense Technologies Limited",
            "RUCHINFRA" ; "Ruchi Infrastructure Limited",
            "MURUDCERA" ; "Murudeshwar Ceramics Limited",
            "DRCSYSTEMS" ; "DRC Systems India Limited",
            "SUNDRMBRAK" ; "Sundaram Brake Linings Limited",
            "VISHWARAJ" ; "Vishwaraj Sugar Industries Limited",
            "USK" ; "Udayshivakumar Infra Limited",
            "HINDCON" ; "Hindcon Chemicals Limited",
            "OSWALSEEDS" ; "ShreeOswal Seeds And Chemicals Limited",
            "PAR" ; "Par Drugs And Chemicals Limited",
            "MEGASTAR" ; "Megastar Foods Limited",
            "ZEAL" ; "Zeal Global Services Limited",
            "BHAGYANGR" ; "Bhagyanagar India Limited",
            "KONSTELEC" ; "Konstelec Engineers Limited",
            "WELINV" ; "Welspun Investments and Commercials Limited",
            "MARALOVER" ; "Maral Overseas Limited",
            "MAGNUM" ; "Magnum Ventures Limited",
            "GINNIFILA" ; "Ginni Filaments Limited",
            "SADHAV" ; "Sadhav Shipping Limited",
            "TARACHAND" ; "Tara Chand InfraLogistic Solutions Limited",
            "KMSUGAR" ; "K.M.Sugar Mills Limited",
            "ASIANHOTNR" ; "Asian Hotels (North) Limited",
            "SVLL" ; "Shree Vasu Logistics Limited",
            "GUJAPOLLO" ; "Gujarat Apollo Industries Limited",
            "NURECA" ; "Nureca Limited",
            "STARTECK" ; "Starteck Finance Limited",
            "FROG" ; "Frog Cellsat Limited",
            "PRAXIS" ; "Praxis Home Retail Limited",
            "SHREEKARNI" ; "Shree Karni Fabcom Limited",
            "COMSYN" ; "Commercial Syn Bags Limited",
            "ABCOTS" ; "A B Cotspin India Limited",
            "BGRENERGY" ; "BGR Energy Systems Limited",
            "RKEC" ; "RKEC Projects Limited",
            "MCLEODRUSS" ; "Mcleod Russel India Limited",
            "CHAVDA" ; "Chavda Infra Limited",
            "LOYALTEX" ; "Loyal Textile Mills Limited",
            "KAPSTON" ; "Kapston Services Limited",
            "BROOKS" ; "Brooks Laboratories Limited",
            "THOMASCOTT" ; "Thomas Scott (India) Limited",
            "BASML" ; "Bannari Amman Spinning Mills Limited",
            "RVHL" ; "Ravinder Heights Limited",
            "PPAP" ; "PPAP Automotive Limited",
            "DELPHIFX" ; "DELPHI WORLD MONEY Limited",
            "ELGIRUBCO" ; "Elgi Rubber Company Limited",
            "SADBHIN" ; "Sadbhav Infrastructure Project Limited",
            "DCI" ; "Dc Infotech And Communication Limited",
            "ANMOL" ; "Anmol India Limited",
            "A2ZINFRA" ; "A2Z Infra Engineering Limited",
            "AHLEAST" ; "Asian Hotels (East) Limited",
            "VETO" ; "Veto Switchgears And Cables Limited",
            "MANORG" ; "Mangalam Organics Limited",
            "SAH" ; "Sah Polymers Limited",
            "ROXHITECH" ; "Rox Hi Tech Limited",
            "AIROLAM" ; "Airo Lam Limited",
            "BAIDFIN" ; "Baid Finserv Limited",
            "SELMC" ; "SEL Manufacturing Company Limited",
            "DRSDILIP" ; "DRS Dilip Roadlines Limited",
            "TEXMOPIPES" ; "Texmo Pipes and Products Limited",
            "TTL" ; "T T Limited",
            "GIRRESORTS" ; "GIR Natureview Resorts Limited",
            "MANAKCOAT" ; "Manaksia Coated Metals & Industries Limited",
            "JMA" ; "Jullundur Motor Agency (Delhi) Limited",
            "CORDSCABLE" ; "Cords Cable Industries Limited",
            "DEVIT" ; "Dev Information Technology Limited",
            "IRIS" ; "Iris Business Services Limited",
            "CROWN" ; "Crown Lifters Limited",
            "RANEENGINE" ; "Rane Engine Valve Limited",
            "OMAXAUTO" ; "Omax Autos Limited",
            "TREJHARA" ; "TREJHARA SOLUTIONS Limited",
            "NILASPACES" ; "Nila Spaces Limited",
            "BYKE" ; "The Byke Hospitality Ltd"
            "MODIRUBBER" ; "Modi Rubber Limited",
            "ANLON" ; "Anlon Technology Solutions Limited",
            "PRITI" ; "Priti International Limited",
            "PARAGON" ; "Paragon Fine and Speciality Chemical Limited",
            "NECCLTD" ; "North Eastern Carrying Corporation Limited",
            "CCHHL" ; "Country Club Hospitality & Holidays Limited",
            "SUPERHOUSE" ; "Superhouse Limited",
            "RAMANEWS" ; "Shree Rama Newsprint Limited",
            "HILTON" ; "Hilton Metal Forging Limited",
            "NDGL" ; "Naga Dhunseri Group Limited",
            "GSS" ; "GSS Infotech Limited",
            "LGBFORGE" ; "LGB Forge Limited",
            "INDOWIND" ; "Indowind Energy Limited",
            "MEP" ; "MEP Infrastructure Developers Limited",
            "BTML" ; "Bodhi Tree Multimedia Limited",
            "VMARCIND" ; "V Marc India Limited",
            "UNITEDPOLY" ; "United Polyfab Gujarat Limited",
            "RMDRIP" ; "R M Drip and Sprinklers Systems Limited",
            "ALPHAGEO" ; "Alphageo (India) Limited",
            "QMSMEDI" ; "QMS Medical Allied Services Limited",
            "USASEEDS" ; "Upsurge Seeds Of Agriculture Limited",
            "UNIHEALTH" ; "Unihealth Consultancy Limited",
            "ROCKINGDCE" ; "Rockingdeals Circular Economy Limited",
            "ESCONET" ; "Esconet Technologies Limited",
            "SMSLIFE" ; "SMS Lifesciences India Limited",
            "VARDMNPOLY" ; "Vardhman Polytex Limited",
            "AVONMORE" ; "Avonmore Capital & Management Services Limited",
            "LAGNAM" ; "Lagnam Spintex Limited",
            "AKSHARCHEM" ; "AksharChem India Limited",
            "MODTHREAD" ; "Modern Threads (India) Limited",
            "SSFL" ; "Srivari Spices And Foods Limited",
            "IEL" ; "Indiabulls Enterprises Limited",
            "BAHETI" ; "Baheti Recycling Industries Limited",
            "ZEELEARN" ; "Zee Learn Limited",
            "GENCON" ; "Generic Engineering Construction and Projects Limited",
            "SURANAT&P" ; "Surana Telecom and Power Limited",
            "DELAPLEX" ; "Delaplex Limited",
            "ASPINWALL" ; "Aspinwall and Company Limited",
            "DTIL" ; "Dhunseri Tea & Industries Limited",
            "DENEERS" ; "De Neers Tools Limited",
            "KCEIL" ; "Kay Cee Energy & Infra Limited",
            "AVPINFRA" ; "AVP Infracon Limited",
            "KANPRPLA" ; "Kanpur Plastipack Limited",
            "CMNL" ; "Chaman Metallics Limited",
            "RAJSREESUG" ; "Rajshree Sugars & Chemicals Limited",
            "KBCGLOBAL" ; "KBC Global Limited",
            "EFORCE" ; "Electro Force (India) Limited",
            "AURDIS" ; "Aurangabad Distillery Limited",
            "INDBANK" ; "Indbank Merchant Banking Services Limited",
            "TARMAT" ; "Tarmat Limited",
            "INM" ; "Interiors & More Limited",
            "MAXPOSURE" ; "Maxposure Limited",
            "INFOLLION" ; "Infollion Research Services Limited",
            "BAFNAPH" ; "Bafna Pharmaceuticals Limited",
            "MAHAPEXLTD" ; "Maha Rashtra Apex Corporation Limited",
            "EFACTOR" ; "E Factor Experiences Limited",
            "CLOUD" ; "Varanium Cloud Limited",
            "COMPUSOFT" ; "Compucom Software Limited",
            "DJML" ; "DJ Mediaprint & Logistics Limited",
            "DUCON" ; "Ducon Infratechnologies Limited",
            "ATLANTAA" ; "ATLANTAA Limited",
            "PRATHAM" ; "Pratham EPC Projects Limited",
            "MADHAVBAUG" ; "Vaidya Sane Ayurved Laboratories Limited",
            "MAHESHWARI" ; "Maheshwari Logistics Limited",
            "SHIVATEX" ; "Shiva Texyarn Limited",
            "SIGIND" ; "Signet Industries Limited",
            "DHRUV" ; "Dhruv Consultancy Services Limited",
            "SECL" ; "Salasar Exteriors and Contour Limited",
            "NITIRAJ" ; "Nitiraj Engineers Limited",
            "INVENTURE" ; "Inventure Growth & Securities Limited",
            "ATAM" ; "Atam Valves Limited",
            "SPECTSTM" ; "Spectrum Talent Management Limited",
            "AARVI" ; "Aarvi Encon Limited",
            "WEIZMANIND" ; "Weizmann Limited",
            "SALSTEEL" ; "S.A.L. Steel Limited",
            "ALPA" ; "Alpa Laboratories Limited",
            "GVPTECH" ; "GVP Infotech Limited",
            "SHREEOSFM" ; "Shree OSFM E-Mobility Limited",
            "SONAMAC" ; "Sona Machinery Limited",
            "GLOBALVECT" ; "Global Vectra Helicorp Limited",
            "MANAKALUCO" ; "Manaksia Aluminium Company Limited",
            "INCREDIBLE" ; "INCREDIBLE INDUSTRIES Limited",
            "BLBLimited" ; "BLB Limited",
            "EROSMEDIA" ; "Eros International Media Limited",
            "SUPREMEINF" ; "Supreme Infrastructure India Limited",
            "SMARTLINK" ; "Smartlink Holdings Limited",
            "VITAL" ; "Vital Chemtech Limited",
            "VISESHINFO" ; "Visesh Infotecnics Limited",
            "CADSYS" ; "Cadsys (India) Limited",
            "XELPMOC" ; "Xelpmoc Design And Tech Limited",
            "SWASTIK" ; "Swastik Pipe Limited",
            "PRAENG" ; "Prajay Engineers Syndicate Limited",
            "MUKTAARTS" ; "Mukta Arts Limited",
            "PARIN" ; "Parin Furniture Limited",
            "VIVIANA" ; "Viviana Power Tech Limited",
            "UMANGDAIRY" ; "Umang Dairies Limited",
            "BSL" ; "BSL Limited",
            "MAHASTEEL" ; "Mahamaya Steel Industries Limited",
            "ARCHIDPLY" ; "Archidply Industries Limited",
            "CTE" ; "Cambridge Technology Enterprises Limited",
            "ARSHIYA" ; "Arshiya Limited",
            "AARTECH" ; "Aartech Solonics Limited",
            "SALONA" ; "Salona Cotspin Limited",
            "LOVABLE" ; "Lovable Lingerie Limited",
            "CANARYS" ; "Canarys Automations Limited",
            "BAWEJA" ; "Baweja Studios Limited",
            "URBAN" ; "Urban Enviro Waste Management Limited",
            "BAGFILMS" ; "B.A.G Films and Media Limited",
            "ISFT" ; "Intrasoft Technologies Limited",
            'KLL' ; "Kaushalya Logistics Limited",
            "GREENCHEF" ; "Greenchef Appliances Limited",
            "IVP" ; "IVP Limited",
            "WORTH" ; "Worth Peripherals Limited",
            "SONAMLTD" ; "SONAM Limited",
            "SUMIT" ; "Sumit Woods Limited",
            "TIRUPATIFL" ; "Tirupati Forge Limited",
            "EMMBI" ; "Emmbi Industries Limited",
            "ARVEE" ; "Arvee Laboratories (India) Limited",
            "UNITEDTEA" ; "The United Nilgiri Tea Estates Company Limited",
            "UNIVASTU" ; "Univastu India Limited",
            "LLOYDS" ; "Lloyds Luxuries Limited",
            "SURANASOL" ; "Surana Solar Limited",
            "SOMICONVEY" ; "Somi Conveyor Beltings Limited",
            "KAKATCEM" ; "Kakatiya Cement Sugar & Industries Limited",
            "SHIGAN" ; "Shigan Quantum Technologies Limited",
            "BHARATGEAR" ; "Bharat Gears Limited",
            "ONDOOR" ; "On Door Concepts Limited",
            "OILCOUNTUB" ; "Oil Country Tubular Limited",
            "SPLIL" ; "SPL Industries Limited",
            "CAPTRUST" ; "Capital Trust Limited",
            "FIDEL" ; "Fidel Softech Limited",
            "MDL" ; "Marvel Decor Limited",
            "3RDROCK" ; "3rd Rock Multimedia Limited",
            "VEEKAYEM" ; "Veekayem Fashion and Apparels Limited",
            "DYNAMIC" ; "Dynamic Services & Security Limited",
            "GILLANDERS" ; "Gillanders Arbuthnot & Company Limited",
            "CENTEXT" ; "Century Extrusions Limited",
            "SHRITECH" ; "Shri Techtex Limited",
            "TOTAL" ; "Total Transport Systems Limited",
            "MITCON" ; "MITCON Consultancy & Engineering Services Limited",
            "ARHAM" ; "Arham Technologies Limited",
            "TOUCHWOOD" ; "Touchwood Entertainment Limited",
            "JOCIL" ; "Jocil Limited",
            "VAISHALI" ; "Vaishali Pharma Limited",
            "FCONSUMER" ; "Future Consumer Limited",
            "DIGIDRIVE" ; "Digidrive Distributors Limited",
            "KEL" ; "Kundan Edifice Limited",
            "CORALFINAC" ; "Coral India Finance & Housing Limited",
            "ACCURACY" ; "Accuracy Shipping Limited",
            "KALYANIFRG" ; "Kalyani Forge Limited",
            "NIRAJ" ; "Niraj Cement Structurals Limited",
            "SRIVASAVI" ; "Srivasavi Adhesive Tapes Limited",
            "IPSL" ; "Integrated Personnel Services Limited",
            "GTL" ; "GTL Limited",
            "RELCHEMQ" ; "Reliance Chemotex Industries Limited",
            "INDIANCARD" ; "Indian Card Clothing Company Limited",
            "MANGALAM" ; "Mangalam Drugs And Organics Limited",
            "PALREDTEC" ; "Palred Technologies Limited",
            "SIL" ; "Standard Industries Limited",
            "LEMERITE" ; "Le Merite Exports Limited",
            "BALPHARMA" ; "Bal Pharma Limited",
            "KOHINOOR" ; "Kohinoor Foods Limited",
            "AKANKSHA" ; "Akanksha Power and Infrastructure Limited",
            "RHFL" ; "Reliance Home Finance Limited",
            "LAMBODHARA" ; "Lambodhara Textiles Limited",
            "CUBEXTUB" ; "Cubex Tubings Limited",
            "GOLDKART" ; "Goldkart Jewels Limited",
            "AHLADA" ; "Ahlada Engineers Limited",
            "BEARDSELL" ; "Beardsell Limited",
            "IL&FSTRANS" ; "IL&FS Transportation Networks Limited",
            "HPIL" ; "Hindprakash Industries Limited",
            "PANSARI" ; "Pansari Developers Limited",
            "AMJLAND" ; "Amj Land Holdings Limited",
            "NOIDATOLL" ; "Noida Toll Bridge Company Limited",
            "DBSTOCKBRO" ; "DB (International) Stock Brokers Limited",
            "HOMESFY" ; "Homesfy Realty Limited",
            "S&SPOWER" ; "S&S Power Switchgears Limited",
            "GRCL" ; "Gayatri Rubbers And Chemicals Limited",
            "PULZ" ; "Pulz Electronics Limited",
            "AKI" ; "AKI India Limited",
            "AGRITECH" ; "Agri-Tech (India) Limited",
            "DCM" ; "DCM  Limited",
            "PRAKASHSTL" ; "Prakash Steelage Limited",
            "SOTAC" ; "Sotac Pharmaceuticals Limited",
            "SHRADHA" ; "Shradha Infraprojects Limited",
            "MADHUSUDAN" ; "Madhusudan Masala Limited",
            "JAINAM" ; "Jainam Ferro Alloys (I) Limited",
            "FONEBOX" ; "Fonebox Retail Limited",
            "SUNDARAM" ; "Sundaram Multi Pap Limited",
            "MRO-TEK" ; "MRO-TEK Realty Limited",
            "KREBSBIO" ; "Krebs Biochemicals and Industries Limited",
            "KHFM" ; "Khfm Hospitality And Facility Management Services Limited",
            "PASHUPATI" ; "Pashupati Cotspin Limited",
            "DUCOL" ; "Ducol Organics And Colours Limited",
            "AKSHOPTFBR" ; "Aksh Optifibre Limited",
            "WIPL" ; "The Western India Plywoods Limited",
            "PATINTLOG" ; "Patel Integrated Logistics Limited",
            "IBLFL" ; "IBL Finance Limited",
            "VR" ; "V R Infraspace Limited",
            "GICL" ; "Globe International Carriers Limited",
            "JHS" ; "JHS Svendgaard Laboratories Limited",
            "FLEXITUFF" ; "Flexituff Ventures International Limited",
            "AUSOMENT" ; "Ausom Enterprise Limited",
            "DANGEE" ; "Dangee Dums Limited",
            "DGCONTENT" ; "Digicontent Limited",
            "ARTNIRMAN" ; "Art Nirman Limited",
            "SHAH" ; "Shah Metacorp Limited",
            "SECURKLOUD" ; "SECUREKLOUD TECHNOLOGIES Limited",
            "SURYALAXMI" ; "Suryalakshmi Cotton Mills Limited",
            "BVCL" ; "Barak Valley Cements Limited",
            "GOYALALUM" ; "Goyal Aluminiums Limited",
            "TRANSTEEL" ; "Transteel Seating Technologies Limited",
            "BHANDARI" ; "Bhandari Hosiery Exports Limited",
            "PARTYCRUS" ; "Party Cruisers Limited",
            "MOTOGENFIN" ; "The Motor & General Finance Limited",
            "PALASHSECU" ; "Palash Securities Limited",
            "ANIKINDS" ; "Anik Industries Limited",
            "SHAHALLOYS" ; "Shah Alloys Limited",
            "TAINWALCHM" ; "Tainwala Chemical and Plastic (I) Limited",
            "SUVIDHAA" ; "Suvidhaa Infoserve Limited",
            "LOTUSEYE" ; "Lotus Eye Hospital and Institute Limited",
            "GANGESSECU" ; "Ganges Securities Limited",
            "AGNI" ; "Agni Green Power Limited",
            "SIKKO" ; "Sikko Industries Limited",
            "AMDIND" ; "AMD Industries Limited",
            "STEELCITY" ; "Steel City Securities Limited",
            "TPHQ" ; "Teamo Productions HQ Limited",
            "GLOBE" ; "Globe Textiles (India) Limited",
            "FRETAIL" ; "Future Retail Limited",
            "SOMATEX" ; "Soma Textiles & Industries Limited",
            "AAREYDRUGS" ; "Aarey Drugs & Pharmaceuticals Limited",
            "QUICKTOUCH" ; "Quicktouch Technologies Limited",
            "LASA" ; "Lasa Supergenerics Limited",
            "ZENITHDRUG" ; "Zenith Drugs Limited",
            "ZENITHSTL" ; "Zenith Steel Pipes & Industries Limited",
            "LPDC" ; "Landmark Property Development Company Limited",
            "NIRMAN" ; "Nirman Agri Genetics Limited",
            "NAGREEKEXP" ; "Nagreeka Exports Limited",
            "AVROIND" ; "AVRO INDIA Limited",
            "ALKALI" ; "Alkali Metals Limited",
            'AAATECH' ; "AAA Technologies Limited",
            "CINEVISTA" ; "Cinevista Limited",
            "ENERGYDEV" ; "Energy Development Company Limited",
            "ATALREAL" ; "Atal Realtech Limited",
            "GROBTEA" ; "The Grob Tea Company Limited",
            "SIMBHALS" ; "Simbhaoli Sugars Limited",
            "GLOBALPET" ; "Global Pet Industries Limited",
            "BANKA" ; "Banka BioLoo Limited",
            "PIONEEREMB" ; "Pioneer Embroideries Limited",
            "KEYFINSERV" ; "Keynote Financial Services Limited",
            "PKTEA" ; "The Peria Karamalai Tea & Produce Company Limited",
            "DELTAMAGNT" ; "Delta Manufacturing Limited",
            "ARCHIES" ; "Archies Limited",
            "MAHICKRA" ; "Mahickra Chemicals Limited",
            "OBCL" ; "Orissa Bengal Carrier Limited",
            "SAIFL" ; "Sameera Agro And Infra Limited",
            "INDSWFTLTD" ; "Ind-Swift Limited",
            "BIOFILCHEM" ; "Biofil Chemicals & Pharmaceuticals Limited",
            "VINNY" ; "Vinny Overseas Limited",
            "SAMBHAAV" ; "Sambhaav Media Limited",
            "DAMODARIND" ; "Damodar Industries Limited",
            "GANGAFORGE" ; "Ganga Forging Limited",
            "MHHL" ; "Mohini Health & Hygiene Limited",
            "VASWANI" ; "Vaswani Industries Limited",
            "HISARMETAL" ; "Hisar Metal Industries Limited",
            "PARASPETRO" ; "Paras Petrofils Limited",
            "SECMARK" ; "SecMark Consultancy Limited",
            "CELEBRITY" ; "Celebrity Fashions Limited",
            "PRESSTONIC" ; "Presstonic Engineering Limited",
            "SYNOPTICS" ; "Synoptics Technologies Limited",
            "YAARI" ; "Yaari Digital Integrated Services Limited",
            "AAKASH" ; "Aakash Exploration Services Limited",
            "REGENCERAM" ; "Regency Ceramics Limited",
            "TOKYOPLAST" ; "Tokyo Plast International Limited",
            "ZENITHEXPO" ; "Zenith Exports Limited",
            "MOKSH" ; "Moksh Ornaments Limited",
            "DOLLEX" ; "Dollex Agrotech Limited",
            "ARABIAN" ; "Arabian Petroleum Limited",
            "TREEHOUSE" ; "Tree House Education & Accessories Limited",
            "DEEM" ; "Deem Roll Tech Limited",
            "ARIHANTACA" ; "Arihant Academy Limited",
            "ASTRON" ; "Astron Paper & Board Mill Limited",
            "PANACHE" ; "Panache Digilife Limited",
            "PRITIKA" ; "Pritika Engineering Components Limited",
            "SAMPANN" ; "Sampann Utpadan India Limited",
            "ENFUSE" ; "Enfuse Solutions Limited",
            "MCL" ; "Madhav Copper Limited",
            "FIBERWEB" ; "Fiberweb (India) Limited",
            "PROLIFE" ; "Prolife Industries Limited",
            "PRECISION" ; "Precision Metaliks Limited",
            "BABAFP" ; "Baba Food Processing (India) Limited",
            "AUROIMPEX" ; "Auro Impex  & Chemicals Limited",
            "PRAMARA" ; "Pramara Promotions Limited",
            "PENTAGON" ; "Pentagon Rubber Limited",
            "MAL" ; "Mangalam Alloys Limited",
            "PIGL" ; "Power & Instrumentation (Gujarat) Limited",
            "RCDL" ; "Rajgor Castor Derivatives Limited",
            "MBECL" ; "Mcnally Bharat Engineering Company Limited",
            "SETCO" ; "Setco Automotive Limited",
            "HOLMARC" ; "Holmarc Opto-Mechatronics Limited",
            "TIMESGTY" ; "Times Guaranty Limited",
            "MAITREYA" ; "Maitreya Medicare Limited",
            "NIBL" ; "NRB Industrial Bearings Limited",
            "SIGNORIA" ; "Signoria Creation Limited",
            "KARMAENG" ; "Karma Energy Limited",
            "AVSL" ; "AVSL Industries Limited",
            "VELS" ; "Vels Film International Limited",
            "LATTEYS" ; "Latteys Industries Limited",
            "PNC" ; "Pritish Nandy Communications Limited",
            "MONOPHARMA" ; "Mono Pharmacare Limited",
            "VERTEXPLUS" ; "Vertexplus Technologies Limited",
            "MVKAGRO" ; "M.V.K. Agro Food Product Limited",
            "SVPGLOB" ; "SVP GLOBAL TEXTILES Limited",
            "DIL" ; "Debock Industries Limited",
            "BALKRISHNA" ; "Balkrishna Paper Mills Limited",
            "MARCO" ; "Marco Cables & Conductors Limited",
            "ORIENTLTD" ; "Orient Press Limited",
            "RILINFRA" ; "Rachana Infrastructure Limited",
            "SPYL" ; "Shekhawati Poly-Yarn Limited",
            "GTECJAINX" ; "G-TEC JAINX EDUCATION Limited",
            "YUDIZ" ; "Yudiz Solutions Limited",
            "AGROPHOS" ; "Agro Phos India Limited",
            "SHUBHLAXMI" ; "Shubhlaxmi Jewel Art Limited",
            "MCON" ; "Mcon Rasayan India Limited",
            "AMBANIORG" ; "Ambani Organics Limited",
            "AISL" ; "ANI Integrated Services Limited",
            "CPS" ; "C P S Shapers Limited",
            "HOVS" ; "HOV Services Limited",
            "KANANIIND" ; "Kanani Industries Limited",
            "SHIVAMILLS" ; "Shiva Mills Limited",
            "PRUDMOULI" ; "Prudential Sugar Corporation Limited",
            "SCML" ; "Sharp Chucks and Machines Limited",
            "AATMAJ" ; "Aatmaj Healthcare Limited",
            "KTL" ; "Kalahridhaan Trendz Limited",
            "CEREBRAINT" ; "Cerebra Integrated Technologies Limited",
            "EXCEL" ; "Excel Realty N Infra Limited",
            "SHEETAL" ; "Sheetal Universal Limited",
            "GRAPHISAD" ; "Graphisads Limited",
            "HECPROJECT" ; "HEC Infra Projects Limited",
            "SECURCRED" ; "SecUR Credentials Limited",
            "AROGRANITE" ; "Aro Granite Industries Limited",
            "MADHUCON" ; "Madhucon Projects Limited",
            "WEWIN" ; "WE WIN Limited",
            "KKVAPOW" ; "KKV Agro Powers Limited",
            "RELIABLE" ; "Reliable Data Services Limited",
            "AKSHAR" ; "Akshar Spintex Limited",
            "DHTL" ; "Docmode Health Technologies Limited",
            "PERFECT" ; "Perfect Infraengineers Limited",
            "MILTON" ; "Milton Industries Limited",
            "GOLDENTOBC" ; "Golden Tobacco Limited",
            "LEXUS" ; "Lexus Granito (India) Limited",
            "MAGSON" ; "Magson Retail And Distribution Limited",
            "SERVICE" ; "Service Care Limited",
            "ROML" ; "Raj Oil Mills Limited",
            "NGIL" ; "Nakoda Group of Industries Limited",
            "CLSL" ; "Crop Life Science Limited",
            "OMFURN" ; "Omfurn India Limited",
            "VIAZ" ; "Viaz Tyres Limited",
            "TRIDHYA" ; "Tridhya Tech Limited",
            "BANG" ; "Bang Overseas Limited",
            "MORARJEE" ; "Morarjee Textiles Limited",
            "MANUGRAPH" ; "Manugraph India Limited",
            "MALUPAPER" ; "Malu Paper Mills Limited",
            "UCL" ; "Ushanti Colour Chem Limited",
            "SIDDHIKA" ; "Siddhika Coatings Limited",
            "JAIPURKURT" ; "Nandani Creation Limited",
            "SPTL" ; "Sintex Plastics Technology Limited",
            "CELLPOINT" ; "Cell Point (India) Limited",
            "MICROPRO" ; "Micropro Software Solutions Limited",
            "COMMITTED" ; "Committed Cargo Care Limited",
            "HBSL" ; "HB Stockholdings Limited",
            "BANARBEADS" ; "Banaras Beads Limited",
            "SANGANI" ; "Sangani Hospitals Limited",
            "BDR" ; "BDR Buildcon Limited",
            "JETFREIGHT" ; "Jet Freight Logistics Limited",
            "MARSHALL" ; "Marshall Machines Limited",
            "ABMINTLLTD" ; "ABM International Limited",
            "TERASOFT" ; "Tera Software Limited",
            "AKG" ; "Akg Exim Limited",
            "PEARLPOLY" ; "Pearl Polymers Limited",
            "PODDARHOUS" ; "Poddar Housing and Development Limited",
            "SHANTHALA" ; "Shanthala FMCG Products Limited",
            "AARVEEDEN" ; "Aarvee Denims & Exports Limited",
            "REXPIPES" ; "Rex Pipes And Cables Industries Limited",
            "JETKNIT" ; "Jet Knitwears Limited",
            "ENSER" ; "Enser Communications Limited",
            "SHRENIK" ; "Shrenik Limited",
            "DNAMEDIA" ; "Diligent Media Corporation Limited",
            "MASTER" ; "Master Components Limited",
            "ACSAL" ; "Arvind and Company Shipping Agencies Limited",
            "SILGO" ; "Silgo Retail Limited",
            "AKASH" ; "Akash Infra-Projects Limited",
            "SEYAIND" ; "Seya Industries Limited",
            "AJOONI" ; "Ajooni Biotech Limited",
            "TFL" ; "Transwarranty Finance Limited",
            "TAPIFRUIT" ; "Tapi Fruit Processing Limited",
            "LFIC" ; "Lakshmi Finance & Industrial Corporation Limited",
            "WOMANCART" ; "Womancart Limited",
            "ASLIND" ; "ASL Industries Limited",
            "TIMESCAN" ; "Timescan Logistics (India) Limited",
            "ANKITMETAL" ; "Ankit Metal & Power Limited",
            "ICDSLTD" ; "ICDS Limited",
            "YCCL" ; "Yasons Chemex Care Limited",
            "UMA" ; "Uma Converter Limited",
            "WALPAR" ; "Walpar Nutritions Limited",
            "SONUINFRA" ; "Sonu Infratech Limited",
            "SEL" ; "Sungarner Energies Limited",
            "LIBAS" ; "Libas Consumer Products Limited",
            "3PLAND" ; "3P Land Holdings Limited",
            "BURNPUR" ; "Burnpur Cement Limited",
            "SITINET" ; "Siti Networks Limited",
            "RKDL" ; "Ravi Kumar Distilleries Limited",
            "MAKS" ; "Maks Energy Solutions India Limited",
            "SRPL" ; "Shree Ram Proteins Limited",
            "BMETRICS" ; "Bombay Metrics Supply Chain Limited",
            "ITALIANE" ; "Italian Edibles Limited",
            "LAXMICOT" ; "Laxmi Cotspin Limited",
            "UWCSL" ; "Ultra Wiring Connectivity System Limited",
            "TNTELE" ; "Tamilnadu Telecommunication Limited",
            "AMBICAAGAR" ; "Ambica Agarbathies & Aroma industries Limited",
            "ASHOKAMET" ; "Ashoka Metcast Limited",
            "ADL" ; "Archidply Decor Limited",
            "KHANDSE" ; "Khandwala Securities Limited",
            "VINEETLAB" ; "Vineet Laboratories Limited",
            "TECHIN" ; "Techindia Nirman Limited",
            "PATTECH" ; "Pattech Fitwell Tube Components Limited",
            "CBAZAAR" ; "Net Avenue Technologies Limited",
            "BINANIIND" ; "Binani Industries Limited",
            "21STCENMGM" ; "21st Century Management Services Limited",
            "KRIDHANINF" ; "Kridhan Infra Limited",
            "GODHA" ; "Godha Cabcon & Insulation Limited",
            "JFLLIFE" ; "Jfl Life Sciences Limited",
            "ISHAN" ; "Ishan International Limited",
            "NEXTMEDIA" ; "Next Mediaworks Limited",
            "SUULD" ; "Suumaya Industries Limited",
            "ARISTO" ; "Aristo Bio-Tech And Lifescience Limited",
            "TGBHOTELS" ; "TGB Banquets And Hotels Limited",
            "DKEGL" ; "D.K. Enterprises Global Limited",
            "MARINETRAN" ; "Marinetrans India Limited",
            "DESTINY" ; "Destiny Logistics & Infra Limited",
            "FLFL" ; "Future Lifestyle Fashions Limited",
            "ARSSINFRA" ; "ARSS Infrastructure Projects Limited",
            "ONELIFECAP" ; "Onelife Capital Advisors Limited",
            "INSPIRE" ; "Inspire Films Limited",
            "VSCL" ; "Vadivarhe Speciality Chemicals Limited",
            "SGL" ; "STL Global Limited",
            "EDUCOMP" ; "Educomp Solutions Limited",
            "SAGARDEEP" ; "Sagardeep Alloys Limited",
            "ROLLT" ; "Rollatainers Limited",
            "KONTOR" ; "Kontor Space Limited",
            "SHAIVAL" ; "Shaival Reality Limited",
            "AGARWALFT" ; "Agarwal Float Glass India Limited",
            "TECILCHEM" ; "TECIL Chemicals and Hydro Power Limited",
            "CMRSL" ; "Cyber Media Research & Services Limited",
            "NIDAN" ; "Nidan Laboratories and Healthcare Limited",
            "UNIINFO" ; "Uniinfo Telecom Services Limited",
            "COUNCODOS" ; "Country Condo's Limited",
            "AMEYA" ; "Ameya Precision Engineers Limited",
            "SUPERSPIN" ; "Super Spinning Mills Limited",
            "CYBERMEDIA" ; "Cyber Media (India) Limited",
            "TIJARIA" ; "Tijaria Polypipes Limited",
            "WILLAMAGOR" ; "Williamson Magor & Company Limited",
            "GSTL" ; "Globesecure Technologies Limited",
            "COMPINFO" ; "Compuage Infocom Limited",
            "MINDPOOL" ; "Mindpool Technologies Limited",
            "POLYSIL" ; "Polysil Irrigation Systems Limited",
            "HAVISHA" ; "Sri Havisha Hospitality and Infrastructure Limited",
            "JIWANRAM" ; "Jiwanram Sheoduttrai Industries Limited",
            "MADHAV" ; "Madhav Marbles and Granites Limited",
            "NKIND" ; "NK Industries Limited",
            "SANGINITA" ; "Sanginita Chemicals Limited",
            "MEGAFLEX" ; "Mega Flex Plastics Limited",
            "ADROITINFO" ; "Adroit Infotech Limited",
            "FMNL" ; "Future Market Networks Limited",
            "HEADSUP" ; "Heads UP Ventures Limited",
            'KEEPLEARN' ; "DSJ Keep Learning Limited",
            "ACEINTEG" ; "Ace Integrated Solutions Limited",
            "VIVIDHA" ; "Visagar Polytex Limited",
            "KCK" ; "Kck Industries Limited",
            "SABAR" ; "Sabar Flex India Limited",
            "AGUL" ; "A G Universal Limited",
            "FSC" ; "Future Supply Chain Solutions Limited",
            "GATECH" ; "GACM Technologies Limited",
            "IMPEXFERRO" ; "Impex Ferro Tech Limited",
            "QFIL" ; "Quality Foils (India) Limited",
            "KHAITANLTD" ; "Khaitan (India) Limited",
            "NARMADA" ; "Narmada Agrobase Limited",
            "FEL" ; "Future Enterprises Limited",
            "GRETEX" ; "Gretex Industries Limited",
            "VIJIFIN" ; "Viji Finance Limited",
            "BOHRAIND" ; "Bohra Industries Limited",
            "MOXSH" ; "Moxsh Overseas Educon Limited",
            "MOHITIND" ; "Mohit Industries Limited",
            "VILINBIO" ; "Vilin Bio Med Limited",
            'HRHNEXT' ; "HRH Next Services Limited",
            "SUNREST" ; "Sunrest Lifescience Limited",
            "SPRL" ; "Sp Refractories Limited",
            "SUMEETINDS" ; "Sumeet Industries Limited",
            "HYBRIDFIN" ; "Hybrid Financial Services Limited",
            "VERA" ; "Vera Synthetic Limited",
            "SAHAJ" ; "Sahaj Fashions Limited",
            "GOENKA" ; "Goenka Diamond and Jewels Limited",
            "QUADPRO" ; "Quadpro Ites Limited",
            "ANTGRAPHIC" ; "Antarctica Limited",
            "INDIFRA" ; "Indifra Limited",
            "ORIENTALTL" ; "Oriental Trimex Limited",
            "LCCINFOTEC" ; "LCC Infotech Limited",
            "LRRPL" ; "Lead Reclaim And Rubber Products Limited",
            "MASKINVEST" ; "Mask Investments Limited",
            "OLIL" ; "Oneclick Logistics India Limited",
            "KAVVERITEL" ; "Kavveri Telecom Products Limited",
            "MITTAL" ; "Mittal Life Style Limited",
            "GUJRAFFIA" ; "Gujarat Raffia Industries Limited",
            "KSHITIJPOL" ; "Kshitij Polyline Limited",
            "CONTI" ; "Continental Seeds and Chemicals Limited",
            "GLFL" ; "Gujarat Lease Financing Limited",
            "NTL" ; "Neueon Towers Limited",
            "CALSOFT" ; "California Software Company Limited",
            "AILimited" ; "Abhishek Integrations Limited",
            "KANDARP" ; "Kandarp Digi Smart BPO Limited",
            "PLADAINFO" ; "Plada Infotech Services Limited",
            "MTEDUCARE" ; "MT Educare Limited",
            "WINSOME" ; "Winsome Yarns Limited",
            "KAUSHALYA" ; "Kaushalya Infrastructure Development Corporation Limited",
            "DRL" ; "Dhanuka Realty Limited",
            "BRIGHT" ; "Bright Solar Limited",
            "NAGREEKCAP" ; "Nagreeka Capital & Infrastructure Limited",
            "TVVISION" ; "TV Vision Limited",
            "VCL" ; "Vaxtex Cotfab Limited",
            "TRANSWIND" ; "Transwind Infrastructures Limited",
            "DIGJAMLMTD" ; "Digjam Limited",
            "RITEZONE" ; "Rite Zone Chemcon India Limited",
            "METALFORGE" ; "Metalyst Forgings Limited",
            "SHANTI" ; "Shanti Overseas (India) Limited",
            "LYPSAGEMS" ; "Lypsa Gems & Jewellery Limited",
            "RICHA" ; "Richa Info Systems Limited",
            "MANAV" ; "Manav Infra Projects Limited",
            "NORBTEAEXP" ; "Norben Tea & Exports Limited",
            "TARAPUR" ; "Tarapur Transformers Limited",
            "BLUECHIP" ; "Blue Chip India Limited",
            "VIVO" ; "Vivo Collaboration Solutions Limited",
            "ORTINLAB" ; "Ortin Laboratories Limited",
            "SAROJA" ; "Saroja Pharma Industries India Limited",
            "JAKHARIA" ; "JAKHARIA FABRIC Limited",
            "MPTODAY" ; "Madhya Pradesh Today Media Limited",
            "SILLYMONKS" ; "Silly Monks Entertainment Limited",
            "EUROTEXIND" ; "Eurotex Industries and Exports Limited",
            "AMIABLE" ; "Amiable Logistics (India) Limited",
            "UMESLTD" ; "Usha Martin Education & Solutions Limited",
            "OMKARCHEM" ; "Omkar Speciality Chemicals Limited",
            "KALYANI" ; "Kalyani Commercials Limited",
            "ARENTERP" ; "Rajdarshan Industries Limited",
            "BKMINDST" ; "Bkm Industries Limited",
            "NIRAJISPAT" ; "Niraj Ispat Industries Limited",
            "INNOVATIVE" ; "Innovative Tyres and Tubes Limited",
            "ACCORD" ; "Accord Synergy Limited",
            "SHYAMTEL" ; "Shyam Telecom Limited",
            "SMVD" ; "SMVD Poly Pack Limited",
            "DCMFINSERV" ; "DCM Financial Services Limited",
            "PREMIER" ; "Premier Limited",
            "CREATIVEYE" ; "Creative Eye Limited",
            "AHIMSA" ; "Ahimsa Industries Limited",
            'ABNINT' ; "A B N Intercorp Limited",
            'ALPSINDUS' ; "Alps Industries Limited",
            "MELSTAR" ; "Melstar Information Technologies Limited",
            "JALAN" ; "Jalan Transolutions (India) Limited",
            "SABEVENTS" ; "Sab Events & Governance Now Media Limited",
            "SANCO" ; "Sanco Industries Limited",
            "BHALCHANDR" ; "Bhalchandram Clothing Limited",
            "LAKPRE" ; "Lakshmi Precision Screws Limited",
            "VASA" ; "Vasa Retail and Overseas Ltd"
            "CMMIPL" ; "CMM Infraprojects Limited",
            "ABHISHEK" ; "Abhishek Corporation Limited",
            "AHLWEST" ; "Asian Hotels (West) Limited",
            "AIFL" ; "Ashapura Intimates Fashion Limited",
            "AJRINFRA" ; "AJR INFRA AND TOLLING Limited",
            "ALCHEM" ; "Alchemist Limited",
            "AMJUMBO" ; "A and M Jumbo Bags Limited",
            "ANSALAPI" ; "Ansal Properties & Infrastructure Limited",
            "ARCOTECH" ; "Arcotech Limited",
            "ARTEDZ" ; "Artedz Fabs Limited",
            "ASIL" ; "Amit Spinning Industries Limited",
            "ATCOM" ; "Atcom Technologies Limited",
            "ATLASCYCLE" ; "Atlas Cycles (Haryana) Limited",
            "ATNINTER" ; "ATN International Limited",
            "BALLARPUR" ; "Ballarpur Industries Limited",
            "BANSAL" ; "Bansal Multiflex Limited",
            "BGLOBAL" ; "Bharatiya Global Infomedia Limited",
            "BHARATIDIL" ; "Bharati Defence and Infrastructure Limited",
            "BILENERGY" ; "Bil Energy Systems Limited",
            "BIRLATYRE" ; "Birla Tyres Limited",
            "BLUEBLENDS" ; "Blue Blends (I) Limited",
            "BLUECOAST" ; "Blue Coast Hotels Limited",
            "BRFL" ; "Bombay Rayon Fashions Limited",
            "CANDC" ; "C & C Constructions Limited",
            "CCCL" ; "Consolidated Construction Consortium Limited",
            "CELESTIAL" ; "Celestial Biolabs Limited",
            "CKFSL" ; "Cox & Kings Financial Service Limited",
            "CMICABLES" ; "CMI Limited",
            "CURATECH" ; "Cura Technologies Limited",
            "DHARSUGAR" ; "Dharani Sugars & Chemicals Limited",
            "DQE" ; "DQ Entertainment (International) Limited",
            "DSKULKARNI" ; "DS Kulkarni Developers Limited",
            "EASTSILK" ; "Eastern Silk Industries Limited",
            "EASTSUGIND" ; "Eastern Sug & Inds Limited",
            "EASUNREYRL" ; "Easun Reyrolle Limited",
            "EON" ; "Eon Electric Limited",
            "EUROCERA" ; "Euro Ceramics Limited",
            "EUROMULTI" ; "Euro Multivision Limited",
            "FEDDERELEC" ; "Fedders Electric and Engineering Limited",
            "FIVECORE" ; "Five Core Electronics Limited",
            "GAMMONIND" ; "Gammon India Limited",
            "GANGOTRI" ; "Gangotri Textiles Limited",
            "GAYAHWS" ; "Gayatri Highways Limited",
            "GAYAPROJ" ; "Gayatri Projects Limited",
            "GBGLOBAL" ; "GB Global Limited",
            "GFSTEELS" ; "Grand Foundry Limited",
            "GITANJALI" ; "Gitanjali Gems Limited",
            "HDIL" ; "Housing Development and Infrastructure Limited",
            "HINDNATGLS" ; "Hindusthan National Glass & Industries Limited",
            "ICSA" ; "ICSA (India) Limited",
            "INDLMETER" ; "IMP Powers Limited",
            "INDOSOLAR" ; "Indosolar Limited",
            "INDUSFILA" ; "Indus Fila Limited",
            "INFOMEDIA" ; "Infomedia Press Limited",
            "INSPIRISYS" ; "Inspirisys Solutions Limited",
            "IVRCLINFRA" ; "IVRCL Limited",
            "JAINSTUDIO" ; "Jain Studios Limited",
            "JBFIND" ; "JBF Industries Limited",
            "JIKIND" ; "JIK Industries Limited",
            "JINDCOT" ; "Jindal Cotex Limited",
            "JPINFRATEC" ; "Jaypee Infratech Limited",
            "KGL" ; "Karuturi Global Limited",
            "KSERASERA" ; "KSS Limited",
            "KSK" ; "KSK Energy Ventures Limited",
            "LAKSHMIEFL" ; "Lakshmi Energy and Foods Limited",
            "LEEL" ; "LEEL Electricals Limited",
            "MANPASAND" ; "Manpasand Beverages Limited",
            "MCDHOLDING" ; "McDowell Holdings Limited",
            "MERCATOR" ; "Mercator Limited",
            "METKORE" ; "Metkore Alloys & Industries Limited",
            "MVL" ; "MVL Limited",
            "NAKODA" ; "Nakoda Limited",
            "NITINFIRE" ; "Nitin Fire Protection Industries Limited",
            "NUTEK" ; "Nu Tek India Limited",
            "OPAL" ; "Opal Luxury Time Products Limited",
            "OPTOCIRCUI" ; "Opto Circuits (India) Limited",
            "ORTEL" ; "Ortel Communications Limited",
            "PDPL" ; "Parenteral Drugs (India) Limited",
            "PENTAGOLD" ; "Penta Gold Limited",
            "PINCON" ; "Pincon Spirit Limited",
            "PRATIBHA" ; "Pratibha Industries Limited",
            "PUNJLLOYD" ; "Punj Lloyd Limited",
            "QUINTEGRA" ; "Quintegra Solutions Limited",
            "RADAAN" ; "Radaan Mediaworks India Limited",
            "RAINBOWPAP" ; "Rainbow Papers Limited",
            "RAJVIR" ; "Rajvir Industries Limited",
            "RCOM" ; "Reliance Communications Limited",
            "RELCAPITAL" ; "Reliance Capital Limited",
            "RMCL" ; "Radha Madhav Corporation Limited",
            "RMMIL" ; "Resurgere Mines & Minerals Limited",
            "RNAVAL" ; "Reliance Naval and Engineering Limited",
            "ROLTA" ; "Rolta India Limited",
            "RUSHABEAR" ; "Rushabh Precision Bearings Limited",
            "SABTN" ; "Sri Adhikari Brothers Television Network Limited",
            'SANWARIA' ; "Sanwaria Consumer Limited",
            "SATHAISPAT" ; "Sathavahana Ispat Limited",
            "SBIHOMEFIN" ; "SBI Home Finance Limited",
            "SETUINFRA" ; "Setubandhan Infrastructure Limited",
            "SHIRPUR-G" ; "Shirpur Gold Refinery Limited",
            "SIIL" ; "Supreme (India) Impex Limited",
            "SKIL" ; "SKIL Infrastructure Limited",
            "SKSTEXTILE" ; "SKS Textiles Limited",
            'SONISOYA' ; "Soni Soya Products Limited",
            "SPENTEX" ; "Spentex Industries Limited",
            "SRIRAM" ; "Shri Ram Switchgears Limited",
            'SSINFRA' ; "S.S. Infrastructure Development Consultants Limited",
            'SUPREMEENG' ; "Supreme Engineering Limited",
            'TALWALKARS' ; "Talwalkars Better Value Fitness Limited",
            'TALWGYM' ; "Talwalkars Healthclubs Limited",
            'TANTIACONS' ; "Tantia Constructions Limited",
            'TCIFINANCE' ; "TCI Finance Limited",
            'TECHNOFAB' ; "Technofab Engineering Limited",
            "TULSI" ; "Tulsi Extrusions Limited",
            "UJAAS" ; "Ujaas Energy Limited",
            "UNIPLY" ; "Uniply Industries Limited",
            "UNITY" ; "Unity Infraprojects Limited",
            "UNIVAFOODS" ; "Univa Foods Limited",
            "VALECHAENG" ; "Valecha Engineering Limited",
            "VALUEIND" ; "Value Industries Limited",
            'VICEROY' ; "Viceroy Hotels Limited",
            "VIDEOIND" ; "Videocon Industries Limited",
            "VISASTEEL" ; "Visa Steel Limited",
            "VISUINTL" ; "Visu International Limited",
            "VIVIMEDLAB" ; "Vivimed Labs Limited",
            "ZICOM" ; "Zicom Electronic Security Systems Limited",
        }
    
# AI validates user preferences based on results from personality test
class AIValidation:
    def __init__(self, user_profile, company_sector, company_data):
        self.user_profile = user_profile
        self.company_sector = company_sector
        self.company_data = company_data

    def validate_sector(self):
        sector_map = {
                    "Technology": {"style": ["Aggressive", "Growth-oriented"], "horizon": ["Long-term", "Medium-term"]},
                    "Finance": {"style": ["Conservative", "Risk-averse"], "horizon": ["Short-term", "Medium-term"]},
                    "Healthcare": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Energy": {"style": ["Aggressive", "Growth-oriented"], "horizon": ["Long-term", "Medium-term"]},
                    "Consumer Goods": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Commodities": {"style": ["Aggressive", "Speculative"], "horizon": ["Short-term", "Medium-term"]},
                    "Consumer Discretionary": {"style": ["Moderate", "Growth-oriented"], "horizon": ["Medium-term", "Long-term"]},
                    "Fast-Moving Consumer Goods": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Financial Services": {"style": ["Conservative", "Risk-averse"], "horizon": ["Short-term", "Medium-term"]},
                    "Industrials": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Information Technology": {"style": ["Aggressive", "Growth-oriented"], "horizon": ["Long-term", "Medium-term"]},
                    "Services": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Telecommunication": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]},
                    "Utilities": {"style": ["Conservative", "Defensive"], "horizon": ["Long-term", "Short-term"]},
                    "Others": {"style": ["Moderate", "Stable"], "horizon": ["Long-term", "Medium-term"]}
                }
        if self.company_sector in sector_map:
            sector_traits = sector_map[self.company_sector]
            if self.user_profile.style.name in sector_traits["style"] and self.user_profile.horizon.name in sector_traits["horizon"]:
                return True
            else:
                print("Warning: The company sector does not align with your investment style and horizon.")
                response = input("Do you want to override this warning? (yes/no): ")
                if response.lower() == "yes":
                    return True
                else:
                    return False
        else:
            print("Error: Unknown company sector.")
            return False

    def validate_company_data(self):
        if self.company_data["revenue_growth"] > 10 and self.company_data["profit_margin"] > 5:
            return True
        else:
            print("Warning: The company's revenue growth and profit margin are not satisfactory.")
            response = input("Do you want to override this warning? (yes/no): ")
            if response.lower() == "yes":
                return True
            else:
                return False

    def validate_investment(self):
        if self.validate_sector() and self.validate_company_data():
            return True
        else:
            return False

# AI searches for all news articles of that company
class AIsearch:
    def __init__(self):
        self.NSEcorp = ["TATASTEEL", "HDFCBANK", "ICICIBANK", "HDFC", "INFY", "KOTAKBANK", "ITC", "SBIN", "TCS", "HCLTECH", "ASIANPAINT", "AXISBANK", "BAJFINANCE", "BHARTIARTL", "BPCL", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HINDALCO", "HINDUNILVR", "ICICIPRULI", "INDUSINDBK", "IOC", "JSWSTEEL", "L&T", "M&M", "MARUTI", "NTPC", "ONGC", "POWERGRID", "RELIANCE", "SBI", "SUNPHARMA", "TATAMOTORS", "TECHM", "TITAN", "ULTRACEMCO", "VEDL", "WIPRO", "ZEEL"]

    def search_company(self, initials):
        company_name = nse_companies.get(initials.upper(), "Company not found")
        if company_name == "Company not found":
            return company_name
        else:
            return company_name, self.retrieve_financial_data(company_name), self.retrieve_news_articles(company_name)

    def retrieve_financial_data(self, company_name: str) -> list:
        Company_name = company_name.replace(" ", "+")
        Company_Name = Company_name.replace("&", "+%26+")
        url = f"https://www.google.com/search?q={Company_Name}+financials"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        financial_data = []

        for result in soup.find_all('div', class_='rc'):
            title = result.find('h3').text
            link = result.find('a')['href']
            financial_data.append((title, link))

        return financial_data

    def retrieve_news_articles(self, company_name):
        news_articles = []
        urls = [
            f"https://www.google.com/search?q={company_name}+news",
            f"https://www.news18.com/search/?q={company_name}",
            f"https://www.ndtv.com/search?q={company_name}",
            f"https://www.republicworld.com/search?q={company_name}",
            f"https://www.indiatimes.com/search?q={company_name}",
            f"https://www.hindustantimes.com/search?q={company_name}",
            f"https://www.livemint.com/search?q={company_name}",
            f"https://www.businesstoday.in/search?q={company_name}",
        ]
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for result in soup.find_all('div', class_='rc'):
                title = result.find('h3').text
                link = result.find('a')['href']
                article = Article(link)
                article.download()
                article.parse()
                news_articles.append((title, link, article.text))
        return news_articles

    def get_et_money_data(self, company_name):
        url = f"https://etmoney.com/search/?q={company_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        for result in soup.find_all('div', class_='stock-card'):
            stock_data = {}
            stock_data['company_name'] = result.find('h2').text.strip()
            stock_data['current_price'] = result.find('span', class_='current-price').text.strip()
            stock_data['change'] = result.find('span', class_='change').text.strip()
            data.append(stock_data)
        return data

    def get_nse_data(self, company_name):
        url = f"https://www.nseindia.com/get-quotes/equity?symbol={company_name}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}
        data['company_name'] = company_name
        data['current_price'] = soup.find('span', id='lastPrice').text.strip()
        data['open']= soup.find('span', id='open').text.strip()
        data['high'] = soup.find('span', id='high').text.strip()
        data['low'] = soup.find('span', id='low').text.strip()
        return data

    def get_moneycontrol_data(self, company_name):
        url = f"https://www.moneycontrol.com/india/stockpricequote/{company_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}
        data['company_name'] = company_name
        data['current_price'] = soup.find('span', class_='span_price_wrap').text.strip()
        data['open'] = soup.find('span', class_='open').text.strip()
        data['high'] = soup.find('span', class_='high').text.strip()
        data['low'] = soup.find('span', class_='low').text.strip()
        return data

    def search_financials(self, company):
        et_money_data = self.get_et_money_data(company)
        nse_data = self.get_nse_data(company)
        moneycontrol_data = self.get_moneycontrol_data(company)
        return et_money_data, nse_data, moneycontrol_data

    def calculate_cagr(self, initial_price, final_price, years):
        if initial_price <= 0 or final_price <= 0 or years <= 0:
            return "Too less data obtained"
        else:
            cagr = (final_price / initial_price) ** (1 / years) - 1
            return cagr

    def evaluate_investment(self, cagr, market_average):
        if cagr > market_average:
            return "Good investment"
        else:
            return "Forego the investment"

    def calculate_market_average(self, market_data):
        total_cagr = 0
        count = 0
        for company in market_data:
            data = self.search_internet(company)
            if len(data) >= 10:
                initial_price = data[0]
                final_price = data[-1]
                years = len(data)
                cagr = self.calculate_cagr(initial_price, final_price, years)
                total_cagr += cagr
                count += 1
        if count == 0:
            return "Not enough data to calculate market average"
        else:
            market_average = total_cagr / count
            return market_average

    def main(self):
        company = input("Enter the company name: ")
        market_data = self.NSEcorp  # list of companies in the market
        market_average = self.calculate_market_average(market_data)
        data = self.search_internet(company)
        if len(data) < 10:
            print("Cannot evaluate investment currently")
        else:
            initial_price = data[0]
            final_price = data[-1]
            years = len(data)
            cagr = self.calculate_cagr(initial_price, final_price, years)
            print(self.evaluate_investment(cagr, market_average))

    def search_internet(self, company):
        # implementation of searching financials on the internet
        # you need to implement this function to retrieve the financial data
        pass

    def track_recession_indicators(self, data):
        recession_indicators = []
        if data['yieldCurveInversion']:
            recession_indicators.append("Yield curve inversion")
        if data['gdpGrowthRate'] < 2:
            recession_indicators.append("GDP growth rate < 2%")
        if data['unemploymentRate'] > 5:
            recession_indicators.append("Unemployment rate > 5%")
        if data['inflationRate'] > 3:
            recession_indicators.append("Inflation rate > 3%")
        if data['cpi'] > 100:
            recession_indicators.append("CPI > 100")
        if data['m2'] < 0:
            recession_indicators.append("M2 growth rate < 0%")
        if data['sp500'] < 0:
            recession_indicators.append("S&P 500 growth rate < 0%")
        return recession_indicators

    def analyze_stock(self, company):
        data = yf.Ticker(company).info
        print(f"Company: {company}")
        print(f"  Current Price: {data['currentPrice']}")

        ratios = self.calculate_ratios(data)
        print(f"  PE Ratio: {ratios['pe_ratio']:.2f}")
        print(f"  PD Ratio: {ratios['pd_ratio']:.2f} (override: {ratios['pd_ratio'] is not None})")
        print(f"  PB Ratio: {ratios['pb_ratio']:.2f}")
        print(f"  PS Ratio: {ratios['ps_ratio']:.2f}")
        print(f"  PCF Ratio: {ratios['pcf_ratio']:.2f}")
        print(f"  Dividend Yield: {ratios['dividend_yield']:.2f}%")
        print(f"  Return on Equity: {ratios['return_on_equity']:.2f}%")
        print(f"  Debt to Equity: {ratios['debt_to_equity']:.2f}")
        print(f"  Interest Coverage: {ratios['interest_coverage']:.2f}")
        print(f"  Asset Turnover: {ratios['asset_turnover']:.2f}")
        print(f"  Profit Margin: {ratios['profit_margin']:.2f}%")

        if ratios['pd_ratio'] is None:
            print("  No dividend yield provided. Most of the income will come through the dividends.")
            override = input("  Do you want to override the AI decision? (yes/no): ")
            if override.lower() == 'yes':
                print("  AI decision overridden.")
            else:
                print("  AI decision not overridden.")

        # Check for dividend yield
        if ratios['dividend_yield'] > self.threshold_dividend_yield:
            print("  This stock has a high dividend yield.")
        else:
            print("  This stock has a low dividend yield.")

        # Check for return on equity
        if ratios['return_on_equity'] > self.threshold_return_on_equity:
            print("  This stock has a high return on equity.")
        else:
            print("  This stock has a low return on equity.")

        # Check for debt to equity
        if ratios['debt_to_equity'] < self.threshold_debt_to_equity:
            print("  This stock has a low debt to equity ratio.")
        else:
            print("  This stock has a high debt to equity ratio.")

        # Check for interest coverage
        if ratios['interest_coverage'] < self.threshold_interest_coverage:
            print("  This stock has a low interest coverage ratio.")
        else:
            print("  This stock has a high interest coverage ratio.")

        # Check for asset turnover
        if ratios['asset_turnover'] < self.threshold_asset_turnover:
            print("  This stock has a low asset turnover ratio.")
        else:
            print("  This stock has a high asset turnover ratio.")

        # Check for profit margin
        if ratios['profit_margin'] < self.threshold_profit_margin:
            print("  This stock has a low profit margin.")
        else:
            print("  This stock has a high profit margin.")

        # Track recession indicators
        recession_indicators = self.track_recession_indicators(data)
        print(f"  Recession Indicators: {recession_indicators}")

        if len(recession_indicators) >= self.threshold_recession_indicators:
            print("  Recession likely. Sell stocks now!")
        else:
            print("  No recession predicted. Hold or buy stocks.")

        print("---------")

    def calculate_ratios(self, data):
        ratios = {}
        ratios['pe_ratio'] = data['currentPrice'] / data['trailingEps']
        ratios['pd_ratio'] = data['currentPrice'] / (data['dividendYield'] * data['currentPrice']) if 'dividendYield' in data and data['dividendYield'] is not None else None
        ratios['pb_ratio'] = data['currentPrice'] / data['bookValue']
        ratios['ps_ratio'] = data['currentPrice'] / data['revenuePerShare']
        ratios['pcf_ratio'] = data['currentPrice'] / data['cashFlowPerShare']
        ratios['dividend_yield'] = data['dividendYield'] if 'dividendYield' in data and data['dividendYield'] is not None else 0
        ratios['return_on_equity'] = data['returnOnEquity'] if 'eturnOnEquity' in data and data['returnOnEquity'] is not None else 0
        ratios['debt_to_equity'] = data['debtToEquity'] if 'debtToEquity' in data and data['debtToEquity'] is not None else 0
        ratios['interest_coverage'] = data['interestCoverage'] if 'interestCoverage' in data and data['interestCoverage'] is not None else 0
        ratios['asset_turnover'] = data['assetTurnover'] if 'assetTurnover' in data and data['assetTurnover'] is not None else 0
        ratios['profit_margin'] = data['profitMargin'] if 'profitMargin' in data and data['profitMargin'] is not None else 0
        return ratios

    if __name__ == "__main__":
        ai_search = AIsearch()
        ai_search.main()

# Analyze the Stock
class StockAnalysis:
    def __init__(self, NIFTY500, threshold_pe=15, threshold_pd=20, threshold_dividend_yield=5, threshold_return_on_equity=15, threshold_debt_to_equity=1, threshold_interest_coverage=5, threshold_asset_turnover=1, threshold_profit_margin=10):
        self.NIFTY500 = NIFTY500
        self.threshold_pe = threshold_pe
        self.threshold_pd = threshold_pd
        self.threshold_dividend_yield = threshold_dividend_yield
        self.threshold_return_on_equity = threshold_return_on_equity
        self.threshold_debt_to_equity = threshold_debt_to_equity
        self.threshold_interest_coverage = threshold_interest_coverage
        self.threshold_asset_turnover = threshold_asset_turnover
        self.threshold_profit_margin = threshold_profit_margin
        self.stock_data = {}

    def fetch_data(self):
        for company in self.NIFTY500.split():
            ticker = company
            data = yf.Ticker(ticker).info
            self.stock_data[company] = data

    def calculate_ratios(self, data):
        ratios = {}
        ratios['pe_ratio'] = data['currentPrice'] / data['trailingEps']
        ratios['pd_ratio'] = data['currentPrice'] / (data['dividendYield'] * data['currentPrice']) if 'dividendYield' in data and data['dividendYield'] is not None else None
        ratios['pb_ratio'] = data['currentPrice'] / data['bookValue']
        ratios['ps_ratio'] = data['currentPrice'] / data['revenuePerShare']
        ratios['pcf_ratio'] = data['currentPrice'] / data['cashFlowPerShare']
        ratios['dividend_yield'] = data['dividendYield'] if 'dividendYield' in data and data['dividendYield'] is not None else 0
        ratios['return_on_equity'] = data['returnOnEquity'] if 'eturnOnEquity' in data and data['returnOnEquity'] is not None else 0
        ratios['debt_to_equity'] = data['debtToEquity'] if 'debtToEquity' in data and data['debtToEquity'] is not None else 0
        ratios['interest_coverage'] = data['interestCoverage'] if 'interestCoverage' in data and data['interestCoverage'] is not None else 0
        ratios['asset_turnover'] = data['assetTurnover'] if 'assetTurnover' in data and data['assetTurnover'] is not None else 0
        ratios['profit_margin'] = data['profitMargin'] if 'profitMargin' in data and data['profitMargin'] is not None else 0
        return ratios

    def analyze_stock(self):
        for company, data in self.stock_data.items():
            print(f"Company: {company}")
            print(f"  Current Price: {data['currentPrice']}")

            ratios = self.calculate_ratios(data)
            print(f"  PE Ratio: {ratios['pe_ratio']:.2f}")
            print(f"  PD Ratio: {ratios['pd_ratio']:.2f} (override: {ratios['pd_ratio'] is not None})")
            print(f"  PB Ratio: {ratios['pb_ratio']:.2f}")
            print(f"  PS Ratio: {ratios['ps_ratio']:.2f}")
            print(f"  PCF Ratio: {ratios['pcf_ratio']:.2f}")
            print(f"  Dividend Yield: {ratios['dividend_yield']:.2f}%")
            print(f"  Return on Equity: {ratios['return_on_equity']:.2f}%")
            print(f"  Debt to Equity: {ratios['debt_to_equity']:.2f}")
            print(f"  Interest Coverage: {ratios['interest_coverage']:.2f}")
            print(f"  Asset Turnover: {ratios['asset_turnover']:.2f}")
            print(f"  Profit Margin: {ratios['profit_margin']:.2f}%")

            if ratios['pd_ratio'] is None:
                print("  No dividend yield provided. Most of the income will come through the dividends.")
                override = input("  Do you want to override the AI decision? (yes/no): ")
                if override.lower() == 'yes':
                    print("  AI decision overridden.")
                else:
                    print("  AI decision not overridden.")

            # Check for dividend yield
            if ratios['dividend_yield'] > self.threshold_dividend_yield:
                print("  This stock has a high dividend yield.")
            else:
                print("  This stock has a low dividend yield.")

            # Check for return on equity
            if ratios['return_on_equity']> self.threshold_return_on_equity:
                print("  This stock has a high return on equity.")
            else:
                print("  This stock has a low return on equity.")

            # Check for debt to equity
            if ratios['debt_to_equity'] < self.threshold_debt_to_equity:
                print("  This stock has a low debt to equity ratio.")
            else:
                print("  This stock has a high debt to equity ratio.")

            # Check for interest coverage
            if ratios['interest_coverage'] < self.threshold_interest_coverage:
                print("  This stock has a low interest coverage ratio.")
            else:
                print("  This stock has a high interest coverage ratio.")

            # Check for asset turnover
            if ratios['asset_turnover'] < self.threshold_asset_turnover:
                print("  This stock has a low asset turnover ratio.")
            else:
                print("  This stock has a high asset turnover ratio.")

            # Check for profit margin
            if ratios['profit_margin'] < self.threshold_profit_margin:
                print("  This stock has a low profit margin.")
            else:
                print("  This stock has a high profit margin.")

            # Track recession indicators
            recession_indicators = self.track_recession_indicators(data)
            print(f"  Recession Indicators: {recession_indicators}")

            print("---------")

    def track_recession_indicators(self, data):
        recession_indicators = []
        if data['yieldCurveInversion']:
            recession_indicators.append("Yield curve inversion")
        if data['gdpGrowthRate'] < 2:
            recession_indicators.append("GDP growth rate < 2%")
        if data['unemploymentRate'] > 5:
            recession_indicators.append("Unemployment rate > 5%")
        if data['inflationRate'] > 3:
            recession_indicators.append("Inflation rate > 3%")
        if data['cpi'] > 100:
            recession_indicators.append("CPI > 100")
        if data['m2'] < 0:
            recession_indicators.append("M2 growth rate < 0%")
        if data['sp500'] < 0:
            recession_indicators.append("S&P 500 growth rate < 0%")
        return recession_indicators

    # Analyze stock Financial Position
    class CandleStick:
        def __init__(self, NIFTY500, threshold_pe=15, threshold_pd=20, threshold_dividend_yield=5, threshold_return_on_equity=15, threshold_debt_to_equity=1, threshold_interest_coverage=5, threshold_asset_turnover=1, threshold_profit_margin=10, threshold_recession_indicators=3):
            self.NIFTY500 = NIFTY500
            self.threshold_pe = threshold_pe
            self.threshold_pd = threshold_pd
            self.threshold_dividend_yield = threshold_dividend_yield
            self.threshold_return_on_equity = threshold_return_on_equity
            self.threshold_debt_to_equity = threshold_debt_to_equity
            self.threshold_interest_coverage = threshold_interest_coverage
            self.threshold_asset_turnover = threshold_asset_turnover
            self.threshold_profit_margin = threshold_profit_margin
            self.threshold_recession_indicators = threshold_recession_indicators
            self.stock_data = {}

        def fetch_data(self):
            for company in self.NIFTY500.split():
                ticker = company
                data = yf.Ticker(ticker).info
                self.stock_data[company] = data

        def calculate_ratios(self, data):
            ratios = {}
            ratios['pe_ratio'] = data['currentPrice'] / data['trailingEps']
            ratios['pd_ratio'] = data['currentPrice'] / (data['dividendYield'] * data['currentPrice']) if 'dividendYield' in data and data['dividendYield'] is not None else None
            ratios['pb_ratio'] = data['currentPrice'] / data['bookValue']
            ratios['ps_ratio'] = data['currentPrice'] / data['revenuePerShare']
            ratios['pcf_ratio'] = data['currentPrice'] / data['cashFlowPerShare']
            ratios['dividend_yield'] = data['dividendYield'] if 'dividendYield' in data and data['dividendYield'] is not None else 0
            ratios['return_on_equity'] = data['returnOnEquity'] if 'returnOnEquity' in data and data['returnOnEquity'] is not None else 0
            ratios['debt_to_equity'] = data['debtToEquity'] if 'debtToEquity' in data and data['debtToEquity'] is not None else 0
            ratios['interest_coverage'] = data['interestCoverage'] if 'interestCoverage' in data and data['interestCoverage'] is not None else 0
            ratios['asset_turnover'] = data['assetTurnover'] if 'assetTurnover' in data and data['assetTurnover'] is not None else 0
            ratios['profit_margin'] = data['profitMargin'] if 'profitMargin' in data and data['profitMargin'] is not None else 0
            return ratios

        def analyze_stock(self):
            for company, data in self.stock_data.items():
                print(f"Company: {company}")
                print(f"  Current Price: {data['currentPrice']}")

                ratios = self.calculate_ratios(data)
                print(f"  PE Ratio: {ratios['pe_ratio']:.2f}")
                print(f"  PD Ratio: {ratios['pd_ratio']:.2f} (override: {ratios['pd_ratio'] is not None})")
                print(f"  PB Ratio: {ratios['pb_ratio']:.2f}")
                print(f"  PS Ratio: {ratios['ps_ratio']:.2f}")
                print(f"  PCF Ratio: {ratios['pcf_ratio']:.2f}")
                print(f"  Dividend Yield: {ratios['dividend_yield']:.2f}%")
                print(f"  Return on Equity: {ratios['return_on_equity']:.2f}%")
                print(f"  Debt to Equity: {ratios['debt_to_equity']:.2f}")
                print(f"  Interest Coverage: {ratios['interest_coverage']:.2f}")
                print(f"  Asset Turnover: {ratios['asset_turnover']:.2f}")
                print(f"  Profit Margin: {ratios['profit_margin']:.2f}%")

                if ratios['pd_ratio'] is None:
                    print("  No dividend yield provided. Most of the income will come through the dividends.")
                    override = input("  Do you want to override the AI decision? (yes/no): ")
                    if override.lower() == 'yes':
                        print("  AI decision overridden.")
                    else:
                        print("  AI decision not overridden.")

                # Check for dividend yield
                if ratios['dividend_yield'] > self.threshold_dividend_yield:
                    print("  This stock hasa high dividend yield.")
                else:
                    print("  This stock has a low dividend yield.")

                # Check for return on equity
                if ratios['return_on_equity']> self.threshold_return_on_equity:
                    print("  This stock has a high return on equity.")
                else:
                    print("  This stock has a low return on equity.")

                # Check for debt to equity
                if ratios['debt_to_equity'] < self.threshold_debt_to_equity:
                    print("  This stock has a low debt to equity ratio.")
                else:
                    print("  This stock has a high debt to equity ratio.")

                # Check for interest coverage
                if ratios['interest_coverage'] < self.threshold_interest_coverage:
                    print("  This stock has a low interest coverage ratio.")
                else:
                    print("  This stock has a high interest coverage ratio.")

                # Check for asset turnover
                if ratios['asset_turnover'] < self.threshold_asset_turnover:
                    print("  This stock has a low asset turnover ratio.")
                else:
                    print("  This stock has a high asset turnover ratio.")

                # Check for profit margin
                if ratios['profit_margin'] < self.threshold_profit_margin:
                    print("  This stock has a low profit margin.")
                else:
                    print("  This stock has a high profit margin.")

                # Track recession indicators
                recession_indicators = self.track_recession_indicators(data)
                print(f"  Recession Indicators: {recession_indicators}")

                if len(recession_indicators) >= self.threshold_recession_indicators:
                    print("  Recession likely. Sell stocks now!")
                else:
                    print("  No recession predicted. Hold or buy stocks.")

                print("---------")

        def track_recession_indicators(self, data):
            recession_indicators = []
            if data['yieldCurveInversion']:
                recession_indicators.append("Yield curve inversion")
            if data['gdpGrowthRate'] < 2:
                recession_indicators.append("GDP growth rate < 2%")
            if data['unemploymentRate'] > 5:
                recession_indicators.append("Unemployment rate > 5%")
            if data['inflationRate'] > 3:
                recession_indicators.append("Inflation rate > 3%")
            if data['cpi'] > 100:
                recession_indicators.append("CPI > 100")
            if data['m2'] < 0:
                recession_indicators.append("M2 growth rate < 0%")
            if data['sp500'] < 0:
                recession_indicators.append("S&P 500 growth rate < 0%")
            return recession_indicators
        
    # Analyze stock public sentiment
    class SentimentAnalysis:
        def __init__(self, NIFTY500):
            self.NIFTY500 = NIFTY500
            self.stock_data = {}

        def fetch_data(self):
            for company in self.NIFTY500.split():
                ticker = company
                data = yf.Ticker(ticker).info
                self.stock_data[company] = data

        def calculate_ratios(self, data):
            ratios = {}
            ratios['pe_ratio'] = data['currentPrice'] / data['trailingEps']
            ratios['pd_ratio'] = data['currentPrice'] / (data['dividendYield'] * data['currentPrice']) if 'dividendYield' in data and data['dividendYield'] is not None else None
            ratios['pb_ratio'] = data['currentPrice'] / data['bookValue']
            ratios['ps_ratio'] = data['currentPrice'] / data['revenuePerShare']
            ratios['pcf_ratio'] = data['currentPrice'] / data['cashFlowPerShare']
            ratios['dividend_yield'] = data['dividendYield'] if 'dividendYield' in data and data['dividendYield'] is not None else 0
            ratios['return_on_equity'] = data['returnOnEquity'] if 'returnOnEquity' in data and data['returnOnEquity'] is not None else 0
            ratios['debt_to_equity'] = data['debtToEquity'] if 'debtToEquity' in data and data['debtToEquity'] is not None else 0
            return ratios

        def analyze_stock(self):
            for company, data in self.stock_data.items():
                print(f"Company: {company}")
                print(f"  Current Price: {data['currentPrice']}")

                ratios = self.calculate_ratios(data)
                print(f"  PE Ratio: {ratios['pe_ratio']:.2f}")
                print(f"  PD Ratio: {ratios['pd_ratio']:.2f} (override: {ratios['pd_ratio'] is not None})")
                print(f"  PB Ratio: {ratios['pb_ratio']:.2f}")
                print(f"  PS Ratio: {ratios['ps_ratio']:.2f}")
                print(f"  PCF Ratio: {ratios['pcf_ratio']:.2f}")
                print(f"  Dividend Yield: {ratios['dividend_yield']:.2f}%")
                print(f"  Return on Equity: {ratios['return_on_equity']:.2f}%")
                print(f"  Debt to Equity: {ratios['debt_to_equity']:.2f}")

                recession_indicators = self.track_recession_indicators(data)
                print(f"  Recession Indicators: {recession_indicators}")

                print("---------")

        def track_recession_indicators(self, data):
            recession_indicators = []
            if data['yieldCurveInversion']:
                recession_indicators.append("Yield curve inversion")
            if data['gdpGrowthRate'] < 2:
                recession_indicators.append("GDP growth rate < 2%")
            if data['unemploymentRate'] > 5:
                recession_indicators.append("Unemployment rate > 5%")
            if data['consumerConfidenceIndex'] < 50:
                recession_indicators.append("Consumer confidence index < 50")
            if data['vix'] > 20:
                recession_indicators.append("Stock market volatility index (VIX) > 20")
            return recession_indicators

        def analyze_news_reports(self, sources=["google", "news18", "ndtv", "republicworld", "indiatimes", "hindustantimes", "livemint", "businesstoday", "financialexpress", "economictimes"]):
            news_articles = []
            for company in self.NIFTY500.split():
                urls = [
                    f"https://www.google.com/search?q={company}+news",
                    f"https://www.news18.com/search?q={company}",
                    f"https://www.ndtv.com/search?q={company}",
                    f"https://www.republicworld.com/search?q={company}",
                    f"https://www.indiatimes.com/search?q={company}",
                    f"https://www.hindustantimes.com/search?q={company}",
                    f"https://www.livemint.com/search?q={company}",
                    f"https://www.businesstoday.in/search?q={company}",
                    f"https://www.financialexpress.com/search?q={company}",
                    f"https://www.economictimes.indiatimes.com/search?q={company}",
                ]
                for url in urls:
                    if url.startswith(f"https://www.{sources[0]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='rc'):
                            title = result.find('h3').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[1]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='news-list-item'):
                            title = result.find('a').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[2]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='story'):
                            title = result.find('h2').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[3]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='news-list-item'):
                            title = result.find('a').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[4]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='news-list-item'):
                            title = result.find('a').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[5]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='story'):
                            title = result.find('h2').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[6]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='news-list-item'):
                            title = result.find('a').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[7]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='story'):
                            title = result.find('h2').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[8]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='news-list-item'):
                            title = result.find('a').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))
                    elif url.startswith(f"https://www.{sources[9]}.com"):
                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        for result in soup.find_all('div', class_='story'):
                            title = result.find('h2').text
                            link = result.find('a')['href']
                            article = Article(link)
                            article.download()
                            article.parse()
                            news_articles.append((title, link, article.text))

            sentiment_analysis = SentimentIntensityAnalyzer()
            sentiments = []
            for title, link, text in news_articles:
                sentiment = sentiment_analysis.polarity_scores(text)
                sentiments.append((title, link, sentiment))

            return sentiments

        def predict_recession(self):
            sentiments = self.analyze_news_reports()
            recession_probability = 0
            for sentiment in sentiments:
                if sentiment[2]['compound'] < 0:
                    recession_probability += 1
            recession_probability /= len(sentiments)
            return recession_probability

        def run_analysis(self):
            self.fetch_data()
            self.analyze_stock()
            recession_probability = self.predict_recession()
            print(f"Recession Probability: {recession_probability:.2f}%")

        if __name__ == "__main__":
            NIFTY500 = "TCS INFY HCLTECH"
            analysis = StockAnalysis(NIFTY500)
            analysis.run_analysis()

# Create NIFTY500 Directory and analyze it
class NIFTY500: 
    nifty500 = {
    '360 ONE WAM Ltd.' : {'sector' : 'Financial Services'},
    '3M India Ltd.' : {'sector' : 'Diversified'},
    'ABB India Ltd.' : {'sector' : 'Capital Goods'},
    'ACC Ltd.' : {'sector' : 'Construction Materials'},
    'AIA Engineering Ltd.' : {'sector' : 'Capital Goods'},
    'APL Apollo Tubes Ltd.' : {'sector' : 'Capital Goods'},
    'AU Small Finance Bank Ltd.' : {'sector' : 'Financial Services'},
    'Aarti Industries Ltd.' : {'sector' : 'Chemicals'},
    'Aavas Financiers Ltd.' : {'sector' : 'Financial Services'},
    'Abbott India Ltd.' : {'sector' : 'Healthcare'},
    'Action Construction Equipment Ltd.' : {'sector' : 'Capital Goods'},
    'Adani Energy Solutions Ltd.' : {'sector' : 'Power'},
    'Adani Enterprises Ltd.' : {'sector' : 'Metals & Mining'},
    'Adani Green Energy Ltd.' : {'sector' : 'Power'},
    'Adani Ports and Special Economic Zone Ltd.' : {'sector' : 'Services'},
    'Adani Power, Ltd.' : {'sector' : 'Power'},
    'Adani Total Gas Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Adani Wilmar Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Aditya Birla Capital Ltd.' : {'sector' : 'Financial Services'},
    'Aditya Birla Fashion and Retail Ltd.' : {'sector' : 'Consumer Services'},
    'Aegis Logistics Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Aether Industries Ltd.' : {'sector' : 'Chemicals'},
    'Affle (India) Ltd.' : {'sector' : 'Information Technology'},
    'Ajanta Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'},
    'Alembic Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'},
    'Alkem Laboratories Ltd.' : {'sector' : 'Healthcare'},
    'Alkyl Amines Chemicals, Ltd.' : {'sector' : 'Chemicals'},
    'Allcargo Logistics Ltd.' : {'sector' : 'Services'},
    'Alok Industries Ltd.' : {'sector' : 'Textiles'},
    'Amara Raja Energy & Mobility Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Amber Enterprises India Ltd.' : {'sector' : 'Consumer Durabless'},
    'Ambuja Cements Ltd.' : {'sector' : 'Construction Materials'},
    'Anand Rathi Wealth Ltd.' : {'sector' : 'Financial Services'},
    'Angel One Ltd.' : {'sector' : 'Financial Services'},
    'Anupam Rasayan India Ltd.' : {'sector' : 'Chemicals'},
    'Apar Industries Ltd.' : {'sector' : 'Capital Goods'},
    'Apollo Hospitals Enterprise Ltd.' : {'sector' : 'Healthcare'},
    'Apollo Tyres Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Aptus Value Housing Finance India Ltd.' : {'sector' : 'Financial Services'},
    'Archean Chemical Industries Ltd.' : {'sector' : 'Chemicals'},
    'Asahi India Glass Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Ashok Leyland Ltd.' : {'sector' : 'Capital Goods'},
    'Asian Paints Ltd.' : {'sector' : 'Consumer Durabless'},
    'Aster DM Healthcare, Ltd.' : {'sector' : 'Healthcare'},
    'AstraZenca Pharma India Ltd.' : {'sector' : 'Healthcare'},
    'Astral Ltd.' : {'sector' : 'Capital Goods'},
    'Atul Ltd.' : {'sector' : 'Chemicals'},
    'Aurobindo Pharma Ltd.' : {'sector' : 'Healthcare'},
    'Avanti Feeds Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Avenue Supermarts Ltd.' : {'sector' : 'Consumer Services'},
    'Axis Bank Ltd.' : {'sector' : 'Financial Services'},
    'BEML Ltd.' : {'sector' : 'Capital Goods'},
    'BLS International Services}, Ltd.' : {'sector' : 'Consumer Services'},
    'BSE Ltd.' : {'sector' : 'Financial Services'},
    'Bajaj Auto Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Bajaj Finance Ltd.' : {'sector' : 'Financial Services'},
    'Bajaj Finserv Ltd.' : {'sector' : 'Financial Services'},
    'Bajaj Holdings & Investment Ltd.' : {'sector' : 'Financial Services'},
    'Balaji Amines Ltd.' : {'sector' : 'Chemicals'},
    'Balkrishna Industries Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Balrampur Chini Mills Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Bandhan Bank Ltd.' : {'sector' : 'Financial Services'},
    'Bank of Baroda' : {'sector' : 'Financial Services'},
    'Bank of India' : {'sector' : 'Financial Services'},
    'Bank of Maharashtra' : {'sector' : 'Financial Services'},
    'Bata India Ltd.' : {'sector' : 'Consumer Durabless'},
    'Bayer Cropscience Ltd.' : {'sector' : 'Chemicals'},
    'Berger Paints India Ltd.' : {'sector' : 'Consumer Durabless'},
    'Bharat Dynamics Ltd.' : {'sector' : 'Capital Goods'},
    'Bharat Electronics Ltd.' : {'sector' : 'Capital Goods'},
    'Bharat Forge Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Bharat Heavy Electricals Ltd.' : {'sector' : 'Capital Goods'},
    'Bharat Petroleum Corporation Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Bharti Airtel Ltd.' : {'sector' : 'Telecommunication'},
    'Bikaji Foods International Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Biocon Ltd.' : {'sector' : 'Healthcare'},
    'Birla Corporation Ltd.' : {'sector' : 'Construction Materials'},
    'Birlasoft Ltd.' : {'sector' : 'Information Technology'},
    'Blue Dart Express Ltd.' : {'sector' : 'Services'},
    'Blue Star Ltd.' : {'sector' : 'Consumer Durabless'},
    'Bombay Burmah Trading Corporation Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Borosil Renewables Ltd.' : {'sector' : 'Capital Goods'},
    'Bosch Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Brigade Enterprises Ltd.' : {'sector' : 'Realty'},
    'Britannia Industries Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'C.E. Info Systems Ltd.' : {'sector' : 'Information Technology'},
    'CCL Products (I) Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'CESC Ltd.' : {'sector' : 'Power'},
    'CG Power, and Industrial Solutions Ltd.' : {'sector' : 'Capital Goods'},
    'CIE Automotive India Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'CRISIL Ltd.' : {'sector' : 'Financial Services'},
    'CSB Bank Ltd.' : {'sector' : 'Financial Services'},
    'Campus Activewear Ltd.' : {'sector' : 'Consumer Durables'},
    'Can Fin Homes Ltd.' : {'sector' : 'Financial Services'},
    'Canara Bank' : {'sector' : 'Financial Services'},
    'Caplin Point Laboratories Ltd.' : {'sector' : 'Healthcare'},
    'Capri Global Capital Ltd.' : {'sector' : 'Financial Services'},
    'Carborundum Universal Ltd.' : {'sector' : 'Capital Goods'},
    'Castrol India Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Ceat Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Cello World Ltd.' : {'sector' : 'Consumer Durabless'},
    'Central Bank of India' : {'sector' : 'Financial Services'},
    'Central Depository Services}, (India) Ltd.' : {'sector' : 'Financial Services'},
    'Century Plyboards (India) Ltd.' : {'sector' : 'Consumer Durabless'},
    'Century Textile & Industries Ltd.' : {'sector' : 'Forest Materials'},
    'Cera Sanitaryware Ltd' : {'sector' : 'Consumer Durabless'},
    'Chalet Hotels Ltd.' : {'sector' : 'Consumer Services'},
    'Chambal Fertilizers & Chemicals, Ltd.' : {'sector' : 'Chemicals'},
    'Chemplast Sanmar Ltd.' : {'sector' : 'Chemicals'},
    'Chennai Petroleum Corporation Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Cholamandalam Financial Holdings Ltd.' : {'sector' : 'Financial Services'},
    'Cholamandalam Investment and Finance Company Ltd.' : {'sector' : 'Financial Services'},
    'Cipla Ltd.' : {'sector' : 'Healthcare'},
    'City Union Bank Ltd.' : {'sector' : 'Financial Services'},
    'Clean Science and Technology}, Ltd.' : {'sector' : 'Chemicals'},
    'Coal India Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Cochin Shipyard Ltd.' : {'sector' : 'Capital Goods'},
    'Coforge Ltd.' : {'sector' : 'Information Technology'},
    'Colgate Palmolive (India) Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Computer Age Management Services}, Ltd.' : {'sector' : 'Financial Services'},
    'Concord Biotech Ltd.' : {'sector' : 'Healthcare'},
    'Container Corporation of India Ltd.' : {'sector' : 'Services'},
    'Coromandel International Ltd.' : {'sector' : 'Chemicals'},
    'Craftsman Automation Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'CreditAccess Grameen Ltd.' : {'sector' : 'Financial Services'},
    'Crompton Greaves Consumer Electricals Ltd.' : {'sector' : 'Consumer Durabless'},
    'Cummins India Ltd.' : {'sector' : 'Capital Goods'},
    'Cyient Ltd.' : {'sector' : 'Information Technology'},
    'DCM Shriram Ltd.' : {'sector' : 'Diversified'},
    'DLF Ltd.' : {'sector' : 'Realty'},
    'DOMS Industries Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Dabur India Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Dalmia Bharat Ltd.' : {'sector' : 'Construction Materials'},
    'Data Patterns (India) Ltd.' : {'sector' : 'Capital Goods'},
    'Deepak Fertilisers & Petrochemicals Corp. Ltd.' : {'sector' : 'Chemicals'},
    'Deepak Nitrite Ltd.' : {'sector' : 'Chemicals'},
    'Delhivery Ltd.' : {'sector' : 'Services'},
    'Devyani International Ltd.' : {'sector' : 'Consumer Services'},
    "Divi's Laboratories Ltd." : {'sector' : 'Healthcare'},
    'Dixon Technologies}, (India) Ltd.' : {'sector' : 'Consumer Durabless'},
    'Dr. Lal Path Labs Ltd.' : {'sector' : 'Healthcare'},
    "Dr. Reddy's Laboratories Ltd." : {'sector' : 'Healthcare'},
    'E.I.D. Parry (India) Ltd.' : {'sector' : 'Chemicals'},
    'EIH Ltd.' : {'sector' : 'Consumer Services'},
    'EPL Ltd.' : {'sector' : 'Capital Goods'},
    'Easy Trip Planners Ltd.' : {'sector' : 'Consumer Services'},
    'Eicher Motors Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Elecon Engineering Co. Ltd.' : {'sector' : 'Capital Goods'},
    'Elgi Equipments Ltd.' : {'sector' : 'Capital Goods'},
    'Emami Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Endurance Technologies}, Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Engineers India Ltd.' : {'sector' : 'Construction'},
    'Equitas Small Finance Bank Ltd.' : {'sector' : 'Financial Services'},
    'Eris Lifesciences Ltd.' : {'sector' : 'Healthcare'},
    'Escorts Kubota Ltd.' : {'sector' : 'Capital Goods'},
    'Exide Industries Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'FDC Ltd.' : {'sector' : 'Healthcare'},
    'FSN E-Commerce Ventures Ltd.' : {'sector' : 'Consumer Services'},
    'Federal Bank Ltd.' : {'sector' : 'Financial Services'},
    'Fertilisers and Chemicals, Travancore Ltd.' : {'sector' : 'Chemicals'},
    'Fine Organic Industries Ltd.' : {'sector' : 'Chemicals'},
    'Finolex Cables Ltd.' : {'sector' : 'Capital Goods'},
    'Finolex Industries Ltd.' : {'sector' : 'Capital Goods'},
    'Firstsource Solutions Ltd.' : {'sector' : 'Services'},
    'Five-Star Business Finance Ltd.' : {'sector' : 'Financial Services'},
    'Fortis Healthcare, Ltd.' : {'sector' : 'Healthcare'},
    'GAIL (India) Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'GMM Pfaudler Ltd.' : {'sector' : 'Capital Goods'},
    'GMR Airports Infrastructure Ltd.' : {'sector' : 'Services'},
    'Garden Reach Shipbuilders & Engineers Ltd.' : {'sector' : 'Capital Goods'},
    'General Insurance Corporation of India' : {'sector' : 'Financial Services'},
    'Gillette India Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Gland Pharma Ltd.' : {'sector' : 'Healthcare'},
    'Glaxosmithkline Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'},
    'Glenmark Life Sciences Ltd.' : {'sector' : 'Healthcare'},
    'Glenmark Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'},
    'Global Health Ltd.' : {'sector' : 'Healthcare'},
    'Godawari Power, & Ispat Ltd.' : {'sector' : 'Capital Goods'},
    'Godfrey Phillips India Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Godrej Consumer Products Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Godrej Industries Ltd.' : {'sector' : 'Diversified'}
    'Godrej Properties Ltd.' : {'sector' : 'Realty'},
    'Granules India Ltd.' : {'sector' : 'Healthcare'},
    'Graphite India Ltd.' : {'sector' : 'Capital Goods'},
    'Grasim Industries Ltd.' : {'sector' : 'Construction Materials'},
    'Great Eastern Shipping Co. Ltd.' : {'sector' : 'Services'},
    'Grindwell Norton Ltd.' : {'sector' : 'Capital Goods'},
    'Gujarat Ambuja Exports Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Gujarat Fluorochemicals Ltd.' : {'sector' : 'Chemicals'},
    'Gujarat Gas Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Gujarat Mineral Development Corporation Ltd.' : {'sector' : 'Metals & Mining'}
    'Gujarat Narmada Valley Fertilizers and Chemicals Ltd.' : {'sector' : 'Chemicals'},
    'Gujarat Pipavav Port Ltd.' : {'sector' : 'Services'},
    'Gujarat State Fertilizers & Chemicals Ltd.' : {'sector' : 'Chemicals'},
    'Gujarat State Petronet Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'H.E.G. Ltd.' : {'sector' : 'Capital Goods'},
    'HBL Power Systems Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'HCL Technologies}, Ltd.' : {'sector' : 'Information Technology'},
    'HDFC Asset Management Company Ltd.' : {'sector' : 'Financial Services'},
    'HDFC Bank Ltd.' : {'sector' : 'Financial Services'},
    'HDFC Life Insurance Company Ltd.' : {'sector' : 'Financial Services'},
    'HFCL Ltd.' : {'sector' : 'Telecommunication'},
    'Happiest Minds Technologies}, Ltd.' : {'sector' : 'Information Technology'},
    'Happy Forgings Ltd.' : {'sector' : 'Capital Goods'},
    'Havells India Ltd.' : {'sector' : 'Consumer Durabless'},
    'Hero MotoCorp Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Himadri Speciality Chemical Ltd.' : {'sector' : 'Chemicals'},
    'Hindalco Industries Ltd.' : {'sector' : 'Metals & Mining'}
    'Hindustan Aeronautics Ltd.' : {'sector' : 'Capital Goods'},
    'Hindustan Copper Ltd.' : {'sector' : 'Metals & Mining'}
    'Hindustan Petroleum Corporation Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Hindustan Unilever Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Hindustan Zinc Ltd.' : {'sector' : 'Metals & Mining'}
    'Hitachi Energy India Ltd.' : {'sector' : 'Capital Goods'},
    'Home First Finance Company India Ltd.' : {'sector' : 'Financial Services'},
    'Honasa Consumer Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Honeywell Automation India Ltd.' : {'sector' : 'Capital Goods'},
    'Housing & Urban Development Corporation Ltd.' : {'sector' : 'Financial Services'},
    'ICICI Bank Ltd.' : {'sector' : 'Financial Services'},
    'ICICI Lombard General Insurance Company Ltd.' : {'sector' : 'Financial Services'},
    'ICICI Prudential Life Insurance Company Ltd.' : {'sector' : 'Financial Services'},
    'ICICI Securities Ltd.' : {'sector' : 'Financial Services'},
    'IDBI Bank Ltd.' : {'sector' : 'Financial Services'},
    'IDFC First Bank Ltd.' : {'sector' : 'Financial Services'},
    'IDFC Ltd.' : {'sector' : 'Financial Services'},
    'IIFL Finance Ltd.' : {'sector' : 'Financial Services'},
    'IRB Infrastructure Developers Ltd.' : {'sector' : 'Construction'},
    'IRCON International Ltd.' : {'sector' : 'Construction'},
    'ITC Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'ITI Ltd.' : {'sector' : 'Telecommunication'},
    'India Cements Ltd.' : {'sector' : 'Construction Materials'},
    'Indiabulls Housing Finance Ltd.' : {'sector' : 'Financial Services'},
    'Indiamart Intermesh Ltd.' : {'sector' : 'Consumer Services'},
    'Indian Bank' : {'sector' : 'Financial Services'},
    'Indian Energy Exchange Ltd.' : {'sector' : 'Financial Services'},
    'Indian Hotels Co. Ltd.' : {'sector' : 'Consumer Services'},
    'Indian Oil Corporation Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Indian Overseas Bank' : {'sector' : 'Financial Services'},
    'Indian Railway Catering And Tourism Corporation Ltd.' : {'sector' : 'Consumer Services'},
    'Indian Railway Finance Corporation Ltd.' : {'sector' : 'Financial Services'},
    'Indigo Paints Ltd.' : {'sector' : 'Consumer Durabless'},
    'Indraprastha Gas Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Indus Towers Ltd.' : {'sector' : 'Telecommunication'},
    'IndusInd Bank Ltd.' : {'sector' : 'Financial Services'},
    'Info Edge (India) Ltd.' : {'sector' : 'Consumer Services'},
    'Infosys Ltd.' : {'sector' : 'Information Technology'},
    'Inox Wind Ltd.' : {'sector' : 'Capital Goods'},
    'Intellect Design Arena Ltd.' : {'sector' : 'Information Technology'},
    'InterGlobe Aviation Ltd.' : {'sector' : 'Services'},
    'Ipca Laboratories Ltd.' : {'sector' : 'Healthcare'},
    'J.B. Chemicals & Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'},
    'J.K. Cement Ltd.' : {'sector' : 'Construction Materials'},
    'JBM Auto Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'JK Lakshmi Cement Ltd.' : {'sector' : 'Construction Materials'},
    'JK Paper Ltd.' : {'sector' : 'Forest Materials'},
    'JM Financial Ltd.' : {'sector' : 'Financial Services'},
    'JSW Energy Ltd.' : {'sector' : 'Power'},
    'JSW Infrastructure Ltd.' : {'sector' : 'Services'},
    'JSW Steel Ltd.' : {'sector' : 'Metals & Mining'}
    'Jai Balaji Industries Ltd.' : {'sector' : 'Metals & Mining'}
    'Jammu & Kashmir Bank Ltd.' : {'sector' : 'Financial Services'},
    'Jindal Saw Ltd.' : {'sector' : 'Capital Goods'},
    'Jindal Stainless Ltd.' : {'sector' : 'Metals & Mining'}
    'Jindal Steel & Power Ltd.' : {'sector' : 'Metals & Mining'}
    'Jio Financial Services Ltd.' : {'sector' : 'Financial Services'},
    'Jubilant Foodworks Ltd.' : {'sector' : 'Consumer Services'},
    'Jubilant Ingrevia Ltd.' : {'sector' : 'Chemicals'},
    'Jubilant Pharmova Ltd.' : {'sector' : 'Healthcare'},
    'Jupiter Wagons Ltd.' : {'sector' : 'Capital Goods'},
    'Justdial Ltd.' : {'sector' : 'Consumer Services'},
    'Jyothy Labs Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'K.P.R. Mill Ltd.' : {'sector' : 'Textiles'},
    'KEI Industries Ltd.' : {'sector' : 'Capital Goods'},
    'KNR Constructions Ltd.' : {'sector' : 'Construction'},
    'KPIT Technologies}, Ltd.' : {'sector' : 'Information Technology'},
    'KRBL Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'KSB Ltd.' : {'sector' : 'Capital Goods'},
    'Kajaria Ceramics Ltd.' : {'sector' : 'Consumer Durabless'},
    'Kalpataru Projects International Ltd.' : {'sector' : 'Construction'},
    'Kalyan Jewellers India Ltd.' : {'sector' : 'Consumer Durabless'},
    'Kansai Nerolac Paints Ltd.' : {'sector' : 'Consumer Durabless'},
    'Karur Vysya Bank Ltd.' : {'sector' : 'Financial Services'},
    'Kaynes Technology India Ltd.' : {'sector' : 'Capital Goods'},
    'Kec International Ltd.' : {'sector' : 'Construction'},
    'Kfin Technologies Ltd.' : {'sector' : 'Financial Services'},
    'Kotak Mahindra Bank Ltd.' : {'sector' : 'Financial Services'},
    'Krishna Institute of Medical Sciences Ltd.' : {'sector' : 'Healthcare'},
    'L&T Finance Ltd.' : {'sector' : 'Financial Services'},
    'L&T Technology Services}, Ltd.' : {'sector' : 'Information Technology'},
    'LIC Housing Finance Ltd.' : {'sector' : 'Financial Services'},
    'LTIMindtree Ltd.' : {'sector' : 'Information Technology'},
    'Larsen & Toubro Ltd.' : {'sector' : 'Construction'},
    'Latent View Analytics Ltd.' : {'sector' : 'Information Technology'},
    'Laurus Labs Ltd.' : {'sector' : 'Healthcare'},
    'Laxmi Organic Industries Ltd.' : {'sector' : 'Chemicals'},
    'Lemon Tree Hotels Ltd.' : {'sector' : 'Consumer Services'},
    'Life Insurance Corporation of India' : {'sector' : 'Financial Services'},
    'Linde India Ltd.' : {'sector' : 'Chemicals'},
    'Lloyds Metals And Energy Ltd.' : {'sector' : 'Metals & Mining'}
    'Lupin Ltd.' : {'sector' : 'Healthcare'},
    'MMTC Ltd.' : {'sector' : 'Services'},
    'MRF Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'MTAR Technologies}, Ltd.' : {'sector' : 'Capital Goods'},
    'Macrotech Developers Ltd.' : {'sector' : 'Realty'},
    'Mahanagar Gas Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Maharashtra Seamless Ltd.' : {'sector' : 'Capital Goods'},
    'Mahindra & Mahindra Financial Services Ltd.' : {'sector' : 'Financial Services'},
    'Mahindra & Mahindra Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Mahindra Holidays & Resorts India Ltd.' : {'sector' : 'Consumer Services'},
    'Mahindra Lifespace Developers Ltd.' : {'sector' : 'Realty'},
    'Manappuram Finance Ltd.' : {'sector' : 'Financial Services'},
    'Mangalore Refinery & Petrochemicals Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Mankind Pharma Ltd.' : {'sector' : 'Healthcare'},
    'Marico Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Maruti Suzuki India Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Mastek Ltd.' : {'sector' : 'Information Technology'},
    'Max Financial Services Ltd.' : {'sector' : 'Financial Services'},
    'Max Healthcare Institute Ltd.' : {'sector' : 'Healthcare'},
    'Mazagoan Dock Shipbuilders Ltd.' : {'sector' : 'Capital Goods'},
    'Medplus Health Services}, Ltd.' : {'sector' : 'Consumer Services'},
    'Metro Brands Ltd.' : {'sector' : 'Consumer Durabless'},
    'Metropolis Healthcare Ltd.' : {'sector' : 'Healthcare'},
    'Minda Corporation Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Motherson Sumi Wiring India Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Motilal Oswal Financial Services Ltd.' : {'sector' : 'Financial Services'},
    'MphasiS Ltd.' : {'sector' : 'Information Technology'},
    'Multi Commodity Exchange of India Ltd.' : {'sector' : 'Financial Services'},
    'Muthoot Finance Ltd.' : {'sector' : 'Financial Services'},
    'NATCO Pharma Ltd.' : {'sector' : 'Healthcare'},
    'NBCC (India) Ltd.' : {'sector' : 'Construction'},
    'NCC Ltd.' : {'sector' : 'Construction'},
    'NHPC Ltd.' : {'sector' : 'Power'},
    'NLC India Ltd.' : {'sector' : 'Power'},
    'NMDC Ltd.' : {'sector' : 'Metals & Mining'}
    'NMDC Steel Ltd.' : {'sector' : 'Metals & Mining'}
    'NTPC Ltd.' : {'sector' : 'Power'},
    'Narayana Hrudayalaya Ltd.' : {'sector' : 'Healthcare'},
    'National Aluminium Co. Ltd.' : {'sector' : 'Metals & Mining'}
    'Navin Fluorine International Ltd.' : {'sector' : 'Chemicals'},
    'Nestle India Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Network18 Media & Investments Ltd.' : {'sector' : 'Media Entertainment & Publication'}
    'Nippon Life India Asset Management Ltd.' : {'sector' : 'Financial Services'},
    'Nuvama Wealth Management Ltd.' : {'sector' : 'Financial Services'},
    'Nuvoco Vistas Corporation Ltd.' : {'sector' : 'Construction Materials'},
    'Oberoi Realty}, Ltd.' : {'sector' : 'Realty'},
    'Oil & Natural Gas Corporation Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Oil India Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Olectra Greentech Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'One 97 Communications Ltd.' : {'sector' : 'Financial Services'},
    'Oracle Financial Services Software Ltd.' : {'sector' : 'Information Technology'},
    'PB Fintech Ltd.' : {'sector' : 'Financial Services'},
    'PCBL Ltd.' : {'sector' : 'Chemicals'},
    'PI Industries Ltd.' : {'sector' : 'Chemicals'},
    'PNB Housing Finance Ltd.' : {'sector' : 'Financial Services'},
    'PNC Infratech Ltd.' : {'sector' : 'Construction'},
    'PVR INOX Ltd.' : {'sector' : 'Media Entertainment & Publication'}
    'Page Industries Ltd.' : {'sector' : 'Textiles'},
    'Patanjali Foods Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Persistent Systems Ltd.' : {'sector' : 'Information Technology'},
    'Petronet LNG Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Phoenix Mills Ltd.' : {'sector' : 'Realty'},
    'Pidilite Industries Ltd.' : {'sector' : 'Chemicals'},
    'Piramal Enterprises Ltd.' : {'sector' : 'Financial Services'},
    'Piramal Pharma Ltd.' : {'sector' : 'Healthcare'},
    'Poly Medicure Ltd.' : {'sector' : 'Healthcare'},
    'Polycab India Ltd.' : {'sector' : 'Capital Goods'},
    'Poonawalla Fincorp Ltd.' : {'sector' : 'Financial Services'},
    'Power Finance Corporation Ltd.' : {'sector' : 'Financial Services'},
    'Power Grid Corporation of India Ltd.' : {'sector' : 'Power'},
    'Praj Industries Ltd.' : {'sector' : 'Capital Goods'},
    'Prestige Estates Projects Ltd.' : {'sector' : 'Realty'},
    'Prince Pipes and Fittings Ltd.' : {'sector' : 'Capital Goods'},
    'Prism Johnson Ltd.' : {'sector' : 'Construction Materials'},
    'Procter & Gamble Hygiene & Health Care Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Punjab National Bank' : {'sector' : 'Financial Services'},
    'Quess Corp Ltd.' : {'sector' : 'Services'},
    'R R Kabel Ltd.' : {'sector' : 'Capital Goods'},
    'RBL Bank Ltd.' : {'sector' : 'Financial Services'},
    'REC Ltd.' : {'sector' : 'Financial Services'},
    'RHI MAGNESITA INDIA LTD.' : {'sector' : 'Capital Goods'},
    'RITES Ltd.' : {'sector' : 'Construction'},
    'Radico Khaitan Ltd' : {'sector' : 'Fast Moving Consumer Goods'},
    'Rail Vikas Nigam Ltd.' : {'sector' : 'Construction'},
    'Railtel Corporation Of India Ltd.' : {'sector' : 'Telecommunication'},
    'Rainbow Childrens Medicare Ltd.' : {'sector' : 'Healthcare'},
    'Rajesh Exports Ltd.' : {'sector' : 'Consumer Durabless'},
    'Ramkrishna Forgings Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Rashtriya Chemicals & Fertilizers Ltd.' : {'sector' : 'Chemicals'},
    'Ratnamani Metals & Tubes Ltd.' : {'sector' : 'Capital Goods'},
    'RattanIndia Enterprises Ltd.' : {'sector' : 'Consumer Services'},
    'Raymond Ltd.' : {'sector' : 'Textiles'},
    'Redington Ltd.' : {'sector' : 'Services'},
    'Reliance Industries Ltd.' : {'sector' : 'Oil Gas & Consumable Fuels'},
    'Restaurant Brands Asia Ltd.' : {'sector' : 'Consumer Services'},
    'Route Mobile Ltd.' : {'sector' : 'Telecommunication'},
    'SBFC Finance Ltd.' : {'sector' : 'Financial Services'},
    'SBI Cards and Payment Services}, Ltd.' : {'sector' : 'Financial Services'},
    'SBI Life Insurance Company Ltd.' : {'sector' : 'Financial Services'},
    'SJVN Ltd.' : {'sector' : 'Power'},
    'SKF India Ltd.' : {'sector' : 'Capital Goods'},
    'SRF Ltd.' : {'sector' : 'Chemicals'},
    'Safari Industries (India) Ltd.' : {'sector' : 'Consumer Durabless'},
    'Samvardhana Motherson International Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Sanofi India Ltd.' : {'sector' : 'Healthcare'},
    'Sapphire Foods India Ltd.' : {'sector' : 'Consumer Services'},
    'Saregama India Ltd' : {'sector' : 'Media Entertainment & Publication'},
    'Schaeffler India Ltd.' : {'sector' : 'Automobile and Auto Components'},
    'Schneider Electric Infrastructure Ltd.' : {'sector' : 'Capital Goods'},
    'Shree Cement Ltd.' : {'sector' : 'Construction Materials'},
    'Shree Renuka Sugars Ltd.' : {'sector' : 'Fast Moving Consumer Goods'},
    'Shriram Finance Ltd.' : {'sector' : 'Financial Services'},
    'Shyam Metalics and Energy Ltd.' : {'sector' : 'Capital Goods'},
    'Siemens Ltd.' : {'sector' : 'Capital Goods'},
    'Signatureglobal (India) Ltd.' : {'sector' : 'Realty'},
    'Sobha Ltd.' : {'sector' : 'Realty'}
    'Solar Industries India Ltd.' : {'sector' : 'Chemicals'}
    'Sona BLW Precision Forgings Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'Sonata Software Ltd.' : {'sector' : 'Information Technology'}
    'Star Health and Allied Insurance Company Ltd.' : {'sector' : 'Financial Services'};
    'State Bank of India' : {'sector' : 'Financial Services'}
    'Steel Authority of India Ltd.' : {'sector' : 'Metals & Mining'}
    'Sterling and Wilson Renewable Energy Ltd.' : {'sector' : 'Construction'}
    'Sterlite Technologies} Ltd.' : {'sector' : 'Telecommunication'}
    'Sumitomo Chemical India Ltd.' : {'sector' : 'Chemicals'}
    'Sun Pharma Advanced Research Company Ltd.' : {'sector' : 'Healthcare'}
    'Sun Pharmaceutical Industries Ltd.' : {'sector' : 'Healthcare'}
    'Sun TV Network Ltd.' : {'sector' : 'Media Entertainment & Publication'}
    'Sundaram Finance Ltd.' : {'sector' : 'Financial Services'}
    'Sundram Fasteners Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'Sunteck Realty} Ltd.' : {'sector' : 'Realty'}
    'Supreme Industries Ltd.' : {'sector' : 'Capital Goods'}
    'Suven Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'}
    'Suzlon Energy Ltd.' : {'sector' : 'Capital Goods'}
    'Swan Energy Ltd.' : {'sector' : 'Diversified'}
    'Syngene International Ltd.' : {'sector' : 'Healthcare'}
    'Syrma SGS Technology} Ltd.' : {'sector' : 'Capital Goods'}
    'TV18 Broadcast Ltd.' : {'sector' : 'Media Entertainment & Publication'}
    'TVS Motor Company Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'TVS Supply Chain Solutions Ltd.' : {'sector' : 'Services'}
    'Tamilnad Mercantile Bank Ltd.' : {'sector' : 'Financial Services'}
    'Tanla Platforms Ltd.' : {'sector' : 'Information Technology'}
    'Tata Chemicals Ltd.' : {'sector' : 'Chemicals'}
    'Tata Communications Ltd.' : {'sector' : 'Telecommunication'}
    'Tata Consultancy Services} Ltd.' : {'sector' : 'Information Technology'}
    'Tata Consumer Products Ltd.' : {'sector' : 'Fast Moving Consumer Goods'}
    'Tata Elxsi Ltd.' : {'sector' : 'Information Technology'}
    'Tata Investment Corporation Ltd.' : {'sector' : 'Financial Services'}
    'Tata Motors Ltd DVR' : {'sector' : 'Automobile and Auto Components'}
    'Tata Motors Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'Tata Power Co. Ltd.' : {'sector' : 'Power'}
    'Tata Steel Ltd.' : {'sector' : 'Metals & Mining'}
    'Tata Technologies} Ltd.' : {'sector' : 'Information Technology'}
    'Tata Teleservices (Maharashtra) Ltd.' : {'sector' : 'Telecommunication'}
    'Tech Mahindra Ltd.' : {'sector' : 'Information Technology'}
    'Tejas Networks Ltd.' : {'sector' : 'Telecommunication'}
    'The New India Assurance Company Ltd.' : {'sector' : 'Financial Services'}
    'The Ramco Cements Ltd.' : {'sector' : 'Construction Materials'}
    'Thermax Ltd.' : {'sector' : 'Capital Goods'}
    'Timken India Ltd.' : {'sector' : 'Capital Goods'}
    'Titagarh Rail Systems Ltd.' : {'sector' : 'Capital Goods'}
    'Titan Company Ltd.' : {'sector' : 'Consumer Durabless'}
    'Torrent Pharmaceuticals Ltd.' : {'sector' : 'Healthcare'}
    'Torrent Power Ltd.' : {'sector' : 'Power'}
    'Trent Ltd.' : {'sector' : 'Consumer Services'}
    'Trident Ltd.' : {'sector' : 'Textiles'}
    'Triveni Engineering & Industries Ltd.' : {'sector' : 'Fast Moving Consumer Goods'}
    'Triveni Turbine Ltd.' : {'sector' : 'Capital Goods'}
    'Tube Investments of India Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'UCO Bank' : {'sector' : 'Financial Services'}
    'UNO Minda Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'UPL Ltd.' : {'sector' : 'Chemicals'}
    'UTI Asset Management Company Ltd.' : {'sector' : 'Financial Services'}
    'Ujjivan Small Finance Bank Ltd.' : {'sector' : 'Financial Services'}
    'UltraTech Cement Ltd.' : {'sector' : 'Construction Materials'}
    'Union Bank of India' : {'sector' : 'Financial Services'}
    'United Breweries Ltd.' : {'sector' : 'Fast Moving Consumer Goods'}
    'United Spirits Ltd.' : {'sector' : 'Fast Moving Consumer Goods'}
    'Usha Martin Ltd.' : {'sector' : 'Capital Goods'}
    'V-Guard Industries Ltd.' : {'sector' : 'Consumer Durabless'}
    'V.I.P. Industries Ltd.' : {'sector' : 'Consumer Durabless'}
    'Vaibhav Global Ltd.' : {'sector' : 'Consumer Durabless'}
    'Vardhman Textiles Ltd.' : {'sector' : 'Textiles'}
    'Varroc Engineering Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'Varun Beverages Ltd.' : {'sector' : 'Fast Moving Consumer Goods'}
    'Vedant Fashions Ltd.' : {'sector' : 'Consumer Services'}
    'Vedanta Ltd.' : {'sector' : 'Metals & Mining'}
    'Vijaya Diagnostic Centre Ltd.' : {'sector' : 'Healthcare'}
    'Vodafone Idea Ltd.' : {'sector' : 'Telecommunication'}
    'Voltas Ltd.' : {'sector' : 'Consumer Durabless'}
    'Welspun Corp Ltd.' : {'sector' : 'Capital Goods'}
    'Welspun Living Ltd.' : {'sector' : 'Textiles'}
    'Westlife Foodworld Ltd.' : {'sector' : 'Consumer Services'}
    'Whirlpool of India Ltd.' : {'sector' : 'Consumer Durabless'}
    'Wipro Ltd.' : {'sector' : 'Information Technology'}
    'Yes Bank Ltd.' : {'sector' : 'Financial Services'}
    'ZF Commercial Vehicle Control Systems India Ltd.' : {'sector' : 'Automobile and Auto Components'}
    'Zee Entertainment Enterprises Ltd.' : {'sector' : 'Media Entertainment & Publication'}
    'Zensar Technolgies Ltd.' : {'sector' : 'Information Technology'}
    'Zomato Ltd.' : {'sector' : 'Consumer Services'}
    'Zydus Lifesciences Ltd.' : {'sector' : 'Healthcare'}
    'eClerx Services} Ltd.' : {'sector' : 'Services'}
    }
    stock_data = {}

    for company in NIFTY500:
        ticker = yf.Ticker(company + ".NS")
        info = ticker.info
        hist = ticker.history(period="1y")
        stock_data[company] = {
            "stock_price": info["regularMarketPrice"],
            "market_cap": info["marketCap"],
            "sector": info["sector"],
            "industry": info["industry"],
            "beta": info["beta"],
            "dividend_yield": info["dividendYield"],
            "eps": info["trailingEps"],
            "pe_ratio": info["trailingPE"],
            "52_week_high": info["fiftyTwoWeekHigh"],
            "52_week_low": info["fiftyTwoWeekLow"],
            "average_volume": info["averageVolume"],
            "market": info["market"],
            "quote_type": info["quoteType"],
            "trailing_annual_dividend_rate": info["trailingAnnualDividendRate"],
            "trailing_annual_dividend_yield": info["trailingAnnualDividendYield"],
            "five_year_avg_dividend_yield": info["fiveYearAvgDividendYield"],
            "payout_ratio": info["payoutRatio"],
            "forward_pe": info["forwardPE"],
            "forward_eps": info["forwardEps"],
            "day_low": hist.iloc[-1]["Low"],
            "day_high": hist.iloc[-1]["High"],
            "day_open": hist.iloc[-1]["Open"],
            "day_close": hist.iloc[-1]["Close"],
            "day_volume": hist.iloc[-1]["Volume"],
            "50_day_ma": hist.iloc[-1]["Close"].rolling(window=50).mean()[-1],
            "200_day_ma": hist.iloc[-1]["Close"].rolling(window=200).mean()[-1]
        }

    df = pd.DataFrame(stock_data).T
    print(df)

# Compare NIFTY500 to target company
class NIFTYanalyitics:
    target_company = "TATASTEEL"
    stock_data = {}
    target_ticker = yf.Ticker(target_company + ".NS")
    target_info = target_ticker.info
    target_hist = target_ticker.history(period="1y")
    target_data = {
        "stock_price": target_info["regularMarketPrice"],
        "market_cap": target_info["marketCap"],
        "sector": target_info["sector"],
        "industry": target_info["industry"],
        "beta": target_info["beta"],
        "dividend_yield": target_info["dividendYield"],
        "eps": target_info["trailingEps"],
        "pe_ratio": target_info["trailingPE"],
        "52_week_high": target_info["fiftyTwoWeekHigh"],
        "52_week_low": target_info["fiftyTwoWeekLow"],
        "average_volume": target_info["averageVolume"],
        "market": target_info["market"],
        "quote_type": target_info["quoteType"],
        "trailing_annual_dividend_rate": target_info["trailingAnnualDividendRate"],
        "trailing_annual_dividend_yield": target_info["trailingAnnualDividendYield"],
        "five_year_avg_dividend_yield": target_info["fiveYearAvgDividendYield"],
        "payout_ratio": target_info["payoutRatio"],
        "forward_pe": target_info["forwardPE"],
        "forward_eps": target_info["forwardEps"],
        "day_low": target_hist.iloc[-1]["Low"],
        "day_high": target_hist.iloc[-1]["High"],
        "day_open": target_hist.iloc[-1]["Open"],
        "day_close": target_hist.iloc[-1]["Close"],
        "day_volume": target_hist.iloc[-1]["Volume"],
        "50_day_ma": target_hist.iloc[-1]["Close"].rolling(window=50).mean()[-1],
        "200_day_ma": target_hist.iloc[-1]["Close"].rolling(window=200).mean()[-1]
    }

    df = pd.DataFrame(stock_data).T
    target_df = pd.DataFrame([target_data], index=[target_company])

    comparison_df = pd.concat([df, target_df])
    print(comparison_df)

# Analyze the comparison
class Comparison:
    def __init__(self, target_company, metrics, threshold, favourable_direction, weighting, normalization, time_period, scaling, categorical_cols, ordinal_cols, model_type, hyperparams, imputation_strategy, feature_scaling):
        self.target_company = target_company
        self.metrics = metrics
        self.threshold = threshold
        self.favourable_direction = favourable_direction
        self.weighting = weighting
        self.normalization = normalization
        self.time_period = time_period
        self.scaling = scaling
        self.categorical_cols = categorical_cols
        self.ordinal_cols = ordinal_cols
        self.model_type = model_type
        self.hyperparams = hyperparams
        self.imputation_strategy = imputation_strategy
        self.feature_scaling = feature_scaling

    def compare(self, nifty500_data):
        comparison_df = pd.DataFrame(nifty500_data).T
        target_data = pd.DataFrame([nifty500_data[self.target_company]], index=[self.target_company])
        comparison_df = pd.concat([comparison_df, target_data])

        comparison_df = comparison_df.set_index("Company")
        target_data = comparison_df.loc[self.target_company]

        comparison_df = comparison_df.drop(self.target_company)

        numerical_cols = [col for col in comparison_df.columns if col not in self.categorical_cols + self.ordinal_cols]
        categorical_cols = self.categorical_cols
        ordinal_cols = self.ordinal_cols

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=self.imputation_strategy)),
            ('scaler', MinMaxScaler() if self.feature_scaling else 'passthrough')
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy=self.imputation_strategy)),
            ('onehot', pd.get_dummies)
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        if self.normalization == "zscore":
            comparison_df[self.metrics] = comparison_df[self.metrics].rolling(window=self.time_period).apply(zscore)
            target_data[self.metrics] = target_data[self.metrics].rolling(window=self.time_period).apply(zscore)
        elif self.normalization == "minmax":
            scaler = MinMaxScaler()
            comparison_df[self.metrics] = scaler.fit_transform(comparison_df[self.metrics].rolling(window=self.time_period).mean().reset_index(0))
            target_data[self.metrics] = scaler.transform(target_data[self.metrics].rolling(window=self.time_period).mean().reset_index(0))

        X = preprocessor.fit_transform(comparison_df)
        y = (X > target_data[self.metrics]).all(axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if self.model_type == "random_forest":
            model = RandomForestClassifier(**self.hyperparams)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        else:
            raise ValueError("Invalid model type")

        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

        comparison_df["Score"] = y_pred

        if self.scaling:
            comparison_df["Score"] = scaler.transform(comparison_df[["Score"]])

        return comparison_df

    nifty500_data = yf.download("^NSEI", start="2020-01-01", end="2024-06-14")["Adj Close"]
    nifty500_data = nifty500_data.pct_change().dropna()

    comparison = Comparison(
        target_company="LAC",
        metrics=["Open", "High", "Low", "Close"],
        threshold=0.5,
        favourable_direction="positive",
        weighting={"Open": 0.3, "High": 0.2, "Low": 0.2, "Close": 0.3},
        normalization="zscore",
        time_period=20,
        scaling=True,
        categorical_cols=["Sector"],
        ordinal_cols=["Industry"],
        model_type="random_forest",
        hyperparams={"n_estimators": 100, "random_state": 42},
        imputation_strategy="mean",
        feature_scaling=True
    )

    result = comparison.compare(nifty500_data)
    print(result)

# Price Predicting Model
class PricePredictor:
    class StockDataset(Dataset):
        def __init__(self, data, seq_len):
            self.data = data
            self.seq_len = seq_len

        def __len__(self):
            return len(self.data) - self.seq_len

        def __getitem__(self, idx):
            seq = self.data[idx:idx+self.seq_len]
            label = self.data[idx+self.seq_len, 0]
            return {'seq': torch.tensor(seq), 'label': torch.tensor(label)}

    class LSTMModel(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(LSTMModel, self).__init__()
            self.hidden_dim = hidden_dim
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True)
            self.fc = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            h0 = torch.zeros(2, x.size(0), self.hidden_dim).to(x.device)
            c0 = torch.zeros(2, x.size(0), self.hidden_dim).to(x.device)
            out, _ = self.lstm(x, (h0, c0))
            out = self.fc(out[:, -1, :])
            return out

    class EarlyStopping:
        def __init__(self, patience=3, min_delta=0):
            self.patience = patience
            self.min_delta = min_delta
            self.counter = 0
            self.min_loss = np.Inf

        def __call__(self, loss):
            if loss < self.min_loss:
                self.min_loss = loss
                self.counter = 0
            elif loss > (self.min_loss + self.min_delta):
                self.counter += 1
                if self.counter >= self.patience:
                    print('Early stopping')
                    return True
            return False

    df = pd.read_csv('stock_market_data-AAL.csv')
    df = df.sort_values('Date')
    df['Mid Price'] = (df['Low'] + df['High']) / 2.0
    mid_prices = df['Mid Price'].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    mid_prices_scaled = scaler.fit_transform(mid_prices)

    dataset = StockDataset(mid_prices_scaled, seq_len=20)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = LSTMModel(input_dim=1, hidden_dim=50, output_dim=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    early_stopping = EarlyStopping(patience=5)

    for epoch in range(100):
        for batch in data_loader:
            seq, label = batch['seq'].float().to(device), batch['label'].float().to(device)
            optimizer.zero_grad()
            output = model(seq)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
        if early_stopping(loss.item()):
            break

    print('Training finished')

    df = pd.read_csv('prices.csv', index_col='date', parse_dates=['date'])

    # Convert the index to a datetime object
    df.index = pd.to_datetime(df.index)

    # Resample the data to a monthly frequency (optional)
    df_monthly = df.resample('M').mean()

    # Plot the original data
    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, df_monthly['price'])
    plt.title('Original Data')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    # Split the data into training and testing sets
    train_size = int(0.8 * len(df_monthly))
    train, test = df_monthly[0:train_size], df_monthly[train_size:]

    # Define the ARIMA model
    model = ARIMA(train, order=(5,1,0))  # p=5, d=1, q=0

    # Fit the model
    model_fit = model.fit()

    # Plot the residuals
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    plt.title('Residuals')
    plt.xlabel('Date')
    plt.ylabel('Residual')
    plt.show()

    # Print the summary of the model
    print(model_fit.summary())

    # Forecast future prices
    forecast_steps = 12  # predict 12 months into the future
    forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

    # Plot the forecast
    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, df_monthly['price'], label='Original')
    plt.plot(pd.date_range(start=df_monthly.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='M'), forecast, label='Forecast')
    plt.fill_between(pd.date_range(start=df_monthly.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='M'), conf_int[:, 0], conf_int[:, 1], alpha=0.2, label='Confidence Interval')
    plt.title('Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # Evaluate the model using mean squared error
    mse = mean_squared_error(test, model_fit.forecast(steps=len(test)))
    print(f'Mean Squared Error: {mse:.2f}')

# Check for algorithmic biases
class BiasDetect:
    def eliminate_algorithmic_biases(X, y):
        # Look-Ahead Bias
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Optimization Bias
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        
        # Selection Bias
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        print(X_pca.head())
        
        # Confirmation Bias
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_pca, y)
        y_pred = model.predict(X_pca)
        accuracy = accuracy_score(y, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        
        # Other Biases
        X_augmented = pd.concat([X, pd.get_dummies(X, columns=['category'])], axis=1)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_augmented, y)
        y_pred = model.predict(X_augmented)
        accuracy = accuracy_score(y, y_pred)
        print(f'Accuracy: {accuracy:.2f}')
        
        return X_train_scaled, X_test_scaled, y_train, y_test

# AI-empowered SWOT analysis model 
class SWOTanalysis:
        def __init__(self):
            self.swot_data = self.get_swot_data()
            self.swot_df = pd.DataFrame(self.swot_data)
            self.plot_swot_analysis()

        def get_swot_data(self):
            strengths = [input("Enter Factor favouring future price increase 1: "), input("Enter Factor favouring future price increase 2: "), input("Enter Factor favouring future price increase 3: ")]
            weaknesses = [input("Enter Factor not favouring future price increase 1: "), input("Enter Factor not favouring future price increase 2: "), input("Enter Factor not favouring future price increase 3: ")]
            opportunities = [input("Enter Opportunity for future price increase 1: "), input("Enter Opportunity for future price increase 2: "), input("Enter Opportunity for future price increase 3: ")]
            threats = [input("Enter Threat to future price increase 1: "), input("Enter Threat to future price increase 2: "), input("Enter Threat to future price increase 3: ")]
            return {
                'Strengths': strengths,
                'Weaknesses': weaknesses,
                'Opportunities': opportunities,
                'Threats': threats
            }

        def plot_swot_analysis(self):
            plt.figure(figsize=(10, 6))
            plt.axis('tight')
            plt.axis('off')
            plt.grid(b=None)
            plt.table(cellText=self.swot_df.values, colLabels=self.swot_df.columns, loc='center')
            plt.title('SWOT Analysis for Future Price Increase')
            plt.show()

        swot_analysis = SWOTanalysis()

# Develop Competitive Pricing Model
class CompetitivePricingModel:
    def __init__(self, user_profile, company_sector, company_data, market_data, economic_data, industry_data, competitor_data, macroeconomic_data, customer_data, product_data, sales_data, marketing_data):
        self.user_profile = user_profile
        self.company_sector = company_sector
        self.company_data = company_data
        self.market_data = market_data
        self.economic_data = economic_data
        self.industry_data = industry_data
        self.competitor_data = competitor_data
        self.macroeconomic_data = macroeconomic_data
        self.customer_data = customer_data
        self.product_data = product_data
        self.sales_data = sales_data
        self.marketing_data = marketing_data

    def calculate_risk_score(self):
        risk_score = 0
        if self.user_profile.style.name == "Aggressive":
            risk_score += 5
        elif self.user_profile.style.name == "Growth-oriented":
            risk_score += 4.5
        elif self.user_profile.style.name == "Moderate":
            risk_score += 4
        elif self.user_profile.style.name == "Conservative":
            risk_score += 3.5
        elif self.user_profile.style.name == "Risk-averse":
            risk_score += 3

        if self.user_profile.horizon.name == "Long-term":
            risk_score += 4
        elif self.user_profile.horizon.name == "Medium-term":
            risk_score += 3.5
        elif self.user_profile.horizon.name == "Short-term":
            risk_score += 3

        if self.company_sector in ["Technology", "Energy"]:
            risk_score += 4
        elif self.company_sector in ["Finance", "Healthcare"]:
            risk_score += 3.5
        elif self.company_sector in ["Consumer Goods"]:
            risk_score += 3

        if self.company_data["revenue_growth"] > 30:
            risk_score += 4
        elif self.company_data["revenue_growth"] > 25:
            risk_score += 3.5
        elif self.company_data["revenue_growth"] < 20:
            risk_score -= 2

        if self.company_data["profit_margin"] > 25:
            risk_score += 4
        elif self.company_data["profit_margin"] > 20:
            risk_score += 3.5
        elif self.company_data["profit_margin"] < 15:
            risk_score -= 2

        if self.market_data["market_volatility"] > 30:
            risk_score += 4
        elif self.market_data["market_volatility"] > 25:
            risk_score += 3.5
        elif self.market_data["market_volatility"] < 20:
            risk_score -= 2

        if self.economic_data["GDP_growth"] > 5:
            risk_score += 3
        elif self.economic_data["GDP_growth"] > 4:
            risk_score += 2.5
        elif self.economic_data["GDP_growth"] < 3:
            risk_score -= 2

        if self.economic_data["inflation_rate"] > 5:
            risk_score += 3
        elif self.economic_data["inflation_rate"] > 4:
            risk_score += 2.5
        elif self.economic_data["inflation_rate"] < 3:
            risk_score -= 2

        if self.industry_data["industry_growth"] > 15:
            risk_score += 3
        elif self.industry_data["industry_growth"] > 10:
            risk_score += 2.5
        elif self.industry_data["industry_growth"] < 5:
            risk_score -= 2

        if self.competitor_data["competitor_strength"] > 0.8:
            risk_score += 3
        elif self.competitor_data["competitor_strength"] > 0.6:
            risk_score += 2.5
        elif self.competitor_data["competitor_strength"] < 0.4:
            risk_score -= 2

        if self.macroeconomic_data["unemployment_rate"] < 4:
            risk_score += 2
        elif self.macroeconomic_data["unemployment_rate"] < 5:
            risk_score += 1.5
        elif self.macroeconomic_data["unemployment_rate"] > 6:
            risk_score -= 2

        if self.customer_data["customer_satisfaction"] > 0.8:
            risk_score += 2
        elif self.customer_data["customer_satisfaction"] > 0.6:
            risk_score += 1.5
        elif self.customer_data["customer_satisfaction"] < 0.4:
            risk_score -= 2

        if self.product_data["product_quality"] > 0.8:
            risk_score += 2
        elif self.product_data["product_quality"] > 0.6:
            risk_score += 1.5
        elif self.product_data["product_quality"] < 0.4:
            risk_score -= 2

        if self.sales_data["sales_growth"] > 20:
            risk_score += 2
        elif self.sales_data["sales_growth"] > 15:
            risk_score += 1.5
        elif self.sales_data["sales_growth"] < 10:
            risk_score -= 2

        if self.marketing_data["marketing_efficiency"] > 0.8:
            risk_score += 2
        elif self.marketing_data["marketing_efficiency"] > 0.6:
            risk_score += 1.5
        elif self.marketing_data["marketing_efficiency"] < 0.4:
            risk_score -= 2

        return risk_score

    def calculate_premium(self):
        risk_score = self.calculate_risk_score()
        if risk_score < 15:
            return 0.005
        elif risk_score < 20:
            return 0.01
        elif risk_score < 25:
            return 0.015
        elif risk_score < 30:
            return 0.02
        else:
            return 0.025

    def calculate_price(self, base_price):
        premium = self.calculate_premium()
        return base_price * (1 + premium)

    class UserProfile:
        def __init__(self, style, horizon):
            self.style = style
            self.horizon = horizon

    class CompanyData:
        def __init__(self, revenue_growth, profit_margin):
            self.revenue_growth = revenue_growth
            self.profit_margin = profit_margin

    class MarketData:
        def __init__(self, market_volatility):
            self.market_volatility = market_volatility

    class EconomicData:
        def __init__(self, GDP_growth, inflation_rate):
            self.GDP_growth = GDP_growth
            self.inflation_rate = inflation_rate

    class IndustryData:
        def __init__(self, industry_growth):
            self.industry_growth = industry_growth

    class CompetitorData:
        def __init__(self, competitor_strength):
            self.competitor_strength = competitor_strength

    class MacroeconomicData:
        def __init__(self, unemployment_rate):
            self.unemployment_rate = unemployment_rate

    class CustomerData:
        def __init__(self, customer_satisfaction):
            self.customer_satisfaction = customer_satisfaction

    class ProductData:
        def __init__(self, product_quality):
            self.product_quality = product_quality

    class SalesData:
        def __init__(self, sales_growth):
            self.sales_growth = sales_growth

    class MarketingData:
        def __init__(self, marketing_efficiency):
            self.marketing_efficiency = marketing_efficiency

# Develop Competitive Pricing Model for consultation to be paid by UPI
class AdvancedCompetitivePricingModel:
    def __init__(self, user_profile, company_sector, company_data, market_data, economic_data, industry_data, competitor_data, macroeconomic_data, customer_data, product_data, sales_data, marketing_data):
        self.user_profile = user_profile
        self.company_sector = company_sector
        self.company_data = company_data
        self.market_data = market_data
        self.economic_data = economic_data
        self.industry_data = industry_data
        self.competitor_data = competitor_data
        self.macroeconomic_data = macroeconomic_data
        self.customer_data = customer_data
        self.product_data = product_data
        self.sales_data = sales_data
        self.marketing_data = marketing_data

    def calculate_risk_score(self):
        risk_score = 0
        if self.user_profile.style.name == "Aggressive":
            risk_score += 5
        elif self.user_profile.style.name == "Growth-oriented":
            risk_score += 4.5
        elif self.user_profile.style.name == "Moderate":
            risk_score += 4
        elif self.user_profile.style.name == "Conservative":
            risk_score += 3.5
        elif self.user_profile.style.name == "Risk-averse":
            risk_score += 3

        if self.user_profile.horizon.name == "Long-term":
            risk_score += 4
        elif self.user_profile.horizon.name == "Medium-term":
            risk_score += 3.5
        elif self.user_profile.horizon.name == "Short-term":
            risk_score += 3

        if self.company_sector in ["Technology", "Energy"]:
            risk_score += 4
        elif self.company_sector in ["Finance", "Healthcare"]:
            risk_score += 3.5
        elif self.company_sector in ["Consumer Goods"]:
            risk_score += 3

        if self.company_data.revenue_growth > 30:
            risk_score += 4
        elif self.company_data.revenue_growth > 25:
            risk_score += 3.5
        elif self.company_data.revenue_growth < 20:
            risk_score -= 2

        if self.company_data.profit_margin > 25:
            risk_score += 4
        elif self.company_data.profit_margin > 20:
            risk_score += 3.5
        elif self.company_data.profit_margin < 15:
            risk_score -= 2

        if self.market_data.market_volatility > 30:
            risk_score += 4
        elif self.market_data.market_volatility > 25:
            risk_score += 3.5
        elif self.market_data.market_volatility < 20:
            risk_score -= 2

        if self.economic_data.GDP_growth > 5:
            risk_score += 3
        elif self.economic_data.GDP_growth > 4:
            risk_score += 2.5
        elif self.economic_data.GDP_growth < 3:
            risk_score -= 2

        if self.economic_data.inflation_rate > 5:
            risk_score += 3
        elif self.economic_data.inflation_rate > 4:
            risk_score += 2.5
        elif self.economic_data.inflation_rate < 3:
            risk_score -= 2

        if self.industry_data.industry_growth > 15:
            risk_score += 3
        elif self.industry_data.industry_growth > 10:
            risk_score += 2.5
        elif self.industry_data.industry_growth < 5:
            risk_score -= 2

        if self.competitor_data.competitor_strength > 0.8:
            risk_score += 3
        elif self.competitor_data.competitor_strength > 0.6:
            risk_score += 2.5
        elif self.competitor_data.competitor_strength < 0.4:
            risk_score -= 2

        if self.macroeconomic_data.unemployment_rate < 4:
            risk_score += 2
        elif self.macroeconomic_data.unemployment_rate < 5:
            risk_score += 1.5
        elif self.macroeconomic_data.unemployment_rate > 6:
            risk_score -= 2

        if self.customer_data.customer_satisfaction > 0.8:
            risk_score += 2
        elif self.customer_data.customer_satisfaction > 0.6:
            risk_score += 1.5
        elif self.customer_data.customer_satisfaction < 0.4:
            risk_score -= 2

        if self.product_data.product_quality > 0.8:
            risk_score += 2
        elif self.product_data.product_quality > 0.6:
            risk_score += 1.5
        elif self.product_data.product_quality < 0.4:
            risk_score -= 2

        if self.sales_data.sales_growth > 20:
            risk_score += 2
        elif self.sales_data.sales_growth > 15:
            risk_score += 1.5
        elif self.sales_data.sales_growth < 10:
            risk_score -= 2

        if self.marketing_data.marketing_efficiency > 0.8:
            risk_score += 2
        elif self.marketing_data.marketing_efficiency > 0.6:
            risk_score += 1.5
        elif self.marketing_data.marketing_efficiency < 0.4:
            risk_score -= 2

        return risk_score

    def calculate_premium(self):
        risk_score = self.calculate_risk_score()
        if risk_score < 15:
            return 0.005
        elif risk_score < 20:
            return 0.01
        elif risk_score < 25:
            return 0.015
        elif risk_score < 30:
            return 0.02
        else:
            return 0.025

    def calculate_price(self, base_price):
        premium = self.calculate_premium()
        return base_price * (1 + premium)

    def generate_qr_code(self, amount, upi_id):
        qr_data = f"upi://sambit1912@oksbi?pn=Sambit%20Mishra&am={amount}&cu=INR"
        img = qrcode.make(qr_data)
        img.save("qr_code.png")

        model = AdvancedCompetitivePricingModel(user_profile, "Technology", company_data, market_data, economic_data, industry_data, competitor_data, macroeconomic_data, customer_data, product_data, sales_data, marketing_data)
        base_price = 1000
        amount = model.calculate_price(base_price)
        upi_id = "sambit1912@oksbi"
        model.generate_qr_code(amount, upi_id)
