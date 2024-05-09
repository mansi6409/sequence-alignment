import matplotlib.pyplot as plt

# Example data
x = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1526, 2048, 2560, 3072, 3584, 3968]  # X-axis values
y1 = [
    0.03910064697265625, 0.3559589385986328, 1.2712478637695312, 5.0067901611328125,
    10.273933410644531, 18.671751022338867, 44.86584663391113, 78.9182186126709,
    123.3220100402832, 184.7059726715088, 327.7161121368408, 524.7609615325928,
    744.2569732666016, 1051.8128871917725, 1252.1069049835205
]
  #basic
y2 = [
    0.07414817810058594, 0.6248950958251953, 2.1848678588867188, 7.786989212036133,
    17.36307144165039, 32.37295150756836, 70.95909118652344, 131.0129165649414,
    199.26023483276367, 283.92815589904785, 524.7781276702881, 816.5361881256104,
    1142.1408653259277, 1594.2142009735107, 1958.8279724121094
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
