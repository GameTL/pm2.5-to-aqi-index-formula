import numpy as np
import matplotlib.pyplot as plt

# AQI Breakpoints as (x, y) coordinates
# x = concentration (µg/m³), y = index value

# Define the key breakpoints from the table
key_breakpoints = [
    (0.0, 0),
    (54.0, 50),
    (55.0, 51),
    (154, 100),
    (155, 101),
    (254, 150),
    (255, 151),
    (354, 200),
    (355, 201),
    (424, 300),
    (425, 301),
    (425, 301),
    (706, 500),
]

def linear_interpolate(x1, y1, x2, y2, x):
    """Linear interpolation between two points"""
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

def generate_all_integer_points(breakpoints):
    """Generate points for all integer x values with linear interpolation"""
    all_points = []
    
    # Find the range of x values
    min_x = int(breakpoints[0][0])
    max_x = int(breakpoints[-1][0])
    
    for x in range(min_x, max_x + 1):
        # Find which segment this x falls into
        for i in range(len(breakpoints) - 1):
            x1, y1 = breakpoints[i]
            x2, y2 = breakpoints[i + 1]
            
            if x1 <= x <= x2:
                if x == x1:
                    y = y1
                elif x == x2:
                    y = y2
                else:
                    y = linear_interpolate(x1, y1, x2, y2, x)
                
                all_points.append((x, round(y, 1)))
                break
    
    return all_points

# Generate all integer points
all_aqi_points = generate_all_integer_points(key_breakpoints)

print("All integer AQI points (concentration, index):")
print(f"Total points: {len(all_aqi_points)}")
print("\nFirst 20 points:")
for i, point in enumerate(all_aqi_points[:20]):
    print(f"({point[0]}, {point[1]})")

print("\n... (middle points omitted for display)")

print(f"\nLast 20 points:")
for point in all_aqi_points[-20:]:
    print(f"({point[0]}, {point[1]})")

# Create separate lists for easy use
pm25 = [point[0] for point in all_aqi_points]
aqi = [point[1] for point in all_aqi_points]

print(f"\nX values (0 to 500): {pm25[:10]}...{pm25[-10:]}")
print(f"Y values (interpolated): {aqi[:10]}...{aqi[-10:]}")

# Original breakpoints for reference
print(f"\nOriginal key breakpoints:")
for point in key_breakpoints:
    print(f"({point[0]}, {point[1]})")
    

print(f'{len(aqi)=}')
# Polynomial degree (adjust as needed)
degree = 6 # 6 has better linearity in the in the 0-100 range

# Fit polynomial
coefficients = np.polyfit(pm25, aqi, degree)
poly = np.poly1d(coefficients)

# Plot
x_fit = np.linspace(0, key_breakpoints[-1][0], 500)
y_fit = poly(x_fit)
formula = "y = " + " + ".join(
    [f"{coef:.4g}x^{i}" if i != 0 else f"{coef:.4g}" 
     for i, coef in enumerate(poly.coefficients[::-1])]
)
print(y_fit)
print(formula)

plt.figure(figsize=(10,6))
plt.plot(pm25, aqi, 'o', markersize=3, label='Raw Data')
plt.plot(x_fit, y_fit, 'r-', label=f'Polynomial Fit (Degree {degree})')
plt.xlabel("PM10 (µg/m³)")
plt.ylabel("AQI (US)")
plt.title(f"Polynomial Fit from PM10 to AQI (US)\nFormula : {formula}")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
# Print the polynomial formula