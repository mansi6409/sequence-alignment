import matplotlib.pyplot as plt

# Example data
x = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1526, 2048, 2560, 3072, 3584, 3968]  # X-axis values
y1 = [16, 64, 208, 496, 608, 752, 1504, 2656, 3968, 5216, 9040, 13792, 19792, 18592, 24432]
  #basic
y2 = [48, 48, 48, 64, 80, 80, 96, 128, 240, 288, 400, 448, 320, 512, 432]
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
