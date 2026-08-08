import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import calendar
import json

fake = Faker('en_US')
# SAME SEEDS AS HISTORICAL SCRIPT TO GUARANTEE CONTINUITY
Faker.seed(42)
random.seed(42)

roles_data = [
    {"role_id": "R001", "department": "Executive", "role_name": "Chief Executive Officer (CEO)", "seniority": "C-Level", "base_salary": 10000, "weight": 0.04},
    {"role_id": "R002", "department": "Finance", "role_name": "Chief Financial Officer (CFO)", "seniority": "C-Level", "base_salary": 8500, "weight": 0.04},
    {"role_id": "R003", "department": "Human Resources", "role_name": "Chief Human Resources Officer (CHRO)", "seniority": "C-Level", "base_salary": 8500, "weight": 0.04},
    {"role_id": "R004", "department": "Operations", "role_name": "Chief Operating Officer (COO)", "seniority": "C-Level", "base_salary": 9000, "weight": 0.04},
    {"role_id": "R005", "department": "IT & Data", "role_name": "Chief Information Officer (CIO)", "seniority": "C-Level", "base_salary": 8500, "weight": 0.04},
    {"role_id": "R006", "department": "Operations", "role_name": "Plant Director", "seniority": "Director", "base_salary": 7000, "weight": 0.20},
    {"role_id": "R007", "department": "IT & Data", "role_name": "Data & Analytics Director", "seniority": "Director", "base_salary": 7500, "weight": 0.20},
    {"role_id": "R008", "department": "Commercial", "role_name": "Sales Director", "seniority": "Director", "base_salary": 7000, "weight": 0.20},
    {"role_id": "R009", "department": "Supply Chain", "role_name": "Logistics & Supply Chain Director", "seniority": "Director", "base_salary": 6800, "weight": 0.20},
    {"role_id": "R010", "department": "Finance", "role_name": "FP&A Manager", "seniority": "Manager", "base_salary": 5000, "weight": 0.80},
    {"role_id": "R011", "department": "Human Resources", "role_name": "Talent Acquisition Manager", "seniority": "Manager", "base_salary": 4500, "weight": 0.80},
    {"role_id": "R012", "department": "Operations", "role_name": "Production Manager", "seniority": "Manager", "base_salary": 4800, "weight": 1.00},
    {"role_id": "R013", "department": "IT & Data", "role_name": "Data Engineering Manager", "seniority": "Manager", "base_salary": 5500, "weight": 0.60},
    {"role_id": "R014", "department": "Supply Chain", "role_name": "Warehouse Manager", "seniority": "Manager", "base_salary": 4200, "weight": 0.80},
    {"role_id": "R015", "department": "Human Resources", "role_name": "HR Business Partner", "seniority": "Professional", "base_salary": 3000, "weight": 2.50},
    {"role_id": "R016", "department": "Human Resources", "role_name": "People Analytics Specialist", "seniority": "Professional", "base_salary": 3200, "weight": 1.00},
    {"role_id": "R017", "department": "IT & Data", "role_name": "Data Scientist", "seniority": "Professional", "base_salary": 4000, "weight": 2.00},
    {"role_id": "R018", "department": "IT & Data", "role_name": "Cloud Infrastructure Architect", "seniority": "Professional", "base_salary": 4500, "weight": 1.50},
    {"role_id": "R019", "department": "Operations", "role_name": "Process Optimization Engineer", "seniority": "Professional", "base_salary": 3500, "weight": 3.50},
    {"role_id": "R020", "department": "Operations", "role_name": "Maintenance Supervisor", "seniority": "Supervisor", "base_salary": 2800, "weight": 4.00},
    {"role_id": "R021", "department": "Supply Chain", "role_name": "Procurement Specialist", "seniority": "Professional", "base_salary": 2500, "weight": 3.00},
    {"role_id": "R022", "department": "Finance", "role_name": "Senior Accountant", "seniority": "Professional", "base_salary": 2600, "weight": 2.50},
    {"role_id": "R023", "department": "Commercial", "role_name": "Key Account Manager", "seniority": "Professional", "base_salary": 3000, "weight": 4.00},
    {"role_id": "R024", "department": "Commercial", "role_name": "Sales Representative", "seniority": "Professional", "base_salary": 1800, "weight": 6.00},
    {"role_id": "R025", "department": "Operations", "role_name": "HSE Supervisor", "seniority": "Supervisor", "base_salary": 2700, "weight": 3.00},
    {"role_id": "R026", "department": "Supply Chain", "role_name": "Zampi Operator", "seniority": "Operator", "base_salary": 1200, "weight": 8.00},
    {"role_id": "R027", "department": "Operations", "role_name": "Shift Operator", "seniority": "Operator", "base_salary": 1100, "weight": 20.00},
    {"role_id": "R028", "department": "Operations", "role_name": "Maintenance Technician", "seniority": "Operator", "base_salary": 1400, "weight": 12.00},
    {"role_id": "R029", "department": "Commercial", "role_name": "Customer Service Agent", "seniority": "Operator", "base_salary": 1000, "weight": 10.00},
    {"role_id": "R030", "department": "Finance", "role_name": "Billing Clerk", "seniority": "Operator", "base_salary": 1100, "weight": 5.00}
]

# Gender distribution: company baseline 55% M / 40% F / 5% X, with a stronger
# male skew in Operations and a lighter one in IT & Data. Same dict must be
# copied into generate_data_hist.py if the historical data ever gets regenerated.
GENDER_WEIGHTS_BY_DEPARTMENT = {
    "Operations": {"M": 65, "F": 30, "X": 5},
    "IT & Data": {"M": 60, "F": 35, "X": 5},
}
DEFAULT_GENDER_WEIGHTS = {"M": 55, "F": 40, "X": 5}

def draw_gender(department):
    weights = GENDER_WEIGHTS_BY_DEPARTMENT.get(department, DEFAULT_GENDER_WEIGHTS)
    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]

# 1. Recreate the exact base universe (to link history)
num_employees = 2500
assigned_roles = []
for r in roles_data:
    assigned_roles.extend([r] * int(num_employees * (r["weight"] / 100)))
while len(assigned_roles) < num_employees:
    assigned_roles.append(roles_data[26])
random.shuffle(assigned_roles)

master_employees = []
base_date = datetime(2026, 7, 31)

for i in range(1, num_employees + 1):
    employee_id = f"EMP{str(i).zfill(5)}"
    role = assigned_roles[i-1]
    gender = draw_gender(role["department"])  # drawn first, same position as in the historical script

    hire_date = base_date - timedelta(days=random.randint(1, 4000))
    if random.random() < 0.20:
        worked_days = random.randint(30, 2000)
        termination_date = hire_date + timedelta(days=worked_days)
        if termination_date > base_date:
            # Right-censored: the calculated termination falls beyond the
            # observation window, so this person hasn't left as far as we can see.
            termination_date = None
    else:
        termination_date = None

    master_employees.append({
        "employee_id": employee_id,
        "role_id": role["role_id"],
        "gender": gender,
        "hire_date": hire_date,
        "termination_date": termination_date,
        "base_variance": random.uniform(0.80, 1.10)
    })

# 2. Execute generation for August 2026 (Month 43 from Jan 2023)
target_month = "2026-08-31"
snapshot_date = datetime.strptime(target_month, "%Y-%m-%d")
inflation_multiplier = (1.005) ** 43

monthly_headcount = []
monthly_roles_dim = []
reference_salaries = []

# --- Dimension Roles & Market Salaries (JSON) ---
for r in roles_data:
    market_salary = round(r["base_salary"] * inflation_multiplier, 2)
    min_salary = round(market_salary * 0.8, 2)
    max_salary = round(market_salary * 1.2, 2)

    reference_salaries.append({
        "role_id": r["role_id"],
        "department": r["department"],
        "role_name": r["role_name"],
        "seniority": r["seniority"],
        "average_market_salary": market_salary,
        "min_market_salary": min_salary,
        "max_market_salary": max_salary,
        "currency": "USD",
        "snapshot_date": target_month
    })

    dept_str = f"  {r['department'].lower()} " if random.random() < 0.15 else r['department']
    monthly_roles_dim.append({
        "role_id": r["role_id"],
        "department": dept_str,
        "role_name": r["role_name"],
        "seniority": r["seniority"],
        "average_market_salary": market_salary,
        "snapshot_date": target_month
    })

# Save Roles CSV and Reference Salary JSON
pd.DataFrame(monthly_roles_dim).to_csv('dim_role.csv', index=False)
with open("reference_salaries.json", "w", encoding="utf-8") as f:
    json.dump(reference_salaries, f, indent=4)

# --- Headcount Generation July 2026 ---
for emp in master_employees:
    if emp["hire_date"] <= snapshot_date:
        is_active = emp["termination_date"] is None or emp["termination_date"] > snapshot_date
        if is_active or (emp["termination_date"].year == snapshot_date.year and emp["termination_date"].month == snapshot_date.month):

            current_market = next(item["average_market_salary"] for item in monthly_roles_dim if item["role_id"] == emp["role_id"])
            real_salary = round(current_market * emp["base_variance"], 2)
            performance_rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 50, 25, 10], k=1)[0]

            final_hire_date = emp["hire_date"].strftime('%Y-%m-%d')
            final_salary = real_salary

            if random.random() < 0.05: final_hire_date = None
            if random.random() < 0.05: final_salary = -abs(real_salary)
            if random.random() < 0.05: performance_rating = random.choice([0, 7, 8, 9])

            monthly_headcount.append({
                "employee_id": emp["employee_id"],
                "role_id": emp["role_id"],
                "gender": emp["gender"],
                "current_salary": final_salary,
                "hire_date": final_hire_date,
                "termination_date": emp["termination_date"].strftime('%Y-%m-%d') if emp["termination_date"] else None,
                "is_active": is_active,
                "performance_rating": performance_rating,
                "snapshot_date": target_month
            })

pd.DataFrame(monthly_headcount).to_csv('headcount.csv', index=False)

# --- Climate Survey (July 2026) ---
surveys = []
positive_feedbacks = ["Great environment", "Very happy with the benefits", "Great team to work with"]
negative_feedbacks = ["Salary is too low compared to the market", "Lack of clear leadership", "Too much workload"]

for emp in monthly_headcount:
    if emp["is_active"] and random.random() < 0.80:
        current_market = next(item["average_market_salary"] for item in monthly_roles_dim if item["role_id"] == emp["role_id"])

        if abs(emp["current_salary"]) < (current_market * 0.9):
            comp_score = random.choices([1, 2, 3], weights=[50, 40, 10], k=1)[0]
            feedback = random.choice(negative_feedbacks)
        else:
            comp_score = random.choices([3, 4, 5], weights=[20, 50, 30], k=1)[0]
            feedback = random.choice(positive_feedbacks)

        leadership_score = random.choices([1, 2, 3, 4, 5], weights=[10, 15, 40, 25, 10], k=1)[0]
        wlb_score = random.choices([1, 2, 3, 4, 5], weights=[15, 20, 30, 25, 10], k=1)[0]

        if random.random() < 0.05:
            leadership_score = None
            average_score = (comp_score + wlb_score) / 2
        else:
            average_score = (comp_score + leadership_score + wlb_score) / 3

        general_score = max(1, min(5, round(average_score + random.uniform(-0.5, 0.5), 1)))

        surveys.append({
            "employee_id": emp["employee_id"],
            "general_satisfaction_score": general_score,
            "compensation_benefits_score": comp_score,
            "leadership_score": leadership_score,
            "work_life_balance_score": wlb_score,
            "feedback": feedback
        })

pd.DataFrame(surveys).to_csv('climate_survey.csv', index=False)
print("July 2026 files generated successfully: headcount.csv, dim_role.csv, reference_salaries.json, and climate_survey.csv")
