import pandas as pd
from functions import verify_user, save_to_csv, read_from_csv, register_user, login_user, tax_relief

filename = "MalaysianDataTax.csv"
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

print("Malaysian Tax Input Program")
#check whether file exist or not, if no create file with header
save_to_csv([], filename)

# Prompt the user for registration or login
while True:
    registered = input("Are you already registered? (Answer can be 'Yes'/'No') : ").strip().lower()
    if registered in ['yes', 'no']:
        break
    else:
        print("Invalid response. Please answer 'yes' or 'no'.")

# go to registration if no and after registration will continue to login
if registered == 'no':
    user_id, ic_number, password = register_user(filename)
    if user_id is not None:
        print("Registration successful. Now you can log in.")
        registered = 'yes'
    else:
        print("IC Number already exists. Pleas login instead")
        registered = 'yes'

if registered == 'yes':
    while True:
        user_id, password = login_user(filename)
        if user_id is None:
            print("Redirecting to registration page.")
            user_id, ic_number, password = register_user(filename)
        else:
            if verify_user(filename, [] , password):
                print("IC number and password verification successful.")
                break
            else:
                print("Verification failed.")
                print("Exiting Program.")
                exit()

tax_relief(user_id, filename)

print("Program Ends! Thank you for using my program.")
