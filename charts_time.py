import matplotlib.pyplot as plt

# Example data
x = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1526, 2048, 2560, 3072, 3584, 3968]  # X-axis values
y1 = [0.04410743713378906,
0.3371238708496094,
1.0821819305419922,
3.8831233978271484,
9.00888442993164,
15.974998474121094,
37.10007667541504,
67.28100776672363,
106.78720474243164,
151.97992324829102,
279.6769142150879,
432.4150085449219,
606.5211296081543,
866.8999671936035,
1083.4169387817383 ]

  #basic
y2 = [
    0.09012222290039062, 0.8509159088134766, 2.953052520751953, 10.490179061889648,
    26.262998580932617, 42.09780693054199, 95.14212608337402, 183.380126953125,
    270.4591751098633, 529.3548107147217, 734.699010848999, 1109.0431213378906,
    1606.6699028015137, 2186.784029006958, 2647.7417945861816
]

  #efficient

# Creating the plot
plt.figure(figsize=(10, 5))  # Set the figure size (optional)

# Plotting the first line
plt.plot(x, y1, label='Basic', marker='o')  # 'marker' adds markers at data points

# Plotting the second line
plt.plot(x, y2, label='Efficient', marker='s')  # Different marker style

# Adding title and labels
plt.title('Time vs Problem size (M+N)')
plt.xlabel('Problem size (M+N)')
plt.ylabel('Time (ms)')

# Adding a legend
plt.legend()

# Showing the grid (optional)
plt.grid(True)

# Display the plot
plt.savefig('timeVSprob.png')
plt.show()
