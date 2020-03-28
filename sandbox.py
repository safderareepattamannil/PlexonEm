import logging
import ffmpeg


logging.basicConfig(format='%(asctime)s %(message)s')

for i in range(100):
    d = "dog"
    print("hello {d}".format(d=d))


# f = open("demofile2.txt","a")
# f.write("automation worked!")
# f.close()
