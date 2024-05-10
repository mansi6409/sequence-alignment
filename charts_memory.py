import matplotlib.pyplot as plt

# Example data
x = [
    0, 96, 208, 672, 1520, 1664, 3024, 3408, 5184, 6688,
    10624, 15552, 20960, 30544, 33904
] # X-axis values
y1 = [
    0, 48, 176, 672, 1536, 1664, 2912, 3488, 5264, 6576,
    10576, 15552, 20848, 30528, 33856
]
  #basic
y2 = [
    48, 32, 32, 64, 64, 80, 96, 160, 176, 3568, 
    656, 496, 592, 704, 736
]
  #efficient

# Creating the plot
plt.figure(figsize=(10, 5))  # Set the figure size (optional)

# Plotting the first line
plt.plot(x, y1, label='Basic', marker='o')  # 'marker' adds markers at data points

# Plotting the second line
plt.plot(x, y2, label='Efficient', marker='s')  # Different marker style

# Adding title and labels
plt.title('Memory vs Problem size (M+N)')
plt.xlabel('Problem size (M+N)')
plt.ylabel('Memory (kB)')

# Adding a legend
plt.legend()

# Showing the grid (optional)
plt.grid(True)

# Display the plot
plt.savefig('memVSprob.png')
plt.show()
