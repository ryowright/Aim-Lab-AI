import os

os.chdir('Pictures')
for count, filename in enumerate(os.listdir("Pictures")):
    newName = "aimlab" + str(count) + ".png"
    os.rename(filename, newName)

#os.getcwd