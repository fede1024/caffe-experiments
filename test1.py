with open("features_lamp", 'w') as outfile:
    for vector in conv_features:
        line = "   "
        for num in vector:
            line += str(num) + " "
        line += "\n"
        outfile.write(line)

