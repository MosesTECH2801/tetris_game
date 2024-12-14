import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Collect employee details
def collect_employee_data():
    employees = []
    num_employees = int(input("Enter the number of employees: "))
    
    for i in range(num_employees):
        print(f"\nEntering details for Employee {i + 1}:")
        name = input("Enter employee name: ")
        age = int(input("Enter employee age: "))
        department = input("Enter employee department: ")
        salary = float(input("Enter employee salary: "))
        performance_score = float(input("Enter employee performance score (0-100): "))
        
        employees.append({
            "Name": name,
            "Age": age,
            "Department": department,
            "Salary": salary,
            "Performance Score": performance_score
        })
    
    return pd.DataFrame(employees)

# Step 2: Generate visualizations
def generate_visualizations(employee_df):
    # Bar chart for department distribution
    plt.figure(figsize=(10, 5))
    department_counts = employee_df['Department'].value_counts()
    department_counts.plot(kind='bar', color='skyblue')
    plt.title('Employee Count by Department')
    plt.xlabel('Department')
    plt.ylabel('Count')
    plt.show()
    
    # Pie chart for performance distribution
    plt.figure(figsize=(8, 8))
    performance_bins = pd.cut(employee_df['Performance Score'], bins=[0, 50, 70, 85, 100], 
                               labels=['Poor', 'Average', 'Good', 'Excellent'])
    performance_bins.value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['red', 'orange', 'yellow', 'green'])
    plt.title('Performance Distribution')
    plt.ylabel('')
    plt.show()
    
    # Scatter plot for salary vs. performance
    plt.figure(figsize=(10, 5))
    plt.scatter(employee_df['Performance Score'], employee_df['Salary'], c='blue', alpha=0.5)
    plt.title('Salary vs. Performance Score')
    plt.xlabel('Performance Score')
    plt.ylabel('Salary')
    plt.grid()
    plt.show()

    # Histogram for age distribution
    plt.figure(figsize=(10, 5))
    employee_df['Age'].plot(kind='hist', bins=10, color='purple', alpha=0.7)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()

# Main execution
if __name__ == "__main__":
    print("Employee Management System")
    employee_df = collect_employee_data()
    print("\nEmployee Details Collected:")
    print(employee_df)
    
    print("\nGenerating Visualizations...")
    generate_visualizations(employee_df)

