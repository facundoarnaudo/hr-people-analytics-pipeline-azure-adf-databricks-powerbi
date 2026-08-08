import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os
import csv
import calendar

fake = Faker('en_US')
Faker.seed(42)
random.seed(42) # Key seed to maintain the same employees across scripts

# 1. Generate 43 months dynamically (Jan 2023 to Jul 2026)
snapshot_dates = []
for year in [2023, 2024, 2025, 2026]:
    for month in range(1, 13):
        if year == 2026 and month > 7:
            break
        last_day = calendar.monthrange(year, month)[1]
        snapshot_dates.append(f"{year}-{month:02d}-{last_day:02d}")

os.makedirs("historical_data", exist_ok=True)

# 2. Realistic Corporate Structure (Weighted)
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
# male skew in Operations and a lighter one in IT & Data. Must stay identical
# to the same block in generate_data.py so future incremental months stay
# coherent with this history.
GENDER_WEIGHTS_BY_DEPARTMENT = {
    "Operations": {"M": 65, "F": 30, "X": 5},
    "IT & Data": {"M": 60, "F": 35, "X": 5},
}
DEFAULT_GENDER_WEIGHTS = {"M": 55, "F": 40, "X": 5}

def draw_gender(department):
    weights = GENDER_WEIGHTS_BY_DEPARTMENT.get(department, DEFAULT_GENDER_WEIGHTS)
    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]

# 3. Strict role assignment for the corporate pyramid
num_employees = 2500
assigned_roles = []
for r in roles_data:
    count = int(num_employees * (r["weight"] / 100))
    assigned_roles.extend([r] * count)

while len(assigned_roles) < num_employees:
    assigned_roles.append(roles_data[26])

random.shuffle(assigned_roles)

# 4. Create static employee universe
master_employees = []
today = datetime(2026, 7, 31) # Global base date to calculate tenure

for i in range(1, num_employees + 1):
    employee_id = f"EMP{str(i).zfill(5)}"
    role = assigned_roles[i-1]
    gender = draw_gender(role["department"])

    hire_date = today - timedelta(days=random.randint(1, 4000))

    if random.random() < 0.20:
        worked_days = random.randint(30, 2000)
        termination_date = hire_date + timedelta(days=worked_days)
        if termination_date > today:
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

# 5. Time Travel Generation (43 months)
for snapshot_str in snapshot_dates:
    snapshot_date = datetime.strptime(snapshot_str, "%Y-%m-%d")

    monthly_headcount = []
    monthly_surveys = []
    monthly_market_salaries = []
    monthly_roles_dim = []

    months_from_start = snapshot_dates.index(snapshot_str)
    inflation_multiplier = (1.005) ** months_from_start

    for r in roles_data:
        market_salary = round(r["base_salary"] * inflation_multiplier, 2)
        min_salary = round(market_salary * 0.8, 2)
        max_salary = round(market_salary * 1.2, 2)

        monthly_market_salaries.append({
            "role_id": r["role_id"],
            "department": r["department"],
            "role_name": r["role_name"],
            "seniority": r["seniority"],
            "average_market_salary": market_salary,
            "min_market_salary": min_salary,
            "max_market_salary": max_salary,
            "currency": "USD",
            "snapshot_date": snapshot_str
        })

        dept_str = f"  {r['department'].lower()} " if random.random() < 0.15 else r['department']

        monthly_roles_dim.append({
            "role_id": r["role_id"],
            "department": dept_str,
            "role_name": r["role_name"],
            "seniority": r["seniority"],
            "average_market_salary": market_salary,
            "snapshot_date": snapshot_str
        })

    pd.DataFrame(monthly_market_salaries).to_csv(
        f'historical_data/reference_salaries_{snapshot_str.replace("-","")}.csv',
        index=False, quoting=csv.QUOTE_NONNUMERIC
    )

    pd.DataFrame(monthly_roles_dim).to_csv(
        f'historical_data/dim_role_{snapshot_str.replace("-","")}.csv',
        index=False, quoting=csv.QUOTE_NONNUMERIC
    )

    for emp in master_employees:
        if emp["hire_date"] <= snapshot_date:
            is_active = emp["termination_date"] is None or emp["termination_date"] > snapshot_date

            if is_active or (emp["termination_date"].year == snapshot_date.year and emp["termination_date"].month == snapshot_date.month):

                current_market = next(item["average_market_salary"] for item in monthly_roles_dim if item["role_id"] == emp["role_id"])

                if snapshot_date.month == 1 and is_active:
                    emp["base_variance"] = random.uniform(0.95, 1.10)

                real_salary = round(current_market * emp["base_variance"], 2)
                performance_rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 50, 25, 10], k=1)[0]

                final_hire_date = emp["hire_date"].strftime('%Y-%m-%d')
                final_salary = real_salary

                # Controlled Chaos: Headcount Data Quality Issues
                if random.random() < 0.05:
                    final_hire_date = None
                if random.random() < 0.05:
                    final_salary = -abs(real_salary)
                if random.random() < 0.05:
                    performance_rating = random.choice([0, 7, 8, 9])

                monthly_headcount.append({
                    "employee_id": emp["employee_id"],
                    "role_id": emp["role_id"],
                    "gender": emp["gender"],
                    "current_salary": final_salary,
                    "hire_date": final_hire_date,
                    "termination_date": emp["termination_date"].strftime('%Y-%m-%d') if emp["termination_date"] else None,
                    "is_active": is_active,
                    "performance_rating": performance_rating,
                    "snapshot_date": snapshot_str
                })

                # SEMI-ANNUAL SURVEY LOGIC (July & December only)
                if snapshot_date.month in [7, 12]:
                    if is_active and random.random() < 0.80:
                        if abs(real_salary) < (current_market * 0.9):
                            comp_score = random.choices([1, 2, 3], weights=[50, 40, 10], k=1)[0]
                        else:
                            comp_score = random.choices([3, 4, 5], weights=[20, 50, 30], k=1)[0]

                        leadership_score = random.choices([1, 2, 3, 4, 5], weights=[10, 15, 40, 25, 10], k=1)[0]
                        wlb_score = random.choices([1, 2, 3, 4, 5], weights=[15, 20, 30, 25, 10], k=1)[0]

                        if random.random() < 0.05:
                            leadership_score = None
                            average_score = (comp_score + wlb_score) / 2
                        else:
                            average_score = (comp_score + leadership_score + wlb_score) / 3

                        general_score = max(1, min(5, round(average_score + random.uniform(-0.5, 0.5), 1)))

                        monthly_surveys.append({
                            "employee_id": emp["employee_id"],
                            "general_satisfaction_score": general_score,
                            "compensation_benefits_score": comp_score,
                            "leadership_score": leadership_score,
                            "work_life_balance_score": wlb_score,
                            "feedback": "Historical feedback"
                        })

    pd.DataFrame(monthly_headcount).to_csv(
        f'historical_data/headcount_{snapshot_str.replace("-","")}.csv',
        index=False, quoting=csv.QUOTE_NONNUMERIC
    )

    if snapshot_date.month in [7, 12] and len(monthly_surveys) > 0:
        pd.DataFrame(monthly_surveys).to_csv(
            f'historical_data/climate_survey_{snapshot_str.replace("-","")}.csv',
            index=False, quoting=csv.QUOTE_MINIMAL
        )

print("43-month history generated successfully with exact corporate pyramid and weighted gender distribution.")
