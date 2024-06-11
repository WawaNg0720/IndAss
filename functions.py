import pandas as pd
import os

headers = ["ID", "IC Number", "Password", "Gender", "Married Status", "No. of Child", "Disabled?", "Working Status for Spouse",
           "Salary for Spouse", "Disability for Spouse", "Annual Income", "Eligibility for Tax", "Individual Relief", 
           "Medical Treatment, Special Needs & Carer Expenses for Parents", 
           "Purchase of Basic Supporting Equipment for Disabled Self, Spouse, Child or Parent",
           "Disabled Individual", "Total Education Fees for Self", "Total Medical Expenses",
           "Lifestyle Expenses", "Additional Lifestyle Expenses", "Purchase of Breastfeeding Equipment",
           "Child Care Fees", "Net Deposit in SSPN", "Husband/Wife/Alimony Payments",
           "Disabled Husband/Wife", "Total Child Relief", "Total Life insurance and EPF",
           "Deferred Annuity and Private Retirement Scheme (PRS)", "Education & Medical Insurance", 
           "Contribution to SOCSO", "Expenses on Charging Facilities for Electric Vehicle (Not for business use)",
           "Total Relief", "Taxable Income", "Tax", "Tax Rate"]

dtypes = {"Password": str, "IC Number": str, "Gender": object, "Married Status": object, "Disabled?": object, "ID": object,
          "Working Status for Spouse": object, "Disability for Spouse": object,
          "Eligibility for Tax": object, "Individual Relief": object, 
          "Medical Treatment, Special Needs & Carer Expenses for Parents": object, 
          "Purchase of Basic Supporting Equipment for Disabled Self, Spouse, Child or Parent": object,
          "Disabled Individual": object, "Total Education Fees for Self": object, "Total Medical Expenses": object,
          "Lifestyle Expenses": object, "Additional Lifestyle Expenses": object, "Purchase of Breastfeeding Equipment": object,
          "Child Care Fees": object, "Net Deposit in SSPN": object, "Husband/Wife/Alimony Payments": object,
          "Disabled Husband/Wife": object, "Total Child Relief": object, "Total Life insurance and EPF": object,
          "Deferred Annuity and Private Retirement Scheme (PRS)": object, "Education & Medical Insurance": object,
          "Contribution to SOCSO": object, "Expenses on Charging Facilities for Electric Vehicle (Not for business use)": object,
          "Total Relief": object, "Taxable Income": object, "Tax": object, "Tax Rate": object}

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=headers)
    
    # Check if the file exists
    if os.path.isfile(filename):
        # Read the existing CSV file
        existing_df = pd.read_csv(filename, dtype=dtypes)

        # Update or append rows as needed
        for index, row in df.iterrows():
            existing_row = existing_df[(existing_df["ID"] == row["ID"]) | (existing_df["IC Number"] == row["IC Number"])]
            if not existing_row.empty:
                # Update the existing row with the new data
                existing_df.loc[existing_row.index, :] = row.values
            else:
                # Append the new row if it doesn't exist
                # First, check for and exclude empty or all-NA columns in the new row
                row_clean = row.dropna(how='all')
                existing_df = pd.concat([existing_df, row_clean.to_frame().T], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        existing_df.to_csv(filename, index=False)
    else:
        # If the file does not exist, create it with headers
        df.to_csv(filename, index=False, header=True)

def read_from_csv(filename):
    try:
        dtypes = {"Password": str, "IC Number": str, "ID": object}
         
        df = pd.read_csv(filename, dtype=dtypes)
        return df
    except FileNotFoundError:
        return None
    
def register_user(filename):
    print("----------Registration Form----------")
    df = read_from_csv(filename)

    ic_number = input("Enter your IC number (without dash '-'): ").strip()

    # ic should be 12 digits
    while len(str(ic_number)) != 12 or not ic_number.isdigit():
        print("Invalid IC number. It must be 12 digits long and contain only numbers. Please try again.")
        ic_number = input("Enter your IC number (without dash '-'): ").strip()

    # check ic number in csv file
    if df is not None and str(ic_number) in df["IC Number"].values:
        return None, None, None
    else:
        confirmation_ic_number = input("Enter your IC number again for confirmation (without dash '-'): ").strip()
        while str(ic_number) != str(confirmation_ic_number):
            print("Error! Please enter your IC number again.")
            confirmation_ic_number = input("Enter your IC number again for confirmation (without dash '-'): ").strip()
    
    # set password equals to last 4 digit ic number
    password = ic_number[8:12]
    
    user_id = input("Enter your user ID (spacing is not allowed and cannot start with number): ").strip()
    
    # no space is allowed and cannot start with number and check condition
    while " " in user_id or user_id[0].isdigit():  
        print("User ID cannot contain spaces or start with a number. Please try again.")
        user_id = input("Enter a new user ID (spacing is not allowed and cannot start with number): ").strip() 
        
    # no duplication of ID
    while user_id in df["ID"].values:
        print("User ID already exists. Please try again.")
        user_id = input("Enter a new user ID (spacing is not allowed and cannot start with number): ").strip() 

    print("Registration successful.")
    print("Your password is the last 4 digit of your IC number: " + password)

    new_data = pd.DataFrame({
        "ID": [user_id],
        "IC Number": [ic_number],
        "Password": [password]},
        columns=headers)
    
    save_to_csv(new_data, filename)
    
    return user_id, ic_number, password

def login_user(filename):
    print("----------Login Page----------")
    
    while True:
        user_id = input("Enter your user ID: ").strip()
        password = input("Enter your password: ").strip()
        df = read_from_csv(filename)
        if df is not None:
            matching_rows = df[(df["ID"] == user_id) & (df["Password"] == password)]
            if not matching_rows.empty:
                print("User authentication successful.")
                return user_id, password
        print("Invalid user ID or password. Please try again.")
        choice = input("Do you want to try logging in again or go to registration? (login/register): ").strip().lower()
        if choice == 'register':
            return None, None
  
def verify_user(filename, ic_number, password):
    while True:
        ic_number = input("Please key in your IC Number (without dash '-') for verification purpose: ").strip()
        if len(ic_number) == 12 and ic_number.isdigit():
            break
        print("Invalid IC number. It must be 12 digits long and contain only numbers. Please try again.")

    df = read_from_csv(filename)
    # Check if the entered IC number exists in the DataFrame and matches the password
    if df is not None:
        matching_row = df[(df["IC Number"] == ic_number) & (df["Password"] == password)]
        if not matching_row.empty:
            return True
        else:
            print("IC number or password does not match. Please try again.")
            return False
    else:
        return False

def is_valid_number(input_str):
    try:
        float(input_str)  # Try to convert the input to a float
        return True
    except ValueError:
        return False

def get_valid_input(prompt):
    value = input(prompt)
    while not is_valid_number(value):
        print("Invalid Input. Only a valid number is allowed.")
        value = input(prompt)
    return round(float(value))

def eligibility_tax(user_id, ic_number, gender, married, children, disabled, working_status_spouse,
                    salary_spouse, disabled_spouse, annual_income, eligible_tax, individual_relief, 
                    medical_parents, purchase_disabled, disabled_individual_relief,
                    total_self_education_fee, total_medical, lifestyle, add_lifestyle,
                    purchase_breastfeeding, child_care_fees, sspn, payment_alimony, 
                    disabled_spouse_relief, total_child_relief, total_life_epf, prs,
                    edu_medical_insurance, socso, exp_vehicle_electric, total_tax_relief, taxable_income, tax, tax_rate, filename):
    
    df = pd.read_csv(filename, dtype=dtypes)
    
    # Use user_id if provided, otherwise use ic_number to find the row
    if user_id:
        user_row = df[df["ID"] == user_id]
    elif ic_number:
        user_row = df[df["IC Number"] == str(ic_number)]
    else:
        return

    if not user_row.empty:
        # Convert values to appropriate data types
        children = int(children) if children.isdigit() else 0

        # Update the row with the new data
        df.loc[user_row.index, ["Gender", "Married Status", "No. of Child", "Disabled?", "Working Status for Spouse",
                                "Salary for Spouse", "Disability for Spouse", "Annual Income", "Eligibility for Tax",
                                "Individual Relief", "Medical Treatment, Special Needs & Carer Expenses for Parents", 
                                "Purchase of Basic Supporting Equipment for Disabled Self, Spouse, Child or Parent",
                                "Disabled Individual", "Total Education Fees for Self", "Total Medical Expenses",
                                "Lifestyle Expenses", "Additional Lifestyle Expenses", "Purchase of Breastfeeding Equipment",
                                "Child Care Fees", "Net Deposit in SSPN", "Husband/Wife/Alimony Payments",
                                "Disabled Husband/Wife", "Total Child Relief", "Total Life insurance and EPF",
                                "Deferred Annuity and Private Retirement Scheme (PRS)", "Education & Medical Insurance",
                                "Contribution to SOCSO", "Expenses on Charging Facilities for Electric Vehicle (Not for business use)",
                                "Total Relief", "Taxable Income", "Tax", "Tax Rate"]] = [gender, married, children, disabled, working_status_spouse, salary_spouse,
                                disabled_spouse, annual_income, eligible_tax, individual_relief, medical_parents, purchase_disabled, disabled_individual_relief, 
                                total_self_education_fee, total_medical, lifestyle, add_lifestyle, purchase_breastfeeding, child_care_fees, sspn, payment_alimony, 
                                disabled_spouse_relief, total_child_relief, total_life_epf, prs, edu_medical_insurance, socso, exp_vehicle_electric, total_tax_relief, 
                                taxable_income, tax, tax_rate]
        
        # Save the updated DataFrame to the CSV file
        save_to_csv(df, filename)
        print("Your data has been updated in the system.")
    else:
        print("User not found in the system.")

def self_education_fee(education_fee_i, education_fee_ii, education_fee_iii):
    total = education_fee_i + education_fee_ii + education_fee_iii
    if total > 7000:
        print("The maximum amount can be declared is RM7000.")
        total = 7000
    return total

def medical_relief(medical_serious, medical_fertility, medical_vaccination, medical_expenses, medical_expenses_child):
    total = medical_serious + medical_fertility + medical_vaccination + medical_expenses + medical_expenses_child
    if total > 10000:
        print("The maximum amount can be declared is RM10000.")
        total = 10000
    return total

# based on assessment year 2023
def calculate_tax(income, total_relief):
    taxable_income = income - total_relief
    if taxable_income <= 5000:
        tax = 0
        tax_rate = "none"
    elif taxable_income >= 5001 and taxable_income <= 20000:
        tax = (taxable_income - 5000) * 0.01
        tax_rate = "1%"
    elif taxable_income >= 200001 and taxable_income <= 35000:
        tax = 150 + ((taxable_income - 20000) * 0.03)
        tax_rate = "3%"
    elif taxable_income >= 35001 and taxable_income <= 50000:
        tax = 600 +((taxable_income - 35000) * 0.06)
        tax_rate = "6%"
    elif taxable_income >= 50001 and taxable_income <= 70000:
        tax = 1500 + ((taxable_income - 50000) * 0.11)
        tax_rate = "11%"
    elif taxable_income >= 70001 and taxable_income <= 100000:
        tax = 3700 + ((taxable_income - 70000) * 0.19)
        tax_rate = "19%"
    elif taxable_income >= 100001 and taxable_income <= 400000:
        tax = 9400 + ((taxable_income - 100000) * 0.25)
        tax_rate = "25%"
    elif taxable_income >= 400001 and taxable_income <= 600000:
        tax = 84400 + ((taxable_income - 400000) * 0.26)
        tax_rate = "26%"
    elif taxable_income >= 600001 and taxable_income <= 2000000:
        tax = 136400 + ((taxable_income - 600001) * 0.28)
        tax_rate = "28%"
    else:
        tax = 528400 + ((taxable_income - 2000001) * 0.30)
        tax_rate = "30%"
    
    return "%.2f"%tax, tax_rate, taxable_income

def tax_relief(user_id, filename):
    print("----------General Questions----------")

    gender = input("Gender (Male/Female): ").lower().strip()
    while gender not in ['male', 'female']:
        print("Invalid Input.")
        gender = input("Gender (Male/Female): ").lower().strip()

    married = input("Please enter your married status (Single, Married, Divorced, or Widowed): ").lower().strip()
    while married not in ['single', 'married', 'divorced', 'widowed']:
        print("Invalid Input.")
        married = input("Please enter your married status (Single, Married, Divorced, or Widowed): ").lower().strip()

    children = input("Number of children you have? (if no, put 0): ").strip()
    while not children.isdigit():
        print("Invalid Input. Only number is allowed.")
        children = input("Number of children you have? (if no, put 0): ").strip()

    disabled = input("Disabled? (if disabled, enter 'yes') [Answer can be 'yes' or 'no']: ").lower().strip()
    while disabled not in ['yes', 'no']:
        print("Invalid Input.")
        disabled = input("Disabled? (if disabled, enter 'yes') [Answer can be 'yes' or 'no']: ").lower().strip()

    if married == "married":
        working_status_spouse = input("Working status for spouse (Work/No Work): ").lower().strip()
        while working_status_spouse not in ['work', 'no work']:
            print("Invalid Input.")
            working_status_spouse = input("Working status for spouse (Work/No Work): ").lower().strip()
    
        disabled_spouse = input("Disability for Spouse. (if disabled, enter 'yes') [Answer can be 'yes' or 'no']: ").lower().strip()
        while disabled_spouse not in ['yes', 'no']:
            print("Invalid Input.")
            disabled_spouse = input("Disablility for Spouse. (if disabled, enter 'yes') [Answer can be 'yes' or 'no']: ").lower().strip()
    else:
        working_status_spouse = "none"
        disabled_spouse = "none"

    if working_status_spouse == "work":
        salary_spouse_input = get_valid_input("Please enter the annual income for spouse (RM): ")
    else:
        salary_spouse_input = 0

    annual_income_input = get_valid_input("Please enter your annual income (RM): ")

    epf_input = get_valid_input("Please enter your EPF contribution (RM): ")

    min_income = annual_income_input - epf_input

    if min_income >= 34000:
        eligible_tax = "yes"
    else:
        eligible_tax = "no"

    if eligible_tax == "no":
        individual_relief = '-'
        medical_parents = '-'
        purchase_disabled = '-'
        disabled_individual_relief = '-'
        total_self_education_fee = '-'
        total_medical = '-'
        lifestyle = '-' 
        add_lifestyle = '-'
        purchase_breastfeeding = '-'
        child_care_fees = '-'
        sspn = '-'
        payment_alimony = '-'
        disabled_spouse_relief = '-'
        total_child_relief = '-'
        total_life_epf = '-'
        prs = '-'
        edu_medical_insurance = '-'
        socso = '-'
        exp_vehicle_electric = '-'
        total_tax_relief = '-'
        taxable_income = '-'
        tax = '-'
        tax_rate = '-'

        eligibility_tax(user_id, [] , gender, married, str(children), disabled, working_status_spouse,
                        salary_spouse_input, disabled_spouse, annual_income_input, eligible_tax, individual_relief, 
                        medical_parents, purchase_disabled, disabled_individual_relief,
                        total_self_education_fee, total_medical, lifestyle, add_lifestyle, purchase_breastfeeding,
                        child_care_fees, sspn, payment_alimony, disabled_spouse_relief, total_child_relief,
                        total_life_epf, prs, edu_medical_insurance, socso, exp_vehicle_electric, 
                        total_tax_relief, taxable_income, tax, tax_rate, filename)
        print("You are not eligible for tax.")

    if eligible_tax == "yes":
        print("You are aligible for tax.")
        print("You are required to answer the following question to calculate tax.")
        print("You will mandatory get RM9000 for Individual Tax Relief.")

        individual_relief = 9000

        if disabled == "yes":
            print("You will get RM6000 for tax relief under category disabled individual.")
            disabled_individual_relief = 6000
        else:
            disabled_individual_relief = 0

        if disabled_spouse == "yes":
            print("You will get RM5000 for tax relief under category disabled husband/wife.")
            disabled_spouse_relief = 5000
        else:
            disabled_spouse_relief = 0
    
        medical_parents = get_valid_input("Please enter the amount for the Medical treatment, special needs and carer expenses for parents (Medical condition certified by medical practitioner) (if no, put 0):")
        if medical_parents > 8000:
            print("The maximum amount can be declared is RM8000.")
            medical_parents = 8000

        purchase_disabled =  get_valid_input("Please enter the amount for the Purchase of basic supporting equipment for disabled self, spouse, child or parent (if no, put 0): ")
        if purchase_disabled > 6000:
            print("The maximum amount can be declared is RM6000.")
            purchase_disabled = 6000

        education_fee_i = get_valid_input("Please enter the education fee for yourself under category: ther than a degree at masters or doctorate level [Course of study in law, accounting, islamic financing, tehcnical, vocational, industrial, scientific or technology] (if no, put 0): ")
    
        education_fee_ii = get_valid_input("Please enter your education fee for Degree at masters or doctorate level [Any course of study] (if no, put 0): ")
    
        education_fee_iii = get_valid_input("Please enter your education fee for Course of study undertaken for the purpose of upskilling or self-enhancement (if no, put 0): ")
        if education_fee_iii > 2000:
            print("The maximum amount can be declared is RM2000.")
            education_fee_iii = 2000

        total_self_education_fee = self_education_fee(education_fee_i,education_fee_ii,education_fee_iii)
    
        medical_serious = get_valid_input("Please enter the medical expenses on Serious diseases for self, spouse or child (if no, put 0): ")
    
        medical_fertility = get_valid_input("Please enter the medical expenses on Fertility treatment for self or spouse (if no, put 0): ")
    
        medical_vaccination = get_valid_input("Please enter the medical expenses on Vaccination for self, spouse and child (if no, put 0): ")
        if medical_vaccination > 1000:
            print("The maximum amount can be declared is RM1000.")
            medical_vaccination = 1000

        medical_expenses = get_valid_input("Please enter the medical expenses on Complete medical examination, COVID-19 detection test including purchase of self-detection test kit, Mental health examination or consultation for self, spouse, child (if no, put 0): ")
        if medical_expenses > 1000:
            print("The maximum amount can be declared is RM1000.")
            medical_expenses = 1000

        medical_expenses_child = get_valid_input("Expenses for child aged 18 and below [Assessment of intellectual disability diagnosis / Early intervention programme / intellectual disability rehabilitation treatment] (if no, put 0): ")
        if medical_expenses_child > 4000:
            print("The maximum amount can be declared is RM4000.")
            medical_expenses_child = 4000
    
        total_medical = medical_relief(medical_serious, medical_fertility, medical_vaccination, medical_expenses, medical_expenses_child)

        lifestyle = get_valid_input("Please enter your expenses on Lifestyle for the use / benefit of self, spouse or child (if no, put 0): ")
        if lifestyle > 2500:
            print("The maximum amount can be declared is RM2500.")
            lifestyle = 2500

        add_lifestyle = get_valid_input("Please enter your additional relief on Lifestyle for the use / benefit of self, spouse or child (if no, put 0): ")
        if add_lifestyle > 500:
            print("The maximum amount can be declared is RM500.")
            add_lifestyle = 500

        purchase_breastfeeding = get_valid_input("Please enter your expenses on Purchase of breastfeeding equipment for own use for a child aged 2 years and below (Deduction allowed once in every TWO (2) years of assessment) (if no, put 0): ")
        if purchase_breastfeeding > 1000:
            print("The maximum amount can be declared is RM1000.")
            purchase_breastfeeding = 1000
    
        child_care_fees = get_valid_input("Child care fees to a registered child care centre / kindergarten for a child aged 6 years and below (if no, put 0): ")
        if child_care_fees > 3000:
            print("The maximum amount can be declared is RM3000.")
            child_care_fees = 3000

        sspn = get_valid_input("Net deposit in Skim Simpanan Pendidikan Nasional (if no, put 0): ")
        if sspn > 8000:
            print("The maximum amount can be declared is RM8000.")
            sspn = 8000

        payment_alimony = get_valid_input("Husband / Wife / Payment of alimony to former wife (if no, put 0): ")
        if payment_alimony > 4000:
            print("The maximum amount can be declared is RM4000.")
            payment_alimony = 4000
    
        if int(children) > 0:
            child_under18 = input("Please enter the number of unmarried child and under the age of 18 years old (if no, put 0): ").strip()
            while not child_under18.isdigit():
                print("Invalid Input. Only number is allowed.")
                child_under18 = input("Please enter the number of unmarried child and under the age of 18 years old (if no, put 0): ").strip()
            amount_child_under18 = int(child_under18) * 2000

            child_above18 = input("Please enter the number of unmarried child of 18 years and above who is receiving full-time education (A-Level, certificate, matriculation or preparatory courses) (if no, put 0): ").strip()
            while not child_above18.isdigit():
                print("Invalid Input. Only number is allowed.")
                child_above18 = input("Please enter the number of unmarried child of 18 years and above who is receiving full-time education (A-Level, certificate, matriculation or preparatory courses) (if no, put 0): ").strip()
            amount_childabove18 = int(child_above18) * 2000

            child_above18_uni = input("Please enter the number of unmarried child of 18 years and receiving further education (if no, put 0): ").strip()
            while not child_above18_uni.isdigit():
                print("Invalid Input. Only number is allowed.")
                child_above18_uni = input("Please enter the number of unmarried child of 18 years and receiving further education (if no, put 0): ").strip()
            amount_child_above18_uni = int(child_above18_uni) * 8000

            child_disabled = input("Please enter the number of disabled child (if no, put 0): ").strip()
            while not child_disabled.isdigit():
                print("Invalid Input. Only number is allowed.")
                child_disabled = input("Please enter the number of disabled child (if no, put 0): ").strip()
            amount_child_disabled = int(child_disabled) * 6000
        
            child_disabled_18 = input("Please enter the number of disable child age 18 years old and above, not married and pursuing diplomas or above qualification in Malaysia @ bachelor degree or above outside Malaysia in program and in Higher Education Institute that is accredited by related Government authorities (if no, put 0): ").strip()
            while not child_disabled_18.isdigit():
                print("Invalid Input. Only number is allowed.")
                child_disabled_18 = input("Please enter the number of disable child age 18 years old and above, not married and pursuing diplomas or above qualification in Malaysia @ bachelor degree or above outside Malaysia in program and in Higher Education Institute that is accredited by related Government authorities (if no, put 0): ").strip()
            amount_child_disabled_18 = int(child_disabled_18) * 6000
        
            total_child_relief = amount_child_disabled_18 + amount_child_above18_uni + amount_child_disabled + amount_child_under18 + amount_childabove18
            print("You will get a total of RM", total_child_relief, " for child relief.")
        else:
            total_child_relief = 0

        civil = input("Are you a civil servant or non-civil servant? (Answer can be 'civil' or 'non-civil'): ").lower().strip()
        while civil not in ['civil', 'non-civil']:
            print("Invalid Input.")
            civil = input("Are you a civil servant or non-civil servant? (Answer can be 'civil' or 'non-civil'): ").lower().strip()
    
        if civil == 'civil':
            civil_input = get_valid_input("Please enter your Life insurance premium payments or family takaful contributions (if no, put 0): ")
            if civil_input > 7000:
                print("The maximum amount can be declared is RM7000.")
                civil_input = 7000
            total_life_epf = civil_input
        else:
            noncivil_input1 = get_valid_input("Please enter your Mandatory contributions to approved schemes or voluntary contributions to EPF (excluding private retirement schemes) or contributions under any written law (if no, put 0): ")
            if noncivil_input1 > 4000:
                print("The maximum amount can be declared is RM4000.")
                noncivil_input1 = 4000
            noncivil_input2 = get_valid_input("Please enter your Life insurance premium payments or family takaful contributions or additional voluntary contributions to EPF (if no, put 0): ")
            if noncivil_input2 > 3000:
                print("The maximum amount can be declared is RM3000.")
                noncivil_input2 = 3000
            total_life_epf = noncivil_input1 + noncivil_input2

        prs = get_valid_input("Please enter your amount for Deferred Annuity and Private Retirement Scheme (PRS) (if no, put 0): ")
        if prs > 3000:
            print("The maximum amount can be declared is RM3000.")
            prs = 3000
    
        edu_medical_insurance = get_valid_input("Please enter your amount for Education and medical insurance (if no, put 0): ")
        if edu_medical_insurance > 3000:
            print("The maximum amount can be declared is RM3000.")
            edu_medical_insurance = 3000
    
        socso = get_valid_input("Please enter your Contribution to the Social Security Organization (SOCSO) (if no, put 0): ")
        if socso > 350:
            print("The maximum amount can be declared is RM350.")
            socso = 350

        exp_vehicle_electric = get_valid_input("Please enter your Expenses on charging facilities for Electric Vehicle (Not for business use) (if no, put 0): ")
        if exp_vehicle_electric > 2500:
            print("The maximum amount can be declared is RM2500.")
            exp_vehicle_electric = 2500
    
        total_tax_relief = individual_relief + medical_parents + purchase_disabled + disabled_individual_relief + total_self_education_fee + total_medical + lifestyle + add_lifestyle + purchase_breastfeeding + child_care_fees + sspn + payment_alimony + disabled_spouse_relief + total_child_relief + total_life_epf + prs + edu_medical_insurance + socso + exp_vehicle_electric
        
        tax, tax_rate, taxable_income = calculate_tax(annual_income_input, total_tax_relief)
        print("Your annual income is RM",annual_income_input,".")
        print("Your total tax relief is RM",total_tax_relief,".")
        print("Your taxable income is RM",taxable_income,".")
        print("Your tax rate is", tax_rate,".")
        print("You will be taxed RM",tax,".")
        eligibility_tax(user_id, [] , gender, married, children, disabled, working_status_spouse,
                        salary_spouse_input, disabled_spouse, annual_income_input, eligible_tax, individual_relief, 
                        medical_parents, purchase_disabled, disabled_individual_relief,
                        total_self_education_fee, total_medical, lifestyle, add_lifestyle, purchase_breastfeeding,
                        child_care_fees, sspn, payment_alimony, disabled_spouse_relief, total_child_relief,
                        total_life_epf, prs, edu_medical_insurance, socso, exp_vehicle_electric, total_tax_relief, taxable_income, tax, tax_rate, filename)
    return total_tax_relief, tax, tax_rate

